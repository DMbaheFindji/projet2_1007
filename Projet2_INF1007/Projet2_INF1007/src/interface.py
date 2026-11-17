import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,QLineEdit,QHBoxLayout,QFrame

class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
            self.setWindowTitle("Évaluateur de robustesse de Mots de Passe")
            self.resize(900, 600)
            
    # Widget central de la fenêtre
            widget_central = QWidget()
            self.setCentralWidget(widget_central)

            layout_principal = QHBoxLayout(widget_central)

            # ==================== COLONNE DE GAUCHE ====================
            widget_gauche = QWidget()
            layout_gauche = QVBoxLayout(widget_gauche)

            # Titre
            self.label_instruction = QLabel('<b>Testez votre mot de passe</b>')
            layout_gauche.addWidget(self.label_instruction)

            # Ligne horizontale pour la saisie  texte + Bouton "Prédire" côte à côte)
            layout_saisie = QHBoxLayout()
            
            self.input_password = QLineEdit()
            self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
            self.input_password.setPlaceholderText("Entrez votre mot de passe...")
            layout_saisie.addWidget(self.input_password)

            self.btn_predire = QPushButton("Prédire")
            self.btn_predire.clicked.connect(self.executer_prediction)
            layout_saisie.addWidget(self.btn_predire)

            # On ajoute la ligne de saisie au layout de gauche
            layout_gauche.addLayout(layout_saisie)

            # Zone de résultat (qui apparaîtra sous le bouton quand on clique)
            self.label_resultat = QLabel("")
            layout_gauche.addWidget(self.label_resultat)

            # Pousse tout vers le haut pour garder un beau design
            layout_gauche.addStretch()

            # On ajoute la colonne de gauche au layout principal
            layout_principal.addWidget(widget_gauche, stretch=1)

            # ==================== SÉPARATEUR VERTICAL ====================
            ligne_separation = QFrame()
            ligne_separation.setFrameShape(QFrame.Shape.VLine)
            ligne_separation.setFrameShadow(QFrame.Shadow.Sunken)
            layout_principal.addWidget(ligne_separation)

            # ==================== COLONNE DE DROITE (Graphique) ====================
            widget_droite = QWidget()
            layout_droite = QVBoxLayout(widget_droite)

            # Espace réservé pour le graphique Matplotlib (pour l'instant, un simple label)
            self.label_graphique_placeholder = QLabel("Le graphique apparaîtra ici")
            self.label_graphique_placeholder.setStyleSheet("color: gray; font-style: italic;")
            layout_droite.addWidget(self.label_graphique_placeholder)

            # On ajoute la colonne de droite au layout principal
            layout_principal.addWidget(widget_droite, stretch=1)

    def executer_prediction(self):
            # Action lors du clic sur le bouton "Prédire"
            password = self.input_password.text()
            
            if not password:
                self.label_resultat.setText("<font color='red'>Veuillez entrer un mot de passe !</font>")
                return

            # Simulation du résultat (ici vous brancherez votre modèle plus tard)
            self.label_resultat.setText(f"<b>Résultat :</b> Mot de passe analysé avec succès !")