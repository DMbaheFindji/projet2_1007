import sys
import json
import os
import csv
from datetime import datetime

from matplotlib.figure import Figure

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt


from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QLabel, QPushButton, QLineEdit, QHBoxLayout, 
    QFrame, QFormLayout, QComboBox,QTableWidget,QDialog,QTableWidgetItem
)

from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from exception import EntreeInvalideError,ModeleNonEntraineError



#Chemins des dossiers et fichier csv,json et png utilisé
cheminMetadonnees = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "modeles", "metadonnees.json")
cheminMatriceConfusion = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "modeles", "matrice_confusion.png")
cheminGraphique = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "modeles", "graphique_prediction.png")
cheminCSVHistorique=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "historiqueFolder", "historique.csv")

#Dictionnaire pour avoir les bons noms affichés dans l'interface
NOMS_AFFICHES={
    'longueur':'Longueur du mot de passe',
    'nbMajuscule':'Nombre de majuscule',
    'nbChiffre':'Nombre de chiffre',
    'nbSpecial':'Nombre de caractères spéciaux',
    'premierCaractere':'Premier caractère'
}



class Application(QMainWindow):

    '''
    Classe responsable de:
            -Charger le fichier de métadonnées contenant les informations importantes que notre modèle utilise pour sa prédiction du jeu de donnée
            -Afficher les graphiques représentant nos prédictions
            -Enregistrer les prédictions faites par le modèle dans un fichier cs nommé historiquue
    '''

    
    def __init__(self,modele,metadonnees):
        super().__init__()
        self.modele=modele
        self._metadonnees=metadonnees

        self.setWindowTitle("Robustesse de Mot de Passe")
        self.resize(900,500)



        centrale=QWidget()#Création du contenu principal
        self.setCentralWidget(centrale)
        principal=QHBoxLayout(centrale)#Craétion de la zone horizontale


        #PARTIE DE GAUCHE
        gauche=QWidget()
        layoutDeGauche=QVBoxLayout(gauche)
        layoutDeGauche.setContentsMargins(20,30,20,20)
        layoutDeGauche.setSpacing(20)
        principal.addWidget(gauche)
        gauche.setFixedWidth(400)


        #Texte d'instruction
        instruction=QLabel("Veuillez saisir les caractéristiques de votre mot de passe :")
        layoutDeGauche.addWidget(instruction)

       
            
        #AJOUT DE LA LIGNE HORIZONTALE 1
        ligneHorizontale1=QFrame()
        ligneHorizontale1.setFrameShape(QFrame.Shape.HLine)
        layoutDeGauche.addWidget(ligneHorizontale1)
    
        layoutDeGauche.addSpacing(20)


       
        #Gestion des informations provenant du fichier metadonnees
        formulaire=QFormLayout()
        self._champ={}#Création du dictionnaire champ qui est un attribut de la classe Application et qui va associer le nom de la variable à ce que l"utilisateur va entrer

        for nom in self._metadonnees['colonnesEntree']:
            information=self._metadonnees['variables'][nom]
            if information['type']=='numerique':
                champ=QLineEdit()
                champ.setPlaceholderText(f"Situé entre {information['min']} et {information['max']}")

            else:
                champ=QComboBox()
                champ.addItems(information['valeurs'])
           
            self._champ[nom]=champ
            formulaire.addRow(NOMS_AFFICHES.get(nom,nom),champ)
        layoutDeGauche.addLayout(formulaire)


        #AJOUT DE LA LIGNE HORIZONTALE
        ligneHorizontale=QFrame()
        ligneHorizontale.setFrameShape(QFrame.Shape.HLine)
        layoutDeGauche.addWidget(ligneHorizontale)
    

        bouton=QPushButton('Prédire la robustesse du mot de passe')

        #on connecte le bouton a l'action de predire la robustesse du mot de passe
        bouton.clicked.connect(self._fairePrediction)
        layoutDeGauche.addSpacing(45)
        layoutDeGauche.addWidget(bouton)


        #Bouton pour voir l'historique
        boutonHistorique=QPushButton("Voir l'historique")
        boutonHistorique.clicked.connect(self._ouvrirHistorique)
        layoutDeGauche.addWidget(boutonHistorique)
       
       

        #AJOUT DE LA LIGNE VERTICALE
        ligneMillieu=QFrame()
        ligneMillieu.setFrameShape(QFrame.Shape.VLine)
        principal.addWidget(ligneMillieu)


        # PARTIE DROITE
        droite=QWidget()
        layoutDeDroite=QVBoxLayout(droite)
        
        
        self._labelGraphiquePrediction=QLabel()
        self._labelGraphiquePrediction.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutDeDroite.addWidget(self._labelGraphiquePrediction)
        
        
        
        
        self._labelMatriceConfusion=QLabel(" Le Graphique de Prédiction de la Robustesse du Modèle s'affichera après la prédiction ")
        self._labelMatriceConfusion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutDeDroite.addWidget(self._labelMatriceConfusion)

    
        self._resultat=QLabel('')
        layoutDeDroite.addWidget(self._resultat)

        principal.addWidget(droite)


        #Les couleurs
        self.setStyleSheet("""  
        QMainWindow, QWidget { background-color: #07140d; color: #39ff14; }
        QLineEdit{border: 1px solid #39ff14; padding: 6px;}
        QPushButton{border: 2px solid #39ff14; padding: 8px;}

        """)


    def _afficherGraphique(self,probabilite)->None:
            """
            Fonction permettant de générer les deux graphiques représentant les prédictions du modèle
            Retourne None 
            
            """
            noms=['Faible','Moyen','Fort']
            valeurs=[probabilite.get(nom,0)*100 for nom in noms ] 

            plt.figure(figsize=(5,4))
            
            plt.bar(noms,valeurs)
            plt.xlabel('Robustesse du mot de passe')
            plt.ylabel('Probabilité (%)')
            plt.title('Probabilité de chaque force')
            
            plt.ylim(0,100)
            plt.savefig(cheminGraphique,bbox_inches="tight")
            plt.close()


        
          
          
          
          
            pixmapGraphiquePrediction=QPixmap(cheminGraphique)

            pixmapGraphique=QPixmap(cheminMatriceConfusion)


            #On vérifie que les graphique existe bien avant de les charger
            if pixmapGraphique.isNull():
                self._labelMatriceConfusion.setText('Le graphique de la matrice de confusion est introuvable')
                return
            else:

                self._labelMatriceConfusion.setPixmap(

                    pixmapGraphique.scaled(350,350,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
                )



            if pixmapGraphiquePrediction.isNull():
                self._labelGraphiquePrediction.setText('Le graphique de prédiction est introuvable')
                return

            else:

                self._labelGraphiquePrediction.setPixmap(

                    pixmapGraphiquePrediction.scaled(350,350,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
                )



    def _enregistrerCSV(self,valeurs,confiance,etiquette)->None:
        """
        Fonction qui enregistre dans un fichier csv l'historique des prédictions faites par l'utilisateur
        Retourne None
        """
        nouveau=not os.path.isfile(cheminCSVHistorique)
        tempsPresent=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(cheminCSVHistorique,"a",encoding="utf-8",newline="") as f:
            ecrivain=csv.writer(f)

            #Si un nouveau fichier historique vient d'être généré on refait l'en tête
            if nouveau:
                ecrivain.writerow([
                    "dateHeure","longueur","nombre de Majuscule","nombre de Chiffre","nombre de caractères Speciaux","premier Caractere","prediction","confiance"
                ])
            ecrivain.writerow([

                tempsPresent,
                valeurs['longueur'],
                valeurs['nbMajuscule'],
                valeurs['nbChiffre'],
                valeurs['nbSpecial'],
                valeurs['premierCaractere'],
                etiquette,
                round(confiance*100,1)
            ])


    def _ouvrirHistorique(self):
        """
        Fonction qui permet de gérer l'ouverture l'accessibilité par l'utilisateur à l'historique 
        des prédictions du modèle 
        Retourne None
        """

        fenetre=QDialog(self)
        fenetre.setWindowTitle('Historique des prédictions du modèle')
        fenetre.resize(900,400)
        layout=QVBoxLayout(fenetre)

        if not os.path.isfile(cheminCSVHistorique):
            layout.addWidget(QLabel('Aucune prédiction enregistrée pour le moment'))
            fenetre.exec()
            return

        with open(cheminCSVHistorique,"r",encoding="utf-8",newline="") as f:
            lignes=list(csv.reader(f))

          
            entete=lignes[0]
            donneesHist=sorted(lignes[1:],key=lambda ligne:ligne[0],reverse=True)
            #Ici on trie les prédictions de l'historique du plus ancien au plus récent


        tableau=QTableWidget(len(donneesHist),len(entete))
        tableau.setHorizontalHeaderLabels(entete)



        for i,l in enumerate(donneesHist):
            for j,valeur in enumerate(l):
                tableau.setItem(i,j,QTableWidgetItem(valeur))


        tableau.resizeColumnsToContents()

        layout.addWidget(tableau)

        fenetre.exec()

      
    def _fairePrediction(self)->None:
        """
        Fonction qui s'occupe de gérer l'action de prédire la robustesse du mot de passe 
        une fois que l'utilisateur clique sur le bouton prédire
        Retourne None
        """

        valeurs={}

        try:
            for nom, champ in self._champ.items():
                
                if isinstance(champ,QLineEdit):#Si c'est un champ où il faut entrer (saisir) quelque chose 
                   
                   
                    try:
                        valeurs[nom]=int(champ.text())#On change le texte en nombre

                    except ValueError:#Si l'utilisateur n'entre rien ou entre une lettre à la place d'un nombre cela lèvera une erreur
                        raise EntreeInvalideError(f'{NOMS_AFFICHES.get(nom,nom)}: Entrer un nombre entier !')
                else:#Dans le cas ou c'est un choix a sélectionner --> Exemple le premier caractère
                    valeurs[nom]=champ.currentText()

            #On récupère la force du modèle et son niveau de confiance
            etiquette,probabilite=self.modele.predire(
                valeurs['longueur'],
                valeurs['nbMajuscule'],
                valeurs['nbChiffre'],
                valeurs['nbSpecial'],
                valeurs['premierCaractere'])

        except(EntreeInvalideError,ModeleNonEntraineError) as e:
            self._resultat.setText(str(e))
            return
        
        #Stocker le niveau de confiance du modèle dans une variable
        confiance=probabilite[etiquette]

        duree=self.modele.dureeEntrainement
        texteDuree=f"{duree} s" if duree is not None else " non disponible"
        


        self._resultat.setText(f"Le mot de passe est prédit comme : {etiquette}\nLe modèle de prédiction est confiant du modèle à : {confiance:.0%}\n Durée de l'entrainement :{texteDuree} ")
        self._resultat.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._resultat.setWordWrap(True)


      
        
        self._afficherGraphique(probabilite)
        self._enregistrerCSV(valeurs,confiance,etiquette)


   
    
