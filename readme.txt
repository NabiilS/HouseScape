Installer Python sur Visual Studio Code

Installer les bibliothèques:
- pip install pandas
- pip install bs4
- pip install selenium
- pip install jupyter 
(Si on obtient un message d'erreur de permission pour l'installation de jupyter, utiliser pip install jupyter --user)
------
Une fois que Jupyter est installé, ajouter jupyter aux variable d'environnement
CTRL X -> Système -> Paramètres avancés du système -> variables d'environnement -> variables sytèmes -> double clique sur PATH
-> Ajouter le fichier de destionation de l'installation de Jupyter,
	- C:\Users\Admin\AppData\Roaming\Python\Python310\Scripts
	- C:\Users\Admin\AppData\Roaming\Python\Python310\site-packages
Ou alors on peut vérifier l'emplacement de l'installation avec pip show jupyter

