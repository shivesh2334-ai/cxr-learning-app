"""
Annotation Tools for CXR Images

Provides drawing and annotation capabilities for educational purposes.
"""

from PIL import Image, ImageDraw, ImageFont
import streamlit as st
from typing import List, Tuple, Dict, Optional
import json


def add_annotation(image: Image.Image,
                  text: str,
                  position: Tuple[int, int],
                  color: str = "red",
                  font_size: int = 20) -> Image.Image:
    """
    Add text annotation to image.
    
    Args:
        image: Input PIL Image
        text: Annotation text
        position: (x, y) position
        color: Text color
        font_size: Font size
    
    Returns:
        Annotated image
    """
    draw = ImageDraw.Draw(image)
    
    # Try to load font, fall back to default
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Draw text with background
    x, y = position
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Draw background rectangle
    draw.rectangle([x, y, x + text_width, y + text_height], 
                   fill="yellow", outline=color)
    
    # Draw text
    draw.text((x, y), text, fill=color, font=font)
    
    return image


def draw_measurements(image: Image.Image,
                     start: Tuple[int, int],
                     end: Tuple[int, int],
                     label: Optional[str] = None,
                     color: str = "red") -> Image.Image:
    """
    Draw measurement line with optional label.
    
    Args:
        image: Input PIL Image
        start: (x, y) start point
        end: (x, y) end point
        label: Optional text label
        color: Line color
    
    Returns:
        Image with measurement
    """
    draw = ImageDraw.Draw(image)
    
    # Draw line
    draw.line([start, end], fill=color, width=2)
    
    # Draw endpoints
    draw.ellipse([start[0]-3, start[1]-3, start[0]+3, start[1]+3], fill=color)
    draw.ellipse([end[0]-3, end[1]-3, end[0]+3, end[1]+3], fill=color)
    
    # Add label if provided
    if label:
        mid_x = (start[0] + end[0]) // 2
        mid_y = (start[1] + end[1]) // 2
        add_annotation(image, label, (mid_x, mid_y - 20), color)
    
    return image


def highlight_region(image: Image.Image,
                    bbox: Tuple[int, int, int, int],
                    label: Optional[str] = None,
                    color: str = "yellow",
                    style: str = "rectangle") -> Image.Image:
    """
    Highlight a region of interest.
    
    Args:
        image: Input PIL Image
        bbox: (x1, y1, x2, y2) bounding box
        label: Optional label
        color: Highlight color
        style: 'rectangle', 'circle', or 'arrow'
    
    Returns:
        Image with highlight
    """
    draw = ImageDraw.Draw(image)
    x1, y1, x2, y2 = bbox
    
    if style == "rectangle":
        draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
    elif style == "circle":
        center = ((x1 + x2) // 2, (y1 + y2) // 2)
        radius = max(x2 - x1, y2 - y1) // 2
        draw.ellipse([center[0]-radius, center[1]-radius,
                     center[0]+radius, center[1]+radius], 
                    outline=color, width=3)
    elif style == "arrow":
        # Draw arrow pointing to region
        draw.line([(x1-50, y1-50), (x1, y1)], fill=color, width=3)
        # Arrowhead
        draw.polygon([(x1, y1), (x1-10, y1-5), (x1-5, y1-10)], fill=color)
    
    if label:
        add_annotation(image, label, (x1, y1 - 25), color)
    
    return image


def draw_anatomy_overlay(image: Image.Image,
                        anatomy_type: str = "standard") -> Image.Image:
    """
    Draw anatomical overlay lines for educational purposes.
    
    Args:
        image: Input PIL Image
        anatomy_type: Type of overlay ('standard', 'fissures', 'zones')
    
    Returns:
        Image with overlay
    """
    draw = ImageDraw.Draw(image)
    width, height = image.size
    color = "rgba(0, 255, 0, 128)"  # Semi-transparent green
    
    if anatomy_type == "standard":
        # Draw basic anatomical landmarks
        # Trachea
        trachea_x = width // 2
        draw.line([(trachea_x, 50), (trachea_x, height//3)], 
                 fill="blue", width=2)
        
        # Hilum level
        hilum_y = height // 2
        draw.line([(0, hilum_y), (width, hilum_y)], 
                 fill="yellow", width=1, dash=(5, 5))
        
        # Cardiac silhouette outline (simplified)
        cardiac_center = (width // 2, height * 2 // 3)
        draw.ellipse([cardiac_center[0]-60, cardiac_center[1]-80,
                     cardiac_center[0]+60, cardiac_center[1]+40], 
                    outline="red", width=2)
    
    elif anatomy_type == "zones":
        # Draw lung zones
        zone_colors = ["cyan", "magenta", "yellow"]
        zone_names = ["Upper", "Middle", "Lower"]
        
        for i, (zone_color, zone_name) in enumerate(zip(zone_colors, zone_names)):
            y_start = (height // 4) * i + 50
            y_end = (height // 4) * (i + 1) + 50
            
            # Zone boundary
            draw.line([(0, y_start), (width, y_start)], 
                     fill=zone_color, width=2)
            
            # Zone label
            add_annotation(image, zone_name, (10, y_start + 10), zone_color)
    
    return image


def create_comparison_view(image1: Image.Image,
                          image2: Image.Image,
                          label1: str = "Before",
                          label2: str = "After") -> Image.Image:
    """
    Create side-by-side comparison image.
    
    Args:
        image1: First image
        image2: Second image
        label1: Label for first image
        label2: Label for second image
    
    Returns:
        Combined comparison image
    """
    # Ensure same height
    h1, h2 = image1.height, image2.height
    target_height = max(h1, h2)
    
    # Resize if needed
    if h1 != target_height:
        ratio = target_height / h1
        image1 = image1.resize((int(image1.width * ratio), target_height))
    
    if h2 != target_height:
        ratio = target_height / h2
        image2 = image2.resize((int(image2.width * ratio), target_height))
    
    # Create combined image
    total_width = image1.width + image2.width + 20  # Gap between
    combined = Image.new('RGB', (total_width, target_height + 40), 'white')
    
    # Paste images
    combined.paste(image1, (0, 20))
    combined.paste(image2, (image1.width + 20, 20))
    
    # Add labels
    draw = ImageDraw.Draw(combined)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    # Center labels
    label1_x = (image1.width - len(label1) * 10) // 2
    label2_x = image1.width + 20 + (image2.width - len(label2) * 10) // 2
    
    draw.text((label1_x, 5), label1, fill="black", font=font)
    draw.text((label2_x, 5), label2, fill="black", font=font)
    
    return combined


def save_annotations(image: Image.Image,
                    annotations: List[Dict],
                    filename: str):
    """
    Save image with annotations and metadata.
    
    Args:
        image: Annotated image
        annotations: List of annotation dictionaries
        filename: Output filename
    """
    # Save image
    image.save(filename)
    
    # Save metadata
    meta_filename = filename.rsplit('.', 1)[0] + '.json'
    with open(meta_filename, 'w') as f:
        json.dump(annotations, f, indent=2)


__all__ = [
    'add_annotation',
    'draw_measurements',
    'highlight_region',
    'draw_anatomy_overlay',
    'create_comparison_view',
    'save_annotations'
]
