####################################################
#              Importation de modules              #
####################################################
import random
import pptk
import numpy as np
import math as m
from scipy.linalg import svd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import time
from scipy.spatial import Delaunay


# La classe MathHelper est un algorithme de partitionnement de données. Réécriture d'un exercice effectué lors d'un Live Coding.
# Utilisation de @staticmethod pour chacune des méthodes de cette classe
# @author Vincent AZINCOURT
class MathHelper:
    @staticmethod
    def isInSphere(X,Y,Z,R,Px,Py,Pz):
        return (X-Px)**2+(Y-Py)**2+(Z-Pz)**2<=R**2
    
    # @param X coordonnees du centre de la sphere suivant l'axe x
    # @param Y coordonnees du centre de la sphere suivant l'axe y
    # @param Z coordonnees du centre de la sphere suivant l'axe z
    # @param R rayon de la sphere
    # @param N nombre de points
    # @return une renvoie une matrice (Nx3) contenant les coordonnées des points générés
    @staticmethod
    def generateSphere(X,Y,Z,R,N):
        i=N
        L=[]
        while i>0:
            x1 = random.random()*100
            y1 = random.random()*100
            z1 = random.random()*100
            if MathHelper.isInSphere(X,Y,Z,R,x1,y1,z1):
                L.append([x1,y1,z1])
                i-=1
        return L
    
    # @param N nombre de points
    # @return renvoie une matrice (Nx3) contenant les coordonnées des points générés    
    @staticmethod
    def generateSpheres(N):
        Spheres=[]
        for i in range(N):
            x = random.random()*100
            y = random.random()*100
            z = random.random()*100
            R = 5
            Spheres.append(MathHelper.generateSphere(x,y,z,R,100))
        return Spheres
    
    # @param N nombre de spheres
    # @return renvoie une liste de spheres
    @staticmethod
    def generateScene(N):
        return np.row_stack(MathHelper.generateSpheres(N))
        
    # @param P vecteur correspondant aux coordonnes du points P
    # @param Q ecteur correspondant aux coordonnes du points Q
    # @return renvoie la distance euclidienne entre deux points
    @staticmethod
    def euclideanDistance(P, Q):
          return m.sqrt((Q[0]-P[0])**2+(Q[1]-P[1])**2+(Q[2]-P[2])**2)
      
    # @param D matrice de points
    # @param eps la distance pour que les MinPts soient considérés comme un cluster
    # @param MinPts le nombre minimum de points
    # @return renvoie une liste d'ensemble des points du cluster
    @staticmethod        
    def DBSCAN(D : np.ndarray, eps, MinPts):
        Id = 0
        Visited = np.zeros(len(D),dtype=int)
        #on coplete la ListId qu'avec des -2
        ListId = np.ones(len(D), dtype=int) * -2
        D = np.column_stack([D, np.linspace(0,D.shape[0]-1, D.shape[0])])
        for j in range(len(D)):
            if Visited[j]!= 1:
                Visited[j]=1
                PtsVoisins = MathHelper.epsilonVoisinage(D, D[j], eps)
                if len(PtsVoisins)< MinPts:
                    ListId[j]=-1
                else:
                    Id+=1
                    ListId,Visited,PtsVoisins = MathHelper.etendreCluster(D, D[j], PtsVoisins, Id, ListId, Visited, eps, MinPts)
        return ListId
    
    @staticmethod                
    def etendreCluster(D, P, PtsVoisins, C, ListeId, Visited, eps, MinPts):
        j=0
        while j<len(PtsVoisins):
            Pprime = PtsVoisins[j]
            if Visited[int(PtsVoisins[j][3])] == 0:
                Visited[int(PtsVoisins[j][3])]= 1
                PtsVoisinsp = MathHelper.epsilonVoisinage(D, Pprime, eps)
                if len(PtsVoisinsp) >= MinPts:
                    PtsVoisins = np.row_stack([PtsVoisins,PtsVoisinsp])
                    PtsVoisins = np.unique(PtsVoisins, axis=0)
                    j=0
            elif ListeId[int(PtsVoisins[j][3])] < 0:

                ListeId[int(PtsVoisins[j][3])] = int(C)
                    
            j = j+1        
        return ListeId,Visited,PtsVoisins
                
    @staticmethod            
    def epsilonVoisinage(D, P, eps):
        Dp = []
        idx = []
        for i in range(len(D)):
            if MathHelper.euclideanDistance(D[i], P)<=eps:
                Dp.append(D[i])
                idx.append(i)
        return Dp
     
    # @param P vecteur correspondant a n angles eulériens
    # @return renvoie un vecteur a n conposantes       
    @staticmethod   
    def convertirDegres(P):
        return [i*180 /m.pi for i in P]
     
    
    # @param R Matrice de rotation
    # @ return Vérifie si une matrice est une matrice de rotation valide.
    @staticmethod
    def isRotationMatrix(R) :
        Rt = np.transpose(R)
        shouldBeIdentity = np.dot(Rt, R)
        I = np.identity(3, dtype = R.dtype)
        n = np.linalg.norm(I - shouldBeIdentity)
        return n < 1e-6
    
    
    
    # @param R Matrice de rotation
    # @return Calcule la matrice de rotation aux angles d'Euler ( on a choisi X-Y-Z)
    @staticmethod
    def rotationMatrixToEulerAngles(R) :
    
        assert(MathHelper.isRotationMatrix(R))
    
        sy = m.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
    
        singular = sy < 1e-6
    
        if  not singular :
            x = m.atan2(R[2,1] , R[2,2])
            y = m.atan2(-R[2,0], sy)
            z = m.atan2(R[1,0], R[0,0])
        else :
            x = m.atan2(-R[1,2], R[1,1])
            y = m.atan2(-R[2,0], sy)
            z = 0
    
        return np.array([x, y, z])
    
# La classe DelaunayTriangulation est un algorithme pour faire la triangulation/tétraédration de Delaunay en modelisation 3D. 
# Utilisation de @staticmethod pour chacune des méthodes de cette classe
# @author Vincent AZINCOURT
class DelaunayTriangulation:
    
    # @param ax Projection matplotlib
    # @param a Matrice de rotation
    # @param tri Application de delaunay
    # @brief le plot est effectué dans la boucle
    @staticmethod
    def plot_tri(ax, points, tri):
        for tr in tri.simplices:
            pts = points[tr, :]
            ax.plot3D(pts[[0,1],0], pts[[0,1],1], pts[[0,1],2], color='g', lw='0.1')
            ax.plot3D(pts[[0,2],0], pts[[0,2],1], pts[[0,2],2], color='g', lw='0.1')
            ax.plot3D(pts[[0,3],0], pts[[0,3],1], pts[[0,3],2], color='g', lw='0.1')
            ax.plot3D(pts[[1,2],0], pts[[1,2],1], pts[[1,2],2], color='g', lw='0.1')
            ax.plot3D(pts[[1,3],0], pts[[1,3],1], pts[[1,3],2], color='g', lw='0.1')
            ax.plot3D(pts[[2,3],0], pts[[2,3],1], pts[[2,3],2], color='g', lw='0.1')
             
        ax.scatter(points[:,0], points[:,1], points[:,2], color='b')        
        """
        
        for tr in tri.simplices:
            points[tr] = [-3,-3,-3] 
        """
     
    # @param ax Projection matplotlib
    # @param a Matrice de rotation
    # @param tri Application de delaunay
    # @brief Utilise une fonction auxiliaire collect_edges pour prendre chaque bord (edge) une seule fois
    @staticmethod      
    def plot_tri_opti(ax, points, tri):
        edges = DelaunayTriangulation.collect_edges(tri)
        x = np.array([])
        y = np.array([])
        z = np.array([])
        for (i,j) in edges:
            x = np.append(x, [points[i, 0], points[j, 0], np.nan])      
            y = np.append(y, [points[i, 1], points[j, 1], np.nan])      
            z = np.append(z, [points[i, 2], points[j, 2], np.nan])
        ax.plot3D(x, y, z, color='g', lw='0.1')
    
        ax.scatter(points[:,0], points[:,1], points[:,2], color='b')
    
    @staticmethod     
    def collect_edges(tri):
        edges = set()
    
        def sorted_tuple(a,b):
            return (a,b) if a < b else (b,a)
        # Ajouter des arêtes de tétraèdre (triées pour ne pas ajouter une arête deux fois, même si cela vient dans l'ordre inverse).
        for (i0, i1, i2, i3) in tri.simplices:
            edges.add(sorted_tuple(i0,i1))
            edges.add(sorted_tuple(i0,i2))
            edges.add(sorted_tuple(i0,i3))
            edges.add(sorted_tuple(i1,i2))
            edges.add(sorted_tuple(i1,i3))
            edges.add(sorted_tuple(i2,i3))
        return edges

if __name__ == "__main__":
    
    a = MathHelper.generateScene(1)   
    idx = MathHelper.DBSCAN(a, 4, 2)
    suppr = np.where(idx <1) #lorsqu'il n'y a pas de voisin 
    a = np.delete(a,suppr[0],0) #On supprime
    angles = [0]*360

    for i in a:
        # Singular-value decomposition
        U, s, VT = svd([i])
        #conversion en angle d'Euler(deg)
        i = MathHelper.rotationMatrixToEulerAngles(VT)
        i = MathHelper.convertirDegres(i)             
        angles[int(i[0]+180)]+=1 #On ne prend que l'azimuth
    angles = [i/100 for i in angles]
    plt.plot(angles)
    plt.show()
    
    tri = Delaunay(a)

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    t1 = time.time()
    DelaunayTriangulation.plot_tri(ax, a, tri)
    t2 = time.time()
    timer1 = t2-t1
    
    t3 = time.time()
    DelaunayTriangulation.plot_tri_opti(ax,a,tri)
    t4 = time.time()
    timer2 = t4-t3
    
    print(f'Le temps d\'exécution est amélioré d\'un facteur x{int(timer1/timer2)} ({round(timer1,3)} ms contre {round(timer2,3)} ms).')
    
    color_mat = np.zeros((100,3))
    for i in range(int(np.max(a))):
        to_select = np.where(a == i)
        color = pptk.rand(3) 
        color_mat[to_select,:] = color
       
    v = pptk.viewer(a, color_mat)
    v.set(point_size=1)
