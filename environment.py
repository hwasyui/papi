import tkinter as tk
import numpy as np
from tkinter import Scale, ttk, messagebox, filedialog
from PIL import Image, ImageTk, ImageFilter, ImageDraw
import cv2
import numpy as np
from mathematicalOperation import MathematicalOperations
from imageEnhancement import ImageEnhancement
from transformAndFiltering import TransformAndFiltering
from imageRestorationAndImageMatching import ImageMatchingAndImageRestorations
from compression import ImageCompressor
from segmentation import ImageSegmentation
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
            ("Reset", self.reset_image),
            ("Delete Image 1", self.delete_first_image),
            ("Delete Image 2", self.delete_second_image),
            ("Delete Result", self.delete_result_image)
            ]

        for text, command in buttons:
            btn = ttk.Button(self.top_panel, text=text, command=command)
            btn.pack(side=tk.LEFT, padx=5, pady=5)

    def get_base_image(self):
        """
        Return the current result image if it exists, otherwise return the original left image.
        """
        return self.result_image if self.result_image else self.left_image

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

        # Create Transform and Filter Tab
        filter_transform_frame = ttk.Frame(self.operations_notebook)
        self.create_filter_transform_tab(filter_transform_frame)
        self.operations_notebook.add(filter_transform_frame, text="Filter and Transform")

        # Create Image Restoration
        filter_transform_frame = ttk.Frame(self.operations_notebook)
        self.create_image_restoration(filter_transform_frame)
        self.operations_notebook.add(filter_transform_frame, text="Image Restoration")

        # Create Image Restoration
        filter_transform_frame = ttk.Frame(self.operations_notebook)
        self.create_image_matching(filter_transform_frame)
        self.operations_notebook.add(filter_transform_frame, text="Image Matching")


        # Create Compression Tab
        compression_ops_frame = ttk.Frame(self.operations_notebook)
        self.create_compression_tab(compression_ops_frame)
        self.operations_notebook.add(compression_ops_frame, text="Compression")

        # Create Segmentation Tab
        segmentation_ops_frame = ttk.Frame(self.operations_notebook)
        self.create_segmentation_tab(segmentation_ops_frame)
        self.operations_notebook.add(segmentation_ops_frame, text="Segmentation")

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
        quality_options = ["Lossy Compression", 10, 30, 50, 70, 90]
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
        # Get the base image (result image if exists, otherwise the left/original image)
        base_image = self.get_base_image()

        if base_image:
            # Initialize compressor and perform RLE compression
            compressor = ImageCompressor(base_image)
            rle_encoded = compressor.apply_rle()
            self.compressed_file_size = len(rle_encoded) * 2
            decoded_image_array = compressor.run_length_decoding(rle_encoded)
            self.result_image = Image.fromarray(decoded_image_array, mode='L')

            # Display the result image in the result canvas
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')

            # Display alert for autosave
            messagebox.showinfo("Autosave", "This is autosave. Compressed image has been saved.")

            # Autosave compressed image
            save_path = filedialog.asksaveasfilename(
                title="Save Compressed Image",
                defaultextension=".png",
                filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("All Files", "*.*")]
            )
            if save_path:
                self.result_image.save(save_path)
                messagebox.showinfo("Success", f"Image saved successfully at: {save_path}")

            # Update file size display
            self.update_file_size_display()

            # Save the current state for undo
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")


    def apply_lossy_compression(self):
        # Get the base image (result image if exists, otherwise the left/original image)
        base_image = self.get_base_image()

        if base_image:
            quality = self.quality_var.get()
            if quality == "Select Quality":
                messagebox.showwarning("Warning", "Please select a quality for lossy compression!")
                return

            quality = int(quality)
            compressor = ImageCompressor(base_image)

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

            # Display the result image
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')

            # Autosave functionality
            messagebox.showinfo("Autosave", "This is autosave. Compressed image has been saved.")
            save_path = filedialog.asksaveasfilename(
                title="Save Compressed Image",
                defaultextension=".jpg",
                filetypes=[("JPEG Files", "*.jpg"), ("PNG Files", "*.png"), ("All Files", "*.*")]
            )
            if save_path:
                self.result_image.save(save_path, format="JPEG", quality=quality)
                messagebox.showinfo("Success", f"Image saved successfully at: {save_path}")

            # Update file size display
            self.update_file_size_display()

            # Save the current state for undo
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def create_segmentation_tab(self, parent):
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.X, padx=10, pady=10)

        # Pixel-based section
        pixel_frame = ttk.LabelFrame(main_frame, text="Pixel-base Segementation")
        pixel_frame.pack(fill=tk.X, pady=5)

        # Edge-based Section
        global_frame = ttk.LabelFrame(main_frame, text="Edge-Based Thresholding")
        global_frame.pack(fill=tk.X, pady=5)
        ttk.Button(global_frame, text="Edge Detected", command=self.edge_detected).pack(pady=5)
        ttk.Button(global_frame, text="Sobel", command=self.apply_edge_sobel).pack(pady=5)
        ttk.Button(global_frame, text="Prewitt", command=self.apply_edge_prewitt).pack(pady=5)
        ttk.Button(global_frame, text="Robert Operator", command=self.apply_edge_robert).pack(pady=5)

        # Region Base Thresholding Section
        adaptive_frame = ttk.LabelFrame(main_frame, text="Region Base")
        adaptive_frame.pack(fill=tk.X, pady=5)
        ttk.Button(adaptive_frame, text="Growing", command=self.apply_region_growing).pack(pady=5)
        ttk.Button(adaptive_frame, text="Watershed", command=self.apply_region_watershed).pack(pady=5)

        # K-means Section
        kmeans_frame = ttk.LabelFrame(main_frame, text="K-Means Clustering")
        kmeans_frame.pack(fill=tk.X, pady=5)
        ttk.Button(kmeans_frame, text="Apply K-Means Clustering", command=self.apply_kmeans_clustering).pack(pady=5)
    
    def edge_detected(self):
        # Get the base image (result image if exists, otherwise the left/original image)
        base_image = self.get_base_image()

        if base_image:
            segmentation = ImageSegmentation(base_image)
            self.result_image = segmentation.edge_detected()
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")
    
    def apply_edge_sobel(self):
        # Get the base image (result image if exists, otherwise the left/original image)
        base_image = self.get_base_image()

        if base_image:
            segmentation = ImageSegmentation(base_image)
            self.result_image = segmentation.apply_edge_sobel()
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    
    def apply_edge_prewitt(self):
        # Get the base image (result image if exists, otherwise the left/original image)
        base_image = self.get_base_image()

        if base_image:
            segmentation = ImageSegmentation(base_image)
            self.result_image = segmentation.apply_edge_prewitt()
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_edge_robert(self):
        # Get the base image (result image if exists, otherwise the left/original image)
        base_image = self.get_base_image()

        if base_image:
            segmentation = ImageSegmentation(base_image)
            self.result_image = segmentation.apply_edge_robert()
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_region_growing(self):
        # Menggunakan gambar basis dari get_base_image
        base_image = self.get_base_image()
        
        if base_image:
            # Contoh titik awal; ganti dengan koordinat aktual
            seed_point = (50, 50)  # Replace with actual coordinates
            segmentation = ImageSegmentation(base_image)
            self.result_image = segmentation.apply_region_growing(seed_point)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")


    def apply_region_watershed(self):
        base_image = self.get_base_image()  # Menggunakan get_base_image untuk mendapatkan gambar yang akan digunakan.
        if base_image:
            segmentation = ImageSegmentation(base_image)
            self.result_image = segmentation.apply_region_watershed()
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")


    def apply_kmeans_clustering(self):
        # Gunakan get_base_image untuk menentukan gambar yang akan diproses
        base_image = self.get_base_image()
        
        if base_image:
            segmentation = ImageSegmentation(base_image)
            self.result_image = segmentation.apply_kmeans_clustering()
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    
    def create_filter_transform_tab(self, parent): 
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(main_frame, text="Apply Fourier Transformation", command=self.apply_fourier_transformation).pack(pady=5)

        # Filter Operations
        pixel_ops_frame = ttk.LabelFrame(main_frame, text="Filter Operations")
        pixel_ops_frame.pack(fill=tk.X, pady=5)

        ttk.Button(pixel_ops_frame, text="Mean", command=self.apply_mean_filter).pack(side=tk.LEFT, padx=5)
        ttk.Button(pixel_ops_frame, text="Gaussian", command=self.apply_gaussian_filter).pack(side=tk.LEFT, padx=5)
        ttk.Button(pixel_ops_frame, text="Median", command=self.apply_median_filter).pack(side=tk.LEFT, padx=5)

         # Transform Operations
        pixel_ops_frame = ttk.LabelFrame(main_frame, text="Transform Operations")
        pixel_ops_frame.pack(fill=tk.X, pady=5)

        ttk.Button(pixel_ops_frame, text="Sobel", command=self.apply_sobel).pack(side=tk.LEFT, padx=5)
        ttk.Button(pixel_ops_frame, text="Canny", command=self.apply_canny).pack(side=tk.LEFT, padx=5)
        ttk.Button(pixel_ops_frame, text="Laplacian", command=self.apply_laplacian).pack(side=tk.LEFT, padx=5)

    def create_image_restoration(self, parent):
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Button(main_frame, text="Apply Wiener Filter", command=self.apply_wiener).pack(pady=5)
        ttk.Button(main_frame, text="Apply Gaussian Filter", command=self.apply_gaussian_filter).pack(pady=5)

    def create_image_matching(self, parent):
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Button(main_frame, text="Apply SIFT Matching", command=self.apply_sift).pack(pady=5)
        ttk.Button(main_frame, text="Apply ORB Matching", command=self.apply_orb).pack(pady=5)


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

    def delete_first_image(self):
        if self.left_image:
            self.left_image = None
            self.original_image = None
            self.result_image = None
            self.display_image(self.left_image, self.left_canvas, self.left_zoom, 'left')  # Clear the left canvas
        else:
            messagebox.showwarning("Warning", "No first image to delete!")

    def delete_second_image(self):
        if self.right_image:
            self.right_image = None
            self.display_image(self.right_image, self.right_canvas, self.right_zoom, 'right')  # Clear the right canvas
        else:
            messagebox.showwarning("Warning", "No second image to delete!")

    def delete_result_image(self):
        if self.result_image:
            self.result_image = None
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')  # Clear the result canvas
        else:
            messagebox.showwarning("Warning", "No result image to delete!")



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
        base_image = self.get_base_image()
        if base_image is None:
            messagebox.showwarning("No Image", "Please upload an image first.")
            return
        self.result_image = basicOperations.to_grayscale(base_image)
        self.save_state_for_undo()
        self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')



    def apply_negative(self):
        base_image = self.get_base_image()
        if base_image is None:
            messagebox.showwarning("No Image", "Please upload an image first.")
            return
        self.save_state_for_undo()
        self.result_image = basicOperations.to_negative(base_image)
        self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')

    def apply_horizontal_flip(self):
        base_image = self.get_base_image()
        if base_image is None:
            messagebox.showwarning("No Image", "Please upload an image first.")
            return
        self.save_state_for_undo()
        self.result_image = basicOperations.horizontal_flip(base_image)
        self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')


    def apply_vertical_flip(self):
        base_image = self.get_base_image()
        if base_image is None:
            messagebox.showwarning("No Image", "Please upload an image first.")
            return
        self.save_state_for_undo()
        self.result_image = basicOperations.vertical_flip(base_image)
        self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')

    def apply_diagonal_flip(self):
        base_image = self.get_base_image()
        if base_image is None:
            messagebox.showwarning("No Image", "Please upload an image first.")
            return
        self.save_state_for_undo()
        self.result_image = basicOperations.diagonal_flip(base_image)
        self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')


    def apply_crop_method1(self):
        # Gunakan gambar dasar (result_image jika ada, atau left_image jika tidak ada)
        base_image = self.get_base_image()

        if base_image:
            try:
                # Ambil nilai width dan height dari input
                width = int(self.crop_width.get())
                height = int(self.crop_height.get())

                # Lakukan cropping pada gambar dasar
                self.result_image = basicOperations.crop_image(base_image, width, height)

                # Tampilkan hasil gambar dan simpan state untuk undo
                self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
                self.save_state_for_undo()
            except ValueError:
                messagebox.showerror("Error", "Invalid width or height value. Please enter valid integers.")
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_crop_method2(self):
        # Gunakan gambar dasar (result_image jika ada, atau left_image jika tidak ada)
        base_image = self.get_base_image()

        if base_image:
            try:
                # Ambil bentuk dari dropdown
                shape = self.shape_var.get()

                # Lakukan cropping berdasarkan bentuk
                self.result_image = basicOperations.crop_image_by_shape(base_image, shape)

                # Tampilkan hasil gambar dan simpan state untuk undo
                self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
                self.save_state_for_undo()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showwarning("Warning", "No image loaded!")



    def apply_translation(self):
        # Gunakan gambar dasar (result_image jika ada, atau left_image jika tidak ada)
        base_image = self.get_base_image()

        if base_image:
            try:
                # Ambil nilai dari slider untuk pergeseran
                right = int(self.translate_right.get())
                left = int(self.translate_left.get())
                up = int(self.translate_up.get())
                down = int(self.translate_down.get())

                # Hitung pergeseran berdasarkan input slider
                self.result_image = basicOperations.translate(base_image, right, left, up, down)

                # Tampilkan hasil gambar dan simpan state untuk undo
                self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
                self.save_state_for_undo()
            except ValueError:
                messagebox.showerror("Error", "Invalid translation values. Please enter valid integers.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showwarning("Warning", "No image loaded!")


    def apply_scaling(self):
        # Gunakan gambar dasar (result_image jika ada, atau left_image jika tidak ada)
        base_image = self.get_base_image()

        if base_image:
            try:
                # Ambil nilai skala dari input (misalnya slider atau entry box)
                scale_x = float(self.scale_x.get())
                scale_y = float(self.scale_y.get())

                # Lakukan operasi scaling pada gambar dasar
                self.result_image = basicOperations.scale(base_image, scale_x, scale_y)

                # Tampilkan hasil gambar dan simpan state untuk undo
                self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
                self.save_state_for_undo()
            except ValueError:
                messagebox.showerror("Error", "Invalid scaling values. Please enter valid numbers.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showwarning("Warning", "No image loaded!")


    def apply_rgb_intensity(self):
        # Gunakan gambar dasar (result_image jika ada, atau left_image jika tidak ada)
        base_image = self.get_base_image()

        if base_image:
            try:
                # Ambil nilai intensitas RGB dari input
                red = int(self.intensity_red.get())
                green = int(self.intensity_green.get())
                blue = int(self.intensity_blue.get())

                # Validasi nilai intensitas (contoh: range 0-255)
                if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
                    raise ValueError("RGB intensity values must be between 0 and 255.")

                # Lakukan operasi penyesuaian intensitas RGB
                self.result_image = basicOperations.adjust_rgb_intensity(base_image, red, green, blue)

                # Tampilkan hasil gambar dan simpan state untuk undo
                self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
                self.save_state_for_undo()

            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showwarning("Warning", "No image loaded!")
    def apply_border(self):
        # Gunakan gambar dasar (result_image jika ada, atau left_image jika tidak ada)
        base_image = self.get_base_image()

        if base_image:
            try:
                # Ambil ketebalan border dan warna dari input pengguna
                thickness = int(self.border_thickness.get())
                color = self.border_color.get() or "black"  # Default ke warna hitam jika tidak ada input

                # Validasi ketebalan border
                if thickness < 0:
                    raise ValueError("Border thickness must be a non-negative integer.")

                # Tambahkan border ke gambar
                self.result_image = basicOperations.add_border(base_image, thickness, color)

                # Tampilkan hasil gambar dan simpan state untuk undo
                self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
                self.save_state_for_undo()
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showwarning("Warning", "No image loaded!")


    def upload_and_drag_overlay(self):
        overlay_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if overlay_path:
            try:
                # Load the overlay image
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
        if self.overlay_image:
            self.overlay_start_x = event.x
            self.overlay_start_y = event.y

    def do_drag(self, event):
        """Handle dragging of overlay."""
        if self.overlay_image:
            # Calculate the drag delta
            dx = event.x - self.overlay_start_x
            dy = event.y - self.overlay_start_y
            
            # Update the overlay position
            self.overlay_position = (self.overlay_position[0] + dx, self.overlay_position[1] + dy)
            
            # Update drag start positions
            self.overlay_start_x = event.x
            self.overlay_start_y = event.y
            
            # Refresh the overlay preview
            self.update_overlay_preview()

    def update_overlay_preview(self):
        """Update the canvas to show the overlay in its current position."""
        base_image = self.get_base_image()  # Get the base image

        if base_image and self.overlay_image:
            try:
                # Apply the overlay to the base image
                overlay_preview = basicOperations.apply_overlay(
                    base_image,
                    self.overlay_image,
                    self.overlay_transparency.get(),
                    self.overlay_position
                )

                # Display the overlay preview
                self.display_image(overlay_preview, self.result_canvas, zoom=1.0, side='result')
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while updating overlay preview: {e}")

    def apply_overlay_to_canvas(self):
        """Apply the overlay and display the final result on the canvas."""
        base_image = self.get_base_image()  # Get the base image

        if base_image and self.overlay_image:
            try:
                # Apply the overlay to the base image
                self.result_image = basicOperations.apply_overlay(
                    base_image,
                    self.overlay_image,
                    self.overlay_transparency.get(),
                    self.overlay_position
                )

                # Display the final image and save the state for undo
                self.display_image(self.result_image, self.result_canvas, zoom=1.0, side='result')
                self.save_state_for_undo()
                messagebox.showinfo("Success", "Overlay applied successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while applying overlay: {e}")
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
        base_image = self.get_base_image()
        if base_image is None:
            messagebox.showwarning("No Image", "Please upload an image first.")
            return
        self.result_image = ImageEnhancement.histogram_equalization(base_image)
        self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
        self.save_state_for_undo()

    def apply_contrast_stretching(self):
        base_image = self.get_base_image()
        if base_image is None:
            messagebox.showwarning("No Image", "Please upload an image first.")
            return
        low_in = int(self.contrast_low_in.get())
        high_in = int(self.contrast_high_in.get())
        low_out = int(self.contrast_low_out.get())
        high_out = int(self.contrast_high_out.get())
        self.result_image = ImageEnhancement.contrast_stretching(base_image, low_in, high_in, low_out, high_out)
        self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
        self.save_state_for_undo()
        

    def apply_gamma_correction(self):
        base_image = self.get_base_image()
        if base_image is None:
            messagebox.showwarning("No Image", "Please upload an image first.")
            return
        gamma = self.gamma_value.get()
        self.result_image = ImageEnhancement.gamma_correction(base_image, gamma)
        self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
        self.save_state_for_undo()

    def apply_fourier_transformation(self):
        if self.left_image:
            self.result_image = TransformAndFiltering.fourier_transformation(self.left_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")
            
    def apply_mean_filter(self):
        if self.left_image:
            self.result_image = TransformAndFiltering.mean_filter(self.left_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_median_filter(self):
        if self.left_image:
            self.result_image = TransformAndFiltering.med_filter(self.left_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_gaussian_filter(self):
        if self.left_image:
            self.result_image = TransformAndFiltering.gaussian_filter(self.left_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_sobel(self):
        if self.left_image:
            self.result_image = TransformAndFiltering.sobel_filter(self.left_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")
    
    def apply_canny(self):
        if self.left_image:
            self.result_image = TransformAndFiltering.canny_filter(self.left_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")
        

    def apply_laplacian(self):
        if self.left_image:
            self.result_image = TransformAndFiltering.laplacian_filter(self.left_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_wiener(self):
        if self.left_image:
            self.result_image = ImageMatchingAndImageRestorations.wiener_filter(self.left_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_sift(self):
        if self.left_image:
            self.result_image = ImageMatchingAndImageRestorations.sift_detector(self.left_image, self.right_image)
            self.display_image(self.result_image, self.result_canvas, self.result_zoom, 'result')
            self.save_state_for_undo()
        else:
            messagebox.showwarning("Warning", "No image loaded!")

    def apply_orb(self):
        if self.left_image:
            self.result_image = ImageMatchingAndImageRestorations.orb_detector(self.left_image, self.right_image)
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
        self.update_file_size_display() 

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()