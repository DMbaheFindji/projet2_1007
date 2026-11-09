import pandas as pd
import matplotlib.pyplot as plt


#Charger le fichier csv avec pandas
colonnes=['password','longueur','contientMajuscule','contientChiffre','contientSpecial','strength']

#On range les infos de donnees.csv dans un tableau virtuel
df=pd.read_csv(r'C:\Users\Danielle Findji\Downloads\SimAuditive\projet2_1007\Projet2_INF1007\Projet2_INF1007\donnees\donnees.csv')
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



'''
Analyse:

*À côté de count, c'est écrit 30 000 pour chaque colonne. 
 Donc,cela prouve que tout est complet 

*Les mots de passe ont une longueur minimal de 4 caractères et maximal de 174 caractères.
 La moyenne étant de 35 caractères

*91.5% des mots de passes contiennent une majuscule
 33% des mots de passes contiennent un caractère spécial

*La moyenne de la robustesse des mots de passe est 1.0 (Moyen)

*Il n'y a pas de ligne double

Le jeu de données est donc déjà bien nettoyer.
Donc, il n'y a rien à corriger !
'''


#GRAPHIQUE1:

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
#alpha-->C'est la trasnparence


#Enregistrer le fichier image avec savefig()
plt.savefig('Graphique1.png', bbox_inches='tight', dpi=300)
print("Graphique d'exploration sauvegardé avec succès !")

#Libérer la mémoire
plt.close()