import streamlit as st
import pandas as pd
import random
from utils import train_predict_from_user_input
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
        color: #123456
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
    # on prend 1 ligne au hasard pour chaque label
    sample_row = (
        df_reduced[df_reduced['etiquette_dpe'] == label]
        .sample(1, random_state=42)
        .drop(columns=['etiquette_dpe'])
    )
    # on transforme en dict {col: valeur}
    EXAMPLES.append(sample_row.iloc[0].to_dict())


# 3️⃣ Préparer la liste des variables
all_cols = [c for c in df_reduced.columns if c != 'etiquette_dpe']
quant_cols = df_reduced[all_cols].select_dtypes(include=['int', 'float']).columns.tolist()
qual_cols = df_reduced[all_cols].select_dtypes(include=['object', 'category']).columns.tolist()
options = { col: sorted(df_reduced[col].dropna().unique().tolist()) for col in qual_cols }

# 4️⃣ Slider et bouton pour charger un exemple
n_fill = st.sidebar.slider(
    "Nombre de variables à pré-remplir", 
    min_value=1, max_value=len(all_cols), value=5
)
if st.sidebar.button("Charger un exemple aléatoire"):
    example = random.choice(EXAMPLES)
    # print(example)
    # on garde juste n_fill clés parmi celles de l'exemple qui existent dans all_cols
    keys = random.sample([k for k in example if k in all_cols], k=min(n_fill, len(example)))
    # on met à jour session_state pour chaque variable
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
                    st.warning(f"⚠️ Valeur « {val} » non trouvée dans les options de {col}")  # sécurité
        else:
            st.session_state[col] = ""

# 3. Streamlit interface
st.title("Simulation DPE")
st.markdown("Remplissez les variables ci-dessous puis cliquez sur 'Lancer la simulation'.")

# Sélection des colonnes
all_cols = [c for c in df_reduced.columns if c != 'etiquette_dpe']
quant_cols = df_reduced[all_cols].select_dtypes(include=['int', 'float']).columns.tolist()
qual_cols = df_reduced[all_cols].select_dtypes(include=['object', 'category']).columns.tolist()

# Préparer les options pour les qualitatives
options = {
    col: sorted(df_reduced[col].dropna().unique().tolist())
    for col in qual_cols
}

print(quant_cols)

with st.form("formulaire_dpe"):
    cols = st.columns(3)
    user_input: Dict[str, Any] = {}
    all_cols = [c for c in df_reduced.columns if c != 'etiquette_dpe']
    for idx, col in enumerate(all_cols):
        widget_col = cols[idx % 3]
        label = col.replace("_", " ").capitalize()
        with widget_col:
            if col in quant_cols:
                raw = st.text_input(
                    label=label, 
                    placeholder="(laisser vide pour ignorer)",
                    key=col
                )
            else:
                opts = [""] + options[col]
                choice = st.selectbox(
                    label=label,
                    options=opts,
                    # index=0,
                    key=col  # par défaut sur vide
                )
    st.markdown("")
    btn1, btn2, btn3 = st.columns([3, 2, 2 ])
    with btn2:
        submitted = st.form_submit_button(
            label="Lancer la simulation", 
            help="Cliquez pour entraîner le modèle sur vos variables"
        )



if submitted:
    for col in all_cols:
        val = st.session_state.get(col, "")
        if val != "":
            try:
                user_input[col] = float(val) if col in quant_cols else val
            except ValueError:
                st.error(f"⚠️ Valeur non valide pour « {col} »")

    prediction, acc = train_predict_from_user_input(df_reduced, user_input)
    if prediction is None:
        st.error("❌ Aucune variable n'a été remplie.")
    else:
        st.success(f"🎯 Étiquette DPE prédite : **{prediction}**")
        st.info(f"📊 Accuracy estimée : **{acc:.2%}**")