# Analyseur Syntaxique Python pour Programmes MTddV
## Description

Dans le dossier "Script" vous trouverez le script Python "analyse_syntaxiquep.py" qui permet de parser des fichiers : extraire les nœuds et arêtes. Il est possible produire des représentations en format JSON ou des représentations graphiques

## Installation

Clonez le dépôt.
Installez les dépendances requises à partir de requirement.txt :

`pip install -r requirement.txt`

## Utilisation

Lancer le script

`python3 analyseur_syntaxique.py -f chemin/vers/fichier [-j] [-g]`

Pour connaitre toutes les arguments possibles

`python3 analyseur_syntaxique.py --help`

## Structure du Projet
 
├── READ.ME.md           # Documentation  
├── requirement.txt      # Liste des dépendances  
├── Data                 # Répertoire de sortie   
├── requirement.txt      # Liste des dépendances  
├── Output               # Répertoire de sortie  
│   ├── data_json        # JSON généré  
│   └── graph            # Graphiques générés  
├── Script               # Répertoire du script python  
│   └── analyseur_syntaxique.py # Le script  
