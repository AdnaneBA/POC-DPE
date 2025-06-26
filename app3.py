import streamlit as st
import pandas as pd
import random
from utils import train_predict_from_user_input, train_predict_from_user_input_xgboost
from typing import Dict, Any

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
        color: #123456;
        background-color: #ffffff !important;
        border: 2px solid #dfe6e9;
        border-radius: 8px;
        transition: border-color 0.3s ease;
    }
    .stTextInput>div>div>input:focus, .stTextArea textarea:focus, .stSelectbox>div>div:focus {
        border-color: #0984e3 !important;
        box-shadow: 0 0 5px rgba(9, 132, 227, 0.3);
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

@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_pickle('df_reduced.pkl')

df_reduced = load_data()

EXAMPLES = []
for label in sorted(df_reduced['etiquette_dpe'].unique()):
    sample_row = (
        df_reduced[df_reduced['etiquette_dpe'] == label]
        .sample(1, random_state=42)
        .drop(columns=['etiquette_dpe'])
    )
    EXAMPLES.append(sample_row.iloc[0].to_dict())

all_cols = [c for c in df_reduced.columns if c != 'etiquette_dpe']
quant_cols = df_reduced[all_cols].select_dtypes(include=['int', 'float']).columns.tolist()
qual_cols = df_reduced[all_cols].select_dtypes(include=['object', 'category']).columns.tolist()
options = { col: sorted(df_reduced[col].dropna().unique().tolist()) for col in qual_cols }

if "is_loading" not in st.session_state:
    st.session_state["is_loading"] = False

def handle_submit():
    st.session_state["is_loading"] = True

st.image("image/Probono.png", width=200) 


n_fill = st.sidebar.slider("Nombre de variables à pré-remplir", min_value=1, max_value=len(all_cols), value=5)
if st.sidebar.button("Charger un exemple aléatoire"):
    example = random.choice(EXAMPLES)
    keys = random.sample([k for k in example if k in all_cols], k=min(n_fill, len(example)))
    for col in all_cols:
        if col in keys:
            if col in quant_cols:
                st.session_state[col] = str(example[col])
            else:
                val = str(example[col])
                if val in options[col]:
                    st.session_state[col] = val
                else:
                    st.session_state[col] = ""
                    st.warning(f"⚠️ Valeur « {val} » non trouvée dans les options de {col}")
        else:
            st.session_state[col] = ""
if st.sidebar.button("Vider tous les champs"):
        st.session_state.update({col: None for col in all_cols})

st.title("Simulation DPE")
st.markdown("Remplissez les variables dans les onglets ci-dessous, puis cliquez sur 'Lancer la simulation'.")

# Sélection des colonnes
all_cols = [c for c in df_reduced.columns if c != 'etiquette_dpe']
quant_cols = df_reduced[all_cols].select_dtypes(include=['int', 'float']).columns.tolist()
qual_cols = df_reduced[all_cols].select_dtypes(include=['object', 'category']).columns.tolist()

# Préparer les options pour les qualitatives
options = {
    col: sorted(df_reduced[col].dropna().unique().tolist())
    for col in qual_cols
}
print(f"ICI c'est les options{options}\n\n")

TABS = {
    "Localisation": ["code_departement_ban", "code_postal_brut", "code_region_ban", "coordonnee_cartographique_x_ban", "coordonnee_cartographique_y_ban", "score_ban", "statut_geocodage", "zone_climatique"],
    "Bâti & Isolation": ["type_batiment", "periode_construction", "hauteur_sous_plafond", "nombre_niveau_logement", "ubat_w_par_m2_k", "classe_inertie_batiment", "qualite_isolation_enveloppe", "qualite_isolation_murs", "qualite_isolation_menuiseries", "qualite_isolation_plancher bas"],
    "Chauffage & ECS": ["type_installation_chauffage_n1", "type_generateur_n1_installation_n1", "type_generateur_chauffage_principal", "type_energie_generateur_n1_installation_n1", "type_energie_principale_chauffage", "description_generateur_chauffage_n1_installation_n1", "conso_chauffage_generateur_n1_installation_n1", "type_installation_ecs_n1", "type_generateur_n1_ecs_n1", "type_generateur_chauffage_principal_ecs", "type_energie_generateur_n1_ecs_n1", "type_energie_principale_ecs", "description_installation_ecs_n1", "volume_stockage_generateur_n1_ecs_n1", "conso_ef_generateur_n1_ecs_n1", "conso_ecs_ef_energie_n1", "usage_generateur_n1_ecs_n1"],
    "Déperditions & Apports": ["surface_chauffee_installation_chauffage_n1", "deperditions_murs", "deperditions_baies_vitrees", "deperditions_portes", "deperditions_planchers_bas", "deperditions_planchers_hauts", "deperditions_ponts_thermiques", "deperditions_renouvellement_air", "apport_solaire_saison_chauffe", "apport_interne_saison_chauffe"],
    "Consommations & Émissions": ["besoin_ecs", "conso_5 usages_par_m2_ef", "conso_5_usages_par_m2_ep", "emission_ges_chauffage_energie_n1", "emission_ges_ecs_energie_n1", "emission_ges_eclairage", "emission_ges_5_usages par_m2", "etiquette_ges"]
}

LABELS = {
    # Localisation
    "code_departement_ban": "Département",
    "code_postal_brut": "Code postal",
    "code_region_ban": "Région",
    "coordonnee_cartographique_x_ban": "Coordonnée X",
    "coordonnee_cartographique_y_ban": "Coordonnée Y",
    "score_ban": "Score de géocodage",
    "statut_geocodage": "Statut du géocodage",
    "zone_climatique": "Zone climatique",

    # Bâti & Isolation
    "type_batiment": "Type de bâtiment",
    "periode_construction": "Période de construction",
    "hauteur_sous_plafond": "Hauteur sous plafond",
    "nombre_niveau_logement": "Nombre de niveaux",
    "ubat_w_par_m2_k": "UBat (W/m².K)",
    "classe_inertie_batiment": "Classe d'inertie",
    "qualite_isolation_enveloppe": "Qualité d'isolation - enveloppe",
    "qualite_isolation_murs": "Qualité d'isolation - murs",
    "qualite_isolation_menuiseries": "Qualité d'isolation - menuiseries",
    "qualite_isolation_plancher bas": "Qualité d'isolation - plancher bas",

    # Chauffage & ECS
    "type_installation_chauffage_n1": "Type d'installation de chauffage",
    "type_generateur_n1_installation_n1": "Type de générateur de chauffage",
    "type_generateur_chauffage_principal": "Générateur principal de chauffage",
    "type_energie_generateur_n1_installation_n1": "Énergie utilisée - générateur chauffage",
    "type_energie_principale_chauffage": "Énergie principale du chauffage",
    "description_generateur_chauffage_n1_installation_n1": "Description générateur chauffage",
    "conso_chauffage_generateur_n1_installation_n1": "Conso chauffage générateur",
    "type_installation_ecs_n1": "Type d'installation ECS",
    "type_generateur_n1_ecs_n1": "Type de générateur ECS",
    "type_generateur_chauffage_principal_ecs": "Générateur principal ECS",
    "type_energie_generateur_n1_ecs_n1": "Énergie générateur ECS",
    "type_energie_principale_ecs": "Énergie principale ECS",
    "description_installation_ecs_n1": "Description installation ECS",
    "volume_stockage_generateur_n1_ecs_n1": "Volume de stockage ECS",
    "conso_ef_generateur_n1_ecs_n1": "Conso d’eau chaude ECS",
    "conso_ecs_ef_energie_n1": "Conso ECS énergie principale",
    "usage_generateur_n1_ecs_n1": "Usage générateur ECS",

    # Déperditions & Apports
    "surface_chauffee_installation_chauffage_n1": "Surface chauffée",
    "deperditions_murs": "Déperditions par les murs",
    "deperditions_baies_vitrees": "Déperditions par les baies vitrées",
    "deperditions_portes": "Déperditions par les portes",
    "deperditions_planchers_bas": "Déperditions plancher bas",
    "deperditions_planchers_hauts": "Déperditions plancher haut",
    "deperditions_ponts_thermiques": "Déperditions ponts thermiques",
    "deperditions_renouvellement_air": "Déperditions renouvellement air",
    "apport_solaire_saison_chauffe": "Apports solaires saison de chauffe",
    "apport_interne_saison_chauffe": "Apports internes saison de chauffe",

    # Consommations & Émissions
    "besoin_ecs": "Besoin en eau chaude sanitaire",
    "conso_5 usages_par_m2_ef": "Conso 5 usages (énergie finale) par m²",
    "conso_5_usages_par_m2_ep": "Conso 5 usages (énergie primaire) par m²",
    "emission_ges_chauffage_energie_n1": "Émissions GES chauffage",
    "emission_ges_ecs_energie_n1": "Émissions GES ECS",
    "emission_ges_eclairage": "Émissions GES éclairage",
    "emission_ges_5_usages par_m2": "Émissions GES (5 usages) par m²",
    "etiquette_ges": "Étiquette GES"
}


print(quant_cols)
with st.form("formulaire_dpe"):
    tab_objects = st.tabs(list(TABS.keys()))
    user_input: Dict[str, Any] = {}
    all_cols = [c for c in df_reduced.columns if c != 'etiquette_dpe']
    for i, (tab_name, cols_list) in enumerate(TABS.items()) :
        with tab_objects[i]:
            cols = st.columns(3)
            for idx, col in enumerate(cols_list):
                widget_col = cols[idx % 3]
                label = LABELS.get(col, col.replace("_", " ").capitalize())
                with widget_col:
                    if col in quant_cols:
                        raw = st.text_input(label=label, placeholder="(laisser vide)", key=col)
                    else:
                        opts = [""] + options[col]
                        choice = st.selectbox(label=label, options=opts, key=col)
    st.markdown("-------------------------")
    btn1, btn2, btn3 = st.columns([3, 2, 2])
    with btn2:
        submitted = st.form_submit_button("Lancer la simulation")

if submitted:
    for col in all_cols:
        val = st.session_state.get(col, "")
        if val != "":
            try:
                user_input[col] = float(val) if col in quant_cols else val
            except ValueError:
                st.error(f"⚠️ Valeur non valide pour « {col} »")

    prediction, acc = train_predict_from_user_input_xgboost(df_reduced, user_input)
    if prediction is None:
        st.error("❌ Aucune variable n'a été remplie.")
    else:
        st.success(f"🎯 Étiquette DPE prédite : **{prediction}**")
        st.info(f"📊 Accuracy estimée : **{acc:.2%}**")
