import math
from PIL import Image, ImageOps, ImageEnhance, ImageDraw

class basicOperations:

    @staticmethod
    def to_grayscale(image):
        """
        Convert the image to grayscale.
        :param image: PIL.Image object
        :return: Grayscale image
        """
        if not isinstance(image, Image.Image):
            raise ValueError("Input must be a PIL.Image object")
        return ImageOps.grayscale(image)

    @staticmethod
    def to_negative(image):
        """
        Convert the image to its negative.
        :param image: PIL.Image object
        :return: Negative image
        """
        if not isinstance(image, Image.Image):
            raise ValueError("Input must be a PIL.Image object")
        return ImageOps.invert(image.convert("RGB"))

    @staticmethod
    def horizontal_flip(image):
        """
        Flip the image horizontally.
        :param image: PIL.Image object
        :return: Horizontally flipped image
        """
        if not isinstance(image, Image.Image):
            raise ValueError("Input must be a PIL.Image object")
        return ImageOps.mirror(image)

    @staticmethod
    def vertical_flip(image):
        """
        Flip the image vertically.
        :param image: PIL.Image object
        :return: Vertically flipped image
        """
        if not isinstance(image, Image.Image):
            raise ValueError("Input must be a PIL.Image object")
        return ImageOps.flip(image)

    @staticmethod
    def diagonal_flip(image):
        """
        Flip the image diagonally (transpose).
        :param image: PIL.Image object
        :return: Diagonally flipped image
        """
        if not isinstance(image, Image.Image):
            raise ValueError("Input must be a PIL.Image object")
        return image.transpose(Image.TRANSPOSE)
    
    @staticmethod
    def crop_image(image, width, height):
        """
        Fungsi untuk melakukan cropping gambar berdasarkan ukuran.
        :param image: Gambar input (PIL Image object)
        :param width: Lebar hasil cropping
        :param height: Tinggi hasil cropping
        :return: Gambar hasil cropping
        """
        from PIL import Image

        # Dapatkan ukuran asli gambar
        original_width, original_height = image.size

        # Hitung titik awal cropping agar gambar terpusat
        left = (original_width - width) // 2
        top = (original_height - height) // 2
        right = left + width
        bottom = top + height

        # Lakukan cropping
        return image.crop((left, top, right, bottom))

    @staticmethod
    def crop_image_by_shape(image, shape):
        """
        Fungsi untuk melakukan cropping gambar berdasarkan bentuk tertentu (lingkaran, bintang, dll).
        :param image: Gambar input (PIL Image object)
        :param shape: Bentuk cropping ("Circle", "Star", "Diamond")
        :return: Gambar hasil cropping
        """
        from PIL import Image, ImageDraw

        # Buat masker berbentuk sesuai parameter
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)

        width, height = image.size

        if shape == "Circle":
            draw.ellipse((0, 0, width, height), fill=255)
        elif shape == "Star":
            # Buat bentuk bintang sederhana (5 sisi)
            center_x, center_y = width // 2, height // 2
            radius = min(width, height) // 2
            points = []
            for i in range(10):
                angle = i * (3.14159 / 5)  # Sudut 36 derajat
                r = radius if i % 2 == 0 else radius // 2
                x = center_x + r * math.cos(angle)
                y = center_y - r * math.sin(angle)
                points.append((x, y))
            draw.polygon(points, fill=255)
        elif shape == "Diamond":
            # Bentuk belah ketupat
            draw.polygon([
                (width // 2, 0),
                (width, height // 2),
                (width // 2, height),
                (0, height // 2)
            ], fill=255)
        else:
            raise ValueError(f"Unknown shape: {shape}")

        # Terapkan masker ke gambar
        result = Image.new("RGBA", image.size)
        result.paste(image, (0, 0), mask=mask)

        return result



    @staticmethod
    def translate(image, right, left, up, down):
        """
        Translate the image by the specified amounts.
        :param image: PIL.Image object
        :param right: Pixels to move right
        :param left: Pixels to move left
        :param up: Pixels to move up
        :param down: Pixels to move down
        :return: Translated image
        """
        if not isinstance(image, Image.Image):
            raise ValueError("Input must be a PIL.Image object")

        # Hitung offset horizontal dan vertikal
        x_offset = right - left
        y_offset = down - up

        # Buat bounding box transformasi
        width, height = image.size
        translation_matrix = (1, 0, x_offset, 0, 1, y_offset)

        # Transformasi gambar dengan offset
        translated_image = image.transform(
            (width, height),
            Image.AFFINE,
            translation_matrix,
            resample=Image.BICUBIC,
        )
        return translated_image


    @staticmethod
    def scale(image, scale_x, scale_y):
        """
        Scale the image by the specified factors.
        :param image: PIL.Image object
        :param scale_x: Scaling factor in the x-direction
        :param scale_y: Scaling factor in the y-direction
        :return: Scaled image
        """
        if not isinstance(image, Image.Image):
            raise ValueError("Input must be a PIL.Image object")
        width, height = image.size
        new_width = int(width * scale_x)
        new_height = int(height * scale_y)
        return image.resize((new_width, new_height))

    @staticmethod
    def adjust_rgb_intensity(image, red, green, blue):
        """
        Adjust the RGB intensity of the image.
        :param image: PIL.Image object
        :param red: Intensity for red channel (0-255)
        :param green: Intensity for green channel (0-255)
        :param blue: Intensity for blue channel (0-255)
        :return: Image with adjusted RGB intensity
        """
        if not isinstance(image, Image.Image):
            raise ValueError("Input must be a PIL.Image object")

        r, g, b = image.split()
        r = ImageEnhance.Brightness(r).enhance(red / 255)
        g = ImageEnhance.Brightness(g).enhance(green / 255)
        b = ImageEnhance.Brightness(b).enhance(blue / 255)
        return Image.merge("RGB", (r, g, b))

    @staticmethod
    def add_border(image, thickness, color):
        """
        Add a border to the image.
        :param image: PIL.Image object
        :param thickness: Thickness of the border
        :param color: Color of the border
        :return: Image with border
        """
        if not isinstance(image, Image.Image):
            raise ValueError("Input must be a PIL.Image object")

        width, height = image.size
        new_width = width + 2 * thickness
        new_height = height + 2 * thickness

        bordered_image = Image.new("RGB", (new_width, new_height), color)
        bordered_image.paste(image, (thickness, thickness))
        return bordered_image

    @staticmethod
    def apply_overlay(base_image, overlay_image, transparency, position):
            """
            Apply an overlay image to the base image at a specific position with transparency.
            :param base_image: PIL Image object for the base image
            :param overlay_image: PIL Image object for the overlay image
            :param transparency: Float value between 0.1 and 1.0 for transparency
            :param position: Tuple (x, y) for the top-left position of the overlay
            :return: PIL Image object with the overlay applied
            """
            from PIL import Image

            # Create a new image to hold the result
            result = base_image.copy().convert("RGBA")
            overlay = overlay_image.copy()

            # Apply transparency to the overlay
            alpha = int(255 * transparency)
            overlay.putalpha(alpha)

            # Paste the overlay onto the base image at the specified position
            result.paste(overlay, position, overlay)

            return result
    
    


    def adjust_brightness(image, value):
        """
        Adjust the brightness of the image.
        :param image: Input PIL image.
        :param value: Float, brightness adjustment factor (negative for decrease, positive for increase).
        :return: Adjusted PIL image.
        """
        try:
            enhancer = ImageEnhance.Brightness(image)
            return enhancer.enhance(1 + value / 100.0)
        except Exception as e:
            raise RuntimeError(f"Failed to adjust brightness: {e}")


    def adjust_contrast(image, value):
        """
        Adjust the contrast of the image.
        :param image: Input PIL image.
        :param value: Float, contrast adjustment factor (negative for decrease, positive for increase).
        :return: Adjusted PIL image.
        """
        try:
            enhancer = ImageEnhance.Contrast(image)
            return enhancer.enhance(1 + value / 100.0)
        except Exception as e:
            raise RuntimeError(f"Failed to adjust contrast: {e}")


    def rotate_image(image, angle):
        """
        Rotate the image by a given angle.
        :param image: Input PIL image.
        :param angle: Float, rotation angle in degrees (-360 to 360).
        :return: Rotated PIL image.
        """
        try:
            return image.rotate(angle, expand=True)
        except Exception as e:
            raise RuntimeError(f"Failed to rotate image: {e}")
        
    def apply_sepia(image):
        """
        Apply a sepia filter to the image.
        :param image: Input PIL image.
        :return: Image with sepia filter applied.
        """
        try:
            sepia_image = image.convert("RGB")
            pixels = sepia_image.load()

            for y in range(sepia_image.height):
                for x in range(sepia_image.width):
                    r, g, b = pixels[x, y]

                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)

                    pixels[x, y] = (min(255, tr), min(255, tg), min(255, tb))

            return sepia_image
        except Exception as e:
            raise RuntimeError(f"Failed to apply sepia filter: {e}")
        
    def apply_cyanotype(image):
        """
        Apply a cyanotype filter to the image.
        :param image: Input PIL image.
        :return: Image with cyanotype filter applied.
        """
        try:
            cyan_image = image.convert("RGB")
            pixels = cyan_image.load()

            for y in range(cyan_image.height):
                for x in range(cyan_image.width):
                    r, g, b = pixels[x, y]

                    # Apply cyanotype effect (boost blue, reduce red/green)
                    tr = int(r * 0.3)
                    tg = int(g * 0.4)
                    tb = int(b * 1.5)

                    pixels[x, y] = (min(255, tr), min(255, tg), min(255, tb))

            return cyan_image
        except Exception as e:
            raise RuntimeError(f"Failed to apply cyanotype filter: {e}")

    def apply_custom_color(image, hex_color):
        """
        Apply a custom color filter to the image.
        :param image: Input PIL image.
        :param hex_color: Hex string for the filter color (e.g., "#FF5733").
        :return: Image with custom color filter applied.
        """
        try:
            # Convert HEX color to RGB
            custom_color = Image.new("RGB", image.size, hex_color)
            return Image.blend(image.convert("RGB"), custom_color, alpha=0.5)
        except Exception as e:
            raise RuntimeError(f"Failed to apply custom color filter: {e}")


