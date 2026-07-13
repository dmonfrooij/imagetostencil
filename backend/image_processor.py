import cv2
import numpy as np
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    """Process images for stencil generation"""
    
    def __init__(self, image_path):
        self.image_path = image_path
        self.original_image = cv2.imread(image_path)
        if self.original_image is None:
            raise ValueError(f"Could not load image from {image_path}")
        
        self.height, self.width = self.original_image.shape[:2]
        logger.info(f"Loaded image: {self.width}x{self.height}")
    
    def resize_if_needed(self, max_dimension=2048):
        """Resize image if it's too large"""
        if max(self.width, self.height) > max_dimension:
            scale = max_dimension / max(self.width, self.height)
            new_width = int(self.width * scale)
            new_height = int(self.height * scale)
            self.original_image = cv2.resize(self.original_image, (new_width, new_height))
            self.width, self.height = new_width, new_height
            logger.info(f"Resized image to: {self.width}x{self.height}")
        return self.original_image
    
    def to_grayscale(self, image=None):
        """Convert to grayscale"""
        img = image if image is not None else self.original_image
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    def apply_threshold(self, image, threshold_value=128):
        """Apply binary threshold"""
        _, thresholded = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
        return thresholded
    
    def apply_canny(self, image, sigma=0.33):
        """Apply Canny edge detection"""
        # Calculate threshold values
        v = np.median(image)
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        
        edges = cv2.Canny(image, lower, upper)
        return edges
    
    def apply_gaussian_blur(self, image, kernel_size=5):
        """Apply Gaussian blur"""
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    
    def apply_morphological_ops(self, image, operation='close', kernel_size=5):
        """Apply morphological operations"""
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        
        if operation == 'close':
            return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        elif operation == 'open':
            return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        elif operation == 'dilate':
            return cv2.dilate(image, kernel, iterations=1)
        elif operation == 'erode':
            return cv2.erode(image, kernel, iterations=1)
        return image
    
    def invert(self, image):
        """Invert image (black becomes white, white becomes black)"""
        return cv2.bitwise_not(image)
    
    def process(self, threshold=128, apply_canny=False, blur=False, 
                morphological_op=None, invert_result=False):
        """Full processing pipeline"""
        logger.info("Starting image processing pipeline")
        
        # Resize if needed
        image = self.resize_if_needed()
        
        # Convert to grayscale
        image = self.to_grayscale(image)
        
        # Apply blur if requested
        if blur:
            image = self.apply_gaussian_blur(image)
        
        # Apply threshold
        image = self.apply_threshold(image, threshold)
        
        # Apply morphological operations if requested
        if morphological_op:
            image = self.apply_morphological_ops(image, operation=morphological_op)
        
        # Apply Canny edge detection if requested
        if apply_canny:
            image = self.apply_canny(image)
        
        # Invert if requested
        if invert_result:
            image = self.invert(image)
        
        logger.info("Image processing completed")
        return image
    
    def get_contours(self, image):
        """Extract contours from processed image"""
        contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours, hierarchy
    
    def simplify_contours(self, contours, epsilon=0.02):
        """Simplify contours using Ramer-Douglas-Peucker algorithm"""
        simplified = []
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon * perimeter, True)
            if len(approx) >= 3:  # Only keep contours with at least 3 points
                simplified.append(approx)
        return simplified
