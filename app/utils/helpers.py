"""
Helper functions for CXR analysis
"""

import re
from typing import List, Dict


def validate_image_format(filename: str) -> bool:
    """Validate if file is acceptable medical image format."""
    valid_extensions = ['.dcm', '.jpg', '.jpeg', '.png', '.tiff']
    return any(filename.lower().endswith(ext) for ext in valid_extensions)


def calculate_ctr(cardiac_width: float, thoracic_width: float) -> float:
    """
    Calculate Cardiothoracic Ratio.
    
    Args:
        cardiac_width: Transverse cardiac diameter (max)
        thoracic_width: Internal thoracic diameter (max)
    
    Returns:
        CTR as percentage
    """
    if thoracic_width == 0:
        return 0
    return (cardiac_width / thoracic_width) * 100


def get_differential_diagnosis(pattern: str, distribution: str) -> List[str]:
    """
    Get differential diagnosis based on pattern and distribution.
    
    Args:
        pattern: Radiographic pattern (reticular, nodular, etc.)
        distribution: Anatomic distribution (upper, lower, etc.)
    
    Returns:
        List of differential diagnoses
    """
    # This would connect to knowledge base
    differentials = {
        ("reticular", "basal"): [
            "Usual Interstitial Pneumonia (IPF)",
            "Nonspecific Interstitial Pneumonia",
            "Asbestosis",
            "Collagen vascular disease"
        ],
        ("nodular", "upper"): [
            "Sarcoidosis",
            "Silicosis",
            "Tuberculosis",
            "Langerhans cell histiocytosis"
        ]
        # Add more combinations...
    }
    
    return differentials.get((pattern, distribution), ["Consider clinical correlation"])


def parse_rib_count(description: str) -> int:
    """Extract rib count from text description."""
    numbers = re.findall(r'\d+', description)
    return int(numbers[0]) if numbers else 0
