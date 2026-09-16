import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


st.set_page_config(page_title="Enquête Titanic", page_icon="🚢", layout="wide")

st.markdown("""
    <style>
    .kpi-card { background-color: #0B1D3A; padding: 15px; border-radius: 8px; color: white; text-align: center; border-left: 5px solid #3498DB; box-shadow: 2px 2px 10px rgba(0,0,0,0.3); }
    .kpi-value { font-size: 1.8rem; font-weight: bold; color: #3498DB; }
    .kpi-label { font-size: 0.9rem; color: #BDC3C7; text-transform: uppercase; }
    </style>
""", unsafe_allow_html=True)

#  CHARGEMENT DES DONNÉES
@st.cache_data
def load_data():
    df = sns.load_dataset('titanic')
    df['mortalite_pct'] = (1 - df['survived']) * 100
    df['taille_famille'] = df['sibsp'] + df['parch'] + 1
    df['age'] = df['age'].fillna(df['age'].median())
    return df

df = load_data()

#  EN-TÊTE IMMERSIF (Sans photo, 100% fiable)
st.title("🧊 Le Naufrage du RMS Titanic")
st.markdown("### *Une tragédie maritime dictée par la classe, le genre et la famille.*")
st.markdown("---")

# 🎛️ SIDEBAR (Filtres avancés)
st.sidebar.markdown("<div style='text-align: center; font-size: 80px;'>🚢</div>", unsafe_allow_html=True)
st.sidebar.title("⚓ Poste de Commandement")

sexe_filtre = st.sidebar.multiselect(" Genre", options=df['sex'].unique(), default=df['sex'].unique())
classe_filtre = st.sidebar.multiselect(" Classe", options=sorted(df['pclass'].unique()), default=sorted(df['pclass'].unique()))
age_min, age_max = st.sidebar.slider(" Tranche d'âge", int(df['age'].min()), int(df['age'].max()), (0, 80))
ports_dispos = df['embark_town'].dropna().unique()
port_filtre = st.sidebar.multiselect(" Port d'embarquement", options=ports_dispos, default=ports_dispos)

# Filtrage dynamique
df_filtre = df[
    (df['sex'].isin(sexe_filtre)) & 
    (df['pclass'].isin(classe_filtre)) & 
    (df['age'] >= age_min) & (df['age'] <= age_max) &
    (df['embark_town'].isin(port_filtre))
]

#  ZONE KPIs 
if df_filtre.empty:
    st.error("🌊 L'océan est vide... Modifiez vos filtres.")
else:
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.markdown(f'<div class="kpi-card"><div class="kpi-label">Passagers</div><div class="kpi-value">🧍 {len(df_filtre)}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="kpi-card"><div class="kpi-label">Survie</div><div class="kpi-value">🛟 {df_filtre["survived"].mean()*100:.1f}%</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="kpi-card"><div class="kpi-label">Prix Moyen</div><div class="kpi-value">💷 £{df_filtre["fare"].mean():.0f}</div></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="kpi-card"><div class="kpi-label">Âge Moyen</div><div class="kpi-value">⏳ {df_filtre["age"].mean():.0f} ans</div></div>', unsafe_allow_html=True)
    c5.markdown(f'<div class="kpi-card"><div class="kpi-label">Famille Moy.</div><div class="kpi-value">👨‍👩‍👧 {df_filtre["taille_famille"].mean():.1f} pers.</div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    #  DÉTAILS
    tab1, tab2, tab3 = st.tabs(["📉 Inégalités Sociales", "👨‍👩‍👧 Effet Famille & Âge", "🗃️ Base de données"])
    
    couleur_fond, texte = '#0B1D3A', '#FFFFFF'
    
    with tab1:
        colA, colB = st.columns(2)
        with colA:
            st.subheader("La classe sociale")
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            fig1.patch.set_facecolor(couleur_fond); ax1.set_facecolor(couleur_fond)
            sns.barplot(data=df_filtre, x='pclass', y='mortalite_pct', errorbar=None, palette=['#E74C3C', '#BDC3C7', '#BDC3C7'], ax=ax1)
            ax1.tick_params(colors=texte); ax1.set_ylabel("Mortalité (%)", color=texte)
            for spine in ax1.spines.values(): spine.set_visible(False)
            st.pyplot(fig1)
            
        with colB:
            st.subheader("Le genre")
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            fig2.patch.set_facecolor(couleur_fond); ax2.set_facecolor(couleur_fond)
            sns.barplot(data=df_filtre, x='sex', y='mortalite_pct', errorbar=None, palette=['#BDC3C7', '#E74C3C'], ax=ax2)
            ax2.tick_params(colors=texte); ax2.set_ylabel("", color=texte)
            for spine in ax2.spines.values(): spine.set_visible(False)
            st.pyplot(fig2)

    with tab2:
        colC, colD = st.columns(2)
        with colC:
            st.subheader("Chances de survie par taille de famille")
            fig3, ax3 = plt.subplots(figsize=(6, 4))
            fig3.patch.set_facecolor(couleur_fond); ax3.set_facecolor(couleur_fond)
            sns.lineplot(data=df_filtre, x='taille_famille', y='survived', color='#F1C40F', marker='o', ax=ax3)
            ax3.tick_params(colors=texte); ax3.set_ylabel("Taux de survie", color=texte)
            for spine in ax3.spines.values(): spine.set_visible(False)
            st.pyplot(fig3)
            
        with colD:
            st.subheader("Distribution des âges")
            fig4, ax4 = plt.subplots(figsize=(6, 4))
            fig4.patch.set_facecolor(couleur_fond); ax4.set_facecolor(couleur_fond)
            sns.histplot(data=df_filtre, x='age', hue='survived', multiple='stack', palette=['#E74C3C', '#2ECC71'], ax=ax4)
            ax4.tick_params(colors=texte); ax4.set_xlabel("Âge", color=texte); ax4.set_ylabel("Nombre", color=texte)
            for spine in ax4.spines.values(): spine.set_visible(False)
            st.pyplot(fig4)

    with tab3:
        st.subheader("Extrait des registres de bord")
        st.dataframe(df_filtre[['survived', 'pclass', 'sex', 'age', 'fare', 'embark_town']], use_container_width=True)  