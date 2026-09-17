import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Audit Rayons - Nutrition", page_icon="🍎", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('projet_F_dataset_food.csv', low_memory=False)
    colonnes_utiles = ['product_name', 'nutrition_grade_fr', 'sugars_100g', 'salt_100g', 'pnns_groups_1']
    df = df[colonnes_utiles].dropna()
    df['nutrition_grade_fr'] = df['nutrition_grade_fr'].str.upper()
    df['pnns_groups_1'] = df['pnns_groups_1'].str.strip()

    # Traduction des rayons en français
    traduction_rayons = {
        "Beverages": "Boissons",
        "Cereals and potatoes": "Céréales et féculents",
        "Fish Meat Eggs": "Poisson, viande, œufs",
        "Fruits and vegetables": "Fruits et légumes",
        "Milk and dairy products": "Lait et produits laitiers",
        "Salty snacks": "Snacks salés",
        "Sugary snacks": "Snacks sucrés",
        "Composite foods": "Plats préparés",
        "Fat and sauces": "Matières grasses et sauces",
        "Alcoholic beverages": "Boissons alcoolisées",
        "unknown": "Non catégorisé",
    }
    df['pnns_groups_1'] = df['pnns_groups_1'].replace(traduction_rayons)

    return df

df = load_data()

st.title("🍎 Radar Rayons : Dissectons la qualité des aliments")
st.markdown("*Analyse ciblée des produits du quotidien et de leur impact réel sur la santé.*")
st.markdown("---")

st.sidebar.header("🛒 Paramètres du Caddie")

categories_dispos = sorted(df['pnns_groups_1'].unique())
choix_categorie = st.sidebar.selectbox("1. Choisir un rayon alimentaire", options=["Tous les rayons"] + categories_dispos)

nutriscores = sorted(df['nutrition_grade_fr'].unique())
filtre_score = st.sidebar.multiselect("2. Nutri-Scores acceptés", options=nutriscores, default=nutriscores)

sucre_max = st.sidebar.slider("3. Seuil max de sucre (g pour 100g)", 0.0, 100.0, 25.0)

df_filtre = df.copy()
if choix_categorie != "Tous les rayons":
    df_filtre = df_filtre[df_filtre['pnns_groups_1'] == choix_categorie]

df_filtre = df_filtre[
    (df_filtre['nutrition_grade_fr'].isin(filtre_score)) &
    (df_filtre['sugars_100g'] <= sucre_max)
]

if df_filtre.empty:
    st.warning("⚠️ Aucun produit ne correspond à ce filtre ultra-strict dans ce rayon.")
else:
    total = len(df_filtre)
    bons = len(df_filtre[df_filtre['nutrition_grade_fr'].isin(['A', 'B'])])
    pct_bons = (bons / total) * 100 if total > 0 else 0
    sucre_moyen = df_filtre['sugars_100g'].mean()
    sel_moyen = df_filtre['salt_100g'].mean()

    st.caption(f"📦 {total:,} produits correspondent à ce filtre.")

    c1, c2, c3 = st.columns(3)
    c1.metric("✨ Produits 'Bons' (A&B)", f"{pct_bons:.1f}%", help="Part de produits recommandés les yeux fermés.")
    c2.metric("🍬 Sucre moyen", f"{sucre_moyen:.1f} g", delta=f"{sucre_moyen - 10:.1f} g vs Repère OMS", delta_color="inverse")
    c3.metric("🧂 Sel moyen", f"{sel_moyen:.2f} g", delta=f"{sel_moyen - 1.5:.2f} g vs Risque sel", delta_color="inverse")

    st.markdown("---")
    st.markdown("### 👨‍⚕️ L'œil du Data Scientist sur ce rayon")

    if choix_categorie == "Tous les rayons":
        st.info("💡 **Observation globale :** En regardant l'ensemble de la base OpenFoodFacts, on remarque un déséquilibre flagrant. Le marketing pousse souvent vers les notes C et D sous couvert de mentions 'allégé' ou 'source de vitamines'.")
    else:
        st.info(f"💡 **Focus sur le rayon '{choix_categorie}' :** Ce filtre permet de mettre en lumière la réalité nutritionnelle spécifique de cette famille d'aliments, loin des promesses affichées sur les emballages.")

    fig, ax = plt.subplots(figsize=(10, 4))
    palette_nutri = {'A': '#038141', 'B': '#85BB2F', 'C': '#FECB02', 'D': '#EE8100', 'E': '#E63E11'}
    data_graph = df_filtre['nutrition_grade_fr'].value_counts().reset_index()
    data_graph.columns = ['Nutri-Score', 'Nombre']
    data_graph = data_graph.sort_values('Nutri-Score')

    sns.barplot(data=data_graph, x='Nutri-Score', y='Nombre', palette=palette_nutri, ax=ax)
    ax.set_ylabel("Nombre de références", color='black', fontweight='bold')
    ax.set_xlabel("Classe Nutri-Score", color='black', fontweight='bold')
    ax.tick_params(colors='black')
    for spine in ax.spines.values(): spine.set_visible(False)
    st.pyplot(fig)