import numpy as np
import cv2  # OpenCV for DCT
from PIL import Image

class ImageCompressor:
    def __init__(self, image):
        self.image = image

    def apply_rle(self):
        """Applies Run Length Encoding (RLE) to the image."""
        img_array = np.array(self.image)
        return self.run_length_encoding(img_array)

    def run_length_encoding(self, img_array):
        """Implements the RLE algorithm."""
        rle_encoded = []
        height, width, _ = img_array.shape  # Get the dimensions of the image

        for row in range(height):
            count = 1
            for col in range(1, width):
                if np.array_equal(img_array[row, col], img_array[row, col - 1]):
                    count += 1
                else:
                    rle_encoded.append((img_array[row, col - 1].tolist(), count))  # Convert to list for storage
                    count = 1
            rle_encoded.append((img_array[row, -1].tolist(), count))  # Append the last run
        return rle_encoded

    def run_length_decoding(self, rle_encoded):
        """Decodes RLE encoded data back to an image."""
        img_array = []
        for value, count in rle_encoded:
            img_array.extend([value] * count)
        return np.array(img_array).reshape(self.image.size[1], self.image.size[0], 3)  # Assuming RGB

    def apply_dct(self, quality):
        """Applies Discrete Cosine Transform (DCT) to the image."""
        img_array = np.array(self.image)
        return self.discrete_cosine_transform(img_array, quality)

    def discrete_cosine_transform(self, img_array, quality):
        """Implements the DCT algorithm."""
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
        dct = cv2.dct(np.float32(img_array))  # Apply DCT
        quantization_matrix = np.ones((8, 8)) * (100 - quality) / 100
        dct_quantized = np.round(dct / quantization_matrix)
        return dct_quantized

    def inverse_dct(self, dct_encoded):
        """Applies Inverse DCT to get back the image."""
        img_reconstructed = cv2.idct(dct_encoded)
        img_reconstructed = np.clip(img_reconstructed, 0, 255).astype(np.uint8)
        return Image.fromarray(img_reconstructed)