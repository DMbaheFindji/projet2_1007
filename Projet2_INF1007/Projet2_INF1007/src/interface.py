import sys
import json
import os

from matplotlib.figure import Figure

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QLabel, QPushButton, QLineEdit, QHBoxLayout, 
    QFrame, QFormLayout, QComboBox
)

from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from exception import EntreeInvalideError,ModeleNonEntraineError

cheminMetadonnees = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "modeles", "metadonnees.json")
cheminMatriceConfusion = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "modeles", "matrice_confusion.png")


class Application(QMainWindow):
    def __init__(self,modele,metadonnees):
        super().__init__()
        self.modele=modele
        self._metadonnees=metadonnees

        self.setWindowTitle("Robustesse de Mot de Passe")
        self.resize(800,400)



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

        self._resultat=QLabel('')
        layoutDeGauche.addWidget(self._resultat)


        #AJOUT DE LA LIGNE VERTICALE
        ligneMillieu=QFrame()
        ligneMillieu.setFrameShape(QFrame.Shape.VLine)
        principal.addWidget(ligneMillieu)


        # PARTIE DROITE
        droite=QWidget()
        layoutDeDroite=QVBoxLayout(droite)
        
        self._labelGraphique=QLabel(" Le Graphique de Prédiction de la Robustesse du Modèle s'affichera après la prédiction ")
        self._labelGraphique.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutDeDroite.addWidget(self._labelGraphique)




        principal.addWidget(droite)


        #Les couleurs
        self.setStyleSheet("""  
        QMainWindow, QWidget { background-color: #07140d; color: #39ff14; }
        QLineEdit{border: 1px solid #39ff14; padding: 6px;}
        QPushButton{border: 2px solid #39ff14; padding: 8px;}

        """)


    def _afficherGraphique(self)->None:
            pixmapGraphique=QPixmap(cheminMatriceConfusion)

            if pixmapGraphique.isNull():
                self._labelGraphique.setText('Le graphique est intruvable')
                return

            self._labelGraphique.setPixmap(

                pixmapGraphique.scaled(380,380,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
            )


      
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
        self._resultat.setWordWrap(True)

        self._afficherGraphique()


   
    
