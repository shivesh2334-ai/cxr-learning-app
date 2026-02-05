import streamlit as st
from typing import Dict, List
import json

def anatomy_systematic_review():
    st.markdown('<p class="section-header">🔍 Systematic Anatomy Analysis</p>', 
                unsafe_allow_html=True)
    
    st.info("""
    **Systematic Approach (Klein & Guilleman):** Follow the sequence:
    1. Support/Monitoring Devices → 2. Chest Wall → 3. Mediastinum → 4. Hila → 
    5. Lungs → 6. Airways → 7. Pleura/Diaphragm
    """)
    
    # Load knowledge base
    with open('app/data/knowledge_base.json', 'r') as f:
        kb = json.load(f)
    
    # Progress tracker
    if 'analysis_progress' not in st.session_state:
        st.session_state.analysis_progress = {}
    
    tabs = st.tabs(["Devices", "Chest Wall", "Mediastinum", "Hila", "Lungs", "Airways", "Pleura"])
    
    with tabs[0]:  # Devices
        st.subheader("Support & Monitoring Devices")
        st.markdown("""
        **Checklist:**
        - [ ] Endotracheal tube position (tip 3-5cm above carina)
        - [ ] Central venous catheter (tip in SVC)
        - [ ] Nasogastric tube (below diaphragm)
        - [ ] Pacemaker/ICD leads
        - [ ] Chest tubes
        - [ ] Intra-aortic balloon pump
        """)
        
        device_findings = st.text_area("Device Findings:", 
                                     placeholder="ETT at T2, CVC tip in SVC, NG tube in stomach...")
        st.session_state.analysis_progress['devices'] = device_findings
    
    with tabs[1]:  # Chest Wall
        st.subheader("Chest Wall Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Symmetry Check**")
            cw_normal = st.checkbox("Symmetric breast shadows", key="cw_sym")
            ribs_intact = st.checkbox("Ribs intact bilaterally", key="cw_ribs")
            st_soft = st.checkbox("Normal soft tissues", key="cw_soft")
        
        with col2:
            st.markdown("**Abnormalities to Exclude**")
            pectus = st.checkbox("Pectus excavatum (mimics middle lobe disease)")
            rib_lesion = st.checkbox("Rib destruction (malignancy indicator)")
            soft_tissue_mass = st.checkbox("Soft tissue mass (incomplete border sign)")
        
        cw_findings = st.text_area("Chest Wall Findings:")
        st.session_state.analysis_progress['chest_wall'] = cw_findings
    
    with tabs[2]:  # Mediastinum
        st.subheader("Mediastinum Assessment")
        
        mediastinum_sections = {
            "Heart": ["Size (CTR <50%)", "Borders sharp", "Apex position"],
            "Aorta": ["Arch contour", "Calcification", "Tortuosity"],
            "SVC/IVC": ["Right border visible", "Azygos arch <1cm"],
            "Lines/Stripes": ["Anterior junction line", "Posterior junction line", 
                            "Paratracheal stripes", "Azygoesophageal recess"]
        }
        
        for section, items in mediastinum_sections.items():
            with st.expander(f"**{section}**"):
                for item in items:
                    st.checkbox(item, key=f"med_{section}_{item}")
        
        med_findings = st.text_area("Mediastinal Findings:")
        st.session_state.analysis_progress['mediastinum'] = med_findings
    
    with tabs[3]:  # Hila
        st.subheader("Hilar Analysis")
        st.markdown("""
        **Normal:** Right hilum lower than left (97% of cases)
        **Convergence Sign:** Vessels course toward enlarged hilum (vascular)
        """)
        
        hilum_positions = st.radio("Hilum Position:", 
                                  ["Normal (R<L)", "Same level", "Abnormal (R>L or elevated)"])
        hilar_size = st.radio("Hilar Size:", ["Normal", "Enlarged", "Prominent vessels"])
        
        if hilar_size == "Enlarged":
            st.multiselect("Differential:", 
                         ["Lymphadenopathy", "Central neoplasm", "Pulmonary hypertension"])
        
        hilar_findings = st.text_area("Hilar Findings:")
        st.session_state.analysis_progress['hila'] = hilar_findings
    
    with tabs[4]:  # Lungs
        st.subheader("Lung Parenchyma Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Volumes**")
            volumes = st.radio("Lung Volumes:", 
                             ["Normal", "Hyperinflated", "Reduced", "Asymmetric"])
            
            st.markdown("**Pattern**")
            pattern = st.selectbox("Predominant Pattern:", 
                                 ["Normal", "Air space opacity", "Interstitial reticular",
                                  "Interstitial nodular", "Mixed", "Destructive"])
        
        with col2:
            st.markdown("**Distribution**")
            distribution = st.multiselect("Distribution:", 
                                        ["Upper zone", "Lower zone", "Central/perihilar",
                                         "Peripheral", "Diffuse", "Unilateral"])
            
            st.markdown("**Specific Findings**")
            nodules = st.checkbox("Solitary pulmonary nodule")
            masses = st.checkbox("Pulmonary mass (≥3cm)")
            effusion = st.checkbox("Pleural effusion")
        
        if nodules:
            st.warning("⚠️ SPN detected: Requires thin-section CT characterization")
            st.markdown("**Malignancy features:** Spiculation, irregular margins, >3cm")
        
        lung_findings = st.text_area("Lung Findings:")
        st.session_state.analysis_progress['lungs'] = lung_findings
    
    with tabs[5]:  # Airways
        st.subheader("Airway Assessment")
        
        trachea = st.radio("Trachea:", ["Midline", "Deviated", "Narrowed"])
        if trachea == "Deviated":
            st.selectbox("Direction:", ["Ipsilateral (volume loss)", "Contralateral (mass effect)"])
        
        bronchi = st.checkbox("Bronchiectasis signs (tram tracks, ring shadows)")
        if bronchi:
            st.selectbox("Type:", ["Cylindrical", "Varicose", "Cystic"])
        
        airway_findings = st.text_area("Airway Findings:")
        st.session_state.analysis_progress['airways'] = airway_findings
    
    with tabs[6]:  # Pleura/Diaphragm
        st.subheader("Pleura & Diaphragm")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Pleura**")
            pneumothorax = st.checkbox("Pneumothorax (visceral pleural line)")
            pleural_effusion = st.checkbox("Pleural effusion")
            if pleural_effusion:
                st.selectbox("Effusion type:", 
                           ["Small (blunts costophrenic)", "Moderate", "Massive", "Loculated"])
            pleural_thickening = st.checkbox("Pleural thickening/plaques")
        
        with col2:
            st.markdown("**Diaphragm**")
            diaphragm = st.radio("Diaphragm Contours:", ["Normal", "Elevated", "Flattened"])
            if diaphragm == "Elevated":
                st.selectbox("Cause:", ["Weakness/paralysis", "Eventration", "Subpulmonic effusion"])
        
        pleura_findings = st.text_area("Pleura/Diaphragm Findings:")
        st.session_state.analysis_progress['pleura'] = pleura_findings
    
    # Summary
    st.markdown("---")
    st.subheader("Analysis Summary")
    if st.button("Generate Structured Findings"):
        generate_findings_summary(st.session_state.analysis_progress)

def generate_findings_summary(progress: Dict):
    st.markdown("### Structured Findings Report")
    for section, findings in progress.items():
        if findings:
            st.markdown(f"**{section.replace('_', ' ').title()}:** {findings}")
