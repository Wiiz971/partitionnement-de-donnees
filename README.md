# Partitionnement de donnees

#### Informations générales :

* [Depôt Github](https://github.com/Wiiz971/partitionnement-de-donnees/)

* Collaborateurs  :
    * [Vincent AZINCOURT](https://github.com/Wiiz971)
    * [Nicolas YAZMAN](https://github.com/jsp)

* Outils utilisés pour le projet :
    * Python 3.6.8
    * Spider version 5.2.2 
    * Documentation comparable à Doxygen
    * Importer le module PPTK ’pip install pptk’ pour visualiser le nuage de points
    
 *******
 
 ####  Tâche 1:
 
* Générer une sphère ✔️
* Générer des points (à une certaine distance) sur la surface de la sphère (DBSCAN) ✔️
* Pour chacun des points, faire une décomposition en valeur singulière (SVD) ✔️
* Faire une matrice 3x3 en angle Eulérien ✔️
* Prendre une des deux composantes du vecteur B (découlant de la matrice 3x3) et convertir en degrés (a × 180/π)
* Incrémenter de 1 pour chaque angle trouvé pour en déduire une densité de probabilité

 ####  Tâche 2:

* Réaliser une triangulation de Delaunay sur l'ensemble des points
* Une fois que les points sont utilisés, remplacer leur valeur par des zones négatives ( ≠ 1)
* Compléter un algorithme permettant de faire plusieurs triangulations de Delaunay en parallèle (afin de réduire l'ordre de complexité de l'algorithme)
* Utiliser un timer entre deux triangulations puis entre chaque itération



