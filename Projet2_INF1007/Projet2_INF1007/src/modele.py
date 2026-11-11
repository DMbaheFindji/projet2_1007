"""\
    modele (volet 2 de l'enonce): separation/test, entrainement, evaluation, comparaison a une reference triviale et sauvegarde (JSON ET joblib)
    
    classification de la force des mdp grace a ses caracteristiques extraites (transformerDATAcsv)
    
    
    """


import json
import os

import joblib # enregistrer le modele entrainer sur le disque
import numpy as np # 
from sklearn.ensemble import RandomForestClassifier # modele pour apprendre a classer moyen/fort/faible
from sklearn.metrics import accuracy_score, confusion_matrix # exactitude de la reference triviale et ou le modele se trompe
from sklearn. model_selection import train_test_split # couper les donne 

from exception import ModeleIntrouvableError # si on charge un fichier inexistant

COLONNES_ENTREE = [
    "longueur",
    "contientMajuscule",
    "contientChiffre",
    "contientSpecial",
]

COLONNE_CIBLE = "strength"



CHEMIN_MODELE = os.path.join("modeles", "modele.joblib")
CHEMIN_METADONNEES = os.path.join("modeles", "metadonnees.json")



class Modele:

    """classifieur de la force des mdp
    
    Attributes: 

    a ecrire
    
    
    """

def __init___(self) ->None:
  """construit modele non entraine"""
  self._classifieur = RandomForestClassifier(random_state=GRAINE_ALEATOIRE)
  self.exactitude_test: float = 0.0
  self.exactitude_reference: float = 0.0
  self.matrice_confusion: list[list[int]] = []


#separer les donnees
def separer(self, X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Sépare les données en entraînement (80 %) et test (20 %).

        Args:
            X: les caractéristiques d'entrée, une ligne par mot de passe.
            y: les étiquettes de force associées.

        Returns:
            Le quadruplet (X_train, X_test, y_train, y_test), reproductible
            grâce à une graine aléatoire fixée.
        """

        #X_train = 80% des mdp
        #y_train la force de ces mdp
        #X_test = 20% des mdp
        #y_test = la force de ces mdp
        return train_test_split(X, y, test_size=0.2, random_state=GRAINE_ALEATOIRE)

