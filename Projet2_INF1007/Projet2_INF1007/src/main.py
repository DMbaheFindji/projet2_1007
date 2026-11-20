from JeuDeDonnees import JeuDeDonnees
import sys

import pandas as pd
import os

from exception import DonneeInvalideError
from modele import (Modele,chargerModele, cheminMatriceConfusion,
                    sauvegarderMatriceConfusion, separerDonnees, cheminMetadonnees,chargerMetadonnees)

from JeuDeDonnees import JeuDeDonnees, lireCsvValide

#Les chemins des fichiers et dossiers importants utilisés :
DOSSIER_SRC=os.path.dirname(os.path.abspath(__file__))
DOSSIER_PROJET=os.path.dirname(DOSSIER_SRC)
DOSSIER_DONNEES=os.path.join(DOSSIER_PROJET,"donneesFolder")
DOSSIER_MODELE=os.path.join(DOSSIER_PROJET,"modeles")

CHEMIN_TSV=os.path.join(DOSSIER_DONNEES,"production.tsv")
CHEMIN_CSV=os.path.join(DOSSIER_DONNEES,"donnees.csv")
CHEMIN_MODELE=os.path.join(DOSSIER_MODELE,"modele.joblib")





def preparer_donnee()->None:
    """
    Fonction qui gère la création et l'extraction du fichier csv de notre jeu de donne,
    le tableau pandas représentant celui-ci et le graphique 1
    Retourne None
    """

    monJeuDonnee=JeuDeDonnees(DOSSIER_DONNEES,'production.tsv','donnees.csv',limiteLigne=30000)

    cheminCSVFinal=monJeuDonnee.convertirETdevelopper()

    #Seulement si le fichier csv existe on créer le tableau pandas et on génère le graphique 1
    if cheminCSVFinal:
        print(f'Le fichier converti est prêt : {cheminCSVFinal}')

        df=monJeuDonnee.triage_ET_charger_Donnee(cheminCSVFinal)

        #Création du graphique1
        monJeuDonnee.creationGraphique1(df)



def entrainer_et_sauvegarder(df: pd.DataFrame) -> None:
    """
    Fonction qui crée un objet représentant le modèle utilisé lors de l'entraînement de notre jeux de donné,
    affiche les métriques observables du modèle suite à l'enraînement
    et sauvegarde ce modèle entraîner et la matrice de confusion générée par celui-ci
    Retourne None
    """
    modele = Modele()

    metriques = modele.entrainer(df)

    print(modele)
    print(f"Exactitude : {metriques['exactitude']:.3f}")
    print(f"Référence : {metriques['exactitudeReference']:.3f}")
    print(f"F1 macro : {metriques['f1Macro']:.3f}")

    modele.sauvegarder(df)
    modele.sauvegarderGraphique(cheminMatriceConfusion)



def premierInstallation()-> None:
    '''
    Fonction qui prépare les données et entraîne le modèle. 
    Elle s'exécute une seul fois.
    '''
    try:
    #Si le fichier donnees.csv n'existe pas on appèle une seul fois la méthode qui doit le créer
        if not os.path.isfile(CHEMIN_CSV):
            preparer_donnee()

        df=lireCsvValide(CHEMIN_CSV)
    except (FileNotFoundError,DonneeInvalideError) as e:
        print(f'Erreur lors de la préparation des données : {e}')
        return
    #si la préparation des données a reussi on execute l'entrainement
    entrainer_et_sauvegarder(df)



def ouvrirApplication()-> None:
    """
    Fonction qui s'occupe d'ouvrir l'interface et de charger le modele et les metadonnées qui seront passés en argument à la classe Application
    Retourne None
    """
    
    from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,QLineEdit,QHBoxLayout,QFrame,QFormLayout,QComboBox
    application = QApplication(sys.argv)

    from interface import Application

    try:
        #Chargement du modèele et des métadonnees
        modele=chargerModele(Modele,CHEMIN_MODELE)
        metadonnees=chargerMetadonnees()

    except FileNotFoundError as e:
        print(f"Impossible d'ouvrir l'application :{e}")
        return 
   
    # Ouverture de l'interface
    fenetre = Application(modele,metadonnees)
    fenetre.show()
    
    sys.exit(application.exec())
    


def main() -> None:
    """
    Fonction qui gère l'exécution de la méthode qui initialise et créer nos fichiers et notre modèle
    et ouvre l'interface graphique si l'initialisation s'est bien déroulée
    Retourne None
    """

    #on fait la première installation seulement si le fichier donnees.csv n'existe pas 
    if not os.path.isfile(CHEMIN_MODELE):
        premierInstallation()

    #Seulement si le modèle a pu être créer on ouvre l'interface
    if os.path.isfile(CHEMIN_MODELE):
        ouvrirApplication()

   
    
#On exécute tout 
if __name__ == "__main__":
    main()



    