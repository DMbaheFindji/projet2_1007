
import csv 

'''
Fichier qui gère la transformation des données tsv en données csv
Puis, qui se rassure de retenir seulement 5000 lignes de data
'''
cheminFichierTsv=r'C:\Users\Danielle Findji\Downloads\SimAuditive\projet2_1007\Projet2_INF1007\Projet2_INF1007\donnees\production.tsv\production.tsv'
cheminFichierCsv=r'C:\Users\Danielle Findji\Downloads\SimAuditive\projet2_1007\Projet2_INF1007\Projet2_INF1007\donnees\donnees.csv'

limiteLignes=30000
try:
    lignes_converties=[]
    compteur=0

    with open(cheminFichierTsv,'r',encoding='utf-8') as entree:

        #On saute l'en-tête
        next(entree,None)

        #On fait l'en-tête
        lignes_converties.append('password,longeur,contientMajuscule,contientChiffre,contientSpecial,strength\n')
        #On va ajouter les lignes a modifier dans la liste tant que le nombre de lignes est inferieur à la limite de 5000
        for ligne in entree:
            if compteur>=limiteLignes:
                 break

            #On sépare la ligne en deux
            elements=ligne.strip().split('\t')

            password=elements[0]
            strength=elements[1]

            #Extraction des caractéristiques--> Je l'ai crée moi-même:
            longueur=len(password)
            #On parcours le mot et regrade s'il y a des majuscules
            contientMajuscule=1 if any(c.isupper() for c in password) else 0
            contientChiffre=1 if any(c.isdigit() for c in password) else 0
            contientSpecial=1 if any(not c.isalnum() for c in password) else 0
           

            contenuModifiee=f'{password},{longueur},{contientMajuscule},{contientChiffre},{contientSpecial},{strength}\n'
            lignes_converties.append(contenuModifiee)
            compteur+=1

    #on écrit les lignes sélectionnées converties dans le fichier donnees.csv
    with  open(cheminFichierCsv,'w',newline="",encoding='utf-8') as sortie:
        sortie.writelines(lignes_converties)
         #On écrit ce qu'on vient de lire dans un fichir csv et on sépare les valeurs avec une virgule cette fois



    print(f'Conversion réussie ! {cheminFichierCsv} générée avce succès !')

except Exception as e:
    print(f'Une erreur est survenue:{e}')

'''
C'est un projet de classification.
La varible strength est la variable cible elle est discrète.
Nous devons prdire la force du mot de passe : Faible,Moyen,Fort


Il y a bel  et bien des variables numériques (ex.longueur)
et des variables catégorielle (ex. contientmajuscule, contientChiffre, contientSpecial)
'''
