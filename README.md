# MagicalQuill
Outil pour traiter les dossiers PDF des candidats Parcoursup

# Installation

## Pré-requis

* Python 3.5.x
* PyPDF2 (installé par pip)
* pdftotext (installé par pip)

Pour extraire les projets au format texte via process.sh, 
il faut également disposer de l'utilitaire pdftotext.

## Installation avec pip

    pip install git+https://github.com/Epithumia/MagicalQuill

# Utilisation

Cet utilitaire permet de découper les fichiers d'impression de Parcoursup
(anciennement APB) étudiant par étudiant.

L'utilitaire **decoupe-psup** permet de saucissonner un fichier issu
de l'impression.

Utilisation seule :

```
decoupe-psup [-o DIR] [-p] [-t] [-f] [-b] [-v] [-h] fichier

Options:
  -o DIR      Dossier de sortie des fichiers individuels.
  -v          Affiche la progression.
  -p          Extrait les projets de formation au format pdf.
  -t          Extrait les projets de formation au format texte.
  -f          Extrait les Fiches Avenir au format pdf.
  -b          Extrait les bulletins au format pdf.
  -h, --help  Affiche le message d'aide et termine.
```

L'utilitaire **process.sh** permet de ranger facilement les résultats et de
générer des fichiers textes comprenant les parcours de formation motivés
(anciennement lettres de motivation). C'est le programme qu'il faut appeler.
Il faut le paramétrer en créant un fichier CONFIG qui contient par exemple:

    FORMATION_INITIALE_INFO:dossiers_12345678_Informatique.pdf
    FORMATION_INITIALE_MECA:dossiers_12345678_Mecanique.pdf

Ensuite on le lance par :

    ./process.sh

Ou pour mettre à jour seulement un des fichiers :

    ./process.sh FORMATION_INTIALE_INFO

# Versions

* 0.2 Retrait de la nécessité d'avoir pdftk installé
* 0.2.1 decoupe-psup peut maintenant extraire les projets de formation motivés
* 0.2.2 projets de formation extraits en pdf ou en texte
* 0.2.3 fiches avenir extraites en pdf
* 0.2.4 bulletins extraits en pdf
