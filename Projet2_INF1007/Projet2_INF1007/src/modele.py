


import json
import os

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from exception import (DonneeInvalideError, EntreeInvalideError,
                        ModeleNonEntraineError)


DOSSIER_PROJET = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER_MODELES = os.path.join(DOSSIER_PROJET, 'modeles')# la ou on va ecrire le modele entraine
DOSSIER_DONNEES = os.path.join(DOSSIER_PROJET, 'donnees')

cheminFichierCsv = os.path.join(DOSSIER_DONNEES, 'donnees.csv') # chemin complet du CSV dentree 
cheminModele = os.path.join(DOSSIER_MODELES, 'modele.joblib') # le modele entrainee 
cheminMetadonnees = os.path.join(DOSSIER_MODELES, 'metadonnees.json') # 
#cheminGraphiqueExploration = os.path.join(DOSSIER_DONNEES, 'graphique_exploration.png')
cheminMatriceConfusion = os.path.join(DOSSIER_MODELES, 'matrice_confusion.png') # pour le gra[hique 2]

graineAleatoire = 42 # pour que les reultat sois reproductible

COLONNES_ENTREE = ['longeur', 'contientMajuscule', 'contientChiffre', 'contientSpecial'] # les 4 caracteristique de prediction c les X
COLONNE_CIBLE = 'strength' # cest le y variable a predire  
ETIQUETTES_FORCE = {0: 'Faible', 1: 'Moyen', 2: 'Fort'} # dictionnaire de traduction
COLONNES_REQUISES = ['password'] + COLONNES_ENTREE + [COLONNE_CIBLE]



#TODO: update docstring enleve les test et juste mettre en 

def chargerDonnees(chemin: str) -> pd.DataFrame: 
    """Charge le CSV avec pandas et nettoie les données.

    Supprime les valeurs manquantes, les mots de passe vides et les doublons.
    Lève FileNotFoundError si le fichier n'existe pas (lancer d'abord la
    classe Transformer pour générer donnees.csv) et ValueError si le
    fichier ne contient aucune donnée quon peut utiliser
    """
    if not os.path.exists(chemin):
        raise FileNotFoundError(
            f'Fichier introuvable : {chemin}. '
            f'Génère-le d\'abord avec la classe Transformer (donnees.py).')
    df = pd.read_csv(chemin) 
# verification des colonnes manquantes
    manquantes = [c for c in COLONNES_REQUISES if c not in df.columns]
    if manquantes:
        raise DonneeInvalideError(f'Colonnes manquantes dans {chemin} : {manquantes}')
    
    df = df.dropna() # au cas ou si une ligne contient des valeurs manquante
    df = df[df['password'].astype(str).str.len() > 0] # enleve si les mdp est vides 
    df = df.drop_duplicates() # supprime ligne identique 
    if df.empty:
        raise DonneeInvalideError(f'Aucune donnée exploitable dans {chemin}')
    return df # retourne un tableau de donnees 


def separerDonnees(df: pd.DataFrame, tailleTest: float = 0.2) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Sépare en ensembles d'entraînement et de test.

    Graine aléatoire fixée et separerDonnees prend toute la table
    de données et la coupe en deux morceaux : un morceau pour apprendre au modèle,
    un morceau pour vérifier s'il a bien appris.
    """
    #0.2 pusiqueon test 20 % et train 80%
    X = df[COLONNES_ENTREE] # contient: longueur, majustcule, chhiffre , special
    y = df[COLONNE_CIBLE] # le strenght 
    #utilisation de la librarie sklearn
    return train_test_split(X, y, test_size=tailleTest,
                            random_state=graineAleatoire, stratify=y) #random test pour melange de la meme maniere les donnes a chaque fois
# stratify garder les meme proportion de classes dans test et entrainment pour que levaluation soit plus exact




def calculerReference(XTrain: pd.DataFrame, yTrain: pd.Series, XTest: pd.DataFrame, yTest: pd.Series) -> float:
    # recoit les 4 morceaux de separeDonnee
    
    """Exactitude d'un modèle trivial prédisant toujours la classe majoritaire.

    sert de bareme, un point de comparaison avec notre vrai
    modele entraine
    """
    reference = DummyClassifier(strategy='most_frequent') # utilisation du dummy pour quon ignore les caracteristique
    reference.fit(XTrain, yTrain) # fit = apprentissage /cherche alors la classe majoritaire de ytrain (le strength majoritaire)

    predictions = reference.predict(XTest) # predit la meme classe majoritaire pour chaque ligne de Xtest

    #nb de predictions correctes / nb total de lignes du test
    exactitude = accuracy_score(yTest, predictions)
    return float(exactitude)



def exactitudeNumpy(yReel: pd.Series, yPredit: np.ndarray) -> float:
    """Exactitude calculée de façon vectorisée avec NumPy (sans boucle).

    Sert à vérifier, dans un test, que le calcul coïncide avec celui de
    scikit-learn.
    """
    #conversion yReel(pd series)
    # compare chaque element avec le "=="
    comparaison = np.asarray(yReel) == np.asarray(yPredit)
    return float(np.mean(comparaison))


#TODO: changer la matrice 
def sauvegarderMatriceConfusion(yTest: pd.Series, yPredit: np.ndarray, chemin: str) -> None:

    """Enregistre avec savefig un graphique en barres de la réussite par force.

    Pour chaque vraie force (Faible, Moyen, Fort), la barre donne le
    pourcentage de mots de passe que le modèle a bien classés. La ligne
    pointillée est l'exactitude globale.
    """
    # cm[i][j] = nombre de lignes dont la vraie classe est i et la prédite est j
    cm = confusion_matrix(yTest, yPredit)
    classes = sorted(set(np.asarray(yTest)) | set(np.asarray(yPredit)))
    etiquettes = [ETIQUETTES_FORCE[int(c)] for c in classes]

    # diagonale = bien classés, somme d'une ligne = total de cette vraie force
    totaux = cm.sum(axis=1)
    reussite = np.diag(cm) / np.where(totaux == 0, 1, totaux)
    exactitude = np.trace(cm) / cm.sum()

    fig, ax = plt.subplots()
    barres = ax.bar(etiquettes, reussite, color='#2A52D6')
    ax.bar_label(barres, labels=[f'{v:.0%}' for v in reussite])
    ax.axhline(exactitude, color='gray', linestyle='--',
               label=f'Moyenne globale : {exactitude:.0%}')
    ax.set_ylim(0, 1.1)
    ax.yaxis.set_major_formatter(lambda y, _: f'{y:.0%}')
    ax.set_xlabel('Force réelle du mot de passe')
    ax.set_ylabel('Bien classés')
    ax.set_title('Réussite du modèle par force (ensemble de test)')
    ax.legend()
    fig.savefig(chemin, bbox_inches='tight')
    plt.close(fig)


class Modele:
    """Modèle de classification de la force d'un mot de passe.
    Encapsule un arbre de décision entraîné sur les caractéristiques
    extraites du mot de passe. Attributs protégés : l'arbre, les métriques
    et l'état d'entraînement.
    """

    #profondeur de l'abre 
    def __init__(self, profondeurMax: int = 10, graine: int = graineAleatoire) -> None:
        #random state pour rendre reporductioible les choix aleatoire durant la construction de larbre 
        self._arbre = DecisionTreeClassifier(max_depth=profondeurMax, random_state=graine) # creation de labre de decision pas encore entraine sklearn
        self._metriques: dict = {} # recois les score dans entrainer
        self._reference: float = 0.0 # recois le score du modele bidon
        self._entraine = False # pour savoir si le modele est entrainer 

    
    
    
    # recois les 4 morceaux de separerDonne
    def entrainer(self, XTrain: pd.DataFrame, yTrain: pd.Series, XTest: pd.DataFrame, yTest: pd.Series) -> dict:
        """Entraîne l'arbre puis évalue sur l'ensemble de test uniquement.

        Stocke la référence (classe majoritaire) et renvoie le dictionnaire
        des métriques : exactitude, F1 macro, vérification NumPy, matrice de
        confusion et exactitude de la référence.
        """
        self._arbre.fit(XTrain, yTrain) #apprentissage cherche tout seul des regles
        self._entraine = True 
        self._reference = calculerReference(XTrain, yTrain, XTest, yTest) # calculer le score de reference
        yPredit = self.predireLot(XTest) #prediction su rle test uniquementaz   `q1`
       
       
        self._metriques = {
            'exactitude': float(accuracy_score(yTest, yPredit)), # metrique princinpale
            'f1Macro': float(f1_score(yTest, yPredit, average='macro')), # la moyenne sur les 3 strentgth
            'exactitudeNumpy': exactitudeNumpy(yTest, yPredit), # doit etre identique a exactitude
            'exactitudeReference': self._reference, #score du dummyclassifier
            'matriceConfusion': confusion_matrix(yTest, yPredit).tolist(), # tableau pour lecrire en JSON
        }
        return self.metriques

    def predire(self, longueur: int, contientMajuscule: int, contientChiffre: int, contientSpecial: int) -> tuple[str, dict[str, float]]:
        """Prédit la force d'un mot de passe à partir de ses caractéristiques.

        Renvoie l'étiquette lisible (Faible, Moyen ou Fort) et les
        probabilités de chaque classe (indice de confiance pour l'interface).
        Lève RuntimeError si le modèle n'a pas encore été entraîné.
        """

        ## exception gestion si il ny a pas dentree valide
        if longueur < 1:
            raise EntreeInvalideError(f'La longueur doit être au moins 1 (reçu : {longueur}).')
        for nom, valeur in (('contientMajuscule', contientMajuscule),
                            ('contientChiffre', contientChiffre),
                            ('contientSpecial', contientSpecial)):
            if valeur not in (0, 1):
                raise EntreeInvalideError(f'{nom} doit valoir 0 ou 1 (reçu : {valeur}).')
        #entree de lutilisateur
        entree = pd.DataFrame([[longueur, contientMajuscule, contientChiffre, contientSpecial]],
                              columns=COLONNES_ENTREE)
        
        
        # retroune le tableau numpy
        prediction = int(self.predireLot(entree)[0])
        #retourne le tableaude probabilite
        probabilites = self._arbre.predict_proba(entree)[0]

        #donne lrodre des colonnes dans predict_proba
        classes = [int(c) for c in self._arbre.classes_]



        #retourne un str dettiquette et le dict de probbilite par strenght 
        return ETIQUETTES_FORCE[prediction], {ETIQUETTES_FORCE[c]: float(p) for c, p in zip(classes, probabilites)}

    
    
    
    
    
    
    def sauvegarder(self, df: pd.DataFrame) -> None:
        """Écrit le modèle entraîné (joblib) et les métadonnées (JSON).

        Le JSON contient les noms des colonnes, les valeurs possibles des
        variables catégorielles, l'intervalle de la variable numérique et
        les métriques obtenues : l'interface s'en servira pour se construire.
        Lève RuntimeError si le modèle n'a pas encore été entraîné.
        """
        if not self._entraine:
            raise ModeleNonEntraineError('Le modèle doit être entraîné avant d\'être sauvegardé.')
        os.makedirs(DOSSIER_MODELES, exist_ok=True)
        joblib.dump(self._arbre, cheminModele)
        metadonnees = {
            'modele': f'Arbre de décision (max_depth={self._arbre.max_depth}, random_state={self._arbre.random_state})',
            'colonnesEntree': COLONNES_ENTREE,
            'colonneCible': COLONNE_CIBLE,
            'classesCible': {str(k): v for k, v in ETIQUETTES_FORCE.items()},
            'variables': {
                'longeur': {'type': 'numerique',
                            'min': int(df['longeur'].min()),
                            'max': int(df['longeur'].max())},
                'contientMajuscule': {'type': 'categorielle', 'valeurs': [0, 1]},
                'contientChiffre': {'type': 'categorielle', 'valeurs': [0, 1]},
                'contientSpecial': {'type': 'categorielle', 'valeurs': [0, 1]},
            },
            'metriques': self._metriques,
        }
        with open(cheminMetadonnees, 'w', encoding='utf-8') as f:
            json.dump(metadonnees, f, indent=2, ensure_ascii=False)

    def predireLot(self, X: pd.DataFrame) -> np.ndarray:
      """Prédit la classe de chaque ligne de X."""
      if not self._entraine:
        raise  ModeleNonEntraineError('Le modèle doit être entraîné avant de prédire.')
      return self._arbre.predict(X)


    @property
    def metriques(self) -> dict:
        """Copie du dictionnaire des métriques d'évaluation."""
        return dict(self._metriques)
    
    @property
    def entraine(self) -> bool:
        """Indique si le modèle a été entraîné."""
        return self._entraine
   
    def __str__(self) -> str:
        exactitude = self._metriques.get('exactitude')
        return (f'Modele(arbre de décision, max_depth={self._arbre.max_depth}, '
                f'entraîné={self._entraine}, exactitude={exactitude})')

    

   