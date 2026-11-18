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

cheminMetadonnees = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "modeles", "metadonnees.json")
cheminMatriceConfusion = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "modeles", "matrice_confusion.png")
cheminGraphique = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "modeles", "graphique_prediction.png")
cheminCSVHistorique=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "historiqueFolder", "historique.csv")


class Application(QMainWindow):
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


        #Un layout vertical de gauche
    
        instruction=QLabel("Veuillez saisir les caractéristiques de votre mot de passe :")
        layoutDeGauche.addWidget(instruction)

       
            
        #AJOUT DE LA LIGNE HORIZONTALE 1
        ligneHorizontale1=QFrame()
        ligneHorizontale1.setFrameShape(QFrame.Shape.HLine)
        layoutDeGauche.addWidget(ligneHorizontale1)
    
        layoutDeGauche.addSpacing(20)



       
        #Gestion des informations provenant du fichier metadonnees
        formulaire=QFormLayout()
        self._champ={}

        for nom in self._metadonnees['colonnesEntree']:
            information=self._metadonnees['variables'][nom]
            if information['type']=='numerique':
                champ=QLineEdit()
                champ.setPlaceholderText(f"Situé entre {information['min']} et {information['max']}")

            else:
                champ=QComboBox()
                champ.addItems(information['valeurs'])
           
            self._champ[nom]=champ
            formulaire.addRow(nom,champ)
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
        
        nouveau=not os.path.isfile(cheminCSVHistorique)
        tempsPresent=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(cheminCSVHistorique,"a",encoding="utf-8",newline="") as f:
            ecrivain=csv.writer(f)

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

        tableau=QTableWidget(len(lignes)-1,len(lignes[0]))
        tableau.setHorizontalHeaderLabels(lignes[0])
        tableau.resizeColumnsToContents()


        for i,l in enumerate(lignes[1:]):
            for j,valeur in enumerate(l):
                tableau.setItem(i,j,QTableWidgetItem(valeur))


        layout.addWidget(tableau)

        fenetre.exec()

      
    def _fairePrediction(self)->None:
        valeurs={}

        try:
            for nom, champ in self._champ.items():
                
                if isinstance(champ,QLineEdit):
                    valeurs[nom]=int(champ.text())

                else:
                    valeurs[nom]=champ.currentText()

            etiquette,probabilite=self.modele.predire(
                valeurs['longueur'],
                valeurs['nbMajuscule'],
                valeurs['nbChiffre'],
                valeurs['nbSpecial'],
                valeurs['premierCaractere'])

        except(EntreeInvalideError,ModeleNonEntraineError) as e:
            self._resultat.setText(str(e))
            return
        except ValueError:
            self._resultat.setText("Veuillez entrer un nombre entier dans chaque champ.")
            return 
        
        confiance=probabilite[etiquette]

        self._resultat.setText(f"Force prédite : {etiquette}\nConfiance du modèle : {confiance:.0%}")
        self._resultat.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._resultat.setWordWrap(True)

        self._afficherGraphique(probabilite)
        self._enregistrerCSV(valeurs,confiance,etiquette)


   
    
