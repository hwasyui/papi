from PIL import Image, ImageChops
import numpy as np

class MathematicalOperations:
    @staticmethod
    def resize_images(image1, image2):
        # Resize image2 to match image1's size
        return image1, image2.resize(image1.size)

    @staticmethod
    def pixelwise_addition(image1, image2):
        image1, image2 = MathematicalOperations.resize_images(image1, image2)
        return ImageChops.add(image1, image2)

    @staticmethod
    def pixelwise_subtraction(image1, image2):
        image1, image2 = MathematicalOperations.resize_images(image1, image2)
        return ImageChops.subtract(image1, image2)

    @staticmethod
    def pixelwise_multiplication(image1, image2):
        image1, image2 = MathematicalOperations.resize_images(image1, image2)
        arr1 = np.array(image1)
        arr2 = np.array(image2)
        result = np.clip(arr1 * arr2 / 255, 0, 255).astype(np.uint8)
        return Image.fromarray(result)

    @staticmethod
    def pixelwise_division(image1, image2):
        image1, image2 = MathematicalOperations.resize_images(image1, image2)
        arr1 = np.array(image1)
        arr2 = np.array(image2)
        result = np.clip(arr1 / (arr2 + 1e-10) * 255, 0, 255).astype(np.uint8)  # Avoid division by zero
        return Image.fromarray(result)

    @staticmethod
    def bitwise_and(image1, image2):
        image1, image2 = MathematicalOperations.resize_images(image1, image2)
        arr1 = np.array(image1)
        arr2 = np.array(image2)
        result = np.bitwise_and(arr1, arr2)
        return Image.fromarray(result)

    @staticmethod
    def bitwise_or(image1, image2):
        image1, image2 = MathematicalOperations.resize_images(image1, image2)
        arr1 = np.array(image1)
        arr2 = np.array(image2)
        result = np.bitwise_or(arr1, arr2)
        return Image.fromarray(result)

    @staticmethod
    def bitwise_xor(image1, image2):
        image1, image2 = MathematicalOperations.resize_images(image1, image2)
        arr1 = np.array(image1)
        arr2 = np.array(image2)
        result = np.bitwise_xor(arr1, arr2)
        return Image.fromarray(result)

    @staticmethod
    def bitwise_not(image):
        arr = np.array(image)
        result = np.bitwise_not(arr)
        return Image.fromarray(result)