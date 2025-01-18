import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk, ImageFilter
from mathematicalOperation import MathematicalOperations
from compression import ImageCompressor
import numpy as np

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Image Editor")
        
        # Make the window full screen
        self.root.state('zoomed')

        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Top panel
        self.create_top_panel()

        # Main content area
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Create three main sections
        self.create_image_sections()

        # Operations Notebook
        self.create_operations_notebook()

        # Initialize image variables
        self.left_image = None
        self.right_image = None
        self.result_image = None
        self.original_image = None

        # Zoom variables
        self.left_zoom = 1.0
        self.right_zoom = 1.0
        self.result_zoom = 1.0

        # Store references to PhotoImage objects
        self.left_tk_image = None
        self.right_tk_image = None
        self.result_tk_image = None

    def create_top_panel(self):
        self.top_panel = ttk.Frame(self.main_frame)
        self.top_panel.pack(side=tk.TOP, fill=tk.X)

        buttons = [
            ("Open First", self.open_first_image),
            ("Open Second", self.open_second_image),
            # ("Undo", self.redo),
            # ("Redo", self.undo),
            # ("Reset", self.reset),
            ("Save", self.save_image)
        ]

        for text, command in buttons:
            btn = ttk.Button(self.top_panel, text=text, command=command)
            btn.pack(side=tk.LEFT, padx=5, pady=5)

    def create_image_sections(self):
        self.left_frame = ttk.Frame(self.content_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.right_frame = ttk.Frame(self.content_frame)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.result_frame = ttk.Frame(self.content_frame)
        self.result_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Left Image Section
        ttk.Label(self.left_frame, text="First Image").pack()
        self.left_canvas = tk.Canvas(self.left_frame, bg="lightgray")
        self.left_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Left Image Zoom
        ttk.Label(self.left_frame, text="Zoom:").pack()
        self.left_zoom_scale = ttk.Scale(
            self.left_frame, 
            from_=0.1, 
            to=3, 
            value=1, 
            orient=tk.HORIZONTAL, 
            command=self.update_left_zoom
        )
        self.left_zoom_scale.pack(fill=tk.X)

        # Right Image Section
        ttk.Label(self.right_frame, text="Second Image").pack()
        self.right_canvas = tk.Canvas(self.right_frame, bg="lightgray")
        self.right_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Right Image Zoom
        ttk.Label(self.right_frame, text="Zoom:").pack()
        self.right_zoom_scale = ttk.Scale(
            self.right_frame, 
            from_=0.1, 
            to=3, 
            value=1, 
            orient=tk.HORIZONTAL, 
            command=self.update_right_zoom
        )
        self.right_zoom_scale.pack(fill=tk.X)

        # Result Image Section
        ttk.Label(self.result_frame, text="Result").pack()
        self.result_canvas = tk.Canvas(self.result_frame, bg="lightgray")
        self.result_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Result Image Zoom
        ttk.Label(self.result_frame, text="Zoom:").pack()
        self.result_zoom_scale = ttk.Scale(
            self.result_frame, 
            from_=0.1, 
            to=3, 
            value=1, 
            orient=tk.HORIZONTAL, 
            command=self.update_result_zoom
        )
        self.result_zoom_scale.pack(fill=tk.X)

    def create_operations_notebook(self):
        self.operations_notebook = ttk.Notebook(self.main_frame)
        self.operations_notebook.pack(fill=tk.X)

        # Create Basic Operations Tab
        basic_ops_frame = ttk.Frame(self.operations_notebook)
        self.create_basic_operations_tab(basic_ops_frame)
        self.operations_notebook.add(basic_ops_frame, text="Basic Operations")

        # Create Mathematical Operations Tab
        math_ops_frame = ttk.Frame(self.operations_notebook)
        self.create_mathematical_operations_tab(math_ops_frame)
        self.operations_notebook.add(math_ops_frame, text="Mathematical Operations")

        # Create Compression Tab
        compression_ops_frame = ttk.Frame(self.operations_notebook)
        self.create_compression_tab(compression_ops_frame)
        self.operations_notebook.add(compression_ops_frame, text="Compression")

    def create_basic_operations_tab(self, parent):
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.X, padx=10, pady=10)

        # Crop Section
        crop_frame = ttk.LabelFrame(main_frame, text="Crop")
        crop_frame.pack(fill=tk.X, pady=5)

        ttk.Label(crop_frame, text="Start X:").grid(row=0, column=0)
        self.crop_start_x = ttk.Scale(crop_frame, from_=0, to=100, orient=tk.HORIZONTAL)
        self.crop_start_x.grid(row=0, column=1, sticky='ew')
        self.crop_start_x_label = ttk.Label(crop_frame, text="0")
        self.crop_start_x_label.grid(row=0, column=2)

        ttk.Label(crop_frame, text="Start Y:").grid(row=1, column=0)
        self.crop_start_y = ttk.Scale(crop_frame, from_=0, to=100, orient=tk.HORIZONTAL)
        self.crop_start_y.grid(row=1, column=1, sticky='ew')
        self.crop_start_y_label = ttk.Label(crop_frame, text="0")
        self.crop_start_y_label.grid(row=1, column=2)

        # Rotate Section
        rotate_frame = ttk.LabelFrame(main_frame, text="Rotate")
        rotate_frame.pack(fill=tk.X, pady=5)

        ttk.Label(rotate_frame, text="Angle:").grid(row=0, column=0)
        self.rotate_angle = ttk.Scale(rotate_frame, from_=0, to=360, orient=tk.HORIZONTAL)
        self.rotate_angle.grid(row=0, column=1, sticky='ew')
        self.rotate_angle_label = ttk.Label(rotate_frame, text="0")
        self.rotate_angle_label.grid(row=0, column=2)

        # Blur Section
        blur_frame = ttk.LabelFrame(main_frame, text="Blur")
        blur_frame.pack(fill=tk.X, pady=5)

        ttk.Label(blur_frame, text="Intensity:").grid(row=0, column=0)
        self.blur_intensity = ttk.Scale(blur_frame, from_=0, to=10, orient=tk.HORIZONTAL)
        self.blur_intensity.grid(row=0, column=1, sticky='ew') 
        self.blur_intensity_label = ttk.Label(blur_frame, text="0")
        self.blur_intensity_label.grid(row=0, column=2)
    
        # Grayscale Section
        self.grayscale_var = tk.BooleanVar()
        grayscale_check = ttk.Checkbutton(main_frame, text="Grayscale", variable=self.grayscale_var)
        grayscale_check.pack(pady=5)

        # Apply Button
        apply_button = ttk.Button(main_frame, text="Apply", command=self.apply_basic_operations)
        apply_button.pack(pady=10)

    def create_mathematical_operations_tab(self, parent):
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.X, padx=10, pady=10)

        # Pixel-wise Operations
        pixel_ops_frame = ttk.LabelFrame(main_frame, text="Pixel-wise Operations")
        pixel_ops_frame.pack(fill=tk.X, pady=5)

        ttk.Button(pixel_ops_frame, text="Add", command=self.pixelwise_addition).pack(side=tk.LEFT, padx=5)
        ttk.Button(pixel_ops_frame, text="Subtract", command=self.pixelwise_subtraction).pack(side=tk.LEFT, padx=5)
        ttk.Button(pixel_ops_frame, text="Multiply", command=self.pixelwise_multiplication).pack(side=tk.LEFT, padx=5)
        ttk.Button(pixel_ops_frame, text="Divide", command=self.pixelwise_division).pack(side=tk.LEFT, padx=5)

        # Bitwise Operations
        bitwise_ops_frame = ttk.LabelFrame(main_frame, text="Bitwise Operations")
        bitwise_ops_frame.pack(fill=tk.X, pady=5)

        ttk.Button(bitwise_ops_frame, text="AND", command=self.bitwise_and).pack(side=tk.LEFT, padx=5)
        ttk.Button(bitwise_ops_frame, text="OR", command=self.bitwise_or).pack(side=tk.LEFT, padx=5)
        ttk.Button(bitwise_ops_frame, text="XOR", command=self.bitwise_xor).pack(side=tk.LEFT, padx=5)
        ttk.Button(bitwise_ops_frame, text="NOT", command=self.bitwise_not).pack(side=tk.LEFT, padx=5)
    
    def create_compression_tab(self, parent):
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.X, padx=10, pady=10)

        # Original File Size Display
        self.original_size_label = ttk.Label(main_frame, text="Original File Size: ")
        self.original_size_label.pack(pady=5)

        # Compressed File Size Display
        self.compressed_size_label = ttk.Label(main_frame, text="Compressed File Size: ")
        self.compressed_size_label.pack(pady=5)

        # Lossless Compression Button
        btn_lossless = ttk.Button(main_frame, text="Apply Lossless Compression", command=self.apply_lossless_compression)
        btn_lossless.pack(pady=5)

        # Lossy Compression Quality Dropdown
        self.quality_var = tk.StringVar(main_frame)
        self.quality_var.set("Select Quality")  # Default value
        quality_options = [10, 30, 50, 70, 90]
        quality_dropdown = ttk.OptionMenu(main_frame, self.quality_var, *quality_options)
        quality_dropdown.pack(pady=5)

        # Apply Lossy Compression Button
        btn_apply_lossy = ttk.Button(main_frame, text="Apply Lossy Compression", command=self.apply_lossy_compression)
        btn_apply_lossy.pack(pady=5)

    def update_file_size_display(self):
        if self.original_image:
            original_size = self.original_image.size[0] * self.original_image.size[1] * 3  # Approximate size in bytes
            self.original_size_label.config(text=f"Original File Size: {original_size / 1024:.2f} KB")
        else:
            self.original_size_label.config(text="Original File Size: ")

        if hasattr(self, 'compressed_file_size') and self.compressed_file_size > 0:
            self.compressed_size_label.config(text=f"Compressed File Size: {self.compressed_file_size / 1024:.2f} KB")
        else:
            self.compressed_size_label.config(text="Compressed File Size: ")

    def apply_lossless_compression(self):
        if self.original_image:
            compressor = ImageCompressor(self.original_image)
            rle_encoded = compressor.apply_rle()
            self.compressed_file_size = len(rle_encoded)  # Simulate file size after compression

            # Decode RLE back to image
            decoded_image_array = compressor.run_length_decoding(rle_encoded)
            self.result_image = Image.fromarray(decoded_image_array)  # Convert NumPy array to PIL Image
            messagebox.showinfo("Success", "Lossless compression applied successfully!")
            self.update_file_size_display()
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')  # Display the result image
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_lossy_compression(self):
        if self.original_image:
            quality = self.quality_var.get()
            if quality == "Select Quality":
                messagebox.showwarning("Warning", "Please select a quality for lossy compression!")
                return

            quality = int(quality)
            compressor = ImageCompressor(self.original_image)
            dct_encoded = compressor.apply_dct(quality)
            self.compressed_file_size = dct_encoded.nbytes  # Simulate file size after compression

            # Decode DCT back to image
            decoded_image = compressor.inverse_dct(dct_encoded)
            self.result_image = decoded_image  # This is already a PIL Image
            messagebox.showinfo("Success", "Lossy compression applied successfully!")
            self.update_file_size_display()
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')  # Display the result image
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def open_first_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.left_image = Image.open(file_path)
            self.original_image = self.left_image.copy()
            self.display_image(self.left_image, self.left_canvas, self.left_zoom, 'left')

    def open_second_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.right_image = Image.open(file_path)
            self.display_image(self.right_image, self.right_canvas, self.right_zoom, 'right')

    def show_history(self):
        messagebox.showinfo("History", "History functionality not implemented.")

    def show_layers(self):
        messagebox.showinfo("Layers", "Layers functionality not implemented.")

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path and self.result_image:
            self.result_image.save(file_path)
            messagebox.showinfo("Save", "Image saved successfully!")

    def update_left_zoom(self, value):
        self.left_zoom = float(value)
        if self.left_image:
            self.display_image(self.left_image, self.left_canvas, self.left_zoom, 'left')

    def update_right_zoom(self, value):
        self.right_zoom = float(value)
        if self.right_image:
            self.display_image(self.right_image, self.right_canvas, self.right_zoom, 'right')

    def update_result_zoom(self, value):
        self.result_zoom = float(value)
        if self.result_image:
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')

    def apply_basic_operations(self):
        if not self.left_image:
            messagebox.showwarning("Warning", "No image loaded!")
            return

        crop_x = int(self.crop_start_x.get())
        crop_y = int(self.crop_start_y.get())
        rotate_angle = int(self.rotate_angle.get())
        blur_intensity = int(self.blur_intensity.get())
        is_grayscale = self.grayscale_var.get()

        if (crop_x == 0 and crop_y == 0 and 
            rotate_angle == 0 and 
            blur_intensity == 0 and 
            not is_grayscale):
            messagebox.showinfo("No Changes", "You changed nothing!")
            return

        confirm = messagebox.askyesno(
            "Confirm Operation", 
            "Upon clicking 'Ok' you won't be able to undo. Are you sure you want to proceed with these changes?"
        )
        
        if not confirm:
            return

        self.result_image = self.original_image.copy()

        if crop_x > 0 or crop_y > 0:
            width = self.result_image.width
            height = self.result_image.height
            crop_width = int(width * (1 - crop_x / 100))
            crop_height = int(height * (1 - crop_y / 100))
            crop_x_start = int(width * (crop_x / 100))
            crop_y_start = int(height * (crop_y / 100))
            self.result_image = self.result_image.crop((
                crop_x_start, 
                crop_y_start, 
                crop_x_start + crop_width, 
                crop_y_start + crop_height
            ))

        if rotate_angle > 0:
            self.result_image = self.result_image.rotate(rotate_angle)

        if blur_intensity > 0:
            self.result_image = self.result_image.filter(ImageFilter.GaussianBlur(blur_intensity))

        if is_grayscale:
            self.result_image = self.result_image.convert("L")

        self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')

        self.crop_start_x.set(0)
        self.crop_start_y.set(0)
        self.rotate_angle.set(0)
        self.blur_intensity.set(0)
        self.grayscale_var.set(False)

        messagebox.showinfo("Success", "Image operations applied successfully!")

    def pixelwise_addition(self):
        if self.left_image and self.right_image:
            self.result_image = MathematicalOperations.pixelwise_addition(self.left_image, self.right_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
        else:
            messagebox.showwarning("Warning", "Both images must be loaded!")

    def pixelwise_subtraction(self):
        if self.left_image and self.right_image:
            self.result_image = MathematicalOperations.pixelwise_subtraction(self.left_image, self.right_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
        else:
            messagebox.showwarning("Warning", "Both images must be loaded!")

    def pixelwise_multiplication(self):
        if self.left_image and self.right_image:
            self.result_image = MathematicalOperations.pixelwise_multiplication(self.left_image, self.right_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
        else:
            messagebox.showwarning("Warning", "Both images must be loaded!")

    def pixelwise_division(self):
        if self.left_image and self.right_image:
            self.result_image = MathematicalOperations.pixelwise_division(self.left_image, self.right_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
        else:
            messagebox.showwarning("Warning", "Both images must be loaded!")

    def bitwise_and(self):
        if self.left_image and self.right_image:
            self.result_image = MathematicalOperations.bitwise_and(self.left_image, self.right_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
        else:
            messagebox.showwarning("Warning", "Both images must be loaded!")

    def bitwise_or(self):
        if self.left_image and self.right_image:
            self.result_image = MathematicalOperations.bitwise_or(self.left_image, self.right_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
        else:
            messagebox.showwarning("Warning", "Both images must be loaded!")

    def bitwise_xor(self):
        if self.left_image and self.right_image:
            self.result_image = MathematicalOperations.bitwise_xor(self.left_image, self.right_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
        else:
            messagebox.showwarning("Warning", "Both images must be loaded!")

    def bitwise_not(self):
        if self.left_image:
            self.result_image = MathematicalOperations.bitwise_not(self.left_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def display_image(self, image, canvas, zoom=1.0, side='left'):
        canvas.delete("all")
        
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        width = int(image.width * zoom)
        height = int(image.height * zoom)
        
        scaled_image = image.copy()
        if width > canvas_width or height > canvas_height:
            scaled_image.thumbnail((canvas_width, canvas_height), Image.LANCZOS)
        else:
            scaled_image = scaled_image.resize((width, height), Image.LANCZOS)
        
        if side == 'left':
            self.left_tk_image = ImageTk.PhotoImage(scaled_image)
            x = (canvas_width - scaled_image.width) // 2
            y = (canvas_height - scaled_image.height) // 2
            canvas.create_image(x, y, anchor=tk.NW, image=self.left_tk_image)
        elif side == 'right':
            self.right_tk_image = ImageTk.PhotoImage(scaled_image)
            x = (canvas_width - scaled_image.width) // 2
            y = (canvas_height - scaled_image.height) // 2
            canvas.create_image(x, y, anchor=tk.NW, image=self.right_tk_image)
        else:
            self.result_tk_image = ImageTk.PhotoImage(scaled_image)
            x = (canvas_width - scaled_image.width) // 2
            y = (canvas_height - scaled_image.height) // 2
            canvas.create_image(x, y, anchor=tk.NW, image=self.result_tk_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()