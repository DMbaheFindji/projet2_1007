# Prédiction de la force d'un mot de passe

Projet 2 d'INF1007 (A2026), réalisé en équipe de deux : **de la donnée à l'application**.
Un modèle simple (arbre de décision) estime la force d'un mot de passe (Faible, Moyen ou Fort) à partir de ses caractéristiques, et une interface graphique PyQt6 permet à un utilisateur de l'interroger.

## Équipe

| Membre | Responsabilités |
|---|---|
| Danielle  | Jeu de données, interface graphique|
| Alia Cayer | Modèle (entraînement, évaluation, sauvegarde), tests |
| Les deux | documentation |


## Données et références

- **Source originale** : Password Strength Dataset (Jerry), Kaggle
- **Lien** : https://www.kaggle.com/datasets/jerry1000/password-strength-dataset
- **Licence** : [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
- **Modifications apportées** : le fichier brut `production.tsv` a été limité à 30 000 lignes et converti au format CSV (`donnees.csv`) par la classe `JeuDeDonnees`. Les caractéristiques `longueur`, `nbMajuscule`, `nbChiffre`, `nbSpecial` et `premierCaractere` ont été calculées à partir de chaque mot de passe.


- **Emplacement du fichier** : Le jeu de données (donnees.csv) est dans `donneesFolder/`.


- **Données personnelles** : le jeu de données ne contient aucunes informations personelles

### Variables

| Colonne | Type | Description |
|---|---|---|
| `longueur` | numérique | nombre de caractères du mot de passe |
| `nbMajuscule` | numérique | nombre de majuscules |
| `nbChiffre` | numérique | nombre de chiffres |
| `nbSpecial` | numérique | nombre de caractères non alphanumériques |
| `premierCaractere` | catégorielle | `lettre`, `chiffre` ou `special` |
| `strength` (cible) | catégorielle ordonnée | 0 = Faible, 1 = Moyen, 2 = Fort |

### Type de problème

Il s'agit d'un problème de **classification** : la variable cible `strength` est discrète et l'on prédit la force du mot de passe (Faible, Moyen ou Fort).

### Exploration et nettoyage

Les données sont examinées avec pandas (`head`, `dtypes`, `isna`, `describe`, `duplicated`) dans `JeuDeDonnees.triage_ET_charger_Donnee`.

- Aucune valeur manquante : le `count` est de 30 000 pour chaque colonne.
- Aucune ligne en double.
- Longueur des mots de passe : minimum 4, maximum 174, moyenne d'environ 35 caractères.
- Environ 91,5 % des mots de passe contiennent au moins une majuscule et environ 33 % contiennent un caractère spécial.
- Force moyenne : 1,0 (Moyen).

Le jeu de données est déjà propre : aucune correction n'a été nécessaire. La seule transformation est la réduction à 30 000 lignes et l'ajout des caractéristiques.

**Graphique d'exploration** : `Graphique1.png`, un diagramme en barres de la répartition des classes de force (enregistré avec `savefig`).

## Modèle

- **Modèle retenu** : arbre de décision (`DecisionTreeClassifier`, `max_depth=10`, `random_state=42`).
- **Préparation** : `premierCaractere` est encodé en trois colonnes 0/1. Séparation 80 % entraînement / 20 % test avec `train_test_split` (graine 42, `stratify` pour conserver les proportions de classes).
- **Métriques** : exactitude (principale) et F1 macro. L'exactitude est aussi recalculée avec NumPy (calcul vectorisé) et comparée à celle de scikit-learn dans un test.
- **Référence** : `DummyClassifier(strategy='most_frequent')`, qui prédit toujours la classe majoritaire.

| | Exactitude (ensemble de test, 6 000 lignes) |
|---|---|
| Référence (classe majoritaire) |0,334  |
| Arbre de décision |  0,934 |
| F1 macro (arbre) | 0,935  |

L'arbre fait presque trois fois mieux que la référence . Le calcul NumPy de l'exactitude donne exactement la même valeur que scikit-learn (0,9342), ce qui est vérifié dans un test.

**Limites** :
- Les erreurs se font surtout entre classes voisines : 258 mots de passe Faibles sont prédits Moyens, et le modèle ne confond jamais Faible et Fort. La classe Faible est la moins bien reconnue.
- Le modèle ne voit que cinq caractéristiques (longueur, majuscules, chiffres, caractères spéciaux, premier caractère), pas le contenu du mot de passe. Il ne peut donc pas détecter un mot courant ou prévisible.
- Un score aussi élevé suggère que l'étiquette de force est fortement liée à ces caractéristiques. 
- Un seul découpage entraînement/test (graine 42) a été utilisé, sans validation croisée.


- **Sauvegarde** : `modeles/modele.joblib` (modèle) et `modeles/metadonnees.json` (colonnes, valeurs possibles, intervalles, métriques). L'interface s'en sert pour se construire : le modèle n'est pas ré-entraîné à chaque lancement.

## Installation et lancement

Prérequis : Python 3.12.9 

```bash
git clone https://github.com/DMbaheFindji/projet2_1007.git
cd projet2_1007
python -m venv .venv
# Windows : .venv\Scripts\activate    |    macOS/Linux : source .venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

Au **premier lancement**, `main.py` convertit le TSV en CSV, produit le graphique d'exploration, entraîne le modèle et le sauvegarde. Les lancements suivants ouvrent directement l'interface.

Tests et couverture :

```bash
python -m pytest
python -m coverage run -m pytest
python -m coverage report
```

## Interface graphique

Technologie : **PyQt6** (application locale, classe `Application` héritant de `QMainWindow`).

- **Saisie** : un champ par variable, construit à partir de `metadonnees.json` : champ texte pour les variables numériques (avec l'intervalle en indication) et liste déroulante pour `premierCaractere`. L'utilisateur ne saisit **jamais son vrai mot de passe**, seulement ses caractéristiques.
- **Validation** : une saisie vide ou non numérique affiche un message clair. Une valeur incohérente (longueur inférieure à 1, nombre négatif, total des caractéristiques supérieur à la longueur) lève `EntreeInvalideError`, dont le message est affiché dans la fenêtre. Aucun traceback n'est montré.
- **Prédiction** : le bouton « Prédire la robustesse du mot de passe » affiche la force prédite et la confiance du modèle en pourcentage.
- **Graphiques Matplotlib** : après chaque prédiction, deux images produites avec `savefig` sont affichées dans la fenêtre : la probabilité de chaque force pour la saisie courante, et la réussite du modèle par force sur l'ensemble de test.
- **Historique** : chaque prédiction est ajoutée à `historiqueFolder/historique.csv`. Le bouton « Voir l'historique » l'affiche dans un tableau.


## Structure du code

```
projet_inf1007/
├── README.md
├── DECISIONS.md
├── JOURNAL_IA.md
├── requirements.txt
├── pytest.ini
├── .github/workflows/tests.yml
├── donneesFolder/            # production.tsv, donnees.csv
├── modeles/                  # modèle, métadonnées, graphiques
├── historiqueFolder/         # historique.csv
└── src/
    ├── main.py               # point d'entrée
    ├── JeuDeDonnees.py       # conversion TSV → CSV, caractéristiques, graphique d'exploration
    ├── modele.py             # séparation, encodage, référence, entraînement, prédiction, sauvegarde
    ├── exception.py          # exceptions personnalisées
    ├── interface.py          # interface PyQt6
    └── test/
        ├── test_jeudedonnees.py
        └── test_modele.py

```   

**Classes**

- `JeuDeDonnees` : conversion, chargement et exploration des données.
- `Modele` : entraînement, prédiction et sauvegarde. Attributs protégés (`_arbre`, `_metriques`, `_entraine`), méthode spéciale `__str__`.
- `Application` : interface, qui **contient** le modèle et les métadonnées (composition).
- **Héritage et polymorphisme** : `Metrique` (classe abstraite) a trois enfants, `Exactitude`, `ExactitudeNumpy` et `F1Macro`, qui redéfinissent chacun la méthode `calculer()`. `Modele.entrainer` les utilise toutes de la même façon, sans savoir comment chacune calcule son score.

**Exceptions** (`exception.py`) : toutes héritent de `ErreurProjet` (qui hérite de `Exception`) :
- `ModeleNonEntraineError` : prédiction ou sauvegarde avant l'entraînement ;
- `DonneeInvalideError` : CSV vide ou colonnes manquantes ;
- `EntreeInvalideError` : caractéristiques hors des valeurs permises.
- `LectureEcritureError` : échec de la lecture ou de la conversion d'un fichier ;



## Outil du chapitre 7

Comme outil du chapitre 7, nous avons utilisé lambda dans l'interface pour trier les prédictions de l'historique du plus ancien au plus récent.
De plus, nous avons également utilisé un décorateur qui a pour but de chronométrer le temps d'exécution de la fonction  `prédire`.

## Tests et couverture

- Nombre de tests pytest : 15
- Couverture mesurée avec `coverage` : 84%
- Intégration continue : workflow GitHub Actions (`.github/workflows/tests.yml`) qui lance `pytest` à chaque `push`.

## Documentation consultée

- pandas : [documentation pandas](https://pandas.pydata.org/docs/)
- scikit-learn : [train_test_split](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html)
- PyQt6 : [Documentation PyQt6](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- PySide6 : [Documentation PySide6](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/index.html#module-PySide6.QtWidgets)

## Autres documents

- `DECISIONS.md` : fiche de décisions
- `JOURNAL_IA.md` : journal d'utilisation de l'IA