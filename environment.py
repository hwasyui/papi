import tkinter as tk
import numpy as np
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk, ImageFilter
from mathematicalOperation import MathematicalOperations
from imageEnhancement import ImageEnhancement
from compression import ImageCompressor

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

        # Undo and Redo stacks
        self.undo_stack = []
        self.redo_stack = []

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
            ("Save", self.save_image),
            ("Undo", self.undo_operation),
            ("Redo", self.redo_operation),
            ("Reset", self.reset_image)
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

        # Create Image Enhancement Tab
        enhancement_frame = ttk.Frame(self.operations_notebook)
        self.create_image_enhancement_tab(enhancement_frame)
        self.operations_notebook.add(enhancement_frame, text="Image Enhancement")

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

    def create_image_enhancement_tab(self, parent):
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.X, padx=10, pady=10)

        # Histogram Equalization
        ttk.Button(main_frame, text="Histogram Equalization", command=self.apply_histogram_equalization).pack(pady=5)

        # Contrast Stretching
        contrast_frame = ttk.LabelFrame(main_frame, text="Contrast Stretching")
        contrast_frame.pack(fill=tk.X, pady=5)

        ttk.Label(contrast_frame, text="Low In:").grid(row=0, column=0)
        self.contrast_low_in = ttk.Scale(contrast_frame, from_=0, to=255, orient=tk.HORIZONTAL)
        self.contrast_low_in.grid(row=0, column=1, sticky='ew')

        ttk.Label(contrast_frame, text="High In:").grid(row=1, column=0)
        self.contrast_high_in = ttk.Scale(contrast_frame, from_=0, to=255, orient=tk.HORIZONTAL)
        self.contrast_high_in.grid(row=1, column=1, sticky='ew')

        ttk.Label(contrast_frame, text="Low Out:").grid(row=2, column=0)
        self.contrast_low_out = ttk.Scale(contrast_frame, from_=0, to=255, orient=tk.HORIZONTAL)
        self.contrast_low_out.grid(row=2, column=1, sticky='ew')

        ttk.Label(contrast_frame, text="High Out:").grid(row=3, column=0)
        self.contrast_high_out = ttk.Scale(contrast_frame, from_=0, to=255, orient=tk.HORIZONTAL)
        self.contrast_high_out.grid(row=3, column=1, sticky='ew')

        ttk.Button(main_frame, text="Apply Contrast Stretching", command=self.apply_contrast_stretching).pack(pady=5)

        # Gamma Correction
        gamma_frame = ttk.LabelFrame(main_frame, text="Gamma Correction")
        gamma_frame.pack(fill=tk.X, pady=5)

        ttk.Label(gamma_frame, text="Gamma:").grid(row=0, column=0)
        self.gamma_value = ttk.Scale(gamma_frame, from_=0.1, to=5.0, orient=tk.HORIZONTAL)
        self.gamma_value.grid(row=0, column=1, sticky='ew')

        ttk.Button(main_frame, text="Apply Gamma Correction", command=self.apply_gamma_correction).pack(pady=5)
    
    def create_compression_tab(self, parent):
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill='x', padx=10, pady=10)

        self.original_size_label = ttk.Label(main_frame, text="Original File Size: ")
        self.original_size_label.pack(pady=5)

        self.compressed_size_label = ttk.Label(main_frame, text="Compressed File Size: ")
        self.compressed_size_label.pack(pady=5)

        btn_lossless = ttk.Button(main_frame, text="Apply Lossless Compression", command=self.apply_lossless_compression)
        btn_lossless.pack(pady=5)

        self.quality_var = tk.StringVar(main_frame)
        self.quality_var.set("Select Quality")
        quality_options = [10, 30, 50, 70, 90]
        quality_dropdown = ttk.OptionMenu(main_frame, self.quality_var, *quality_options)
        quality_dropdown.pack(pady=5)

        btn_apply_lossy = ttk.Button(main_frame, text="Apply Lossy Compression", command=self.apply_lossy_compression)
        btn_apply_lossy.pack(pady=5)

    def update_file_size_display(self):
        if self.original_image:
            original_size = self.original_image.size[0] * self.original_image.size[1] * 3
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
            self.compressed_file_size = len(rle_encoded) * 2
            decoded_image_array = compressor.run_length_decoding(rle_encoded)
            self.result_image = Image.fromarray(decoded_image_array, mode='L')
            
            # Display the result image in the result canvas
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            
            messagebox.showinfo("Success", "Lossless compression applied successfully!")
            self.update_file_size_display()
            
            # Save the current state for undo
            self.save_state_for_undo()
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

            # Apply DCT and get encoded data
            dct_encoded = compressor.apply_dct(quality)

            # Calculate compressed size based on non-zero coefficients
            self.compressed_file_size = np.count_nonzero(dct_encoded) * 2  # Approximate byte size

            # Decode the image from DCT
            decoded_image = compressor.inverse_dct(dct_encoded)

            # Convert to PIL Image and display
            if isinstance(decoded_image, np.ndarray):
                self.result_image = Image.fromarray(decoded_image.astype(np.uint8))
            else:
                messagebox.showwarning("Warning", "Decoded image is not in the expected format!")
                return

            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            messagebox.showinfo("Success", "Lossy compression applied successfully!")
            self.update_file_size_display()
            
            # Save the current state for undo
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")



    def open_first_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.left_image = Image.open(file_path)
            self.original_image = self.left_image.copy()
            self.display_image(self.left_image, self.left_canvas, self.left_zoom, 'left')
            # Do not display in result canvas immediately

    def open_second_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.right_image = Image.open(file_path)
            self.display_image(self.right_image, self.right_canvas, self.right_zoom, 'right')

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

        # Save the current state for undo
        self.undo_stack.append(self.original_image.copy())
        self.redo_stack.clear()  # Clear redo stack on new operation

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
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "Both images must be loaded!")

    def pixelwise_subtraction(self):
        if self.left_image and self.right_image:
            self.result_image = MathematicalOperations.pixelwise_subtraction(self.left_image, self.right_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "Both images must be loaded!")

    def pixelwise_multiplication(self):
        if self.left_image and self.right_image:
            self.result_image = MathematicalOperations.pixelwise_multiplication(self.left_image, self.right_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "Both images must be loaded!")

    def pixelwise_division(self):
        if self.left_image and self.right_image:
            self.result_image = MathematicalOperations.pixelwise_division(self.left_image, self.right_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "Both images must be loaded!")

    def bitwise_and(self):
        if self.left_image and self.right_image:
            self.result_image = MathematicalOperations.bitwise_and(self.left_image, self.right_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "Both images must be loaded!")

    def bitwise_or(self):
        if self.left_image and self.right_image:
            self.result_image = MathematicalOperations.bitwise_or(self.left_image, self.right_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "Both images must be loaded!")

    def bitwise_xor(self):
        if self.left_image and self.right_image:
            self.result_image = MathematicalOperations.bitwise_xor(self.left_image, self.right_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "Both images must be loaded!")

    def bitwise_not(self):
        if self.left_image:
            self.result_image = MathematicalOperations.bitwise_not(self.left_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_histogram_equalization(self):
        if self.left_image:
            self.result_image = ImageEnhancement.histogram_equalization(self.left_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_contrast_stretching(self):
        if self.left_image:
            low_in = int(self.contrast_low_in.get())
            high_in = int(self.contrast_high_in.get())
            low_out = int(self.contrast_low_out.get())
            high_out = int(self.contrast_high_out.get())
            self.result_image = ImageEnhancement.contrast_stretching(self.left_image, low_in, high_in, low_out, high_out)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_gamma_correction(self):
        if self.left_image:
            gamma = self.gamma_value.get()
            self.result_image = ImageEnhancement.gamma_correction(self.left_image, gamma)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
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

    def save_state_for_undo(self):
        if self.result_image:
            self.undo_stack.append(self.result_image.copy())
            self.redo_stack.clear()  # Clear redo stack on new operation

    def undo_operation(self):
        if self.undo_stack:
            self.redo_stack.append(self.undo_stack.pop())
            if self.undo_stack:
                self.result_image = self.undo_stack[-1]
                self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            else:
                self.result_image = self.original_image
                self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
        else:
            messagebox.showwarning("Warning", "No operation to undo!")

    def redo_operation(self):
        if self.redo_stack:
            self.result_image = self.redo_stack.pop()
            self.undo_stack.append(self.result_image.copy())
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
        else:
            messagebox.showwarning("Warning", "No operation to redo!")

    def reset_image(self):
        self.result_image = self.original_image.copy() if self.original_image else None
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
        self.update_file_size_display() 

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()