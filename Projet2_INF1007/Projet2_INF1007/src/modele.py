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



def sauvegarder(self, chemin_modele: str = CHEMIN_MODELE,chemin_metadonnees: str = CHEMIN_METADONNEES) -> None:
        """Enregistre le modèle (joblib) et ses métadonnées (JSON).

        L'interface se construira à partir du JSON : le modèle n'est
        jamais ré-entraîné au lancement de l'application.

        Args:
            chemin_modele: chemin du fichier .joblib à écrire.
            chemin_metadonnees: chemin du fichier .json à écrire.

        Raises:
            ModeleIntrouvableError: si le modèle n'a jamais été entraîné.
        """
        if not hasattr(self._classifieur, "classes_"):
            raise ModeleIntrouvableError(
                "Impossible de sauvegarder : le modèle n'est pas encore entraîné."
            )
        os.makedirs(os.path.dirname(chemin_modele), exist_ok=True)
        joblib.dump(self._classifieur, chemin_modele)

        metadonnees = {
            "colonnes": COLONNES_ENTREE,
            "numeriques": {c: [0, 0] for c in COLONNES_ENTREE},  # bornes à remplir
            "categorielles": {},
            "classes": [str(c) for c in self._classifieur.classes_],
            "metrique": {
                "exactitude": self.exactitude_test,
                "reference": self.exactitude_reference,
            },
        }
        with open(chemin_metadonnees, "w", encoding="utf-8") as sortie:
            json.dump(metadonnees, sortie, ensure_ascii=False, indent=4)

@classmethod
def charger(cls, chemin_modele: str = CHEMIN_MODELE) -> "Modele":
        """Charge un modèle sauvegardé (utilisé par l'interface).

        Args:
            chemin_modele: chemin du fichier .joblib.

        Returns:
            Une instance de Modele prête à prédire.

        Raises:
            ModeleIntrouvableError: si le fichier .joblib n'existe pas.
        """
        if not os.path.exists(chemin_modele):
            raise ModeleIntrouvableError(f"Modèle introuvable : {chemin_modele}")
        modele = cls()
        modele._classifieur = joblib.load(chemin_modele)
        return modele

   # pour POO
def __str__(self) -> str:
        """Représentation lisible du modèle, pour le README et les messages."""
        return (
            f"Modele RandomForest — exactitude test : {self.exactitude_test:.2%}, "
            f"référence : {self.exactitude_reference:.2%}"
        )