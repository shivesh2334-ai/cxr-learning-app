"""
CXR Learning & Diagnosis Application

A systematic approach to chest radiographic analysis based on:
- Klein JS, Guilleman RP. Systematic Approach to Chest Radiographic Analysis. NCBI. 2019
- Stark P. Radiographic approach to diffuse lung disease. UpToDate. 2026

Modules:
    components: UI components for systematic analysis
    utils: Helper functions and image processing
    data: Knowledge base and reference materials
"""

__version__ = "1.0.0"
__author__ = "CXR Learning Team"
__license__ = "MIT"

# Make key components easily importable
from app.components.technical_quality import technical_quality_assessor
from app.components.anatomy_analyzer import anatomy_systematic_review
from app.components.pattern_recognizer import pattern_analysis
from app.components.report_generator import generate_structured_report

__all__ = [
    "technical_quality_assessor",
    "anatomy_systematic_review", 
    "pattern_analysis",
    "generate_structured_report"
]
