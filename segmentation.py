import numpy as np
import cv2
from PIL import Image

class ImageSegmentation:
    def __init__(self, image):
        self.image = image.convert("RGB")  # Ensure the image is in RGB format
        self.image_array = np.array(self.image)

    def edge_detected(self):
        # Convert to grayscale
        gray_image = cv2.cvtColor(self.image_array, cv2.COLOR_RGB2GRAY)
        # Apply Canny edge detection
        edges = cv2.Canny(gray_image, 100, 200)
        return Image.fromarray(edges)

    def apply_edge_sobel(self):
        # Convert to grayscale
        gray_image = cv2.cvtColor(self.image_array, cv2.COLOR_RGB2GRAY)
        # Apply Sobel operator
        sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
        # Convert gradients to absolute values
        sobel_x = cv2.convertScaleAbs(sobel_x)
        sobel_y = cv2.convertScaleAbs(sobel_y)
        #Sobel combined
        sobel_combined = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)
        return Image.fromarray(sobel_combined)

    def apply_edge_prewitt(self):
        # Prewitt operator kernels
        kernel_x = np.array([[-1, 0, 1],
                             [-1, 0, 1],
                             [-1, 0, 1]])
        kernel_y = np.array([[1, 1, 1],
                             [0, 0, 0],
                             [-1, -1, -1]])
        
        # Convert to grayscale
        gray_image = cv2.cvtColor(self.image_array, cv2.COLOR_RGB2GRAY)
        # Apply Prewitt operator
        prewitt_x = cv2.filter2D(gray_image, -1, kernel_x)
        prewitt_y = cv2.filter2D(gray_image, -1, kernel_y)
        prewitt_combined = cv2.addWeighted(prewitt_x, 0.5, prewitt_y, 0.5, 0)  # Ensure values are in valid range
        return Image.fromarray(prewitt_combined)

    
    def apply_edge_robert(self):
        # Roberts operator kernels
        kernel_x = np.array([[1, 0],
                             [0, -1]])
        kernel_y = np.array([[0, 1],
                             [-1, 0]])
        
        # Convert to grayscale
        gray_image = cv2.cvtColor(self.image_array, cv2.COLOR_RGB2GRAY)
        # Apply Roberts operator
        roberts_x = cv2.filter2D(gray_image, -1, kernel_x)
        roberts_y = cv2.filter2D(gray_image, -1, kernel_y)
        roberts_combined = cv2.addWeighted(roberts_x, 0.5, roberts_y, 0.5, 0)
        return Image.fromarray(roberts_combined)

    def apply_region_growing(self, seed_point, threshold=10):
        # Convert to grayscale
        gray_image = cv2.cvtColor(self.image_array, cv2.COLOR_RGB2GRAY)
        height, width = gray_image.shape
        segmented_image = np.zeros_like(gray_image)

        # Initialize the seed point
        x, y = seed_point
        seed_value = gray_image[y, x]
        segmented_image[y, x] = 255  # Mark the seed point

        # Create a list for the pixels to be checked
        pixel_list = [(x, y)]

        while pixel_list:
            x, y = pixel_list.pop()
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        if segmented_image[ny, nx] == 0:  # Not yet segmented
                            if abs(int(gray_image[ny, nx]) - int(seed_value)) < threshold:
                                segmented_image[ny, nx] = 255  # Mark as part of the region
                                pixel_list.append((nx, ny))

        return Image.fromarray(segmented_image)


    def apply_region_watershed(self):
        # Convert to grayscale and apply Gaussian blur
        gray_image = cv2.cvtColor(self.image_array, cv2.COLOR_RGB2GRAY)
        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

        # Apply thresholding to get a binary image
        _, binary_image = cv2.threshold(blurred_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Find sure background area
        sure_bg = cv2.dilate(binary_image, np.ones((3, 3), np.uint8), iterations=3)

        # Find sure foreground area
        dist_transform = cv2.distanceTransform(binary_image, cv2.DIST_L2, 5)
        _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

        # Find unknown region
        unknown = cv2.subtract(sure_bg, np.uint8(sure_fg))

        # Label markers
        _, markers = cv2.connectedComponents(np.uint8(sure_fg))

        # Add one to all the labels to distinguish sure regions from unknown
        markers = markers + 1
        markers[unknown == 255] = 0  # Mark the unknown region with zero

        # Apply watershed algorithm
        markers = cv2.watershed(self.image_array, markers)
        self.image_array[markers == -1] = [255, 0, 0]  # Mark the boundaries in red

        # Convert back to RGB for display
        return Image.fromarray(self.image_array)

    def apply_kmeans_clustering(self, k=3):
        # Reshape the image to a 2D array of pixels
        pixel_values = self.image_array.reshape((-1, 3))
        pixel_values = np.float32(pixel_values)

        # Define criteria and apply kmeans
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        _, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        # Convert back to 8 bit values
        centers = np.uint8(centers)
        segmented_image = centers[labels.flatten()]
        segmented_image = segmented_image.reshape(self.image_array.shape)

        return Image.fromarray(segmented_image)