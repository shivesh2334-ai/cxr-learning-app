"""
Image Processing Utilities
Handles CXR image preprocessing and manipulation
"""

from PIL import Image, ImageEnhance
import numpy as np
import cv2
from typing import Tuple, Optional

def resize_image(
    image: Image.Image, 
    max_size: Tuple[int, int] = (1024, 1024)
) -> Image.Image:
    """
    Resize image while maintaining aspect ratio
    
    Args:
        image: PIL Image object
        max_size: Maximum dimensions (width, height)
    
    Returns:
        Resized PIL Image
    """
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    return image

def enhance_contrast(
    image: Image.Image, 
    factor: float = 1.5
) -> Image.Image:
    """
    Enhance image contrast
    
    Args:
        image: PIL Image object
        factor: Contrast enhancement factor (1.0 = no change)
    
    Returns:
        Enhanced PIL Image
    """
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def convert_to_grayscale(image: Image.Image) -> Image.Image:
    """Convert image to grayscale"""
    return image.convert('L')

def normalize_image(image: Image.Image) -> Image.Image:
    """
    Normalize image intensity values
    
    Args:
        image: PIL Image object
    
    Returns:
        Normalized PIL Image
    """
    img_array = np.array(image)
    
    # Normalize to 0-255 range
    img_normalized = cv2.normalize(
        img_array, 
        None, 
        0, 
        255, 
        cv2.NORM_MINMAX
    )
    
    return Image.fromarray(img_normalized.astype(np.uint8))

def apply_clahe(
    image: Image.Image, 
    clip_limit: float = 2.0,
    tile_grid_size: Tuple[int, int] = (8, 8)
) -> Image.Image:
    """
    Apply Contrast Limited Adaptive Histogram Equalization (CLAHE)
    Useful for enhancing CXR images
    
    Args:
        image: PIL Image object
        clip_limit: Threshold for contrast limiting
        tile_grid_size: Size of grid for histogram equalization
    
    Returns:
        Enhanced PIL Image
    """
    # Convert to grayscale if needed
    if image.mode != 'L':
        image = convert_to_grayscale(image)
    
    img_array = np.array(image)
    
    # Apply CLAHE
    clahe = cv2.createCLAHE(
        clipLimit=clip_limit, 
        tileGridSize=tile_grid_size
    )
    enhanced = clahe.apply(img_array)
    
    return Image.fromarray(enhanced)

def detect_edges(
    image: Image.Image,
    low_threshold: int = 50,
    high_threshold: int = 150
) -> Image.Image:
    """
    Detect edges using Canny edge detection
    
    Args:
        image: PIL Image object
        low_threshold: Lower threshold for edge detection
        high_threshold: Upper threshold for edge detection
    
    Returns:
        Edge-detected PIL Image
    """
    # Convert to grayscale if needed
    if image.mode != 'L':
        image = convert_to_grayscale(image)
    
    img_array = np.array(image)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(img_array, (5, 5), 0)
    
    # Detect edges
    edges = cv2.Canny(blurred, low_threshold, high_threshold)
    
    return Image.fromarray(edges)

def crop_to_chest(
    image: Image.Image,
    border_percent: float = 0.05
) -> Image.Image:
    """
    Crop image to focus on chest area, removing excess borders
    
    Args:
        image: PIL Image object
        border_percent: Percentage of border to remove
    
    Returns:
        Cropped PIL Image
    """
    width, height = image.size
    
    border_x = int(width * border_percent)
    border_y = int(height * border_percent)
    
    return image.crop((
        border_x,
        border_y,
        width - border_x,
        height - border_y
    ))

def invert_if_negative(image: Image.Image) -> Image.Image:
    """
    Detect and invert negative images
    
    Args:
        image: PIL Image object
    
    Returns:
        Corrected PIL Image
    """
    img_array = np.array(image)
    
    # Check if image is likely negative (low mean intensity)
    mean_intensity = np.mean(img_array)
    
    if mean_intensity < 128:  # Likely a negative
        img_array = 255 - img_array
    
    return Image.fromarray(img_array)

def get_image_stats(image: Image.Image) -> dict:
    """
    Get statistical information about the image
    
    Args:
        image: PIL Image object
    
    Returns:
        Dictionary with image statistics
    """
    img_array = np.array(image)
    
    return {
        'shape': img_array.shape,
        'dtype': str(img_array.dtype),
        'min': float(np.min(img_array)),
        'max': float(np.max(img_array)),
        'mean': float(np.mean(img_array)),
        'std': float(np.std(img_array)),
        'size_kb': img_array.nbytes / 1024
    }

def prepare_for_analysis(
    image: Image.Image,
    enhance: bool = True,
    max_size: Tuple[int, int] = (1024, 1024)
) -> Image.Image:
    """
    Prepare CXR image for AI analysis
    
    Args:
        image: PIL Image object
        enhance: Whether to apply enhancement
        max_size: Maximum image dimensions
    
    Returns:
        Processed PIL Image ready for analysis
    """
    # Resize if too large
    processed = resize_image(image, max_size)
    
    # Convert to grayscale if needed
    if processed.mode != 'L' and processed.mode != 'RGB':
        processed = processed.convert('RGB')
    
    if enhance:
        # Apply CLAHE for better contrast
        if processed.mode == 'L':
            processed = apply_clahe(processed)
        else:
            # Convert to grayscale, enhance, then back to RGB
            gray = convert_to_grayscale(processed)
            enhanced = apply_clahe(gray)
            processed = enhanced.convert('RGB')
    
    return processed
