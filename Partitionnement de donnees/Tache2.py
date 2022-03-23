####################################################
#              Importation de modules              #
####################################################
import random
import pptk
import numpy as np
import math as m
from scipy.linalg import svd
import sys
import matplotlib.pyplot as plt



# La classe MathHelper est un algorithme de partitionnement de données DBSCAN. Réécriture d'un exercice effectué lors d'un Live Coding.
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
      
    
    @staticmethod        
    def DBSCAN(D : np.ndarray, eps, MinPts):
        Id = 0
        Visited = np.zeros(len(D),dtype=int)
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
            
if __name__ == "__main__":
    
    a = MathHelper.generateScene(1)
    angles = [0 for i in range (360)]
    for i in a:
        # Singular-value decomposition
        U, s, VT = svd([i])
        
        tol = sys.float_info.epsilon * 10
        
        if abs(VT.item(0,0))< tol and abs(VT.item(1,0)) < tol:
           eul1 = 0
           eul2 = m.atan2(-VT.item(2,0), VT.item(0,0))
           eul3 = m.atan2(-VT.item(1,2), VT.item(1,1))
        else:
           eul1 = m.atan2(VT.item(1,0),VT.item(0,0))
           sp = m.sin(eul1)
           cp = m.cos(eul1)
           eul2 = m.atan2(-VT.item(2,0),cp*VT.item(0,0)+sp*VT.item(1,0))
           eul3 = m.atan2(sp*VT.item(0,2)-cp*VT.item(1,2),cp*VT.item(1,1)-sp*VT.item(0,1))
        eul1Deg,eul2Deg,eul3Deg = MathHelper.convertirDegres([eul1,eul2,eul3])      
        
        #On ne prend que la composante suivant theta (2)
        angles[int(eul2Deg+180)]+=1

    plt.plot(angles)
    plt.show()
    
    #Scipy Delaunay est à N dimensions de la triangulation, donc si vous donnez des points 3D il renvoie les objets 3D. Donner 2D des points et il renvoie à des objets 2D.

    idx = MathHelper.DBSCAN(a, 5, 4)
    color_mat = np.zeros((100,3))
    for i in range(int(np.max(idx))):
        to_select = np.where(idx == i)
        color = pptk.rand(3) 
        color_mat[to_select,:] = color
       
    v = pptk.viewer(a, color_mat)
    v.set(point_size=1)
    
