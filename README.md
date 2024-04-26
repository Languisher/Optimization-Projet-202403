# Optimisation des Performances des Véhicules Électriques avec des Systèmes de Récupération d'Énergie

## Présentation du Projet

Ce projet présente des stratégies optimales pour améliorer la performance des véhicules électriques lors de courses de vitesse à travers des systèmes de récupération d'énergie. Utilisant le Principe Minimum de Pontryagin (PMP), le modèle optimise la distribution de la vitesse en contrôlant la puissance de sortie. Ce dépôt contient tous les codes nécessaires et les simulations utilisées dans la recherche.

### Caractéristiques Principales

- **Modèle de Contrôle Optimal** : Implémente le Principe Minimum de Pontryagin pour minimiser le temps utilisé sous différentes conditions de piste : terrain plat, rampe, et un groupe de deux collines.
- **Système de Récupération d'Énergie** : Intègre des systèmes de récupération d'énergie au freinage pour améliorer l'efficacité énergétique des véhicules électriques.
- **Simulation et Test** : Inclut divers scripts Python et notebooks Jupyter pour la simulation et la visualisation des stratégies optimales.

## Structure du Répertoire

- `optimisation_rapport.pdf` : Contient le rapport complet du projet détaillant le contexte théorique, la méthodologie et les résultats.
- `optimization_figure.ipynb` : Notebook Jupyter pour visualiser les résultats de l'optimisation.
- `route.py` : Module Python définissant les parcours et conditions de course.
- `simulation.py` : Script Python pour exécuter des simulations de base.
- `test.ipynb` : Notebook Jupyter pour tester les modèles et simulations.
- `vehicle.py` : Module Python décrivant le modèle de véhicule électrique.

## Installation

Pour exécuter les simulations et tester les stratégies d'optimisation, vous aurez besoin de Python 3.8 ou supérieur. Clonez le dépôt et installez les dépendances nécessaires :

```bash
git clone https://github.com/Languisher/Optimization-Projet-202403
cd Optimization-Projet-202403
pip install -r requirements.txt
```

## Utilisation
Pour exécuter la simulation principale : `test.ipynb`


## Contribution
Les contributions à ce projet sont les bienvenues. Veuillez forker le dépôt et soumettre vos pull requests avec vos modifications proposées.

## Licence
Ce projet est sous licence MIT - voir le fichier LICENSE pour les détails.

## Auteurs
Wei Teng
Nan Lin
Yuang Ding
Qingyue Deng
Ke Ma
Bingru Wang

## Remerciements
Un merci spécial à tous les contributeurs et chercheurs qui ont fourni des perspectives et des retours sur ce projet.