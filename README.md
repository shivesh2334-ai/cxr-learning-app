# CXR Learning & Diagnosis Application

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_STREAMLUL_URL)

An educational web application for systematic chest X-ray analysis based on established radiological principles from NIH/NCBI and UpToDate publications.

## Features

- **Technical Quality Assessment**: Check positioning, penetration, inspiration, motion
- **Systematic Anatomy Review**: 9-component structured analysis
- **Pattern Recognition**: ILO classification-based differential diagnosis
- **Interactive Cases**: Practice with sample scenarios
- **Structured Reporting**: Generate standardized radiology reports

## Systematic Approach Components

Based on Klein & Guilleman (NCBI):

1. Technical Quality
2. Support/Monitoring Devices
3. Chest Wall
4. Mediastinum (Heart, Great Vessels, Lines/Stripes)
5. Hila
6. Lungs (Volumes, Patterns, Nodules)
7. Airways (Trachea, Bronchi)
8. Pleura/Diaphragm

## Pattern Recognition

Based on UpToDate/Stark:

- **Small Opacities**: Nodular (p,q,r) vs Irregular (s,t,u) per ILO
- **Large Opacities**: Consolidation patterns
- **Linear**: Kerley lines, tram tracks
- **Distribution**: Upper vs Lower vs Peripheral vs Central

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/cxr-learning-app.git
cd cxr-learning-app
pip install -r requirements.txt
streamlit run app/main.py
