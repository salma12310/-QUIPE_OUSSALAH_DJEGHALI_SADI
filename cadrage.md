# Cadrage du projet — Dashboard OpenFoodFacts

## Notre message

Le Nutri-Score seul ne suffit pas pour savoir si un produit est vraiment sain. Beaucoup de produits qui ont l'air "allégés" en sucre compensent en fait avec plus de matières grasses.

## À qui s'adresse le dashboard

On s'adresse au grand public, pas à des experts. L'idée c'est qu'une personne qui fait ses courses puisse regarder un rayon et se faire une idée rapide, sans connaître le détail de la nutrition. C'est pour ça qu'on a gardé un ton simple ("caddie", "rayon") plutôt qu'un vocabulaire scientifique.

## Les KPIs qu'on a choisis

### Dashboard 1 (Audit Rayons)

- **% de produits notés A ou B** : on trouvait ça plus utile qu'une simple moyenne, parce que ça dit directement si le rayon est plutôt fiable ou pas.
- **Sucre moyen, comparé au repère OMS (10g)** : on ne voulait pas juste afficher un chiffre brut, donc on le compare à un seuil connu pour que ce soit parlant.
- **Sel moyen, comparé à un seuil de risque (1.5g)** : même logique que le sucre.

On a volontairement enlevé le "nombre de produits filtrés" de la zone KPI (on le met juste en petit texte au dessus) parce que ce chiffre ne sert à rien pour décider quoi que ce soit, c'est juste de l'info de contexte. On voulait éviter les vanity metrics comme vu en cours.

### Dashboard 2 (Arbitrage Sucre/Gras)

- **% de produits "compensateurs"** (peu de sucre mais beaucoup de gras) : c'est le chiffre qui illustre le mieux notre message, donc on l'a mis en premier.
- **Corrélation sucre / gras** : pour appuyer visuellement ce qu'on voit sur le nuage de points, avec un vrai chiffre statistique.
- **% de produits notés E** : pour donner une idée du niveau de risque du rayon regardé.

## Comment le dashboard est organisé

- Une page d'accueil avec le message clé et un texte qui explique comment naviguer entre les deux dashboards
- Dashboard 1 : 3 filtres dans la sidebar (rayon, Nutri-Score, seuil de sucre) → 3 KPIs → un graphique en barres qui réagit aux filtres
- Dashboard 2 : 2 filtres dans la sidebar (rayon, Nutri-Score) → 3 KPIs → un nuage de points qui réagit aux filtres

## À propos de l'IA

On a utilisé Claude pour nous aider à écrire le code Streamlit. On a relu et compris chaque partie.
