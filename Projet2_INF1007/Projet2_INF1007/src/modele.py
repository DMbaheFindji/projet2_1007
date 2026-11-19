


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

from exception import (EntreeInvalideError,
                        ModeleNonEntraineError)

import functools
import time


DOSSIER_PROJET = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER_MODELES = os.path.join(DOSSIER_PROJET, 'modeles')# la ou on va ecrire le modele entraine
DOSSIER_DONNEES = os.path.join(DOSSIER_PROJET, 'donneesFolder')

cheminFichierCsv = os.path.join(DOSSIER_DONNEES, 'donnees.csv') # chemin complet du CSV dentree 
cheminModele = os.path.join(DOSSIER_MODELES, 'modele.joblib') # le modele entrainee 
cheminMetadonnees = os.path.join(DOSSIER_MODELES, 'metadonnees.json') # 
#cheminGraphiqueExploration = os.path.join(DOSSIER_DONNEES, 'graphique_exploration.png')
cheminMatriceConfusion = os.path.join(DOSSIER_MODELES, 'matrice_confusion.png') # pour le gra[hique 2]

graineAleatoire = 42 # pour que les reultat sois reproductible

COLONNES_NUMERIQUES = ['longueur', 'nbMajuscule', 'nbChiffre', 'nbSpecial'] # variables numeriques
COLONNE_CATEGORIELLE = 'premierCaractere' # variable categorielle (du texte)
VALEURS_PREMIER_CARACTERE = ['lettre', 'chiffre', 'special'] # valeurs permises de premierCaractere
COLONNES_ENTREE = COLONNES_NUMERIQUES + [COLONNE_CATEGORIELLE]
COLONNE_CIBLE = 'strength' # cest le y variable a predire
ETIQUETTES_FORCE = {0: 'Faible', 1: 'Moyen', 2: 'Fort'} # dictionnaire de traduction
COLONNES_REQUISES = ['password'] + COLONNES_ENTREE + [COLONNE_CIBLE]


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

# ajout de encoder pour conevrtir le premier caractere 
def encoderEntrees(X: pd.DataFrame) -> pd.DataFrame:
    """Transforme les 5 caractéristiques en colonnes toutes numériques.

    premierCaractere (lettre, chiffre, special) devient trois colonnes 0/1.
    """
    encode = X[COLONNES_NUMERIQUES].copy()
    for valeur in VALEURS_PREMIER_CARACTERE:
        encode[f'{COLONNE_CATEGORIELLE}_{valeur}'] = (X[COLONNE_CATEGORIELLE] == valeur).astype(int)
    return encode

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



def chronometrer(fonction):
        """
        Cette fonction est un décorateur qui a pour but de chronométrer le temps
        d'exécution de la fonction
        Retourne Temps d'exécution de la fonction
        """
        @functools.wraps(fonction)
        def enveloppe(*args):
            debut=time.time()
            resultat=fonction(*args)
            fin=time.time()
            duree=round(fin-debut,1)
            print("Durée :",duree,"s")
            args[0]._dureeEntrainement=duree
            return resultat
        return enveloppe


class Modele:

    def __init__(self, profondeurMax: int = 10,
                 graine: int = graineAleatoire) -> None:

        self._arbre = DecisionTreeClassifier(
            max_depth=profondeurMax,
            random_state=graine
        )

        self._metriques = {}
        self._entraine = False
        self._yTest = None
        self._yPredit = None
        self._dureeEntrainement=None


 


    @chronometrer
    def entrainer(self, df: pd.DataFrame) -> dict:
        """Sépare les données, entraîne le modèle et calcule les métriques."""

        # Séparation du DataFrame en données d'entraînement et de test
        XTrain, XTest, yTrain, yTest = separerDonnees(df)

        # Entraînement de l'arbre
        self._arbre.fit(encoderEntrees(XTrain), yTrain)
        self._entraine = True

        # Prédictions sur les données de test
        yPredit = self.predireLot(XTest)

        # Conservation des résultats pour la matrice de confusion
        self._yTest = yTest
        self._yPredit = yPredit

        # Calcul des métriques
        self._metriques = {
            'exactitude': float(accuracy_score(yTest, yPredit)),
            'f1Macro': float(f1_score(yTest, yPredit, average='macro')),
            'exactitudeNumpy': exactitudeNumpy(yTest, yPredit),
            'exactitudeReference': calculerReference(
                XTrain, yTrain, XTest, yTest
            ),
            'matriceConfusion': confusion_matrix(
                yTest, yPredit
            ).tolist()
        }

        return self.metriques



    def predireLot(self, X: pd.DataFrame) -> np.ndarray:
        """Prédit la classe de chaque ligne de X."""

        if not self._entraine:
            raise ModeleNonEntraineError(
                'Le modèle doit être entraîné avant de prédire.'
            )

        return self._arbre.predict(encoderEntrees(X))



    def predire(self, longueur: int, nbMajuscule: int,
                nbChiffre: int, nbSpecial: int,
                premierCaractere: str):

        if longueur < 1:
            raise EntreeInvalideError(
                'La longueur doit être au moins 1.'
            )

        for nom, valeur in (
            ('nbMajuscule', nbMajuscule),
            ('nbChiffre', nbChiffre),
            ('nbSpecial', nbSpecial)
        ):
            if valeur < 0:
                raise EntreeInvalideError(
                    f'{nom} ne peut pas être négatif.'
                )

        if nbMajuscule + nbChiffre + nbSpecial > longueur:
            raise EntreeInvalideError(
                'Le total des caractéristiques dépasse la longueur.'
            )

        if premierCaractere not in VALEURS_PREMIER_CARACTERE:
            raise EntreeInvalideError(
                f'premierCaractere doit valoir {VALEURS_PREMIER_CARACTERE}.'
            )

        entree = pd.DataFrame(
            [[longueur, nbMajuscule, nbChiffre,
              nbSpecial, premierCaractere]],
            columns=COLONNES_ENTREE
        )

        prediction = int(self.predireLot(entree)[0])

        probabilites = self._arbre.predict_proba(
            encoderEntrees(entree)
        )[0]

        classes = [int(c) for c in self._arbre.classes_]

        return (
            ETIQUETTES_FORCE[prediction],
            {
                ETIQUETTES_FORCE[c]: float(p)
                for c, p in zip(classes, probabilites)
            }
        )

    def sauvegarder(self, df: pd.DataFrame) -> None:
        """Sauvegarde le modèle et ses métadonnées."""

        if not self._entraine:
            raise ModeleNonEntraineError(
                'Le modèle doit être entraîné avant d’être sauvegardé.'
            )

        os.makedirs(DOSSIER_MODELES, exist_ok=True)

        joblib.dump(self._arbre, cheminModele)

        variables = {}

        for colonne in COLONNES_NUMERIQUES:
            variables[colonne] = {
                'type': 'numerique',
                'min': int(df[colonne].min()),
                'max': int(df[colonne].max())
            }

        variables[COLONNE_CATEGORIELLE] = {
            'type': 'categorielle',
            'valeurs': VALEURS_PREMIER_CARACTERE
        }

        metadonnees = {
            'modele': f'Arbre de décision (max_depth={self._arbre.max_depth}, random_state={self._arbre.random_state})',
            'colonnesEntree': COLONNES_ENTREE,
            'colonneCible': COLONNE_CIBLE,
            'classesCible': {
                str(k): v for k, v in ETIQUETTES_FORCE.items()
            },
            'variables': variables,
            'metriques': self._metriques,
            'dureeEntrainement': self._dureeEntrainement
        }


        with open(cheminMetadonnees, 'w', encoding='utf-8') as f:
            json.dump(metadonnees, f, indent=2, ensure_ascii=False)

    def sauvegarderGraphique(self, chemin: str) -> None:
        """Sauvegarde le graphique de la matrice de confusion."""

        if not self._entraine:
            raise ModeleNonEntraineError(
                'Le modèle doit être entraîné avant de créer le graphique.'
            )

        sauvegarderMatriceConfusion(
            self._yTest, self._yPredit, chemin
        )

    @property
    def metriques(self) -> dict:
        return dict(self._metriques)

    @property
    def dureeEntrainement(self) -> float:
        return self._dureeEntrainement


    @property
    def entraine(self) -> bool:
        return self._entraine

    def __str__(self) -> str:
        exactitude = self._metriques.get('exactitude')

        return (
            f'Modele(arbre de décision, '
            f'max_depth={self._arbre.max_depth}, '
            f'entraîné={self._entraine}, '
            f'exactitude={exactitude})'
        )

def chargerMetadonnees(chemin:str=cheminMetadonnees)-> dict:
    """
    Cette fonction ouvre et lit le fichier metadonnee.json
    """
        
    if not os.path.isfile(chemin):
        raise FileNotFoundError(f'Le fichier métadonné est introuvable : {chemin}')
        

    with open (chemin,"r",encoding="utf-8") as f:
        return json.load(f)#Retourne un dictionnaire 



def chargerModele(cls=Modele,chemin:str=cheminModele)->'Modele':
    """Cette fonction reconstruit le fichier joblib sauvegardé du modèle pour pouvoir reutiliser le modele deja entrainé"
    """
    if not os.path.isfile(chemin):
        raise FileNotFoundError(f'Le modèle est introuvable : {chemin}')

    modele=cls()
    modele._arbre=joblib.load(chemin)
    modele._entraine=True

    metaDonne=chargerMetadonnees()
    modele._metriques=metaDonne['metriques']
    modele._dureeEntrainement=metaDonne.get('dureeEntrainement')
    return modele


