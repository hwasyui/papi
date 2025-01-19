import numpy as np
import cv2
from scipy.ndimage import median_filter
from PIL import Image

class TransformAndFiltering:
    @staticmethod
    def fourier_transformation(image):
        dft = np.fft.fft2(image)
        dft_shift = np.fft.fftshift(dft)  

        magnitude = np.abs(dft_shift)

        # Normalize the magnitude to the range [0, 255] for visualization
        magnitude_normalized = (magnitude / np.max(magnitude)) * 255
        magnitude_normalized = magnitude_normalized.astype(np.uint8)

        # Convert the normalized magnitude to an image
        return Image.fromarray(magnitude_normalized)

    @staticmethod
    def mean_filter(image):
        kernel = np.ones((5, 5), np.float32) / 25 
        filtered_image = cv2.filter2D(np.array(image), -1, kernel)
        return Image.fromarray(filtered_image)
        
    @staticmethod
    def gaussian_filter(image): 
        filtered_image = cv2.GaussianBlur(np.array(image), (5, 5), sigmaX=1)
        return Image.fromarray(filtered_image)

    @staticmethod
    def med_filter(image):
        filtered_image = median_filter(np.array(image), size=3)
        return Image.fromarray(filtered_image)
    
    @staticmethod
    def sobel_filter(image):
        image_array = np.array(image.convert('L'))

        sobel_x = cv2.Sobel(image_array, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(image_array, cv2.CV_64F, 0, 1, ksize=3)

        gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
        gradient_magnitude = (gradient_magnitude / np.max(gradient_magnitude)) * 255
        gradient_magnitude = gradient_magnitude.astype(np.uint8)

        return Image.fromarray(gradient_magnitude)
    
    @staticmethod
    def canny_filter(image, low_threshold=100, high_threshold=200):
        image_array = np.array(image.convert('L'))  
        edges = cv2.Canny(image_array, low_threshold, high_threshold)
        return Image.fromarray(edges)
    
    @staticmethod
    def laplacian_filter(image):
        image_array = np.array(image.convert('L'))
        laplacian = cv2.Laplacian(image_array, cv2.CV_64F)
        laplacian = np.uint8(np.absolute(laplacian))
        return Image.fromarray(laplacian)