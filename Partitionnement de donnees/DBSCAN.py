
####################################################
#              Importation de modules              #
####################################################
import random
import pptk
import numpy as np
import math


class MathHelper:
    @staticmethod
    def isInSphere(X,Y,Z,R,Px,Py,Pz):
        return (X-Px)**2+(Y-Py)**2+(Z-Pz)**2<=R**2
          
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
    
    @staticmethod
    def generateScene(N):
        return np.row_stack(MathHelper.generateSpheres(N))
        
    @staticmethod
    def euclideanDistance(P, Q):
          return math.sqrt((Q[0]-P[0])**2+(Q[1]-P[1])**2+(Q[2]-P[2])**2)
      
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
                
                
"""
DBSCAN(D, eps, MinPts)
   C = 0
   pour chaque point P non visité des données D
      marquer P comme visité
      PtsVoisins = epsilonVoisinage(D, P, eps)
      si tailleDe(PtsVoisins) < MinPts
         marquer P comme BRUIT
      sinon
         C++
         etendreCluster(D, P, PtsVoisins, C, eps, MinPts)
          
etendreCluster(D, P, PtsVoisins, C, eps, MinPts)
   ajouter P au cluster C
   pour chaque point P' de PtsVoisins 
      si P' n'a pas été visité
         marquer P' comme visité
         PtsVoisins' = epsilonVoisinage(D, P', eps)
         si tailleDe(PtsVoisins') >= MinPts
            PtsVoisins = PtsVoisins U PtsVoisins'
      si P' n'est membre d'aucun cluster
         ajouter P' au cluster C
          
epsilonVoisinage(D, P, eps)
   retourner tous les points de D qui sont à une distance inférieure à epsilon de P
"""


        
    
if __name__ == "__main__":
    
    a = MathHelper.generateScene(3)

    idx = MathHelper.DBSCAN(a, 5, 4)
    color_mat = np.zeros((300,3))
    for i in range(int(np.max(idx))):
        to_select = np.where(idx == i)
        color = pptk.rand(3) 
        color_mat[to_select,:] = color
       
    v = pptk.viewer(a, color_mat)
    v.set(point_size=1)
