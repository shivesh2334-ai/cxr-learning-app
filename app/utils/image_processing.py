"""
Image Processing Utilities for CXR Analysis

Provides functions for loading, preprocessing, and analyzing chest X-ray images.
Includes quality assessment tools and enhancement functions.
"""

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import streamlit as st
from typing import Tuple, Optional, Dict, Union
import io
import base64


def load_cxr_image(uploaded_file) -> Optional[Image.Image]:
    """
    Load and validate CXR image from uploaded file.
    
    Args:
        uploaded_file: Streamlit uploaded file object
    
    Returns:
        PIL Image object or None if invalid
    """
    try:
        if uploaded_file is None:
            return None
        
        # Read file
        bytes_data = uploaded_file.getvalue()
        image = Image.open(io.BytesIO(bytes_data))
        
        # Convert to grayscale if RGB
        if image.mode != 'L':
            image = image.convert('L')
        
        return image
    
    except Exception as e:
        st.error(f"Error loading image: {str(e)}")
        return None


def preprocess_image(image: Image.Image, 
                    contrast: float = 1.0,
                    brightness: float = 1.0,
                    sharpness: float = 1.0) -> Image.Image:
    """
    Apply basic preprocessing adjustments to CXR image.
    
    Args:
        image: Input PIL Image
        contrast: Contrast factor (1.0 = original)
        brightness: Brightness factor (1.0 = original)
        sharpness: Sharpness factor (1.0 = original)
    
    Returns:
        Processed PIL Image
    """
    # Apply adjustments
    if contrast != 1.0:
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(contrast)
    
    if brightness != 1.0:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(brightness)
    
    if sharpness != 1.0:
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(sharpness)
    
    return image


def adjust_contrast(image: Image.Image, 
                   method: str = "adaptive",
                   clip_limit: float = 2.0) -> Image.Image:
    """
    Apply contrast enhancement using various methods.
    
    Args:
        image: Input PIL Image
        method: 'adaptive', 'histogram', or 'linear'
        clip_limit: Clip limit for adaptive histogram equalization
    
    Returns:
        Contrast-enhanced image
    """
    # Convert to numpy array
    img_array = np.array(image)
    
    if method == "adaptive":
        # Adaptive histogram equalization (CLAHE)
        # This is a simplified version - full implementation would use cv2
        from PIL import ImageOps
        return ImageOps.equalize(image)
    
    elif method == "histogram":
        # Global histogram equalization
        from PIL import ImageOps
        return ImageOps.equalize(image)
    
    else:  # linear
        # Linear stretch
        img_min, img_max = img_array.min(), img_array.max()
        stretched = ((img_array - img_min) / (img_max - img_min) * 255).astype(np.uint8)
        return Image.fromarray(stretched)


def detect_rotation(image: Image.Image) -> Dict:
    """
    Analyze image for rotation/positioning quality.
    
    Uses simple heuristics based on symmetry analysis.
    In production, this would use more sophisticated methods.
    
    Args:
        image: Input CXR image
    
    Returns:
        Dictionary with rotation analysis results
    """
    img_array = np.array(image)
    height, width = img_array.shape
    
    # Split image vertically
    left_half = img_array[:, :width//2]
    right_half = np.fliplr(img_array[:, width//2:])
    
    # Calculate symmetry score (simplified)
    min_width = min(left_half.shape[1], right_half.shape[1])
    symmetry_diff = np.abs(left_half[:, :min_width] - right_half[:, :min_width])
    symmetry_score = 1 - (np.mean(symmetry_diff) / 255)
    
    # Determine rotation status
    if symmetry_score > 0.85:
        rotation_status = "No significant rotation"
        quality = "optimal"
    elif symmetry_score > 0.70:
        rotation_status = "Mild rotation"
        quality = "acceptable"
    else:
        rotation_status = "Significant rotation"
        quality = "suboptimal"
    
    return {
        'symmetry_score': float(symmetry_score),
        'rotation_status': rotation_status,
        'quality': quality,
        'recommendation': "Repeat with proper positioning" if quality == "suboptimal" else None
    }


def assess_penetration(image: Image.Image) -> Dict:
    """
    Assess radiographic penetration by analyzing pixel intensity distribution.
    
    Args:
        image: Input CXR image
    
    Returns:
        Dictionary with penetration assessment
    """
    img_array = np.array(image)
    
    # Calculate statistics
    mean_intensity = np.mean(img_array)
    std_intensity = np.std(img_array)
    
    # Define regions (simplified - would use segmentation in production)
    height, width = img_array.shape
    
    # Central region (mediastinum)
    center_y, center_x = height // 2, width // 2
    mediastinum = img_array[center_y-50:center_y+50, center_x-50:center_x+50]
    
    # Peripheral region (lung)
    lung_region = img_array[100:200, 100:200]  # Simplified
    
    mediastinum_mean = np.mean(mediastinum)
    lung_mean = np.mean(lung_region)
    
    # Assess penetration
    # Optimal: mediastinum should be darker (higher attenuation) than lungs
    # but vertebral bodies should still be faintly visible
    
    if 120 < mediastinum_mean < 180 and 140 < lung_mean < 200:
        penetration = "optimal"
        status = "Adequate penetration"
    elif mediastinum_mean < 120:
        penetration = "under_penetrated"
        status = "Under-penetrated"
    else:
        penetration = "over_penetrated"
        status = "Over-penetrated"
    
    return {
        'mean_intensity': float(mean_intensity),
        'mediastinum_density': float(mediastinum_mean),
        'lung_density': float(lung_mean),
        'penetration': penetration,
        'status': status,
        'histogram_std': float(std_intensity)
    }


def calculate_ctr(image: Image.Image, 
                 cardiac_roi: Optional[Tuple] = None,
                 thoracic_roi: Optional[Tuple] = None) -> Dict:
    """
    Calculate Cardiothoracic Ratio from image.
    
    In production, this would use automated segmentation.
    For now, provides manual ROI selection interface.
    
    Args:
        image: Input CXR image
        cardiac_roi: (x, y, w, h) for cardiac silhouette
        thoracic_roi: (x, y, w, h) for thoracic cage
    
    Returns:
        Dictionary with CTR calculation
    """
    if cardiac_roi is None or thoracic_roi is None:
        return {
            'ctr': None,
            'status': 'manual_measurement_required',
            'message': 'Please define cardiac and thoracic regions'
        }
    
    # Extract measurements
    cx, cy, cw, ch = cardiac_roi
    tx, ty, tw, th = thoracic_roi
    
    cardiac_width = cw
    thoracic_width = tw
    
    if thoracic_width == 0:
        return {'ctr': None, 'status': 'error', 'message': 'Invalid thoracic width'}
    
    ctr = (cardiac_width / thoracic_width) * 100
    
    # Interpret CTR
    if ctr < 50:
        interpretation = "Normal heart size"
    elif ctr < 55:
        interpretation = "Borderline cardiomegaly"
    else:
        interpretation = "Cardiomegaly"
    
    return {
        'ctr': round(ctr, 1),
        'cardiac_width': cardiac_width,
        'thoracic_width': thoracic_width,
        'status': 'calculated',
        'interpretation': interpretation
    }


def enhance_edges(image: Image.Image, 
                 factor: float = 2.0) -> Image.Image:
    """
    Enhance edges to better visualize lines and borders.
    
    Args:
        image: Input image
        factor: Enhancement factor
    
    Returns:
        Edge-enhanced image
    """
    # Apply unsharp mask for edge enhancement
    sharpened = image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    return sharpened


def invert_image(image: Image.Image) -> Image.Image:
    """
    Invert image (useful for certain analyses).
    
    Args:
        image: Input image
    
    Returns:
        Inverted image
    """
    from PIL import ImageOps
    return ImageOps.invert(image)


def get_image_metadata(uploaded_file) -> Dict:
    """
    Extract metadata from uploaded image file.
    
    Args:
        uploaded_file: Streamlit uploaded file
    
    Returns:
        Dictionary with metadata
    """
    metadata = {
        'filename': uploaded_file.name if uploaded_file else None,
        'size_bytes': len(uploaded_file.getvalue()) if uploaded_file else 0,
        'format': None,
        'mode': None,
        'dimensions': None
    }
    
    try:
        image = Image.open(io.BytesIO(uploaded_file.getvalue()))
        metadata['format'] = image.format
        metadata['mode'] = image.mode
        metadata['dimensions'] = image.size
    except Exception as e:
        metadata['error'] = str(e)
    
    return metadata


def create_thumbnail(image: Image.Image, 
                    max_size: Tuple[int, int] = (400, 400)) -> Image.Image:
    """
    Create thumbnail while maintaining aspect ratio.
    
    Args:
        image: Input image
        max_size: Maximum (width, height)
    
    Returns:
        Thumbnail image
    """
    thumb = image.copy()
    thumb.thumbnail(max_size)
    return thumb


def apply_window_level(image: Image.Image,
                      window_center: int = 128,
                      window_width: int = 256) -> Image.Image:
    """
    Apply window/level adjustment (medical imaging style).
    
    Args:
        image: Input image
        window_center: Center of window
        window_width: Width of window
    
    Returns:
        Windowed image
    """
    img_array = np.array(image).astype(float)
    
    # Calculate window bounds
    min_val = window_center - window_width // 2
    max_val = window_center + window_width // 2
    
    # Apply window
    windowed = np.clip(img_array, min_val, max_val)
    windowed = ((windowed - min_val) / (max_val - min_val) * 255).astype(np.uint8)
    
    return Image.fromarray(windowed)


def measure_distance(image: Image.Image,
                    point1: Tuple[int, int],
                    point2: Tuple[int, int],
                    calibration: Optional[float] = None) -> Dict:
    """
    Measure distance between two points in pixels (and calibrated units if provided).
    
    Args:
        image: Input image
        point1: (x, y) first point
        point2: (x, y) second point
        calibration: Pixels per unit (e.g., pixels per cm)
    
    Returns:
        Dictionary with measurements
    """
    x1, y1 = point1
    x2, y2 = point2
    
    pixel_distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    result = {
        'pixel_distance': float(pixel_distance),
        'point1': point1,
        'point2': point2
    }
    
    if calibration:
        real_distance = pixel_distance / calibration
        result['calibrated_distance'] = float(real_distance)
        result['units'] = 'cm'  # or whatever unit calibration represents
    
    return result


def detect_grid_lines(image: Image.Image) -> Dict:
    """
    Detect potential grid lines or artifacts in image.
    
    Args:
        image: Input image
    
    Returns:
        Dictionary with artifact detection results
    """
    img_array = np.array(image)
    
    # Simple detection based on periodic patterns
    # In production, would use Fourier analysis or Hough transform
    
    # Check for horizontal lines
    horizontal_variance = np.var(np.diff(img_array, axis=0))
    vertical_variance = np.var(np.diff(img_array, axis=1))
    
    # High variance in one direction suggests lines in that direction
    has_horizontal_lines = horizontal_variance > 1000
    has_vertical_lines = vertical_variance > 1000
    
    return {
        'has_horizontal_lines': bool(has_horizontal_lines),
        'has_vertical_lines': bool(has_vertical_lines),
        'horizontal_variance': float(horizontal_variance),
        'vertical_variance': float(vertical_variance),
        'recommendation': 'Check for grid artifacts' if (has_horizontal_lines or has_vertical_lines) else 'No obvious grid lines detected'
    }


def image_to_base64(image: Image.Image, format: str = "PNG") -> str:
    """
    Convert PIL Image to base64 string for embedding.
    
    Args:
        image: Input image
        format: Image format
    
    Returns:
        Base64 encoded string
    """
    buffered = io.BytesIO()
    image.save(buffered, format=format)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/{format.lower()};base64,{img_str}"


# Export all functions
__all__ = [
    'load_cxr_image',
    'preprocess_image',
    'adjust_contrast',
    'detect_rotation',
    'assess_penetration',
    'calculate_ctr',
    'enhance_edges',
    'invert_image',
    'get_image_metadata',
    'create_thumbnail',
    'apply_window_level',
    'measure_distance',
    'detect_grid_lines',
    'image_to_base64'
]
