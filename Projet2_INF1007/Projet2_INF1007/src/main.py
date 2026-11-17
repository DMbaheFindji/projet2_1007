from JeuDeDonnees import JeuDeDonnees
import sys
from PyQt6.QtWidgets import QApplication
from interface import Application
import pandas as pd

from exception import DonneeInvalideError
from modele import (Modele, chargerDonnees, cheminMatriceConfusion,
                    sauvegarderMatriceConfusion, separerDonnees, cheminMetadonnees)

def preparer_donnee()->None:
    
    monJeuDonnee=JeuDeDonnees('..\\..','production.tsv','donnees.csv',limiteLigne=30000)

    cheminCSVFinal=monJeuDonnee.convertirETdevelopper()

    if cheminCSVFinal:
        print(f'Le fichier converti est prêt : {cheminCSVFinal}')

    df=monJeuDonnee.triage_ET_charger_Donnee(cheminCSVFinal)
   
    graphique1 = monJeuDonnee.creationGraphique1(df)

    entrainer_et_sauvegarder(df)


    #Création du graphique1
    graphique1=monJeuDonnee.creationGraphique1(df)
def entrainer_et_sauvegarder(df: pd.DataFrame) -> None:

    modele = Modele()

    metriques = modele.entrainer(df)

    print(modele)
    print(f"Exactitude : {metriques['exactitude']:.3f}")
    print(f"Référence : {metriques['exactitudeReference']:.3f}")
    print(f"F1 macro : {metriques['f1Macro']:.3f}")

    modele.sauvegarder(df)
    modele.sauvegarderGraphique(cheminMatriceConfusion)

def main() -> None:

    # Préparation des données et entraînement
    preparer_donnee()

    # Ouverture de l'interface
    application = QApplication(sys.argv)
    fenetre = Application()
    fenetre.show()

    sys.exit(application.exec())

    
    

#Création de donnees.csv et récupération de son chemin 
if __name__ == "__main__":
    main()

    