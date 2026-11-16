from JeuDeDonnees import JeuDeDonnees


#Création de donnees.csv et récupération de son chemin 
if __name__ == "__main__":

    monJeuDonnee=JeuDeDonnees('..\\..','production.tsv','donnees.csv',limiteLigne=30000)

    cheminCSVFinal=monJeuDonnee.convertirETdevelopper()

    if cheminCSVFinal:
        print(f'Le fichier converti est prêt : {cheminCSVFinal}')

    df=monJeuDonnee.triage_ET_charger_Donnee(cheminCSVFinal)


    #Création du graphique1
    graphique1=monJeuDonnee.creationGraphique1(df)