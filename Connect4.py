# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 18:14:50 2020

@author: Stéphan
"""
import numpy as np
import time

def Affichage(grid):
    print(" ", end="")
    for k in range(len(grid[0])):
        if k>8: print(k+1,"",  end="")
        else: print(k+1," ",  end="")
        
    print() 
    for i in range(len(grid)):
        print('\x1b[4;37;44m' + "|" + '\x1b[0m', end='')
        for j in range(len(grid[0])):
            if grid[i][j]==0: 
                print('\x1b[4;37;44m' + "  |" + '\x1b[0m', end='')
            elif grid[i][j]==1: 
                print('\x1b[4;31;41m' + " O" + '\x1b[0m', end='')
                print('\x1b[4;37;44m' + "|" + '\x1b[0m', end='')
            elif grid[i][j]==2: 
                print('\x1b[1;33;43m' + " O" + '\x1b[0m', end='')
                print('\x1b[4;37;44m' + "|" + '\x1b[0m', end='')                
        print('')
    print("\n")  
   
def ActionPossible(grid):
    coup_dispo=[]
    for j in range(len(grid[0])):
        if Affect(grid,j)[0]:
            coup_dispo.append(j)
    return coup_dispo   

def Result(grid,colonne,maximizingPlayer,Player):
    new_grid=[]
    for i in range(len(grid)):
        new_grid.append([])
        for j in range(len(grid[0])):
            new_grid[i].append(grid[i][j])
    affectation=Affect(grid, colonne)    
    if Player==1:
        if maximizingPlayer:
            new_grid[affectation[1]][colonne]=1
        else:
            new_grid[affectation[1]][colonne]=2
    if Player==2:
        if maximizingPlayer:
            new_grid[affectation[1]][colonne]=2
        else:
            new_grid[affectation[1]][colonne]=1           
    return new_grid


def NbrPionMax(grid, Ligne, Colonne):
    nbPions = int(1) # nombre de pions alignés
    if grid[Ligne][Colonne] != 0 :
        # Déterminer le plus grand alignement
        #Dans la diagonale descandente
        nbPions = max(nbPions, nbrPionsDir(grid, Ligne, Colonne, 1, 1))
        #A l'horizontale
        nbPions = max(nbPions, nbrPionsDir(grid, Ligne, Colonne, 1, 0))
        #Dans la diagonale ascendante
        nbPions = max(nbPions, nbrPionsDir(grid, Ligne, Colonne, 1,-1))
        #A la verticale 
        nbPions = max(nbPions, nbrPionsDir(grid, Ligne, Colonne, 0, 1))
    return nbPions        
    
def nbrPionsDir(grid, ligne, colonne, directionX, directionY):
    """retourne le plus grand nombre de jetons de la même couleur alignés suivant une direction (le jeton inclu)
     Les directions possibles : (1,1), (1,0), (1,-1) ou (0,1)
     """
    couleur = grid[ligne][colonne] # la couleur de l’alignement
    nbrPions = 1 # le jeton situé en (inLigne, inColonne)
    #Comptabiliser les jetons dans la direction (inDirX,inDirY)
    lig = ligne + directionY # ligne dans la direction +/- inDirY
    col = colonne + directionX # colonne dans la direction +/- inDirX
    while (lig<len(grid) and lig>=0) and (col<len(grid[0]) and col>=0): # boucle finie car bords atteint
        if grid[lig][col] == couleur:
            nbrPions = nbrPions + 1
            lig = lig + directionY
            col = col + directionX
        else: break;
    # On comptabilise les jetons dans la direction opposée
    lig = ligne - directionY
    col = colonne - directionX
    while (lig<len(grid) and lig>=0) and (col<len(grid[0]) and col>=0): # boucle finie car bords atteints
        if grid[lig][col] == couleur:
            nbrPions = nbrPions + 1
            lig = lig - directionY
            col = col - directionX
        else: break;   
    #Affichage-test
    #print("("+str(directionX)+","+str(directionY)+"):", nbPions) 
    return nbrPions

def NbrCombinaisonsGagnantesPossibles(grid, Ligne, Colonne, Joueur):
    combinaisons = 0 # nombre de pions alignés
    # Déterminer le nombre d'alignement possible
    
    #Dans la diagonale descandente en partant du pion
    combinaisons += NbrAlignements(grid, Ligne, Colonne, 1, 1, Joueur, 0, 0)
    #Dans la diagonale descandente en partant du pion juste au dessus
    combinaisons += NbrAlignements(grid, Ligne, Colonne, 1, 1, Joueur, -1, -1)        
    #Dans la diagonale descandente en partant du pion au dessus de 2 rangs
    combinaisons += NbrAlignements(grid, Ligne, Colonne, 1, 1, Joueur, -2, -2)
    #Dans la diagonale descandente en partant du pion au dessus de 3 rangs
    combinaisons += NbrAlignements(grid, Ligne, Colonne, 1, 1, Joueur, -3, -3)
       
    #A l'horizontale vers la droite
    combinaisons += NbrAlignements(grid, Ligne, Colonne, 1, 0, Joueur, 0, 0)        
    #A l'horizontale décalé d'1 rang vers la droite
    combinaisons += NbrAlignements(grid, Ligne, Colonne, 1, 0, Joueur, -1, 0)        
    #A l'horizontale décalé de 2 rangs vers la droite
    combinaisons += NbrAlignements(grid, Ligne, Colonne, 1, 0, Joueur, -2, 0)        
    #A l'horizontale décalé de 3 rangs vers la droite
    combinaisons += NbrAlignements(grid, Ligne, Colonne, 1, 0, Joueur, -3, 0)        
                       
    #Dans la diagonale ascendante
    combinaisons += NbrAlignements(grid, Ligne, Colonne, 1,-1, Joueur, 0, 0)
    #Dans la diagonale ascendante d'1 rang en diagonal vers la droite
    combinaisons += NbrAlignements(grid, Ligne, Colonne, 1,-1, Joueur, -1, 1)
    #Dans la diagonale ascendante
    combinaisons += NbrAlignements(grid, Ligne, Colonne, 1,-1, Joueur, -2, 2)
    #Dans la diagonale ascendante
    combinaisons += NbrAlignements(grid, Ligne, Colonne, 1,-1, Joueur, -3, 3)
                                  
    #A la verticale 
    combinaisons += NbrAlignements(grid, Ligne, Colonne, 0, 1, Joueur, 0, 0)
    #A la verticale 
    combinaisons += NbrAlignements(grid, Ligne, Colonne, 0, 1, Joueur, 0, -1)
    #A la verticale 
    combinaisons += NbrAlignements(grid, Ligne, Colonne, 0, 1, Joueur, 0, -2)
    #A la verticale 
    combinaisons += NbrAlignements(grid, Ligne, Colonne, 0, 1, Joueur, 0, -3)       
    return combinaisons 

def NbrAlignements(grid, ligne, colonne, directionX, directionY, Joueur, initX, initY):
    """retourne le nombre de rangées gagantes possibles jouable à ce moment de la partie pour une case donnée
     Les directions possibles : (1,1), (1,0), (1,-1) ou (0,1)
     """
    couleur = Joueur # 1 ou 2 
    nbrPions = 0 # le jeton situé en (inLigne, inColonne)
    #Comptabiliser les jetons dans la direction (inDirX,inDirY) ou si case vide
    lig = ligne + initY # ligne dans la direction +/- inDirY
    col = colonne + initX # colonne dans la direction +/- inDirX
    while (lig<len(grid) and lig>=0) and (col<len(grid[0]) and col>=0) and nbrPions < 4 : # boucle finie car bords atteint
        if (grid[lig][col] == couleur or grid[lig][col] == 0):
            nbrPions = nbrPions + 1
            lig = lig + directionY
            col = col + directionX
        else: break;
    # On comptabilise les jetons alignés
    if nbrPions == 4: return 1   
    else : return 0
  
def Terminal_Test(grid,inLigne,inColonne):
    if NbrPionMax(grid, inLigne, inColonne)>=4:
        if grid[inLigne][inColonne]==1:
            return True, 1
        if grid[inLigne][inColonne]==2:
            return True, 2
    #Si aucun joueur n'a gagné la partie s'arrête
    if len(ActionPossible(grid))==0:
        return True,0  
    return False,0

def Utility(grid, playerIA, terminal, maximizingPlayer): 
    matricemax = np.zeros((len(grid),len(grid[0])))
    matricemin = np.zeros((len(grid),len(grid[0])))
    somme=0  
    if playerIA==1:
        Joueurmax = 1 
        Joueurmin = 2
        if terminal==2:
            somme -=500  
        if terminal==1:
            somme +=1000  
    if playerIA==2:
        Joueurmax = 2 
        Joueurmin = 1       
        if terminal==1:
            somme -=500  
        if terminal==2:
            somme +=1000             
    for i in range(matricemax.shape[0]):
        for j in range(matricemax.shape[1]):
            matricemax[i][j]=NbrCombinaisonsGagnantesPossibles(grid, i, j, Joueurmax)
            #print(matrice[i][j])
    for i in range(matricemin.shape[0]):
        for j in range(matricemin.shape[1]):
            matricemin[i][j]=NbrCombinaisonsGagnantesPossibles(grid, i, j, Joueurmin)
            #print(matrice[i][j])  
    for i in range(matricemax.shape[0]):
        for j in range(matricemax.shape[1]):
            if grid[i][j]==Joueurmax:
                somme += matricemax[i][j]
            if grid[i][j]==Joueurmin:
                somme -= matricemin[i][j]
    return somme    

#coup est compris entre 1 et 7 et renvoi si oui on non on peut jouer dans cette colonne et à quelle ligne on va jouer.
def Affect(grid, coup):
    retour=(False,0)
    if coup>len(grid[0]) or coup <0:
        return retour
    for i in range(len(grid)):
        if grid[i][coup]==0:
            retour=(True,i)    
    return retour

def LastcoupX(grid, coup):
    for i in range(len(grid)):
        if grid[i][coup]!=0:
           return i 
    return 0

global compt
compt=0
#L'algo minimax avec l'élagage alpha/béta.    
def minimax(grid, depth, maximizingPlayer, coupjoué, alpha=-np.inf, beta=np.inf):
    best_child=[0, -np.inf]  
    global compt
    compt=compt+1
    if depth == 0 or Terminal_Test(grid, LastcoupX(grid,coupjoué), coupjoué)[0]:
        return Utility(grid, Player, Terminal_Test(grid, LastcoupX(grid,coupjoué), coupjoué)[1], maximizingPlayer), best_child
    if maximizingPlayer:
        value=-np.inf
        for child in ActionPossible(grid): 
            temp = minimax(Result(grid,child,maximizingPlayer,Player), depth-1, False, child, alpha, beta)[0]    
            value = max(value, temp)  
            #Elaguage
            if value>=beta:            
                return value, best_child
            alpha=max(alpha, value)
            #C'est ici qu'on stock le premier meilleur chemin
            if best_child[1]<value and depth==profondeur:
                best_child=[child,value]   
            #if depth==profondeur:
                #print(temp,child+1)                                 
    else:
        value=np.inf
        for child in ActionPossible(grid):
            temp2 = minimax(Result(grid,child,maximizingPlayer,Player), depth-1, True, child, alpha, beta)[0]                  
            value = min(value, temp2)  
            #Elaguage
            if value<=alpha:            
                return value, best_child
            beta=min(beta, value)            
    return value, best_child  

def Game():
    """Grille de départ : un 0 pour rien, un 1 pour un rouge, un 2 pour un jaune"""
    grid = np.zeros((6,12))
    """Select the first player : 1 for red team, 2 for yellow team"""
    global Player     
    Player=1    
    IA1=0
    IA2=0
    dernier_coup_joué = (Affect(grid,0)[1],0)
    joueur1 = input("Le joueur 1 est-il une IA ? (oui/non)=>")
    if joueur1 in ["yes","y","Yes","YES","ye","Oui","O","o","ou"]: 
        IA1 = 1 
    joueur2 = input("Le joueur 2 est-il une IA ? (oui/non)=>")
    if joueur2 in ["yes","y","Yes","YES","ye","Oui","O","o","ou"]: 
        IA2 = 2
    #Init the game
    while True:
        #Choose the smartness of the IA (1 : weak and quick to 8 : strong but long)
        global profondeur
        profondeur=3
        global compt
        compt=0
        Affichage(grid)
        # Debut du decompte du temps
        start_time = time.time()
        if Terminal_Test(grid,dernier_coup_joué[0],dernier_coup_joué[1])[0]==True:
            break;
        else:
            print("C'est au tour du joueur %i:" % Player)
            #Pour que les IA s'affrontent ==>
            if IA1 == Player or IA2 == Player: 
                print('Calcul du prochain coup...')
                toto=minimax(grid, profondeur, True, dernier_coup_joué[1])
                #On affiche le nombre de fois que le minimax s'est rappelé récursivement
                choice = toto[1][0]
                print(toto)
                affectation=Affect(grid, choice)
                print("Le minimax s'est relancé %i fois récursivement" %compt)
            else :
                choice=int(input())-1
                affectation=Affect(grid, choice)           
                while affectation[0]==False:
                    print("Case déjà jouée, veuillez en saisir une autre :")
                    Affichage(grid)
                    choice=int(input())-1
                    affectation=Affect(grid, choice)   
            #affect the chosen state
            grid[affectation[1]][choice]=Player
            #Tour suivant
            if Player==2: Player=1
            elif Player==1: Player=2
        # Affichage du temps d execution
        print("Temps d'execution : %f secondes." % (time.time() - start_time))
        dernier_coup_joué=(affectation[1],choice)
    if Terminal_Test(grid,dernier_coup_joué[0],dernier_coup_joué[1])[0]:
        if Terminal_Test(grid,dernier_coup_joué[0],dernier_coup_joué[1])[1]==1:
            print("Joueur 1 a gagné !")
        if Terminal_Test(grid,dernier_coup_joué[0],dernier_coup_joué[1])[1]==2:
            print("Joueur 2 a gagné !")
        if Terminal_Test(grid,dernier_coup_joué[0],dernier_coup_joué[1])[1]==0:
            print("Tie !")   
Game()
