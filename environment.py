import tkinter as tk
from tkinter import Scale, ttk, messagebox, filedialog
from PIL import Image, ImageTk, ImageFilter, ImageDraw
import cv2
import numpy as np
from mathematicalOperation import MathematicalOperations
from imageEnhancement import ImageEnhancement
from binaryOperation import BinaryOperation
from basicOperation import basicOperations
import math

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
        self.overlay_image = None
        self.overlay_position = (0, 0)  # Initial position of overlay

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

        # Create Image Enhancement Tab
        binary_frame = ttk.Frame(self.operations_notebook)
        self.create_image_binary_frame_tab(binary_frame)
        self.operations_notebook.add(binary_frame, text="Binary Image")

    def create_basic_operations_tab(self, parent):
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.X, padx=10, pady=10)

        # Grayscale Button
        ttk.Button(main_frame, text="Apply Grayscale", command=self.apply_grayscale).grid(row=0, column=0, columnspan=2, pady=5, padx=10)

        # Negative Button
        ttk.Button(main_frame, text="Apply Negative", command=self.apply_negative).grid(row=1, column=0, columnspan=2, pady=5,padx=10)

        # Flip Buttons
        flip_frame = ttk.LabelFrame(main_frame, text="Image Flipping")
        flip_frame.grid(row=0, column=5, columnspan=2, pady=5,padx=20, sticky='ew')

        ttk.Button(flip_frame, text="Horizontal Flip", command=self.apply_horizontal_flip).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(flip_frame, text="Vertical Flip", command=self.apply_vertical_flip).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(flip_frame, text="Diagonal Flip", command=self.apply_diagonal_flip).grid(row=0, column=2, padx=5, pady=5)
        
        # Section Crop
        crop_frame1 = ttk.LabelFrame(main_frame, text="Cropping Method 1")
        crop_frame1.grid(row=1, column=5, columnspan=2, padx=20, pady=5, sticky='ew')

        ttk.Label(crop_frame1, text="Width:").grid(row=0, column=0, padx=5, pady=5)
        self.crop_width = ttk.Entry(crop_frame1)
        self.crop_width.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(crop_frame1, text="Height:").grid(row=1, column=0, padx=5, pady=5)
        self.crop_height = ttk.Entry(crop_frame1)
        self.crop_height.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(crop_frame1, text="Apply Crop", command=self.apply_crop_method1).grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        # Cropping Method 2
        crop_frame2 = ttk.LabelFrame(main_frame, text="Cropping Method 2")
        crop_frame2.grid(row=1, column=8, columnspan=2, padx=30, pady=5, sticky='ew')

        ttk.Label(crop_frame2, text="Select Shape:").grid(row=0, column=0, padx=5, pady=5)
        self.shape_var = tk.StringVar(value="Circle")
        shapes = ["Star", "Diamond", "Circle"]
        self.shape_menu = ttk.OptionMenu(crop_frame2, self.shape_var, shapes[0], *shapes)
        self.shape_menu.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(crop_frame2, text="Apply Crop", command=self.apply_crop_method2).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')


        # Translation Section
        translate_frame = ttk.LabelFrame(main_frame, text="Translation")
        translate_frame.grid(row=0, column=8, columnspan=2, padx=30, pady=5, sticky='ew')

        ttk.Label(translate_frame, text="Right :").grid(row=0, column=0)
        self.translate_right = ttk.Scale(translate_frame, from_=0, to=100, orient="horizontal")
        self.translate_right.grid(row=0, column=1, padx=5)

        ttk.Label(translate_frame, text="Left :").grid(row=1, column=0)
        self.translate_left = ttk.Scale(translate_frame, from_=0, to=100, orient="horizontal")
        self.translate_left.grid(row=1, column=1, padx=5)

        ttk.Label(translate_frame, text="Up :").grid(row=2, column=0)
        self.translate_up = ttk.Scale(translate_frame, from_=0, to=100, orient="horizontal")
        self.translate_up.grid(row=2, column=1, padx=5)

        ttk.Label(translate_frame, text="Down :").grid(row=3, column=0)
        self.translate_down = ttk.Scale(translate_frame, from_=0, to=100, orient="horizontal")
        self.translate_down.grid(row=3, column=1, padx=5)

        ttk.Button(translate_frame, text="Apply Translation", command=self.apply_translation).grid(row=4, column=0, columnspan=2, pady=5)

        # Scaling Section
        scaling_frame = ttk.LabelFrame(main_frame, text="Scaling")
        scaling_frame.grid(row=0, column=14, columnspan=2, pady=5,padx=40, sticky='ew')

        ttk.Label(scaling_frame, text="Scale X:").grid(row=0, column=0)
        self.scale_x = ttk.Scale(scaling_frame, from_=0.5, to=2.0, orient=tk.HORIZONTAL)
        self.scale_x.grid(row=0, column=1, sticky='ew')

        ttk.Label(scaling_frame, text="Scale Y:").grid(row=1, column=0)
        self.scale_y = ttk.Scale(scaling_frame, from_=0.5, to=2.0, orient=tk.HORIZONTAL)
        self.scale_y.grid(row=1, column=1, sticky='ew')

        ttk.Button(scaling_frame, text="Apply Scaling", command=self.apply_scaling).grid(row=2, column=0, columnspan=2, pady=5)

        # RGB Intensity Section
        intensity_frame = ttk.LabelFrame(main_frame, text="RGB Intensity")
        intensity_frame.grid(row=1, column=14, columnspan=2, pady=5,padx=40, sticky='ew')

        ttk.Label(intensity_frame, text="Red:").grid(row=0, column=0)
        self.intensity_red = ttk.Scale(intensity_frame, from_=0, to=255, orient=tk.HORIZONTAL)
        self.intensity_red.grid(row=0, column=1, sticky='ew')

        ttk.Label(intensity_frame, text="Green:").grid(row=1, column=0)
        self.intensity_green = ttk.Scale(intensity_frame, from_=0, to=255, orient=tk.HORIZONTAL)
        self.intensity_green.grid(row=1, column=1, sticky='ew')

        ttk.Label(intensity_frame, text="Blue:").grid(row=2, column=0)
        self.intensity_blue = ttk.Scale(intensity_frame, from_=0, to=255, orient=tk.HORIZONTAL)
        self.intensity_blue.grid(row=2, column=1, sticky='ew')

        ttk.Button(intensity_frame, text="Apply RGB Intensity", command=self.apply_rgb_intensity).grid(row=3, column=0, columnspan=2, pady=5)

        # Border Section
        border_frame = ttk.LabelFrame(main_frame, text="Border")
        border_frame.grid(row=0, column=22, columnspan=2, pady=5,padx=40, sticky='ew')

        ttk.Label(border_frame, text="Border Thickness:").grid(row=0, column=0)
        self.border_thickness = ttk.Scale(border_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.border_thickness.grid(row=0, column=1, sticky='ew')

        ttk.Label(border_frame, text="Border Color:").grid(row=1, column=0)
        self.border_color = ttk.Entry(border_frame)
        self.border_color.grid(row=1, column=1, sticky='ew')

        ttk.Button(border_frame, text="Apply Border", command=self.apply_border).grid(row=2, column=0, columnspan=2, pady=5)

        #overlay section
        overlay_frame = ttk.LabelFrame(main_frame, text="Image Overlay")
        overlay_frame.grid(row=1, column=22, pady=5,padx=40, sticky='ew')

        ttk.Label(overlay_frame, text="Transparency:").grid(row=0, column=0)
        self.overlay_transparency = ttk.Scale(overlay_frame, from_=0.1, to=1.0, orient=tk.HORIZONTAL)
        self.overlay_transparency.grid(row=0, column=1, sticky='ew')

        upload_button = tk.Button(overlay_frame, text="Upload and Overlay", command=self.upload_and_drag_overlay)
        upload_button.grid(row=1, column=0, columnspan=2, pady=5)

        apply_button = tk.Button(overlay_frame, text="Apply Overlay", command=self.apply_overlay_to_canvas)
        apply_button.grid(row=2, column=0, columnspan=2, pady=5)


        # Bind mouse events for dragging
        self.result_canvas.bind("<Button-1>", self.start_drag)
        self.result_canvas.bind("<B1-Motion>", self.do_drag)


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

    def create_image_binary_frame_tab(self, parent):
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.X, padx=10, pady=10)

        # Morphological Operations Frame
        morph_frame = ttk.LabelFrame(main_frame, text="Morphological Operations")
        morph_frame.pack(fill=tk.X, pady=5)

        ttk.Button(morph_frame, text="Dilation", command=self.apply_dilation).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(morph_frame, text="Erosion", command=self.apply_erosion).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(morph_frame, text="Opening", command=self.apply_opening).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(morph_frame, text="Closing", command=self.apply_closing).pack(side=tk.LEFT, padx=5, pady=5)

        # Boundary Extraction Frame
        boundary_frame = ttk.LabelFrame(main_frame, text="Boundary Extraction")
        boundary_frame.pack(fill=tk.X, pady=5)

        ttk.Button(boundary_frame, text="Extract Boundary", command=self.apply_boundary_extraction).pack(pady=5)

        # Skeletonization Frame
        skeleton_frame = ttk.LabelFrame(main_frame, text="Skeletonization")
        skeleton_frame.pack(fill=tk.X, pady=5)

        ttk.Button(skeleton_frame, text="Skeletonize", command=self.apply_skeletonization).pack(pady=5)


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


    def apply_grayscale(self):
        if self.left_image:
            self.result_image = basicOperations.to_grayscale(self.left_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_negative(self):
        if self.left_image:
            self.result_image = basicOperations.to_negative(self.left_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_horizontal_flip(self):
        if self.left_image:
            self.result_image = basicOperations.horizontal_flip(self.left_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_vertical_flip(self):
        if self.left_image:
            self.result_image = basicOperations.vertical_flip(self.left_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_diagonal_flip(self):
        if self.left_image:
            self.result_image = basicOperations.diagonal_flip(self.left_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_crop_method1(self):
        if self.left_image:
            try:
                # Ambil nilai width dan height dari input
                width = int(self.crop_width.get())
                height = int(self.crop_height.get())

                # Lakukan cropping
                self.result_image = basicOperations.crop_image(self.left_image, width, height)

                # Tampilkan hasil gambar dan simpan state untuk undo
                self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
                self.save_state_for_undo()
            except ValueError:
                messagebox.showerror("Error", "Invalid width or height value. Please enter valid integers.")
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_crop_method2(self):
        if self.left_image:
            try:
                # Ambil bentuk dari dropdown
                shape = self.shape_var.get()

                # Lakukan cropping berdasarkan bentuk
                self.result_image = basicOperations.crop_image_by_shape(self.left_image, shape)

                # Tampilkan hasil gambar dan simpan state untuk undo
                self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
                self.save_state_for_undo()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showwarning("Warning", "No image loaded!")
 


    def apply_translation(self):
        if self.left_image:
            right = int(self.translate_right.get())
            left = int(self.translate_left.get())
            up = int(self.translate_up.get())
            down = int(self.translate_down.get())

            # Hitung pergeseran berdasarkan input slider
            self.result_image = basicOperations.translate(self.left_image, right, left, up, down)

            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_scaling(self):
        if self.left_image:
            scale_x = self.scale_x.get()
            scale_y = self.scale_y.get()
            self.result_image = basicOperations.scale(self.left_image, scale_x, scale_y)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_rgb_intensity(self):
        if self.left_image:
            red = int(self.intensity_red.get())
            green = int(self.intensity_green.get())
            blue = int(self.intensity_blue.get())
            self.result_image = basicOperations.adjust_rgb_intensity(self.left_image, red, green, blue)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()

    def apply_border(self):
        if self.left_image:
            thickness = int(self.border_thickness.get())
            color = self.border_color.get() or "black"  # Default to black if no color specified
            self.result_image = basicOperations.add_border(self.left_image, thickness, color)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def upload_and_drag_overlay(self):
        overlay_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if overlay_path:
            try:
                self.overlay_image = Image.open(overlay_path).convert("RGBA")
                if self.left_image:
                    # Resize overlay to fit the base image size
                    self.overlay_image = self.overlay_image.resize(self.left_image.size, Image.Resampling.LANCZOS)
                    self.overlay_position = (0, 0)  # Reset overlay position
                    self.update_overlay_preview()
                else:
                    messagebox.showwarning("Warning", "No base image loaded!")
            except Exception as e:
                messagebox.showerror("Error", f"Unable to load overlay image: {e}")

    def start_drag(self, event):
        """Initialize drag operation."""
        self.overlay_start_x = event.x
        self.overlay_start_y = event.y

    def do_drag(self, event):
        """Handle dragging of overlay."""
        if self.overlay_image:
            dx = event.x - self.overlay_start_x
            dy = event.y - self.overlay_start_y
            self.overlay_position = (self.overlay_position[0] + dx, self.overlay_position[1] + dy)
            self.overlay_start_x = event.x
            self.overlay_start_y = event.y
            self.update_overlay_preview()

    def update_overlay_preview(self):
        """Update the canvas to show the overlay in its current position."""
        if self.left_image and self.overlay_image:  # Importing here to ensure modular design
            overlay_preview = basicOperations.apply_overlay(
                self.left_image, self.overlay_image, self.overlay_transparency.get(), self.overlay_position
            )
            self.display_image(overlay_preview, self.result_canvas, zoom=1.0, side='result')

    def apply_overlay_to_canvas(self):
        """Apply the overlay and display the final result on the canvas."""
        if self.left_image and self.overlay_image:  
            self.result_image = basicOperations.apply_overlay(
                self.left_image, self.overlay_image, self.overlay_transparency.get(), self.overlay_position
            )
            self.display_image(self.result_image, self.result_canvas, zoom=1.0, side='result')
            messagebox.showinfo("Success", "Overlay applied successfully!")
        else:
            messagebox.showwarning("Warning", "Please upload both base image and overlay image before applying!")





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


    def apply_dilation(self):
        if self.left_image:
            self.result_image = BinaryOperation.dilation(self.left_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_erosion(self):
        if self.left_image:
            self.result_image = BinaryOperation.erosion(self.left_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_opening(self):
        if self.left_image:
            self.result_image = BinaryOperation.opening(self.left_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_closing(self):
        if self.left_image:
            self.result_image = BinaryOperation.closing(self.left_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_boundary_extraction(self):
        if self.left_image:
            self.result_image = BinaryOperation.boundary_extraction(self.left_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_skeletonization(self):
        if self.left_image:
            # Convert to grayscale and binary
            gray_image = self.left_image.convert('L')  # Convert to grayscale
            binary_image = np.array(gray_image)  # Convert to numpy array
            _, binary_image = cv2.threshold(binary_image, 127, 255, cv2.THRESH_BINARY)
            
            # Perform skeletonization
            skeleton_image = BinaryOperation.skeletonization(binary_image)
            
            # Display result
            self.result_image = skeleton_image
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

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()