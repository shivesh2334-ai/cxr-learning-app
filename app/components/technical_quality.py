"""
Technical Quality Assessment Module

Based on: Klein JS, Guilleman RP. Systematic Approach to Chest Radiographic Analysis. 2019

Evaluates five main technical factors:
1. Patient Positioning (rotation, scapular position)
2. Mediastinal Penetration
3. Motion (sharpness)
4. Lung Volumes (inspiration)
5. Artifacts
"""

import streamlit as st
from typing import Dict, List, Tuple, Optional
import json
from dataclasses import dataclass
from enum import Enum


class PositionQuality(Enum):
    """Positioning quality ratings"""
    OPTIMAL = "optimal"
    ACCEPTABLE = "acceptable" 
    SUBOPTIMAL = "suboptimal"
    NON_DIAGNOSTIC = "non_diagnostic"


@dataclass
class TechnicalAssessment:
    """Data class to store technical quality assessment results"""
    positioning: Dict
    penetration: Dict
    motion: Dict
    inspiration: Dict
    artifacts: Dict
    overall_quality: str
    recommendations: List[str]


def technical_quality_assessor():
    """
    Main function for technical quality assessment module.
    Provides interactive checklist and assessment tools.
    """
    st.markdown('<p class="section-header">📋 Technical Quality Assessment</p>', 
                unsafe_allow_html=True)
    
    st.info("""
    **Reference:** Klein JS, Guilleman RP. Systematic Approach to Chest Radiographic Analysis.
    
    Technical adequacy must be confirmed before interpretation to avoid:
    - **Overdiagnosis** (low lung volume may simulate lung disease)
    - **Underdiagnosis** (motion or rotation may limit evaluation)
    """)
    
    # Create tabs for organized assessment
    tabs = st.tabs([
        "🎯 Positioning", 
        "💡 Penetration", 
        "📸 Motion", 
        "🫁 Inspiration",
        "⚠️ Artifacts",
        "📊 Summary"
    ])
    
    # Initialize session state for storing assessments
    if 'tech_assessment' not in st.session_state:
        st.session_state.tech_assessment = {}
    
    with tabs[0]:
        positioning_assessment = assess_positioning()
        st.session_state.tech_assessment['positioning'] = positioning_assessment
    
    with tabs[1]:
        penetration_assessment = assess_penetration()
        st.session_state.tech_assessment['penetration'] = penetration_assessment
    
    with tabs[2]:
        motion_assessment = assess_motion()
        st.session_state.tech_assessment['motion'] = motion_assessment
    
    with tabs[3]:
        inspiration_assessment = assess_inspiration()
        st.session_state.tech_assessment['inspiration'] = inspiration_assessment
    
    with tabs[4]:
        artifacts_assessment = assess_artifacts()
        st.session_state.tech_assessment['artifacts'] = artifacts_assessment
    
    with tabs[5]:
        display_summary(st.session_state.tech_assessment)


def assess_positioning() -> Dict:
    """
    Assess patient positioning and rotation.
    
    Criteria:
    - Spinous processes align with imaginary vertical line midway between clavicular heads
    - Scapulae rotated laterally (not superimposed on upper lungs)
    - Clavicles equidistant from spinous processes
    """
    st.subheader("Patient Positioning Assessment")
    
    st.markdown("""
    **Optimal Positioning Criteria:**
    1. **Rotation:** Spinous processes midway between clavicular heads
    2. **Scapulae:** Rotated laterally, clear of lung fields
    3. **Clavicles:** Symmetric, equal distance from spine
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Rotation Check**")
        rotation = st.radio(
            "Spinous process position:",
            [
                "Midway between clavicles (no rotation)",
                "Slightly off-center (<1cm deviation)",
                "Obviously rotated (>1cm deviation)",
                "Severely rotated (non-diagnostic)"
            ],
            key="pos_rotation"
        )
        
        st.markdown("**Scapular Position**")
        scapulae = st.radio(
            "Scapulae position:",
            [
                "Rotated laterally, clear of lungs",
                "Partially overlapping upper lungs",
                "Heavily superimposed on lung fields"
            ],
            key="pos_scapulae"
        )
    
    with col2:
        st.markdown("**Clavicular Symmetry**")
        clavicles = st.radio(
            "Clavicle symmetry:",
            [
                "Symmetric, equal distance from spine",
                "Slightly asymmetric",
                "Markedly asymmetric"
            ],
            key="pos_clavicles"
        )
        
        # Visual guide
        st.info("""
        **Tip:** On proper PA film:
        - Medial clavicle ends equidistant from spinous process
        - Scapular shadows lateral to lung apices
        """)
    
    # Calculate positioning quality
    quality_score = calculate_positioning_quality(rotation, scapulae, clavicles)
    
    # Detailed findings input
    findings = st.text_area(
        "Positioning Findings:",
        placeholder="Describe any rotation, scapular position, or other positioning issues...",
        key="pos_findings"
    )
    
    return {
        'rotation': rotation,
        'scapulae': scapulae,
        'clavicles': clavicles,
        'quality_score': quality_score,
        'findings': findings,
        'is_diagnostic': quality_score != PositionQuality.NON_DIAGNOSTIC
    }


def calculate_positioning_quality(rotation: str, scapulae: str, clavicles: str) -> PositionQuality:
    """Calculate overall positioning quality based on individual factors."""
    
    # Define quality levels
    quality_map = {
        "no rotation": 3, "Midway": 3,
        "<1cm": 2, "Slightly": 2,
        ">1cm": 1, "Obviously": 1, "Partially": 1, "asymmetric": 1,
        "Severely": 0, "Heavily": 0, "Markedly": 0, "non-diagnostic": 0
    }
    
    score = 0
    total = 0
    
    for text in [rotation, scapulae, clavicles]:
        for key, value in quality_map.items():
            if key in text:
                score += value
                total += 3
                break
    
    avg_score = score / total if total > 0 else 0
    
    if avg_score >= 0.9:
        return PositionQuality.OPTIMAL
    elif avg_score >= 0.7:
        return PositionQuality.ACCEPTABLE
    elif avg_score >= 0.4:
        return PositionQuality.SUBOPTIMAL
    else:
        return PositionQuality.NON_DIAGNOSTIC


def assess_penetration() -> Dict:
    """
    Assess radiographic penetration.
    
    Criteria:
    - Faint visualization of vertebral bodies and disc spaces through mediastinum
    - Lungs gray in density (not black/white)
    - Pulmonary vessels easily seen
    """
    st.subheader("Radiographic Penetration Assessment")
    
    st.markdown("""
    **Optimal Penetration Criteria:**
    - **Mediastinum:** Vertebral bodies faintly visible through heart shadow
    - **Lung Fields:** Gray density (not black/white)
    - **Vessels:** Pulmonary vessels easily distinguished
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Mediastinal Penetration**")
        mediastinum = st.radio(
            "Vertebral body visualization:",
            [
                "Faintly visible through mediastinum (optimal)",
                "Clearly visible (over-penetrated)",
                "Not visible (under-penetrated)",
                "Barely visible (slightly under-penetrated)"
            ],
            key="pen_mediastinum"
        )
        
        st.markdown("**Lung Density**")
        lung_density = st.radio(
            "Lung field density:",
            [
                "Gray (optimal)",
                "Black (over-penetrated)",
                "White (under-penetrated)",
                "Patchy (inconsistent)"
            ],
            key="pen_lungs"
        )
    
    with col2:
        st.markdown("**Vascular Markings**")
        vessels = st.radio(
            "Pulmonary vessel visibility:",
            [
                "Easily seen throughout lungs",
                "Too prominent (over-penetrated)",
                "Obscured (under-penetrated)",
                "Poorly visualized"
            ],
            key="pen_vessels"
        )
        
        # Penetration guide
        st.warning("""
        **Clinical Impact:**
        - **Under-penetrated:** May miss lung nodules, vascular markings obscured
        - **Over-penetrated:** Mediastinal details lost, may miss subtle infiltrates
        """)
    
    # Determine penetration quality
    penetration_quality = "optimal"
    issues = []
    
    if "over-penetrated" in mediastinum or "Black" in lung_density:
        penetration_quality = "over_penetrated"
        issues.append("Over-penetration may obscure mediastinal abnormalities")
    elif "under-penetrated" in mediastinum or "White" in lung_density:
        penetration_quality = "under_penetrated"
        issues.append("Under-penetration may obscure lung parenchymal details")
    
    findings = st.text_area(
        "Penetration Findings:",
        placeholder="Describe penetration quality and any limitations...",
        key="pen_findings"
    )
    
    return {
        'mediastinum': mediastinum,
        'lung_density': lung_density,
        'vessels': vessels,
        'quality': penetration_quality,
        'issues': issues,
        'findings': findings
    }


def assess_motion() -> Dict:
    """
    Assess for motion artifact.
    
    Criteria:
    - Sharpness of superior cortices of ribs
    - Sharpness of vessel margins
    - Sharpness of diaphragmatic contours
    """
    st.subheader("Motion Artifact Assessment")
    
    st.markdown("""
    **Motion Detection:**
    Motion degrades image quality by blurring structures. Check:
    1. **Rib cortices:** Should be sharp, well-defined
    2. **Vessel margins:** Should be crisp
    3. **Diaphragm:** Contours should be distinct
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Rib Sharpness**")
        ribs = st.radio(
            "Rib cortices:",
            [
                "Sharp and well-defined",
                "Slightly blurred",
                "Moderately blurred",
                "Severely blurred"
            ],
            key="mot_ribs"
        )
        
        st.markdown("**Vessel Margins**")
        vessels = st.radio(
            "Pulmonary vessel margins:",
            [
                "Sharp and distinct",
                "Slightly indistinct",
                "Blurred",
                "Severely blurred"
            ],
            key="mot_vessels"
        )
    
    with col2:
        st.markdown("**Diaphragm Contours**")
        diaphragm = st.radio(
            "Diaphragmatic contours:",
            [
                "Sharp and distinct",
                "Slightly blurred",
                "Moderately blurred",
                "Severely blurred/indistinct"
            ],
            key="mot_diaphragm"
        )
        
        st.markdown("**Heart Borders**")
        heart = st.radio(
            "Cardiac borders:",
            [
                "Sharp and distinct",
                "Slightly blurred",
                "Blurred",
                "Severely blurred"
            ],
            key="mot_heart"
        )
    
    # Calculate motion score
    motion_items = [ribs, vessels, diaphragm, heart]
    blur_count = sum(1 for item in motion_items if "blurred" in item)
    severe_count = sum(1 for item in motion_items if "Severely" in item)
    
    if severe_count >= 2:
        motion_quality = "severe_motion"
        diagnostic = False
    elif blur_count >= 3:
        motion_quality = "moderate_motion"
        diagnostic = False
    elif blur_count >= 1:
        motion_quality = "mild_motion"
        diagnostic = True
    else:
        motion_quality = "no_motion"
        diagnostic = True
    
    if not diagnostic:
        st.error("⚠️ **Significant motion artifact - Image may be non-diagnostic**")
    
    findings = st.text_area(
        "Motion Assessment:",
        placeholder="Describe any motion artifacts and their impact...",
        key="mot_findings"
    )
    
    return {
        'ribs': ribs,
        'vessels': vessels,
        'diaphragm': diaphragm,
        'heart': heart,
        'quality': motion_quality,
        'is_diagnostic': diagnostic,
        'findings': findings
    }


def assess_inspiration() -> Dict:
    """
    Assess adequacy of inspiration.
    
    Criteria:
    - Right hemidiaphragm at level of 6th anterior rib or 10th posterior rib
    - At mid-clavicular line
    - Minimum 8-9 posterior ribs should be visible above diaphragm
    """
    st.subheader("Inspiratory Effort Assessment")
    
    st.markdown("""
    **Optimal Inspiration Criteria:**
    - **Right hemidiaphragm:** At level of 6th anterior rib OR 10th posterior rib
    - **Measurement point:** Mid-clavicular line
    - **Posterior ribs:** Minimum 8-9 visible above diaphragm
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Anterior Rib Count**")
        anterior_rib = st.selectbox(
            "Right hemidiaphragm level (anterior ribs):",
            ["4th", "5th", "6th (optimal)", "7th", "8th or below"],
            key="insp_anterior"
        )
        
        st.markdown("**Posterior Rib Count**")
        posterior_ribs = st.slider(
            "Number of posterior ribs above diaphragm:",
            min_value=5,
            max_value=12,
            value=9,
            key="insp_posterior"
        )
    
    with col2:
        st.markdown("**Hemidiaphragm Position**")
        diaphragm_pos = st.radio(
            "Hemidiaphragm position:",
            [
                "Normal (6th anterior/10th posterior)",
                "Elevated (poor inspiration)",
                "Lowered (hyperinflation)",
                "Asymmetric (pathology)"
            ],
            key="insp_diaphragm"
        )
        
        # Clinical correlation
        st.info("""
        **Clinical Impact:**
        - **Poor inspiration:** Crowds vessels, mimics cardiomegaly, obscures bases
        - **Hyperinflation:** Suggests COPD/asthma
        """)
    
    # Assess inspiration quality
    rib_count_ok = posterior_ribs >= 8
    position_ok = "optimal" in anterior_rib or "Normal" in diaphragm_pos
    
    if position_ok and rib_count_ok:
        inspiration_quality = "adequate"
    elif posterior_ribs >= 7:
        inspiration_quality = "suboptimal"
    else:
        inspiration_quality = "poor"
    
    if "poor" in inspiration_quality:
        st.warning("⚠️ Poor inspiration may simulate lung disease or cardiomegaly")
    
    findings = st.text_area(
        "Inspiration Assessment:",
        placeholder="Describe inspiratory effort and any limitations...",
        key="insp_findings"
    )
    
    return {
        'anterior_rib': anterior_rib,
        'posterior_rib_count': posterior_ribs,
        'diaphragm_position': diaphragm_pos,
        'quality': inspiration_quality,
        'is_adequate': inspiration_quality == "adequate",
        'findings': findings
    }


def assess_artifacts() -> Dict:
    """
    Assess for artifacts in digital radiography.
    
    Common artifacts:
    - Grid lines
    - Detector faults
    - Motion artifacts (already assessed)
    - Processing artifacts
    - Foreign objects
    """
    st.subheader("Artifact Assessment")
    
    st.markdown("""
    **Digital Radiography Artifacts:**
    - Grid lines (improper grid technique)
    - Detector faults (dead pixels, lines)
    - Processing artifacts (edge enhancement, noise)
    - Foreign objects (clothing, jewelry, monitoring equipment)
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Equipment Artifacts**")
        grid_lines = st.checkbox("Visible grid lines", key="art_grid")
        detector_faults = st.checkbox("Detector faults/dead pixels", key="art_detector")
        processing = st.checkbox("Processing artifacts", key="art_processing")
        
        st.markdown("**Foreign Objects**")
        clothing = st.checkbox("Clothing artifacts (buttons, zippers)", key="art_clothing")
        jewelry = st.checkbox("Jewelry not removed", key="art_jewelry")
        medical = st.checkbox("External medical devices", key="art_medical")
    
    with col2:
        st.markdown("**Image Quality Issues**")
        noise = st.checkbox("Excessive noise", key="art_noise")
        saturation = st.checkbox("Saturation (too bright/dark areas)", key="art_saturation")
        stitching = st.checkbox("Stitching artifacts (if composite)", key="art_stitch")
        
        # Artifact severity
        if any([grid_lines, detector_faults, processing, noise, saturation]):
            severity = st.radio(
                "Artifact severity:",
                ["Minimal (no impact)", "Mild (minor impact)", 
                 "Moderate (significant impact)", "Severe (non-diagnostic)"]
            )
        else:
            severity = "None"
    
    # Determine if artifacts affect diagnosis
    diagnostic_impact = severity in ["Moderate (significant impact)", "Severe (non-diagnostic)"]
    
    findings = st.text_area(
        "Artifact Description:",
        placeholder="Describe any artifacts and their location/impact...",
        key="art_findings"
    )
    
    return {
        'grid_lines': grid_lines,
        'detector_faults': detector_faults,
        'processing': processing,
        'foreign_objects': {
            'clothing': clothing,
            'jewelry': jewelry,
            'medical': medical
        },
        'quality_issues': {
            'noise': noise,
            'saturation': saturation,
            'stitching': stitching
        },
        'severity': severity,
        'affects_diagnosis': diagnostic_impact,
        'findings': findings
    }


def display_summary(assessment: Dict):
    """
    Display comprehensive technical quality summary.
    """
    st.subheader("Technical Quality Summary")
    
    # Calculate overall quality
    quality_scores = []
    diagnostic_concerns = []
    
    # Positioning
    if 'positioning' in assessment:
        pos = assessment['positioning']
        quality_scores.append(3 if pos['quality_score'] == PositionQuality.OPTIMAL else 
                            2 if pos['quality_score'] == PositionQuality.ACCEPTABLE else 1)
        if pos['quality_score'] == PositionQuality.NON_DIAGNOSTIC:
            diagnostic_concerns.append("Positioning: Non-diagnostic rotation")
    
    # Penetration
    if 'penetration' in assessment:
        pen = assessment['penetration']
        quality_scores.append(3 if pen['quality'] == "optimal" else 2 if "slight" in pen['quality'] else 1)
        if pen['issues']:
            diagnostic_concerns.extend(pen['issues'])
    
    # Motion
    if 'motion' in assessment:
        mot = assessment['motion']
        if mot['quality'] == "no_motion":
            quality_scores.append(3)
        elif mot['quality'] == "mild_motion":
            quality_scores.append(2)
        else:
            quality_scores.append(1)
            if not mot['is_diagnostic']:
                diagnostic_concerns.append("Motion: Non-diagnostic blur")
    
    # Inspiration
    if 'inspiration' in assessment:
        insp = assessment['inspiration']
        quality_scores.append(3 if insp['quality'] == "adequate" else 
                            2 if insp['quality'] == "suboptimal" else 1)
        if insp['quality'] == "poor":
            diagnostic_concerns.append("Inspiration: Poor effort may obscure findings")
    
    # Artifacts
    if 'artifacts' in assessment:
        art = assessment['artifacts']
        if art['severity'] == "None":
            quality_scores.append(3)
        elif art['severity'] == "Minimal (no impact)":
            quality_scores.append(3)
        elif art['severity'] == "Mild (minor impact)":
            quality_scores.append(2)
        else:
            quality_scores.append(1)
            if art['affects_diagnosis']:
                diagnostic_concerns.append(f"Artifacts: {art['severity']}")
    
    # Overall assessment
    avg_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0
    
    if avg_score >= 2.5:
        overall = "OPTIMAL"
        color = "green"
    elif avg_score >= 1.8:
        overall = "ACCEPTABLE"
        color = "blue"
    elif avg_score >= 1.2:
        overall = "SUBOPTIMAL - Interpret with caution"
        color = "orange"
    else:
        overall = "NON-DIAGNOSTIC - Repeat recommended"
        color = "red"
    
    # Display summary card
    st.markdown(f"""
    <div style='padding: 20px; border-radius: 10px; background-color: {color}; color: white;'>
        <h3 style='margin: 0;'>Overall Quality: {overall}</h3>
        <p style='margin: 5px 0 0 0;'>Score: {avg_score:.1f}/3.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed breakdown
    st.markdown("### Detailed Assessment")
    
    cols = st.columns(5)
    components = [
        ("Positioning", assessment.get('positioning', {})),
        ("Penetration", assessment.get('penetration', {})),
        ("Motion", assessment.get('motion', {})),
        ("Inspiration", assessment.get('inspiration', {})),
        ("Artifacts", assessment.get('artifacts', {}))
    ]
    
    for col, (name, data) in zip(cols, components):
        with col:
            st.markdown(f"**{name}**")
            if data:
                if 'quality_score' in data:
                    st.write(f"Quality: {data['quality_score'].value}")
                elif 'quality' in data:
                    st.write(f"Quality: {data['quality']}")
                elif 'is_diagnostic' in data:
                    st.write(f"Diagnostic: {'Yes' if data['is_diagnostic'] else 'No'}")
            else:
                st.write("Not assessed")
    
    # Concerns and recommendations
    if diagnostic_concerns:
        st.markdown("### ⚠️ Diagnostic Concerns")
        for concern in diagnostic_concerns:
            st.warning(concern)
    
    # Generate structured report section
    st.markdown("---")
    st.subheader("Technical Quality Report Text")
    
    report_text = generate_technical_report(assessment)
    st.text_area("Copy for report:", report_text, height=200)
    
    if st.button("Copy to Clipboard"):
        st.code(report_text)
        st.success("Text ready to copy!")


def generate_technical_report(assessment: Dict) -> str:
    """
    Generate structured technical quality text for radiology report.
    """
    lines = ["TECHNICAL QUALITY:"]
    
    # Positioning
    if 'positioning' in assessment:
        pos = assessment['positioning']
        lines.append(f"Positioning: {pos['quality_score'].value}. {pos.get('findings', 'No significant issues')}")
    
    # Penetration
    if 'penetration' in assessment:
        pen = assessment['penetration']
        lines.append(f"Penetration: {pen['quality']}. {pen.get('findings', '')}")
    
    # Motion
    if 'motion' in assessment:
        mot = assessment['motion']
        motion_desc = "No significant motion" if mot['quality'] == "no_motion" else f"{mot['quality']} present"
        lines.append(f"Motion: {motion_desc}. {mot.get('findings', '')}")
    
    # Inspiration
    if 'inspiration' in assessment:
        insp = assessment['inspiration']
        lines.append(f"Inspiration: {insp['quality']} ({insp['posterior_rib_count']} posterior ribs). {insp.get('findings', '')}")
    
    # Artifacts
    if 'artifacts' in assessment:
        art = assessment['artifacts']
        if art['severity'] != "None":
            lines.append(f"Artifacts: {art['severity']}. {art.get('findings', '')}")
        else:
            lines.append("Artifacts: None significant.")
    
    return "\n".join(lines)


# Export for use in other modules
__all__ = ['technical_quality_assessor', 'TechnicalAssessment']
