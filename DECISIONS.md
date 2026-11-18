# projet2_1007

Question : Pourquoi ce sujet ?
    Nous avons choisi ce sujet,car nous n'avons pas encore eu locasion de travailler sur un projet lié à la cybersécurité et nous aimerions découvrir ce monde de la programmation.



Question : Pourquoi ce dataset ?
    Nous avons choisi ce dataset, car il contient exactement toutes les principales informations dont nous avons besoins(password,strength). De plus, il a une grande quantité de donnée ce qui rendra notre modèle plus précis, car il sera entraîné sur une plus grade base de données.



Decisions prises:

### Pourquoi scikit-learn ?

 Il fournit tout ce dont le projet a besoin dans une seule bibliothèque :
  `DecisionTreeClassifier` (modèle), `train_test_split` (séparation avec graine fixée
  et classes stratifiées), `DummyClassifier` (référence), `accuracy_score`, `f1_score`
  et `confusion_matrix` (évaluation), et `joblib` pour sauvegarder le modèle entraîné.

###  décision de l'arbre de décision:

modele envisagé:
- foret aleatoire: souvent plus precise mais plus lourde et difficile
-k plus proche du voisins: comparaison de distaance entre variables d'échelle tres differentes 
-Arbre de décision (retenu):Gère sans préparation des variables numériques et binaires, prédit directement trois classes, donne des probabilités (predict), plus comprehensif

### profondeur maximale choisi:
- depth = 10 pour eviter le surapprentissage

