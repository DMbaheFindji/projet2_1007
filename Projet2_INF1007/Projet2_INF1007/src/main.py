from JeuDeDonnees import JeuDeDonnees
import sys

import pandas as pd
import os

from exception import DonneeInvalideError
from modele import (Modele,chargerModele, cheminMatriceConfusion,
                    sauvegarderMatriceConfusion, separerDonnees, cheminMetadonnees,chargerMetadonnees)


#Les chemins:

DOSSIER_SRC=os.path.dirname(os.path.abspath(__file__))
DOSSIER_PROJET=os.path.dirname(DOSSIER_SRC)
DOSSIER_DONNEES=os.path.join(DOSSIER_PROJET,"donneesFolder")
DOSSIER_MODELE=os.path.join(DOSSIER_PROJET,"modeles")

CHEMIN_TSV=os.path.join(DOSSIER_DONNEES,"production.tsv")
CHEMIN_CSV=os.path.join(DOSSIER_DONNEES,"donnees.csv")
CHEMIN_MODELE=os.path.join(DOSSIER_MODELE,"modele.joblib")






def preparer_donnee()->None:
    
    monJeuDonnee=JeuDeDonnees(DOSSIER_DONNEES,'production.tsv','donnees.csv',limiteLigne=30000)

    cheminCSVFinal=monJeuDonnee.convertirETdevelopper()

    if cheminCSVFinal:
        print(f'Le fichier converti est prêt : {cheminCSVFinal}')

        df=monJeuDonnee.triage_ET_charger_Donnee(cheminCSVFinal)

        #Création du graphique1
        monJeuDonnee.creationGraphique1(df)



def entrainer_et_sauvegarder(df: pd.DataFrame) -> None:

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
    Elle s'exécute une seul fois
    '''
    if not os.path.isfile(CHEMIN_CSV):
        preparer_donnee()
        if not os.path.isfile(CHEMIN_CSV):
            return #Si la preparationd es données a echouée on sort de l methode
    #si la préparationd es données a reussi on execute l'entrainement
    entrainer_et_sauvegarder(pd.read_csv(CHEMIN_CSV))



def ouvrirApplication()-> None:
    
    from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,QLineEdit,QHBoxLayout,QFrame,QFormLayout,QComboBox

    from interface import Application

    modele=chargerModele(Modele,CHEMIN_MODELE)
    metadonnees=chargerMetadonnees()

    # Ouverture de l'interface
    application = QApplication(sys.argv)
    fenetre = Application(modele,metadonnees)
    fenetre.show()
    
    sys.exit(application.exec())
    




def main() -> None:
    #on prépare les données seulement si donnees.csv n'existe pas 
    if not os.path.isfile(CHEMIN_MODELE):
        premierInstallation()

    if os.path.isfile(CHEMIN_MODELE):
        ouvrirApplication()

   
   
    
    

#Création de donnees.csv et récupération de son chemin 
if __name__ == "__main__":
    main()

    