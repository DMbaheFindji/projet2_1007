from JeuDeDonnees import JeuDeDonnees
import sys
from PyQt6.QtWidgets import QApplication
from interface import Application


def preparer_donnee()->None:
    
    monJeuDonnee=JeuDeDonnees('..\\..','production.tsv','donnees.csv',limiteLigne=30000)

    cheminCSVFinal=monJeuDonnee.convertirETdevelopper()

    if cheminCSVFinal:
        print(f'Le fichier converti est prêt : {cheminCSVFinal}')

    df=monJeuDonnee.triage_ET_charger_Donnee(cheminCSVFinal)


    #Création du graphique1
    graphique1=monJeuDonnee.creationGraphique1(df)

def main()-> None:
    application=QApplication(sys.argv)
    fenetre = Application()
    fenetre.show()
    sys.exit(application.exec())


#Création de donnees.csv et récupération de son chemin 
if __name__ == "__main__":
    main()