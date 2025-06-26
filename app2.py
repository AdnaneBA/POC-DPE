import streamlit as st
import uuid


st.set_page_config(page_title="Simulation DPE Interface", layout="wide", initial_sidebar_state="expanded")

 
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: #2d3436;
    }
    .stTextInput>div>div>input, .stTextArea textarea, .stSelectbox>div>div {
        background-color: #ffffff !important;
        border: 2px solid #dfe6e9;
        border-radius: 8px;
        padding: 0.75rem;
        transition: border-color 0.3s ease;
    }
    .stTextInput>div>div>input:focus, .stTextArea textarea:focus, .stSelectbox>div>div:focus {
        border-color: #0984e3 !important;
        box-shadow: 0 0 5px rgba(9, 132, 227, 0.3);
    }
    .stButton>button {
        background-color: #0984e3;
        color: white;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #0652dd;
    }
    h1 {
        color: #2d3436;
        font-size: 2.5rem;
        font-weight: 700;
    }
    h3 {
        color: #636e72;
        font-size: 1.5rem;
        font-weight: 600;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
        border-right: 1px solid #dfe6e9;
    }
    .stExpander {
        background-color: #ffffff;
        border-radius: 10px;
        border: 1px solid #dfe6e9;
    }
    </style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.header("Navigation")
    st.markdown("Utilisez les sections ci-dessous pour naviguer rapidement :")
    sections = ["Données générales", "Localisation", "Enveloppe", "Émissions GES", "Description technique"]
    selected_section = st.radio("Aller à :", sections, index=0)

# --- Fonction pour champ numérique avec validation ---
def input_float(label, placeholder="", key=None):
    val_str = st.text_input(label, placeholder=placeholder, key=key)
    try:
        return float(val_str) if val_str.strip() else None
    except ValueError:
        if val_str.strip():
            st.warning(f"⚠️ '{label}' doit être un nombre valide.")
        return None

# --- Titre et introduction ---
st.title(" Interface DPE ")
st.markdown("""
    Une interface  pour saisir les données i**.  
  
""")
st.markdown("---")

# --- Onglets pour une meilleure organisation ---
tabs = st.tabs([" Général", " Localisation", " Enveloppe", " GES", " Technique"])

# --- Tab 1 : Données générales ---
with tabs[0]:
    if selected_section == "Données générales":
        st.markdown("<div id='general'></div>", unsafe_allow_html=True)
    st.subheader(" Données générales")
    col1, col2 = st.columns(2)
    
    with col1:
        apport_interne = input_float("Apport interne (saison chauffe)", "ex: 1077425.6", key=str(uuid.uuid4()))
        apport_solaire = input_float("Apport solaire (saison chauffe)", "ex: 1030843.1", key=str(uuid.uuid4()))
        besoin_ecs = input_float("Besoin ECS", "ex: 865.5", key=str(uuid.uuid4()))
        conso_m2_ef = input_float("Conso 5 usages/m² (EF)", "ex: 23.0", key=str(uuid.uuid4()))
    
    with col2:
        conso_m2_ep = input_float("Conso 5 usages/m² (EP)", "ex: 54.0", key=str(uuid.uuid4()))
        conso_chauffage = input_float("Conso chauffage N1", "ex: 332.4", key=str(uuid.uuid4()))
        conso_ecs = input_float("Conso ECS N1", "ex: 320.9", key=str(uuid.uuid4()))
        cout_auxiliaires = input_float("Coût auxiliaires (€)", "ex: 38.1", key=str(uuid.uuid4()))

# --- Tab 2 : Localisation et dimensions ---
with tabs[1]:
    if selected_section == "Localisation":
        st.markdown("<div id='localisation'></div>", unsafe_allow_html=True)
    st.subheader(" Localisation et dimensions")
    col1, col2 = st.columns(2)
    
    with col1:
        coord_x = input_float("Coordonnée X", "ex: 1030391.03", key=str(uuid.uuid4()))
        coord_y = input_float("Coordonnée Y", "ex: 6286468.25", key=str(uuid.uuid4()))
        ubat = input_float("UBAT (W/m².K)", "ex: 1.53", key=str(uuid.uuid4()))
    
    with col2:
        volume_stockage = input_float("Stockage ECS (L)", "ex: 200.0", key=str(uuid.uuid4()))
        region = st.selectbox("Code région BAN", ["", 93.0, 84.0, 75.0], key=str(uuid.uuid4()))
        dep = st.text_input("Code département BAN", placeholder="ex: 06", key=str(uuid.uuid4()))
        postal = st.text_input("Code postal brut", placeholder="ex: 06600", key=str(uuid.uuid4()))
        zone_clim = st.selectbox("Zone climatique", ["", "H1", "H2", "H3"], key=str(uuid.uuid4()))

# --- Tab 3 : Enveloppe et déperditions ---
with tabs[2]:
    if selected_section == "Enveloppe":
        st.markdown("<div id='enveloppe'></div>", unsafe_allow_html=True)
    st.subheader(" Enveloppe et déperditions")
    with st.expander(" Saisir les déperditions", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            dep_baies = input_float("Déperditions baies vitrées", "ex: 17.6", key=str(uuid.uuid4()))
            dep_murs = input_float("Déperditions murs", "ex: 4.5", key=str(uuid.uuid4()))
            dep_planchers_bas = input_float("Déperditions planchers bas", "ex: 0.0", key=str(uuid.uuid4()))
        with col2:
            dep_planchers_hauts = input_float("Déperditions planchers hauts", "ex: 0.0", key=str(uuid.uuid4()))
            dep_ponts = input_float("Déperditions ponts thermiques", "ex: 7.0", key=str(uuid.uuid4()))
            dep_portes = input_float("Déperditions portes", "ex: 0.0", key=str(uuid.uuid4()))
            dep_air = input_float("Déperditions renouvellement air", "ex: 19.8", key=str(uuid.uuid4()))

# --- Tab 4 : Émissions GES ---
with tabs[3]:
    if selected_section == "Émissions GES":
        st.markdown("<div id='ges'></div>", unsafe_allow_html=True)
    st.subheader(" Émissions GES")
    col1, col2 = st.columns(2)
    with col1:
        ges_ep = input_float("Émission GES 5 usages/m²", "ex: 1.0", key=str(uuid.uuid4()))
        ges_chauffage = input_float("Émission GES chauffage", "ex: 26.3", key=str(uuid.uuid4()))
    with col2:
        ges_ecs = input_float("Émission GES ECS", "ex: 20.9", key=str(uuid.uuid4()))
        ges_eclairage = input_float("Émission GES éclairage", "ex: 5.3", key=str(uuid.uuid4()))

# --- Tab 5 : Description technique ---
with tabs[4]:
    if selected_section == "Description technique":
        st.markdown("<div id='technique'></div>", unsafe_allow_html=True)
    st.subheader(" Description technique")
    col1, col2 = st.columns(2)
    with col1:
        inertie = st.selectbox("Classe inertie bâtiment", ["", "Légère", "Moyenne", "Lourde"], key=str(uuid.uuid4()))
        description_chauffage = st.text_area("Description générateur chauffage", placeholder="ex: Convecteur électrique NFC...", key=str(uuid.uuid4()))
        usage_chauffage = st.selectbox("Usage générateur chauffage", ["", "chauffage"], key=str(uuid.uuid4()))
    with col2:
        description_ecs = st.text_area("Description installation ECS", placeholder="ex: CET sur air extrait...", key=str(uuid.uuid4()))
        usage_ecs = st.selectbox("Usage générateur ECS", ["", "ecs"], key=str(uuid.uuid4()))

    # --- Soumission des données (placée uniquement dans le dernier onglet) ---
    st.markdown("---")
    if st.button(" Soumettre les données", use_container_width=True):
        champs = {
            "apport_interne_saison_chauffe": apport_interne,
            "apport_solaire_saison_chauffe": apport_solaire,
            "besoin_ecs": besoin_ecs,
            "classe_inertie_batiment": inertie or None,
            "code_departement_ban": dep or None,
            "code_postal_brut": postal or None,
            "code_region_ban": region or None,
            "conso_5_usages_par_m2_ef": conso_m2_ef,
            "conso_5_usages_par_m2_ep": conso_m2_ep,
            "conso_chauffage_generateur_n1_installation_n1": conso_chauffage,
            "conso_ecs_ef_energie_n1": conso_ecs,
            "coordonnee_cartographique_x_ban": coord_x,
            "coordonnee_cartographique_y_ban": coord_y,
            "cout_auxiliaires": cout_auxiliaires,
            "deperditions_baies_vitrees": dep_baies,
            "deperditions_murs": dep_murs,
            "deperditions_planchers_bas": dep_planchers_bas,
            "deperditions_planchers_hauts": dep_planchers_hauts,
            "deperditions_ponts_thermiques": dep_ponts,
            "deperditions_portes": dep_portes,
            "deperditions_renouvellement_air": dep_air,
            "description_generateur_chauffage_n1_installation_n1": description_chauffage or None,
            "description_installation_ecs_n1": description_ecs or None,
            "emission_ges_5_usages_par_m2": ges_ep,
            "emission_ges_chauffage_energie_n1": ges_chauffage,
            "emission_ges_ecs_energie_n1": ges_ecs,
            "emission_ges_eclairage": ges_eclairage,
            "ubat_w_par_m2_k": ubat,
            "usage_generateur_n1_ecs_n1": usage_ecs or None,
            "usage_generateur_n1_installation_n1": usage_chauffage or None,
            "volume_stockage_generateur_n1_ecs_n1": volume_stockage,
            "zone_climatique": zone_clim or None
        }

        result = {k: v for k, v in champs.items() if v is not None}

        if result:
            st.success("✅ Données soumises avec succès !")
            st.json(result)
        else:
            st.info("ℹ️ Aucun champ rempli.")