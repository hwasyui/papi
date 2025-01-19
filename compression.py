import cv2
import numpy as np
import os
from tkinter import Tk, filedialog, Button, Label, OptionMenu, StringVar, messagebox, ttk
from PIL import Image, ImageTk


class ImageCompressor:
    def __init__(self, image):
        self.image = image

    def apply_rle(self):
        pixels = np.array(self.image.convert('L')).flatten()
        encoded = []
        prev_pixel = pixels[0]
        count = 1
        for pixel in pixels[1:]:
            if pixel == prev_pixel:
                count += 1
            else:
                encoded.append((prev_pixel, count))
                prev_pixel = pixel
                count = 1
        encoded.append((prev_pixel, count))
        return encoded

    def run_length_decoding(self, encoded):
        decoded = []
        for pixel, count in encoded:
            decoded.extend([pixel] * count)
        decoded_array = np.array(decoded, dtype=np.uint8)
        size = self.image.size[::-1]  # Get original shape (height, width)
        return decoded_array.reshape(size)  # Reshape to original image dimensions

    def apply_dct(self, quality):
        image = self.image.convert('L')
        image = np.array(image, dtype=np.float32)

        # Ensure dimensions are multiples of 8
        height, width = image.shape
        padded_height = (height + 7) // 8 * 8
        padded_width = (width + 7) // 8 * 8
        padded_image = np.zeros((padded_height, padded_width), dtype=np.float32)
        padded_image[:height, :width] = image

        # Shift values for DCT processing
        padded_image -= 128

        # Standard JPEG quantization matrix
        quantization_table = np.array([
            [16, 11, 10, 16, 24, 40, 51, 61],
            [12, 12, 14, 19, 26, 58, 60, 55],
            [14, 13, 16, 24, 40, 57, 69, 56],
            [14, 17, 22, 29, 51, 87, 80, 62],
            [18, 22, 37, 56, 68, 109, 103, 77],
            [24, 35, 55, 64, 81, 104, 113, 92],
            [49, 64, 78, 87, 103, 121, 120, 101],
            [72, 92, 95, 98, 112, 100, 103, 99]
        ], dtype=np.float32)

        # Adjust quantization based on quality
        scale_factor = max(1, (100 - quality) / 50.0)
        quantization_matrix = np.clip(quantization_table * scale_factor, 1, 255)

        # Apply DCT and quantization in 8×8 blocks
        dct_encoded = np.zeros_like(padded_image)
        for i in range(0, padded_height, 8):
            for j in range(0, padded_width, 8):
                block = padded_image[i:i+8, j:j+8]
                dct_block = cv2.dct(block)

                # Quantization (zeroing small values)
                quantized_block = np.round(dct_block / quantization_matrix)
                
                # Remove small coefficients based on quality
                threshold = np.max(quantized_block) * (quality / 100.0)
                quantized_block[np.abs(quantized_block) < threshold] = 0

                dct_encoded[i:i+8, j:j+8] = quantized_block * quantization_matrix

        return dct_encoded[:height, :width]  # Remove padding

    def inverse_dct(self, dct_encoded):
        height, width = dct_encoded.shape
        padded_height = (height + 7) // 8 * 8
        padded_width = (width + 7) // 8 * 8
        padded_dct = np.zeros((padded_height, padded_width), dtype=np.float32)
        padded_dct[:height, :width] = dct_encoded

        # Define standard quantization matrix (JPEG-like)
        quantization_table = np.array([
            [16, 11, 10, 16, 24, 40, 51, 61],
            [12, 12, 14, 19, 26, 58, 60, 55],
            [14, 13, 16, 24, 40, 57, 69, 56],
            [14, 17, 22, 29, 51, 87, 80, 62],
            [18, 22, 37, 56, 68, 109, 103, 77],
            [24, 35, 55, 64, 81, 104, 113, 92],
            [49, 64, 78, 87, 103, 121, 120, 101],
            [72, 92, 95, 98, 112, 100, 103, 99]
        ], dtype=np.float32)

        # Apply Inverse DCT in 8x8 blocks
        decoded_image = np.zeros_like(padded_dct)
        for i in range(0, padded_height, 8):
            for j in range(0, padded_width, 8):
                quantized_block = padded_dct[i:i+8, j:j+8]
                idct_block = cv2.idct(quantized_block)
                decoded_image[i:i+8, j:j+8] = idct_block

        # Shift values back to 0-255 range
        decoded_image += 128
        decoded_image = np.clip(decoded_image, 0, 255).astype(np.uint8)

        return decoded_image[:height, :width]  # Remove padding before returning