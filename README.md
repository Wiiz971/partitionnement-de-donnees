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
    * Importer le module scipy ’pip install scipy' pour faire la décomposition en valeur singulière (SVD)
    * Importer le module matplotlib ’pip install matplotlib' pour visualiser la courbe pour chaque angle trouvé
    
 *******
 
 ####  Tâche 1: [UPDATE]
 
* Générer une sphère ✔️
~~* Générer des points (à une certaine distance) sur la surface de la sphère (DBSCAN) ✔️
~* Pour chacun des points, faire une décomposition en valeur singulière (SVD) ✔️
~* Faire une matrice 3x3 en angle Eulérien ✔️
~* Prendre une des trois composantes du vecteur B (de la matrice 3x3) et convertir en degrés (a × 180/π) ✔️
~* Incrémenter de 1 pour chaque angle trouvé pour en déduire une densité de probabilité ✔️~~

* Pour chaque point du nuage de point, regarder ceux qui sont en dessous d'une certaine distance parmi tous les points de la sphère (distance euclidienne/DBSCAN)
* Si c'est inférieur à un seuil, on les ajoute à un ensemble
* Faire une SVD sur cet ensemble une fois que tous les points ont été traité
* Prendre la matrice V (si c'est Nx3 l'ensemble) et transformer les coordonnées en angles euleriens
* Prendre l'azimuth en radians (premiere coordonnée du vecteur) et * 180 / pi. 
* Round le nombre au plus proche et incrémenter compteur[angle]++

![image](https://user-images.githubusercontent.com/47423231/159677223-7af89ab6-2500-4275-b493-c98f895e737f.png)

![image](https://user-images.githubusercontent.com/47423231/159676851-0812a089-ce65-4766-a8ff-eff113ddbaf4.png)

![image](https://user-images.githubusercontent.com/47423231/159676478-49c213b6-d123-439d-8b91-f114f877eaf5.png)
_suivant l'angle θ_





 ####  Tâche 2:

* Réaliser une triangulation de Delaunay sur l'ensemble des points ✔️
* Une fois que les points sont utilisés, remplacer leur valeur par des zones négatives ( ≠ 1) ✔️
* Compléter un algorithme permettant de faire plusieurs triangulations de Delaunay en parallèle (afin de réduire l'ordre de complexité de l'algorithme)
* Utiliser un timer entre deux triangulations puis entre chaque itération





