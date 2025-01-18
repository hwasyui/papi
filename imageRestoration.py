import numpy as np
import cv2
from scipy.signal import convolve2d

class ImageRestorations:
    @staticmethod
    def wiener_filter(image, kernel_size=5, noise_var=25, signal_var=100):
        kernel = np.ones((kernel_size, kernel_size)) / (kernel_size * kernel_size)
        blurred_image = convolve2d(image, kernel, mode='same', boundary='symm')
        noise_est = noise_var
        signal_est = signal_var
        ratio = signal_est / (signal_est + noise_est)
        filtered_image = blurred_image * ratio
        return np.clip(filtered_image, 0, 255).astype(np.uint8)

    @staticmethod
    def sift_detector(image1, image2 ):
        sift = cv2.SIFT_create()
        keypoints1, descriptors1 = sift.detectAndCompute(image1, None)
        keypoints2, descriptors2 = sift.detectAndCompute(image2, None)
        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
        matches = bf.match(descriptors1, descriptors2)
        matches = sorted(matches, key=lambda x: x.distance)
        matching_result = cv2.drawMatches(image1, keypoints1, image2, keypoints2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        return matching_result

    @staticmethod
    def orb_detector(image1, image2):
        orb= cv2.ORB_create()
        keypoints1, descriptors1 = orb.detectAndCompute(image1, None) 
        keypoints2, descriptors2 = orb.detectAndCompute(image2, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(descriptors1, descriptors2)
        matches = sorted(matches, key = lambda x: x.distance)
        result_image = cv2.drawMatches(image1, keypoints1, image2, keypoints2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        return result_image