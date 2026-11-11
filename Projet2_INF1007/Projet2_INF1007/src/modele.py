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





def calculer_reference(self, y_train: np.ndarray, y_test: np.ndarray) -> float:
        """bareme de comparaison pour le modele 
        la reference ne regarde jamais les caracteristique repere seulement
        la force la plus frequente


        Args:
            y_train: étiquettes d'entraînement - pour trouver la classe majoritaire
            y_test: étiquettes de test - pour mesurer la référence

        Returns:
            L'exactitude de la référence sur l'ensemble de test.
        """

        # trouver la classe majoritaire - ce qui devient la reference triviale
        valeurs, comptes = np.unique(y_train, return_counts=True)
        classe_majoritaire = valeurs[np.argmax(comptes)]
       
       
       # predire la classe pour tout les mdp du test 
        predictions_triviales = np.full_like(y_test, classe_majoritaire)
       
       # mesure son exactitude
        self.exactitude_reference = float(accuracy_score(y_test, predictions_triviales))
        return self.exactitude_reference



@staticmethod 
def exactitude_numpy(predictions: np.ndarray, y_vrai: np.ndarray) -> float:
        """Calcule l'exactitude nous-mêmes avec NumPy (calcul vectorisé, sans boucle).

        exactitude -> proportions des predictions correcte
         verifier si le resultat en utilisant le calcul vectorise est 
         pareille que le resulat avec scikit-learn.


        Args:
            predictions: prédictions du modèle.
            y_vrai: étiquettes réelles.

        Returns:
            La proportion de prédictions correctes.
        """
        #compare element par element dun seul coup
        # donne un tableau true/false (en 0 et 1)
        comparaisons = predictions == y_vrai

        # faire la moyenne 
        moyenne = np.mean(comparaisons)


        return float(moyenne)


  
def predire(self, X: np.ndarray) -> tuple[str, float]:
        """Prédit la force d'un mot de passe décrit par ses caractéristiques.

        methode que linterface appel


        Args:
            X: une seule ligne de caractéristiques.

        Returns:
            La classe prédite (0/1/2) et la confiance du modèle.
        
        """
        
        # demander la classe predite
        #[0] signifie quon prend le premierelement de la reponse
        #car ya quune prediction par mdp
        prediction = self._classifieur.predict(X)[0]


        # demande certitude du modele
        #retourne un tableau de probabilite pour chaque strength 
        probabilites = self._classifieur.predict_proba(X)[0]

        #extrait la porbabilite la plus eleve (faible, moyen, fort)
        confiance = float(np.max(probabilites))

       
        # pour laffichage de la prediction 
        return str(prediction), confiance