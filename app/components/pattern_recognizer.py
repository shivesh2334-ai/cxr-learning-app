import streamlit as st
import json

def pattern_analysis():
    st.markdown('<p class="section-header">🎯 Pattern Recognition & Differential Diagnosis</p>', 
                unsafe_allow_html=True)
    
    with open('app/data/knowledge_base.json', 'r') as f:
        kb = json.load(f)
    
    st.markdown("""
    **Approach:** Based on ILO classification and descriptive patterns 
    (Felson, McLoud, and Fleischner Society terminology)
    """)
    
    pattern_type = st.selectbox(
        "Select Pattern Type:",
        ["Small Opacities (Nodular/Reticular)", "Large Opacities (Consolidation)",
         "Linear Opacities", "Destructive Pattern", "Vascular Pattern"]
    )
    
    if "Small Opacities" in pattern_type:
        analyze_small_opacities(kb)
    elif "Large Opacities" in pattern_type:
        analyze_large_opacities(kb)
    elif "Linear" in pattern_type:
        analyze_linear_opacities(kb)
    elif "Destructive" in pattern_type:
        analyze_destructive_pattern(kb)
    else:
        analyze_vascular_pattern(kb)

def analyze_small_opacities(kb):
    st.subheader("Small Opacity Analysis (ILO Classification)")
    
    col1, col2 = st.columns(2)
    with col1:
        shape = st.radio("Shape:", ["Round (nodular)", "Irregular (reticular)"])
        if shape == "Round (nodular)":
            size = st.selectbox("Size:", 
                              ["p (<1.5mm)", "q (1.5-3mm)", "r (3-10mm)"])
        else:
            size = st.selectbox("Size:", 
                              ["s (<1.5mm)", "t (1.5-3mm)", "u (3-10mm)"])
    
    with col2:
        profusion = st.slider("Profusion (density):", 0, 3, 1)
        distribution = st.multiselect("Distribution:", 
                                    ["Upper zones", "Middle zones", "Lower zones",
                                     "Diffuse", "Perihilar", "Peripheral"])
    
    # Differential logic
    st.markdown("---")
    st.subheader("Differential Diagnosis")
    
    if shape == "Round (nodular)":
        if "p" in size:
            st.markdown("""
            **Micronodular Pattern (<1.5mm):**
            - Alveolar microlithiasis
            - Intravenous talc granulomatosis
            - Early pneumoconiosis (silicosis, CWP)
            - Subacinar foci (PAP, PCP)
            """)
        else:
            st.markdown("""
            **Nodular Pattern (1.5-10mm):**
            - Miliary tuberculosis
            - Sarcoidosis
            - Fungal infections
            - Pneumoconiosis (silicosis, CWP)
            - Metastatic disease
            - Langerhans cell histiocytosis
            """)
    else:
        st.markdown("""
        **Reticular Pattern:**
        - **Acute:** Interstitial edema, viral pneumonia, acute hypersensitivity
        - **Chronic:** IPF/UIP, NSIP, asbestosis, collagen vascular disease
        """)
    
    # Distribution-based refinement
    if "Upper zones" in distribution:
        st.info("Upper zone predominance suggests: TB, sarcoidosis, pneumoconiosis, LCH")
    if "Lower zones" in distribution:
        st.info("Lower zone predominance suggests: IPF, asbestosis, scleroderma, rheumatoid lung")

def analyze_large_opacities(kb):
    st.subheader("Large Opacity (Consolidation) Analysis")
    
    pattern = st.selectbox("Consolidation Pattern:", [
        "Diffuse homogeneous",
        "Multifocal patchy",
        "Lobar without atelectasis",
        "Lobar with atelectasis",
        "Perihilar (batwing/butterfly)",
        "Peripheral"
    ])
    
    air_bronchograms = st.checkbox("Air bronchograms present")
    
    st.markdown("---")
    st.subheader("Differential Diagnosis")
    
    differentials = {
        "Diffuse homogeneous": ["Severe pneumonia", "ARDS", "Pulmonary edema", "Diffuse alveolar hemorrhage"],
        "Multifocal patchy": ["Bronchopneumonia", "Aspiration", "Organizing pneumonia", "Hemorrhage"],
        "Lobar without atelectasis": ["Lobar pneumonia", "Pulmonary infarction"],
        "Lobar with atelectasis": ["Obstructive pneumonia", "Mucus plugging"],
        "Perihilar (batwing/butterfly)": ["Cardiogenic edema", "Alveolar proteinosis", "Pulmonary hemorrhage"],
        "Peripheral": ["Cryptogenic organizing pneumonia", "Chronic eosinophilic pneumonia", "COVID-19"]
    }
    
    for dx in differentials.get(pattern, []):
        st.markdown(f"- {dx}")
    
    if air_bronchograms:
        st.success("Air bronchograms suggest: Air space disease (pneumonia, edema, hemorrhage)")

def analyze_linear_opacities(kb):
    st.subheader("Linear Opacity Analysis")
    
    line_type = st.selectbox("Type:", ["Kerley A", "Kerley B", "Kerley C", "Tram lines"])
    
    descriptions = {
        "Kerley A": "2-4cm lines radiating from hilum to upper lobes (axial interstitium)",
        "Kerley B": "1cm lines at lung periphery, abutting pleura (subpleural interstitium)",
        "Kerley C": "Fine reticular pattern (parenchymal interstitium)",
        "Tram lines": "Parallel lines representing thickened bronchial walls"
    }
    
    st.info(descriptions[line_type])
    
    if line_type == "Kerley B":
        st.markdown("""
        **Causes of Kerley B lines:**
        - Chronic left ventricular failure
        - Mitral valve disease
        - Lymphangitic carcinomatosis
        - Asbestosis
        - Viral pneumonia (Hantavirus, coronavirus, measles)
        """)
    elif line_type == "Tram lines":
        st.markdown("""
        **Causes of tram lines:**
        - Bronchiectasis
        - Chronic bronchitis
        - Asthma
        - ABPA (Allergic bronchopulmonary aspergillosis)
        """)

def analyze_destructive_pattern(kb):
    st.subheader("Destructive Lung Disease")
    
    features = st.multiselect("Features present:", [
        "Small lungs/volume loss",
        "Honeycombing",
        "Bullae/cysts",
        "Bronchiolectasis",
        "Hilar retraction",
        "Pulmonary hypertension"
    ])
    
    st.markdown("""
    **Causes of Destructive Pattern:**
    - End-stage interstitial lung disease (IPF/UIP)
    - Advanced emphysema
    - Langerhans cell histiocytosis (end-stage)
    - Lymphangioleiomyomatosis
    - End-stage granulomatous disease
    """)

def analyze_vascular_pattern(kb):
    st.subheader("Vascular Pattern Analysis")
    
    pattern = st.selectbox("Vascular Pattern:", [
        "Cephalization (upper lobe diversion)",
        "Equalization with hyperemia",
        "Equalization with oligemia",
        "Centralization (pruned tree)",
        "Lateralization (asymmetric)",
        "Mosaic perfusion"
    ])
    
    explanations = {
        "Cephalization": "Upper lobe vessels > lower lobe (LV failure, mitral stenosis, emphysema)",
        "Equalization with hyperemia": "Similar size upper/lower vessels (L-R shunt, hyperthyroidism, anemia)",
        "Equalization with oligemia": "Similar size but reduced (hypovolemia, R-L shunt)",
        "Centralization": "Large central, small peripheral (pulmonary hypertension)",
        "Lateralization": "One lung larger than other (unilateral emphysema, pulmonary artery obstruction)",
        "Mosaic perfusion": "Patchy attenuation (emphysema, CTEPH, bronchiolitis obliterans)"
    }
    
    st.info(explanations[pattern])
