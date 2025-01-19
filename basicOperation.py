from PIL import Image, ImageOps, ImageEnhance

class BasicOperations:
    @staticmethod
    def grayscale(image):
        """Convert image to grayscale"""
        return image.convert('L')
    
    @staticmethod
    def negative(image):
        """Create negative of the image"""
        return ImageOps.invert(image)
    
    @staticmethod
    def horizontal_flip(image):
        """Flip image horizontally"""
        return ImageOps.mirror(image)
    
    @staticmethod
    def vertical_flip(image):
        """Flip image vertically"""
        return ImageOps.flip(image)
    
    @staticmethod
    def diagonal_flip(image):
        """Flip image diagonally (rotate 180 degrees)"""
        return image.rotate(180)
    
    @staticmethod
    def crop_image(image, left, top, right, bottom):
        """Crop image based on coordinates"""
        width, height = image.size
        left = int(width * left)
        top = int(height * top)
        right = int(width * right)
        bottom = int(height * bottom)
        return image.crop((left, top, right, bottom))
    
    @staticmethod
    def translate(image, x_offset, y_offset):
        """Translate image by x and y offset"""
        return ImageOps.expand(image, border=(x_offset, y_offset, 0, 0), fill='white')
    
    @staticmethod
    def scale(image, scale_x, scale_y):
        """Scale image by x and y factors"""
        width, height = image.size
        new_width = int(width * scale_x)
        new_height = int(height * scale_y)
        return image.resize((new_width, new_height), Image.LANCZOS)
    
    @staticmethod
    def adjust_rgb_intensity(image, r_intensity, g_intensity, b_intensity):
        """Adjust RGB channel intensities"""
        # Split the image into RGB channels
        r, g, b = image.split()
        
        # Adjust each channel's intensity
        r = ImageEnhance.Brightness(r).enhance(r_intensity / 128)
        g = ImageEnhance.Brightness(g).enhance(g_intensity / 128)
        b = ImageEnhance.Brightness(b).enhance(b_intensity / 128)
        
        # Merge channels back
        return Image.merge('RGB', (r, g, b))