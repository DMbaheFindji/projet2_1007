# projet2_1007
## Données et Références

* **Source originale :** [Password Strength Dataset Jerry] 

* **Lien vers la source :** [https://www.kaggle.com/datasets/jerry1000/password-strength-dataset]


* **Licence :** Ce jeu de données est régi par la licence [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).



* **Modifications apportées :**
* Le fichier brut au format TSV (`production.tsv`) a été filtré (limité à 30 000 lignes) et transformé au format CSV (`donnees.csv`) avec l'extraction de nouvelles caractéristiques (longueur, présence de majuscules, de chiffres et de caractères spéciaux) pour les besoins du modèle de Machine Learning.


* ***Analyse du type de projet (Classification) et des variables utilisées dans le jeu de donnée ***
   
    C'est un projet de classification.
    La varible strength est la variable cible elle est discrète.
    Nous devons prdire la force du mot de passe : Faible,Moyen,Fort

    Il y a bel  et bien des variables numériques (ex.longueur)
    et des variables catégorielle (ex. contientmajuscule, contientChiffre, contientSpecial)
     

* ***Analyse du data dans (triage) ***

    *À côté de count, c'est écrit 30 000 pour chaque colonne. 
    Donc,cela prouve que tout est complet 

    *Les mots de passe ont une longueur minimal de 4 caractères et maximal de 174 caractères.
    La moyenne étant de 35 caractères

    *91.5% des mots de passes contiennent une majuscule
    33% des mots de passes contiennent un caractère spécial

    *La moyenne de la robustesse des mots de passe est 1.0 (Moyen)

    *Il n'y a pas de ligne double

    Le jeu de données est donc déjà bien nettoyer.
    Donc, il n'y a rien à corriger !

    La seul chose que nous avions fais était de garder seulemnt 30 000 lignes dans le data nous l'effectuons dans la classe JeuDeDonnee

