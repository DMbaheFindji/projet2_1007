import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton

class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mon Application INF1007")
        self.resize(800, 600)

        # 1. Créer un conteneur central et un layout (dispositif d'alignement)
        conteneur = QWidget()
        self.setCentralWidget(conteneur)
        layout = QVBoxLayout()  # Empile les éléments verticalement
        conteneur.setLayout(layout)

        # 2. Ajouter des composants (Widgets)
        self.texte = QLabel("En attente d'une prédiction...")
        bouton = QPushButton("Prédire")

        # 3. Connecter l'action du bouton (Signal -> Slot)
        bouton.clicked.connect(self.action_predire)

        layout.addWidget(self.texte)
        layout.addWidget(bouton)

    def action_predire(self):
        self.texte.setText("Le bouton fonctionne !")

