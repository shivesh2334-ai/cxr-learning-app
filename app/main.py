import streamlit as st
from components.technical_quality import technical_quality_assessor
from components.anatomy_analyzer import anatomy_systematic_review
from components.pattern_recognizer import pattern_analysis
from components.case_study import interactive_case_study
from components.report_generator import generate_structured_report

# Page configuration
st.set_page_config(
    page_title="CXR Learning & Diagnosis System",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: bold; color: #1f77b4; }
    .section-header { font-size: 1.5rem; font-weight: bold; color: #2c3e50; margin-top: 1rem; }
    .info-box { background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; }
    .checklist-item { margin-left: 1rem; }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<p class="main-header">🫁 Chest X-Ray Systematic Analysis</p>', 
                unsafe_allow_html=True)
    st.markdown("""
    **Educational tool based on:** Systematic Approach to Chest Radiographic Analysis (NIH/NCBI) 
    & Radiographic Approach to Diffuse Lung Disease (UpToDate)
    """)
    
    # Sidebar navigation
    with st.sidebar:
        st.header("Analysis Modules")
        module = st.radio(
            "Select Module:",
            ["📋 Technical Quality", "🔍 Systematic Anatomy Review", 
             "🎯 Pattern Recognition", "📚 Interactive Cases", 
             "📄 Report Generator", "ℹ️ Knowledge Base"]
        )
        
        st.markdown("---")
        st.info("""
        **Systematic Components:**
        1. Technical Quality
        2. Support/Monitoring Devices
        3. Chest Wall
        4. Mediastinum
        5. Hila
        6. Lungs
        7. Airways
        8. Pleura/Diaphragm
        """)
    
    # Module routing
    if "Technical Quality" in module:
        technical_quality_assessor()
    elif "Systematic Anatomy" in module:
        anatomy_systematic_review()
    elif "Pattern Recognition" in module:
        pattern_analysis()
    elif "Interactive Cases" in module:
        interactive_case_study()
    elif "Report Generator" in module:
        generate_structured_report()
    else:
        display_knowledge_base()

def display_knowledge_base():
    st.markdown('<p class="section-header">Reference Knowledge Base</p>', 
                unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Technical Factors", "Anatomic Regions", "Differential Diagnoses"])
    
    with tab1:
        st.subheader("Technical Quality Assessment")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Positioning:**
            - Spinous processes midline between clavicular heads
            - Scapulae rotated laterally (elbows forward)
            - No rotation
            
            **Penetration:**
            - Vertebral bodies faintly visible through mediastinum
            - Lung fields gray (not black/white)
            - Vascular markings visible
            """)
        with col2:
            st.markdown("""
            **Inspiration:**
            - Right hemidiaphragm at 6th anterior rib
            - Or 10th posterior rib at mid-clavicular line
            
            **Motion:**
            - Sharp rib cortices
            - Sharp vessel margins
            - Sharp diaphragm contours
            """)
    
    with tab2:
        st.subheader("Systematic Anatomic Review")
        regions = {
            "Chest Wall": "Check symmetry, rib integrity, soft tissues, breast shadows",
            "Mediastinum": "Heart size/shape, aortic arch, SVC, lines/stripes",
            "Hila": "Right normally lower than left, assess size/density",
            "Lungs": "Volumes, vascularity, opacities (air space vs interstitial)",
            "Airways": "Trachea position, bronchi, bronchiectasis signs",
            "Pleura": "Effusions (meniscus sign), pneumothorax (pleural line)"
        }
        for region, desc in regions.items():
            st.markdown(f"**{region}:** {desc}")
    
    with tab3:
        st.subheader("Pattern-Based Differential Diagnosis")
        patterns = {
            "Reticular + Basal": "UIP/IPF, NSIP, Asbestosis, Collagen vascular disease",
            "Nodular + Upper Zone": "TB, Sarcoidosis, Silicosis, Langerhans cell histiocytosis",
            "Perihilar": "Sarcoidosis, Lymphoma, Pulmonary edema, Kaposi sarcoma",
            "Air Space": "Pneumonia, Pulmonary edema, Hemorrhage, Lipoid pneumonia"
        }
        for pattern, dd in patterns.items():
            st.markdown(f"**{pattern}:** {dd}")

if __name__ == "__main__":
    main()
