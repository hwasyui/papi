import cv2
import numpy as np
from PIL import Image

class BinaryOperation:
    @staticmethod
    def dilation(image):
        kernel = np.ones((3, 3), np.uint8)
        dilated_image = cv2.dilate(np.array(image), kernel, iterations=1)
        return Image.fromarray(dilated_image)

    @staticmethod
    def erosion(image):
        kernel = np.ones((3, 3), np.uint8)
        eroded_image = cv2.erode(np.array(image), kernel, iterations=1)
        return Image.fromarray(eroded_image)

    @staticmethod
    def opening(image):
        kernel = np.ones((3, 3), np.uint8)
        opened_image = cv2.morphologyEx(np.array(image), cv2.MORPH_OPEN, kernel)
        return Image.fromarray(opened_image)

    @staticmethod
    def closing(image):
        kernel = np.ones((3, 3), np.uint8)
        closed_image = cv2.morphologyEx(np.array(image), cv2.MORPH_CLOSE, kernel)
        return Image.fromarray(closed_image)

    @staticmethod
    def boundary_extraction(image):
        kernel = np.ones((3, 3), np.uint8)
        eroded_image = cv2.erode(np.array(image), kernel, iterations=1)
        boundary_image = cv2.subtract(np.array(image), eroded_image)
        return Image.fromarray(boundary_image)

    @staticmethod
    def skeletonization(image):
        # Ensure the image is binary
        skeleton = np.zeros_like(image, dtype=np.uint8)
        temp_image = image.copy()
        kernel = np.ones((3, 3), np.uint8)
        
        while True:
            eroded = cv2.erode(temp_image, kernel)
            temp = cv2.dilate(eroded, kernel)
            temp = cv2.subtract(temp_image, temp)
            skeleton = cv2.bitwise_or(skeleton, temp)
            temp_image = eroded.copy()
            if cv2.countNonZero(temp_image) == 0:
                break
        
        return Image.fromarray(skeleton)
