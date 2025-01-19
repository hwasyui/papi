from PIL import Image, ImageOps, ImageEnhance
import numpy as np

class ImageEnhancement:
    @staticmethod
    def histogram_equalization(image):
        if image.mode != 'L':
            image = image.convert('L')
        histogram, _ = np.histogram(np.array(image).flatten(), bins=256, range=[0, 256])
        cdf = histogram.cumsum()
        cdf_normalized = cdf * histogram.max() / cdf.max()
        image_equalized = ImageOps.equalize(image)
        return image_equalized

    @staticmethod
    def contrast_stretching(image, low_in=0, high_in=255, low_out=0, high_out=255):
        if low_in >= high_in:
            raise ValueError("low_in must be less than high_in")
        if low_out >= high_out:
            raise ValueError("low_out must be less than high_out")

        if image.mode != 'L':
            image = image.convert('L')
        img_array = np.array(image, dtype=np.float32)

        # Apply contrast stretching formula
        img_array = np.clip((img_array - low_in) * (high_out - low_out) / (high_in - low_in) + low_out, 0, 255)
        return Image.fromarray(img_array.astype('uint8'))

    @staticmethod
    def gamma_correction(image, gamma=1.0):
        if image.mode != 'L':
            image = image.convert('L')
        img_array = np.array(image) / 255.0
        img_array = np.clip(img_array ** gamma, 0, 1) * 255
        return Image.fromarray(img_array.astype('uint8'))