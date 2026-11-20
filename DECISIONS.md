# projet2_1007


### domaine 
Question: Quel est notre sujet ?
    Nous avons décidé de faire un modèle qui prédit la robustesse d'un mot de passe.
    Donc, l'utilisateur pourra entrer les caractéristiques de son mot de passe à travers l'interface et , en fonction de celles-ci, le modèle sera en mesure de dire si la robustesse du mot de passe est Faible, Moyenne ou Forte.


Question : Pourquoi ce sujet ?
    Nous avons choisi ce sujet,car nous n'avons pas encore eu locasion de travailler sur un projet lié à la cybersécurité et nous aimerions découvrir ce monde de la programmation. Même si nous n'utilisons pas directement les concepts clés de la cybersécurité, la robustesse des mots de passe est un sujet qui nous y initie bienune excellente façon pour nous d'initier ce domaine.


Question : Pourquoi ce dataset ?
    Nous avons choisi ce dataset, car il contient exactement toutes les principales informations dont nous avons besoins(password,strength). De plus, il a une grande quantité de donnée ce qui rendra notre modèle plus précis, car il sera entraîné sur une plus grande base de données.


'''
C'est un projet de classification.
La varible strength(force) est la variable cible elle est discrète.
Nous devons prdire la force du mot de passe : Faible,Moyen,Fort


Il y a bel  et bien des variables numériques (ex.longueur,nombre de majuscule, nombre de chiffres, nombre de caractères spéciaux)
et une variable catégorielle (premier caractère :'spécial','chiffre' ou 'lettre')

'''


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



## Cible et métrique

- Options envisagées : exactitude seule , f1 macros, recall
- Choix retenu : cible `strength` (0 = Faible, 1 = Moyen, 2 = Fort), classification ; métrique : exactitude, complétée par le F1 macro.
- Justification : les trois classes sont presque équilibrées (la référence obtient environ 33 %), donc l'exactitude est facile à lire. Le F1 macro vérifie que chaque classe est bien traitée.
- Validé par l'auxiliaire : 13 novembre 2026



### Technologie d'interface

- Options envisagées : PyQt6
- Choix retenu : PyQt6.
- Justification : Lors de projets personnels nous avions déjà utilisé PyQt6. Donc, le choix a été assez simple nous avons choisi la technologie d'interface avec laquelle nous étions le plus familière.



Outil du chapitre 7 utilisé :
Donc, nous avons décidé de suivre la proposition donné dans l'énoncé du porjet en implémentant chronomètre à l'aide d'un décodeur dans notre code. En effet, ce chronomètre est un décodeur qui permet de chronométrer le temps entre le début et la fin d'une focntion sans avoir à changer le code interne de cette fonction. Ce décodeur reçoit en paramètre la fonction entraîner et retourne une nouvelle fonction nommée enveloppe qui va la remplacé. Donc, quand la fonction est appelé, on debut le timer, on appèle la focntion, puis on finit le timer.


