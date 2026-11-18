# projet2_1007


### domaine 
Question : Pourquoi ce sujet ?
    Nous avons choisi ce sujet,car nous n'avons pas encore eu locasion de travailler sur un projet lié à la cybersécurité et nous aimerions découvrir ce monde de la programmation.



Question : Pourquoi ce dataset ?
    Nous avons choisi ce dataset, car il contient exactement toutes les principales informations dont nous avons besoins(password,strength). De plus, il a une grande quantité de donnée ce qui rendra notre modèle plus précis, car il sera entraîné sur une plus grade base de données.



Decisions prises:

### Pourquoi scikit-learn ?

- Options envisagées : [À COMPLÉTER : autres bibliothèques envisagées]
- Choix retenu : scikit-learn.
- Justification : il fournit tout ce dont le projet a besoin dans une seule bibliothèque : `DecisionTreeClassifier` (modèle), `train_test_split` (séparation avec graine fixée et classes stratifiées), `DummyClassifier` (référence), `accuracy_score`, `f1_score` et `confusion_matrix` (évaluation), et `joblib` pour sauvegarder le modèle entraîné.


### modele
- Options envisagées :
    - Forêt aléatoire : souvent plus précise, mais plus complexe et plus lourde.
    - K plus proches voisins (KNN) : nécessite de tenir compte des différences d'échelle    entre  les variables, notamment les distances.
    - Arbre de décision : modèle simple à comprendre et à interpréter, qui permet de visualiser les critères utilisés pour effectuer une prédiction.
- Choix retenu : Arbre de décision (DecisionTreeClassifier).
- Justification : Nous avons retenu l'arbre de décision, car il permet de classifier directement les mots de passe selon trois catégories de robustesse. Il est relativement simple à comprendre et à interpréter, ce qui facilite l'explication des résultats. 
- date: 5 novembre 2026

### profondeur maximale choisi:
- Options envisagées : 5, 10, 25
- Choix retenu : `max_depth = 10`.
- Justification : pour éviter le surapprentissage.
- date: 6 novembre 2026
#
## Cible et métrique

- Options envisagées : exactitude seule , f1 macros, recall
- Choix retenu : cible `strength` (0 = Faible, 1 = Moyen, 2 = Fort), classification ; métrique : exactitude, complétée par le F1 macro.
- Justification : les trois classes sont presque équilibrées (la référence obtient environ 33 %), donc l'exactitude est facile à lire. Le F1 macro vérifie que chaque classe est bien traitée.
- Validé par l'auxiliaire : 13 novembre 2026

### Technologie d'interface

- Options envisagées : a finir
- Choix retenu : PyQt6.
- Justification : a finir
