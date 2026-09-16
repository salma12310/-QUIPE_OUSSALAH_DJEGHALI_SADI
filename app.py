import streamlit as st
import pandas as pd

st.set_page_config(page_title="Accueil - TP6 Nutrition", page_icon="🍏", layout="wide")

st.title("🍏 OpenFoodFacts : Déjouer les pièges de l'industrie agroalimentaire")
st.markdown("### *Rapport d'audit nutritionnel et aide à la décision grand public*")
st.markdown("---")

# La conclusion claire exigée par la grille (Principe de Minto)
st.success("""
💡 **CONCLUSION CLÉ DU PROJET :**  
L'analyse croisée des données montre que **les produits les plus transformés masquent massivement leur teneur en sucre et en sel**, tout en bénéficiant parfois d'un marketing trompeur. Se fier uniquement au Nutri-Score ne suffit pas : un audit combiné du sucre et des lipides est indispensable pour identifier les véritables produits sains.
""")

st.markdown("### 🧭 Comment naviguer dans ce livrable ?")
st.markdown("""
Ce dashboard interactif est divisé en deux axes d'analyse disponibles dans le menu latéral gauche :
1. **Dashboard 1 (Analyse Santé) :** Étude de la répartition des Nutri-Scores et de l'impact direct du sucre et du sel.
2. **Dashboard 2 (Arbitrage Lipides/Protéines) :** Mise en évidence des compromis nutritionnels entre graisses et protéines selon les catégories de produits.
""")

st.info("👈 **Sélectionnez une page dans le menu de gauche pour lancer l'exploration interactive.**")
