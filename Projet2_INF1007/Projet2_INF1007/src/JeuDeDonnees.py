
import csv 
import os
import pandas as pd
import matplotlib.pyplot as plt


class JeuDeDonnees:
    '''
    Classe responsable de:
        -Convertir le fichier tsv trouvé sur kaggle en un fichier csv
        -Extraire des caractéristiques du fichier csv pour en obtenir au moins cinq au total
        -Vérifier que que le fichier csv de donné ne contienne pas de valeurs eronées ou manquantes
        -Générer un graphique représentant le jeu de donné de notre fichier csv
    '''

    def __init__(self,nomDossier:str,nomFichierTSV:str,nomFichierCSV:str,limiteLigne:int=30000):
        self.nomDossier=nomDossier
        self.nomFichierTSV=os.path.join(nomDossier,nomFichierTSV)
        self.nomFichierCSV=os.path.join(nomDossier,nomFichierCSV)
        self.limiteLigne=limiteLigne




    def convertirETdevelopper(self)-> str:
        '''
        Fonction qui transforme le fichier tsv en fichier csv, extrait et ajoute les caractristiques manquantes à notre jeu de donnée
        et génère le fichier csv final

        
        Retourne une chaîne vide si une erreur lors du processus de transformation du fichier tsv en csv est survenue
        '''
        try:
            lignes_converties=[]
            compteur=0

            if not os.path.isfile(self.nomFichierTSV):
                raise FileNotFoundError(f'Ce n\'est pas un fichier valide : {self.nomFichierTSV}')
                        
            with open(self.nomFichierTSV,'r',encoding='utf-8') as entree:

                #On saute l'en-tête du fichier tsv que l'on est en train de lire
                next(entree,None)

                #On fait l'en-tête pour le nouveau fichier csv
                lignes_converties.append('password,longueur,nbMajuscule,nbChiffre,nbSpecial,premierCaractere,strength\n')
               
                #On va ajouter les lignes a modifier dans la liste tant que le nombre de lignes est inferieur à la limite de 30 000
                for ligne in entree:
                    if compteur>=self.limiteLigne:
                        break

                    #On sépare la ligne en deux
                    elements=ligne.strip().split('\t')

                    #On s'assure que la ligne contient au moins deux parties
                    if len(elements)<2:
                        continue

                    #On divise la ligne en deux partie
                    password=elements[0]
                    strength=elements[1]

                    #Extraction des caractéristiques en fonction de caractéristiques observables des mots de passe dans le jeu de donné
                    longueur=len(password)
                    #On parcours le mot et regrade s'il y a des majuscules, chiffres ou carcatères spéciaux
                    nbMajuscule= sum( 1 for c in password if c.isupper())
                    nbChiffre= sum( 1 for c in password if c.isdigit())
                    nbSpeciaux= sum( 1 for c in password if not c.isalnum())

                    f=password[0]
                    premierCaractere= 'lettre' if f.isalpha() else ('chiffre' if f.isdigit() else 'special')
                

                    contenuModifiee=f'{password},{longueur},{nbMajuscule},{nbChiffre},{nbSpeciaux},{premierCaractere},{strength}\n'#C'est ici que les virgules pour le fichier csv sont ajoutées
                    lignes_converties.append(contenuModifiee)
                    compteur+=1

            #On écrit les lignes sélectionnées converties ( lignes_converties) dans le fichier donnees.csv
            with  open(self.nomFichierCSV,'w',newline="",encoding='utf-8') as sortie:
                sortie.writelines(lignes_converties)
                #On écrit ce qu'on vient de lire dans un fichir csv et on sépare les valeurs avec une virgule cette fois


            print(f'Conversion réussie ! {self.nomFichierCSV} générée avce succès !')
            return self.nomFichierCSV

        except Exception as e:
            print(f'Une erreur est survenue:{e}')
            return ""
        


    def triage_ET_charger_Donnee(self,cheminCSV)-> pd.DataFrame:

        """
        Fonction qui vérifie que le fichier csv généré ne contient pas de valeurs aberrantes 
        ou manquantes
        Retourne toujours le tableau pandas df généré par le fichier csv de notre jeu de donnée
        
        """
        
        #On range les infos de donnees.csv dans un tableau virtuel pandas
        df=pd.read_csv(cheminCSV)
        #C'est ce tableau virtuel df(dataframe) que pyhton manipule pour faire le nettoyage du fichier donnees.csv

        print('Aperçu des données:')
        print(df.head())

        #Vérification des types de chaque colonne
        print('Types des colonnes:')
        print(df.dtypes)

        #Vérification si il y a des valeurs manquantes 
        print('Valeurs manquantes:')
        print(df.isna().sum())

        #Vérification mean,max,min,count
        print('Statistiques descriptives:')
        print(df.describe())

        #Vérification s'il y a des doublons
        doublons=df.duplicated().sum()
        print(f'Nombre de lignes doubles:{doublons}')
        #Il y a 0 ligne double

        return df


    
    def creationGraphique1(self,df: pd.DataFrame)->None:
        '''
        Fonction qui gère la création et la sauvegarde du graphique 1
        Utilise pour entré un tableau pandas (df) pour générer ce graphique
        Retourne None
        '''

        #créer figure
        plt.figure(figsize=(8,5))

        df['strength'].value_counts().sort_index().plot(kind='bar',color='red',edgecolor='black')

        #Ajouter le titre et étiqueter les axes
        plt.title('Répartition des classes de force des mots de passes',fontsize=12,fontweight='bold')
        plt.xlabel('Niveau de force ',fontsize=10)
        plt.ylabel('Nombre de mots de passe',fontsize=10)

        #Ajuster la lisibilité du graphique
        plt.xticks(ticks=[0, 1, 2], labels=['0 (Faible)', '1 (Moyen)', '2 (Fort)'], rotation=0)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        #On met des pointillés au niveau des valeurs en y 
        #alpha-->C'est la transparence


        #Enregistrer le fichier image avec savefig()
        plt.savefig('Graphique1.png', bbox_inches='tight', dpi=300)
        print("Graphique d'exploration sauvegardé avec succès !")

        #Libérer la mémoire
        plt.close()