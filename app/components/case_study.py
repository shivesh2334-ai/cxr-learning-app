"""
Interactive Case Study Module

Provides interactive learning cases based on real-world CXR scenarios
from the systematic analysis literature.
"""

import streamlit as st
from typing import Dict, List, Optional
import json
from dataclasses import dataclass
from enum import Enum


class CaseDifficulty(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class CXRCase:
    """Data class for CXR case studies"""
    case_id: str
    title: str
    difficulty: CaseDifficulty
    patient_history: str
    clinical_context: str
    image_description: str  # Text description since we may not have actual images
    findings: Dict[str, str]  # Organized by anatomical region
    key_findings: List[str]
    diagnosis: str
    teaching_points: List[str]
    differentials_considered: List[str]
    references: List[str]


def interactive_case_study():
    """
    Main function for interactive case study module.
    Provides case-based learning with progressive disclosure.
    """
    st.markdown('<p class="section-header">📚 Interactive Case Studies</p>', 
                unsafe_allow_html=True)
    
    st.info("""
    **Learning Approach:** Work through real-world cases using the systematic analysis method.
    Cases are organized by difficulty and cover common pathologies from the NCBI/UpToDate references.
    """)
    
    # Case selection
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Select Case")
        difficulty_filter = st.selectbox(
            "Filter by difficulty:",
            ["All", "Beginner", "Intermediate", "Advanced"]
        )
        
        case_category = st.selectbox(
            "Case category:",
            [
                "All Categories",
                "Air Space Disease",
                "Interstitial Lung Disease",
                "Nodules and Masses",
                "Pleural Disease",
                "Mediastinal Abnormalities",
                "Technical Quality Issues"
            ]
        )
        
        # Get available cases
        available_cases = load_cases(difficulty_filter, case_category)
        selected_case_id = st.selectbox(
            "Select case:",
            list(available_cases.keys()),
            format_func=lambda x: available_cases[x].title
        )
    
    with col2:
        if selected_case_id:
            display_case(available_cases[selected_case_id])
        else:
            st.info("Select a case to begin learning")
    
    # Case management section
    st.markdown("---")
    col3, col4 = st.columns(2)
    
    with col3:
        if st.button("➕ Create Custom Case"):
            create_custom_case()
    
    with col4:
        if st.button("📊 View Progress"):
            display_learning_progress()


def load_cases(difficulty_filter: str, category_filter: str) -> Dict[str, CXRCase]:
    """
    Load case library. In production, this would load from database.
    For now, using built-in educational cases based on the PDF content.
    """
    
    cases = {
        # Case 1: Air Space Disease - Pneumonia
        "case_001": CXRCase(
            case_id="case_001",
            title="Case 1: Right Upper Lobe Pneumonia",
            difficulty=CaseDifficulty.BEGINNER,
            patient_history="""
            **Patient:** 45-year-old male
            **Presentation:** 3 days of fever, productive cough, right-sided chest pain
            **Vitals:** Temp 38.5°C, HR 95, RR 22, BP 130/80
            **Labs:** WBC 15,000, neutrophilia
            """,
            clinical_context="Community-acquired pneumonia, previously healthy",
            image_description="""
            **Technical Quality:** Good inspiration, adequate penetration, no motion
            
            **Findings:**
            - Frontal view: Patchy opacity right upper lobe, air bronchograms visible
            - Right heart border preserved (not silhouetted)
            - Lateral view: Opacity projects over anterior segment RUL
            - No pleural effusion, no lymphadenopathy
            """,
            findings={
                "technical": "Adequate technique",
                "devices": "None present",
                "chest_wall": "Normal",
                "mediastinum": "Normal cardiac silhouette, no shift",
                "hila": "Normal, symmetric",
                "lungs": "Right upper lobe air space opacity with air bronchograms",
                "airways": "Trachea midline, no bronchial wall thickening",
                "pleura": "No effusion or pneumothorax"
            },
            key_findings=[
                "Air space opacity with air bronchograms",
                "Lobar distribution (RUL)",
                "Acute clinical presentation"
            ],
            diagnosis="Right upper lobe pneumonia (Streptococcus pneumoniae most likely)",
            teaching_points=[
                "Air bronchograms indicate air space disease (alveolar filling)",
                "Preservation of right heart border suggests anterior/posterior location",
                "Lobar distribution typical of bacterial pneumonia",
                "Follow-up imaging recommended to ensure resolution (rule out underlying lesion)"
            ],
            differentials_considered=[
                "Pulmonary infarction (clinical context makes less likely)",
                "Pulmonary hemorrhage (no hemoptysis)",
                "Cryptogenic organizing pneumonia (subacute presentation)"
            ],
            references=["Klein JS - Air space opacification patterns"]
        ),
        
        # Case 2: Interstitial Lung Disease - IPF
        "case_002": CXRCase(
            case_id="case_002",
            title="Case 2: Idiopathic Pulmonary Fibrosis",
            difficulty=CaseDifficulty.INTERMEDIATE,
            patient_history="""
            **Patient:** 68-year-old male, former smoker (40 pack-years)
            **Presentation:** Progressive dyspnea on exertion over 18 months
            **Vitals:** SpO2 88% on room air, fine bibasilar crackles
            **PFTs:** Restrictive pattern, reduced DLCO
            """,
            clinical_context="Suspected interstitial lung disease, refer for HRCT",
            image_description="""
            **Technical Quality:** Suboptimal inspiration (shallow breathing), adequate penetration
            
            **Findings:**
            - Reduced lung volumes bilaterally
            - Bilateral basal predominant reticular opacities
            - Honeycombing suggested at lung bases
            - Traction bronchiectasis visible
            - No hilar lymphadenopathy
            - Cardiac size normal
            """,
            findings={
                "technical": "Suboptimal inspiration due to disease",
                "devices": "None",
                "chest_wall": "Normal",
                "mediastinum": "Normal, no shift",
                "hila": "Normal, no enlargement",
                "lungs": "Bilateral basal reticular opacities, volume loss, honeycombing",
                "airways": "Traction bronchiectasis at bases",
                "pleura": "No significant pleural disease"
            },
            key_findings=[
                "Bilateral basal reticular pattern",
                "Reduced lung volumes",
                "Honeycombing (end-stage fibrosis)",
                "Traction bronchiectasis",
                "No upper lobe predominance"
            ],
            diagnosis="Usual Interstitial Pneumonia (UIP) pattern - Idiopathic Pulmonary Fibrosis",
            teaching_points=[
                "Basal and peripheral predominance characteristic of UIP",
                "Reticular pattern indicates interstitial disease",
                "Honeycombing = irreversible fibrosis, poor prognosis",
                "HRCT required for definitive diagnosis (UIP vs NSIP)",
                "No role for surgical lung biopsy if definite UIP pattern on HRCT"
            ],
            differentials_considered=[
                "Fibrotic NSIP (more ground glass, less honeycombing)",
                "Asbestosis (requires exposure history, pleural plaques)",
                "Collagen vascular disease-related ILD (check autoantibodies)",
                "Chronic hypersensitivity pneumonitis (upper lobe predominance, air trapping)"
            ],
            references=["Klein JS - Interstitial patterns", "UpToDate - UIP/IPF diagnosis"]
        ),
        
        # Case 3: Technical Quality - Poor Inspiration
        "case_003": CXRCase(
            case_id="case_003",
            title="Case 3: Pseudo-Cardiomegaly from Poor Inspiration",
            difficulty=CaseDifficulty.BEGINNER,
            patient_history="""
            **Patient:** 35-year-old female
            **Presentation:** Pre-operative chest X-ray for elective surgery
            **Vitals:** Normal
            **History:** No cardiac symptoms, no risk factors
            """,
            clinical_context="Routine pre-op screening",
            image_description="""
            **Technical Quality:** Poor inspiratory effort (only 6 posterior ribs visible)
            
            **Findings:**
            - Cardiothoracic ratio appears increased (0.58)
            - Crowding of bronchovascular markings at bases
            - Apparent widening of mediastinum
            - No pulmonary edema
            - No pleural effusions
            """,
            findings={
                "technical": "Poor inspiration - only 6 posterior ribs above diaphragm",
                "devices": "None",
                "chest_wall": "Normal",
                "mediastinum": "Appears widened due to poor inspiration",
                "hila": "Normal, appear prominent due to crowding",
                "lungs": "Crowded vessels at bases, no infiltrates",
                "airways": "Normal",
                "pleura": "Normal"
            },
            key_findings=[
                "Poor inspiratory effort (<8 posterior ribs)",
                "Apparent cardiomegaly (CTR >0.5)",
                "Crowded bronchovascular markings",
                "Clinical context inconsistent with heart failure"
            ],
            diagnosis="Normal heart size with pseudo-cardiomegaly due to poor inspiration",
            teaching_points=[
                "Poor inspiration causes apparent cardiomegaly (CTR falsely elevated)",
                "Crowding of vessels mimics vascular congestion",
                "Always assess technical quality before interpreting findings",
                "Repeat with better inspiration if clinically indicated",
                "Correlation with clinical context essential"
            ],
            differentials_considered=[
                "Cardiomegaly (clinical context makes unlikely)",
                "Pericardial effusion (no water bottle configuration)"
            ],
            references=["Klein JS - Technical quality assessment"]
        ),
        
        # Case 4: Pleural Disease - Loculated Effusion
        "case_004": CXRCase(
            case_id="case_004",
            title="Case 4: Loculated Pleural Effusion (Empyema)",
            difficulty=CaseDifficulty.INTERMEDIATE,
            patient_history="""
            **Patient:** 52-year-old male with history of IV drug use
            **Presentation:** Fever, chest pain, productive cough for 1 week
            **Vitals:** Temp 39°C, HR 110, RR 28
            **Labs:** WBC 22,000, elevated procalcitonin
            """,
            clinical_context="Complicated parapneumonic effusion vs empyema",
            image_description="""
            **Technical Quality:** Good technique, upright film
            
            **Findings:**
            - Left lower zone biconvex opacity (D-shaped)
            - Does not layer dependently
            - Obscures left hemidiaphragm
            - No air-fluid level visible
            - Adjacent lung consolidation
            - Mediastinum not shifted (trapped lung)
            """,
            findings={
                "technical": "Adequate",
                "devices": "None",
                "chest_wall": "Normal",
                "mediastinum": "Midline, no mass effect",
                "hila": "Normal",
                "lungs": "Left lower lobe consolidation adjacent to effusion",
                "airways": "Normal",
                "pleura": "Loculated left pleural effusion (biconvex, non-mobile)"
            },
            key_findings=[
                "Biconvex (lenticular) shape - key sign of loculation",
                "Does not layer with gravity",
                "Adjacent lung consolidation (pneumonia)",
                "No mediastinal shift (lung trapped by fibrosis)"
            ],
            diagnosis="Loculated parapneumonic effusion, likely evolving empyema",
            teaching_points=[
                "Loculated effusions have biconvex (D-shaped) appearance",
                "Different from free-flowing effusion (meniscus sign)",
                "Usually indicates infection (parapneumonic) or malignancy",
                "Requires drainage (chest tube or surgery)",
                "CT helpful to define extent and plan intervention"
            ],
            differentials_considered=[
                "Free pleural effusion (shape is wrong)",
                "Pleural mass/tumor (clinical context favors infection)",
                "Lung abscess (would have air-fluid level)"
            ],
            references=["Klein JS - Pleural disease patterns"]
        ),
        
        # Case 5: Nodule - Solitary Pulmonary Nodule
        "case_005": CXRCase(
            case_id="case_005",
            title="Case 5: Solitary Pulmonary Nodule - Malignancy",
            difficulty=CaseDifficulty.ADVANCED,
            patient_history="""
            **Patient:** 58-year-old male, 30 pack-year smoking history
            **Presentation:** Incidental finding on pre-employment CXR
            **Vitals:** Normal
            **History:** No prior imaging available for comparison
            """,
            clinical_context="Incidental solitary pulmonary nodule - evaluate for malignancy",
            image_description="""
            **Technical Quality:** Good inspiration and penetration
            
            **Findings:**
            - 2.3 cm nodule right upper lobe, peripheral location
            - Spiculated margins (corona radiata sign)
            - No calcification visible
            - No satellite lesions
            - No hilar or mediastinal lymphadenopathy
            - No pleural effusion
            """,
            findings={
                "technical": "Optimal",
                "devices": "None",
                "chest_wall": "Normal",
                "mediastinum": "No lymphadenopathy",
                "hila": "Normal",
                "lungs": "RUL spiculated nodule, 2.3 cm, no calcification",
                "airways": "Normal",
                "pleura": "No effusion"
            },
            key_findings=[
                "Solitary pulmonary nodule (>3cm would be mass)",
                "Spiculated margins (highly suspicious for malignancy)",
                "Upper lobe location (common for lung cancer)",
                "No calcification (would suggest benign)",
                "Risk factors: age, smoking history"
            ],
            diagnosis="Highly suspicious for primary lung cancer (T1b if <3cm, no node involvement)",
            teaching_points=[
                "Spiculation = malignant sign (corona radiata = desmoplastic reaction)",
                "Size >2cm increases malignancy risk significantly",
                "Upper lobe location favors malignancy over benign",
                "Requires CT chest with contrast for staging",
                "Tissue diagnosis needed (CT-guided biopsy or surgical)",
                "Check for extrathoracic metastases (PET-CT, brain MRI)"
            ],
            differentials_considered=[
                "Granuloma (would typically have calcification or be smaller)",
                "Hamartoma (would have fat/popcorn calcification)",
                "Metastasis (solitary, no known primary)",
                "Organizing pneumonia (would have surrounding ground glass)"
            ],
            references=["Klein JS - Solitary pulmonary nodule", "Fleischner Society guidelines"]
        ),
        
        # Case 6: Mediastinal Mass
        "case_006": CXRCase(
            case_id="case_006",
            title="Case 6: Anterior Mediastinal Mass - Lymphoma",
            difficulty=CaseDifficulty.INTERMEDIATE,
            patient_history="""
            **Patient:** 28-year-old male
            **Presentation:** 2 months of cough, weight loss, night sweats
            **Vitals:** Temp 37.8°C, HR 85
            **Labs:** Elevated LDH, mild anemia
            """,
            clinical_context="B symptoms with mediastinal mass - suspect lymphoma",
            image_description="""
            **Technical Quality:** Good
            
            **Findings:**
            - Large lobulated anterior mediastinal mass
            - Widening of superior mediastinum
            - Mass silhouettes with cardiac border (anterior location confirmed on lateral)
            - Bilateral hilar lymphadenopathy
            - No pleural effusion
            - Lungs clear
            """,
            findings={
                "technical": "Adequate",
                "devices": "None",
                "chest_wall": "Normal",
                "mediastinum": "Large anterior mediastinal mass, lobulated",
                "hila": "Bilateral hilar lymphadenopathy",
                "lungs": "Clear",
                "airways": "Trachea not significantly deviated",
                "pleura": "No effusion"
            },
            key_findings=[
                "Anterior mediastinal mass (silhouettes heart on lateral)",
                "Lobulated contour",
                "Bilateral hilar involvement",
                "B symptoms (fever, weight loss, night sweats)",
                "Young adult male"
            ],
            diagnosis="Hodgkin lymphoma (most likely given age and presentation)",
            teaching_points=[
                "Anterior mediastinum: 4T's - Thymoma, Teratoma, Thyroid, T-cell lymphoma",
                "Hodgkin lymphoma commonly presents with mediastinal mass in young adults",
                "B symptoms indicate systemic disease",
                "CT chest/abdomen/pelvis needed for staging",
                "Tissue diagnosis via mediastinoscopy or CT-guided biopsy",
                "Elevated LDH suggests high tumor burden"
            ],
            differentials_considered=[
                "Thymoma (usually older patients, no B symptoms)",
                "Germ cell tumor (check AFP, beta-HCG)",
                "Substernal thyroid (would extend from neck, check thyroid)",
                "Non-Hodgkin lymphoma (usually older, more aggressive)"
            ],
            references=["Klein JS - Mediastinal masses", "Carter BW - ITMIG classification"]
        )
    }
    
    # Apply filters
    filtered_cases = {}
    for case_id, case in cases.items():
        # Difficulty filter
        if difficulty_filter != "All":
            if case.difficulty.value != difficulty_filter.lower():
                continue
        
        # Category filter (simplified logic)
        if category_filter != "All Categories":
            category_map = {
                "Air Space Disease": ["pneumonia", "consolidation", "air space"],
                "Interstitial Lung Disease": ["fibrosis", "interstitial", "reticular"],
                "Nodules and Masses": ["nodule", "mass", "tumor"],
                "Pleural Disease": ["pleural", "effusion", "pneumothorax"],
                "Mediastinal Abnormalities": ["mediastinal", "hilar"],
                "Technical Quality Issues": ["technical", "pseudo", "poor inspiration"]
            }
            keywords = category_map.get(category_filter, [])
            if not any(kw in case.title.lower() or kw in case.diagnosis.lower() 
                      for kw in keywords):
                continue
        
        filtered_cases[case_id] = case
    
    return filtered_cases if filtered_cases else cases


def display_case(case: CXRCase):
    """
    Display selected case with progressive disclosure learning.
    """
    st.markdown(f"### {case.title}")
    st.caption(f"Difficulty: {case.difficulty.value.title()} | Case ID: {case.case_id}")
    
    # Create tabs for progressive learning
    tabs = st.tabs([
        "📋 History", 
        "🔍 Image Description", 
        "📝 Your Analysis",
        "✅ Key Findings",
        "🎯 Diagnosis",
        "📚 Teaching Points"
    ])
    
    with tabs[0]:
        st.markdown("### Clinical History")
        st.markdown(case.patient_history)
        st.markdown("### Clinical Context")
        st.info(case.clinical_context)
    
    with tabs[1]:
        st.markdown("### Image Description")
        st.markdown(case.image_description)
        
        st.warning("""
        **Note:** In a full implementation, the actual CXR image would be displayed here
        with interactive annotation tools. For this educational version, detailed 
        descriptions are provided.
        """)
        
        # Allow user to make notes
        st.text_area("Your observations:", key=f"obs_{case.case_id}")
    
    with tabs[2]:
        st.markdown("### Systematic Analysis Checklist")
        
        # Interactive checklist
        checklist_items = [
            "Technical quality assessed",
            "Devices/lines evaluated",
            "Chest wall examined",
            "Mediastinum evaluated",
            "Hila assessed",
            "Lung parenchyma analyzed",
            "Airways checked",
            "Pleura/diaphragm evaluated"
        ]
        
        for item in checklist_items:
            st.checkbox(item, key=f"check_{case.case_id}_{item}")
        
        user_diagnosis = st.text_input("Your differential diagnosis:", 
                                      key=f"dx_{case.case_id}")
        
        if st.button("Submit Analysis", key=f"submit_{case.case_id}"):
            st.success("Analysis submitted! Check the 'Key Findings' and 'Diagnosis' tabs.")
    
    with tabs[3]:
        st.markdown("### Key Radiographic Findings")
        for i, finding in enumerate(case.key_findings, 1):
            st.markdown(f"{i}. {finding}")
        
        st.markdown("### Findings by Region")
        for region, finding in case.findings.items():
            with st.expander(f"**{region.replace('_', ' ').title()}**"):
                st.write(finding)
    
    with tabs[4]:
        st.markdown("### Final Diagnosis")
        st.success(f"**{case.diagnosis}**")
        
        st.markdown("### Differential Diagnoses Considered")
        for dx in case.differentials_considered:
            st.markdown(f"- {dx}")
    
    with tabs[5]:
        st.markdown("### Teaching Points")
        for i, point in enumerate(case.teaching_points, 1):
            st.markdown(f"{i}. {point}")
        
        st.markdown("### References")
        for ref in case.references:
            st.caption(f"- {ref}")


def create_custom_case():
    """
    Allow users to create their own case studies.
    """
    st.markdown("### Create Custom Case")
    
    with st.form("custom_case"):
        title = st.text_input("Case Title")
        difficulty = st.selectbox("Difficulty", ["beginner", "intermediate", "advanced"])
        history = st.text_area("Patient History")
        findings = st.text_area("Key Findings (one per line)")
        diagnosis = st.text_input("Diagnosis")
        teaching = st.text_area("Teaching Points")
        
        submitted = st.form_submit_button("Save Case")
        
        if submitted:
            st.success("Case saved! (In production, this would save to database)")
            # Here you would save to database or JSON file


def display_learning_progress():
    """
    Display user's learning progress and statistics.
    """
    st.markdown("### Learning Progress")
    
    # Mock statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Cases Completed", "3/6")
    with col2:
        st.metric("Accuracy", "85%")
    with col3:
        st.metric("Time Spent", "2.5 hrs")
    with col4:
        st.metric("Streak", "5 days")
    
    # Progress by category
    st.markdown("### Progress by Category")
    categories = {
        "Air Space Disease": 100,
        "Interstitial Disease": 50,
        "Nodules/Masses": 0,
        "Pleural Disease": 100,
        "Mediastinal": 0,
        "Technical Quality": 100
    }
    
    for cat, pct in categories.items():
        st.progress(pct / 100, text=f"{cat}: {pct}%")


# Export
__all__ = ['interactive_case_study', 'CXRCase', 'CaseDifficulty']
