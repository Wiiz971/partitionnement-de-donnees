####################################################
#              Importation de modules              #
####################################################
import random
import pptk
import numpy as np
import math as m
from scipy.linalg import svd
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
            x1 = random.random()
            y1 = random.random()
            z1 = random.random()
            if MathHelper.isInSphere(X,Y,Z,R,x1,y1,z1):
                L.append([x1,y1,z1])
                i-=1
        return L
    
    # @param N nombre de sphere
    # @param NbrePts nombre de points
    # @return renvoie une matrice (Nx3) contenant les coordonnées des points générés    
    @staticmethod
    def generateSpheres(N,NbrePts):
        Spheres=[]
        for i in range(N):
            x = random.random()
            y = random.random()
            z = random.random()
            R = 10
            Spheres.append(MathHelper.generateSphere(x,y,z,R,NbrePts))
        return Spheres
    
    # @param N nombre de spheres
    # @param NbrePts nombre de points
    # @return renvoie une liste de spheres
    @staticmethod
    def generateScene(N,NbrePts):
        return np.row_stack(MathHelper.generateSpheres(N,NbrePts))
    
        
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

if __name__ == "__main__":
    
    Nbre_pts = 1000
    aSphere = MathHelper.generateScene(1,Nbre_pts)   
    idx = MathHelper.DBSCAN(aSphere, 4, 2)
    suppr = np.where(idx <1) #lorsqu'il n'y a pas de voisin 
    aSphere = np.delete(aSphere,suppr[0],0) #On supprime
    angles = [0]*360
    
    for i in aSphere:
        collection = []
        for j in aSphere:
            if MathHelper.euclideanDistance(i, j)<=0.3:
                collection.append(j)
        # Singular-value decomposition
        U, s, VT = svd(collection)
        #conversion en angle d'Euler(deg)
        i = MathHelper.rotationMatrixToEulerAngles(VT)
        i = MathHelper.convertirDegres(i)             
        angles[int(i[0]+180)]+=1 #On ne prend que l'azimuth
    angles = [i/Nbre_pts for i in angles]
    print(angles)
    plt.plot(angles)
    plt.show()
    
    color_mat = np.zeros((Nbre_pts,3))
    for i in range(int(np.max(aSphere))):
        to_select = np.where(aSphere == i)
        color = pptk.rand(3) 
        color_mat[to_select,:] = color
       
    v = pptk.viewer(aSphere, color_mat)
    v.set(point_size=1)
