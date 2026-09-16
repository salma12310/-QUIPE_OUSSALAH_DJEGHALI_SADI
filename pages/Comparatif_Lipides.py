import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Arbitrage Sucre/Gras", page_icon="⚖️", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('projet_F_dataset_food.csv', low_memory=False)
    colonnes_utiles = ['product_name', 'nutrition_grade_fr', 'sugars_100g', 'fat_100g', 'pnns_groups_1']
    df = df[colonnes_utiles].dropna()
    df['nutrition_grade_fr'] = df['nutrition_grade_fr'].str.upper()
    df['pnns_groups_1'] = df['pnns_groups_1'].str.strip()
    return df

df = load_data()

st.title("⚖️ Le Piège des Étiquettes : Sucre vs Matières Grasses")
st.markdown("*Analyse des compromis nutritionnels : un produit allégé en sucre est-il vraiment un bon choix ?*")
st.markdown("---")

# 🎛️ SIDEBAR : Filtre par catégorie pour rendre l'analyse interactive devant le jury
st.sidebar.header("🔍 Zoom par Rayon")
categories_dispos = sorted(df['pnns_groups_1'].unique())
choix_cat_2 = st.sidebar.selectbox("Filtrer le graphique par rayon", options=["Tous les rayons"] + categories_dispos, key="cat2")

df_plot = df.copy()
if choix_cat_2 != "Tous les rayons":
    df_plot = df_plot[df_plot['pnns_groups_1'] == choix_cat_2]

# Explications textuelles ancrées dans le réel
st.markdown("### 🕵️‍♂️ Décryptage du compromis industriel")
st.markdown("""
Lorsqu'un industriel réduit le sucre dans un produit (pour afficher un argument marketing flatteur), il compense souvent par **un ajout de matières grasses** pour préserver la texture et le goût. 
* Ce nuage de points met en évidence cette réalité : chaque point représente un produit positionné selon sa teneur en sucre et en lipides.
* La couleur indique directement son **Nutri-Score réel** (du vert au rouge).
""")

# GRAPHIQUE DE CORRÉLATION AMÉLIORÉ
fig, ax = plt.subplots(figsize=(10, 5))
palette_nutri = {'A': '#038141', 'B': '#85BB2F', 'C': '#FECB02', 'D': '#EE8100', 'E': '#E63E11'}

# Échantillonnage intelligent pour garder l'app fluide
df_sample = df_plot.sample(min(1500, len(df_plot)), random_state=42)

sns.scatterplot(
    data=df_sample, 
    x='sugars_100g', 
    y='fat_100g', 
    hue='nutrition_grade_fr', 
    palette=palette_nutri, 
    alpha=0.7, 
    s=70,
    ax=ax
)

ax.set_xlabel("Teneur en Sucre (g pour 100g)", color='black', fontweight='bold')
ax.set_ylabel("Teneur en Matières Grasses (g pour 100g)", color='black', fontweight='bold')
ax.tick_params(colors='black')
ax.legend(title="Nutri-Score", bbox_to_anchor=(1.05, 1), loc='upper left')

for spine in ax.spines.values(): 
    spine.set_visible(False)

st.pyplot(fig)

# Conclusion terrain
if choix_cat_2 == "Tous les rayons":
    st.success("""
    ** On remarque que les produits classés 'E' (en rouge) s'étalent non seulement sur le sucre mais explosent aussi le compteur des lipides. C'est la preuve visuelle qu'un mauvais profil nutritionnel cumule souvent les deux péchés mignons de l'agroalimentaire.
    """)
else:
    st.success(f"""
    🎯 **Focus sur le rayon '{choix_cat_2}' :** En filtrant uniquement sur cette catégorie, on observe précisément où se situe la limite à ne pas dépasser en termes de graisses et de sucres pour espérer conserver un Nutri-Score 'A' ou 'B'.
    """) 