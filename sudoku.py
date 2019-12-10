#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 10:32:32 2018

@author: alex
"""

import os
import random
os.chdir('/home/alex/Documents') #changement de repertoire
path = "./sudoku.txt" # Variable globale qui indique le chemin du fichier .txt
#On definit la classe Sudoku
class sudoku :

    #On cree la grille
    def __init__(self):
        self.colonnes = 9
        self.lignes = 9
        self.grille= [[0]*self.colonnes for _ in range(self.lignes)]
        self.coordonnees_interdites=[]

    def lire_fichier_sudoku(self,fichier,ligne,nb):
        with open(fichier,'r') as fichier1 : #Ouvrir avec with evite de 'bloquer'
                                            # le fichier lors d'un crash
            chiffres = fichier1.read()
        fichier1.close()
        grille_lue=""
        u=0
        while(chiffres[u+(82*nb)]!='\n'): #chaque sudoku present dans le .txt
                        # a 81 caracteres et un \n on a donc 82 carac par ligne
            grille_lue=grille_lue+str(chiffres[u+(82*nb)]) # u va evoluer jusqu'a
                                # retrouver \n qui simbolise la fin du sudoku
            u=u+1
        ligne_a_retourner=""
        # grille_lue contient les chiffres, cependant ils ne sont pas rangés en lignes et colonnes
        for i in range((ligne*9),(ligne+1)*9):
            # On range UNE ligne
            ligne_a_retourner=ligne_a_retourner+grille_lue[i]
        return ligne_a_retourner

    def remplir_sudoku(self,chemin,num) :
        for x in range(9):
            ligne_remplie=self.lire_fichier_sudoku(chemin,x,num)
            # On distribue la ligne en colonnes :
            for i in range(9):
                if(ligne_remplie[i]!='0'):
                    self.coordonnees_interdites.append((x,i))
                self.grille[x][i]=str(ligne_remplie[i])


    def saisir_sudoku(self): #Rentrer une grille de sudoku manuellement
        compteur = 0
        ligne_index=0
        colonne_index=0
        while(compteur != 81): #On rentre la grille dans l'ordre
            print("Vous vous trouvez au",compteur," indice")
            try :
                self.grille[ligne_index][colonne_index]=int(input("Entrez un chiffre: "))
                self.coordonnees_interdites.append((ligne_index,colonne_index))
            except TypeError :
                print("Merci de n'utiliser que des chiffres !")
            except ValueError :
                print("Des chiffres je vous dis !")
            if((self.grille[ligne_index][colonne_index]) >= 10):
                print("Un chiffre est un nombre compris entre 0 et 9 inclus")
            # si pas compris entre 0 et 9 alors pas d'incremenation
            else :
                compteur = compteur + 1
                if(colonne_index==8):
                    ligne_index = ligne_index + 1
                    colonne_index = 0
                else :
                    colonne_index = colonne_index + 1

    def remplir_case_utilisateur(self):
        coordonnees = input("Coordonnées de la case ?(ligne(0 a 8),colonne(0 a 8)) :")
        tab_coordonneees = coordonnees.split(",")
        l1 = int(tab_coordonneees[0])
        c1 = int(tab_coordonneees[1])
        #Il ne faut pas que les coordonnees soient celles d'un chiffre originel

        if(((l1,c1) in self.coordonnees_interdites) == False):
            try :
                self.grille[l1][c1]=input("Valeur de la case ? :")
            except ValueError :
                print("Valeur non acceptee")
        else :
            print("Coordonnees incorrectes !")

    def remplir_utilisateur(self):
        stop = ''
        while((stop!='y')and(stop!='oui')and(stop!='Oui')and(self.est_valide()!=1)):
            self.afficher_sudoku()
            self.remplir_case_utilisateur()
            stop = input("Voulez vous arreter ? :")

    def afficher_sudoku(self):

        print("-------------")
        for l in range(9):
            ligne_actuelle="|" #chaque debut de ligne
            if((l==3)or(l==6)):
                print("-------------")
            for i in range(9):
                ligne_actuelle = ligne_actuelle + self.grille[l][i]
                if((i==2) or (i==5) or (i==8)):
                    ligne_actuelle = ligne_actuelle + "|"
            print(ligne_actuelle)
        print("-------------")


    def valide_ligne(self): #On verifie que toutes les lignes soient valides
        res1 = 1
        for l in range(9):
            ligne_verifier=""
            for c in range(9):
                ligne_verifier=ligne_verifier+self.grille[l][c]
            for x in range(1,10):
                apparition = 0
                for chiffre in ligne_verifier:
                    if (chiffre == str(x)):
                        apparition = apparition + 1
                    if (chiffre == '0'):
                        res1 = 0
                if(apparition>1):
                    res1=0
            return res1
    def valide_colonne(self): #On verifie que toutes les colonnes soient valides
        res2 = 1
        for c in range(9):
            ligne_verifier=""
            for l in range(9):
                ligne_verifier=ligne_verifier+self.grille[l][c]
            for x in range(1,10):
                apparition = 0
                for chiffre in ligne_verifier:
                    if (chiffre == str(x)):
                        apparition = apparition + 1
                    if (chiffre == '0'):
                        res2 = 0
                if(apparition>1):
                    res2=0
        return res2

    def valide_region(self): #On verifie que toues les regions soient valides
        res=1
        for x in range(3):
            for y in range(3):
                region=""
                apparition = 0
                for ln in range(x*3,x*3+3):
                    for cl in range(y*3,y*3+3):
                        region = region + self.grille[ln][cl]
                for chiffre in region:
                    if (chiffre == str(x)):
                        apparition = apparition + 1
                    if (chiffre == '0'):
                        res = 0
                if(apparition>1):
                    res=0
        return res

    def reperer_region(self): #Permet de stocker les regions dans une liste ordonnée
        liste = []
        for x in range(3):
            for y in range(3):
                region=""
                for ln in range(x*3,x*3+3):
                    for cl in range(y*3,y*3+3):
                        region = region + self.grille[ln][cl]
                liste.append(region)
        return liste

    def trouver_region(self,ligne,colonne): #Sert a trouver la region dans laquelle on est
        # Elles sont numerotees de 0 a 8, la region la plus a droite de la ligne 0 est la 3
        # la region la plus a gauche de la ligne 1 est la 4

        if(ligne<=2):
            if(colonne<=2):
                res = 0
            elif(colonne<=5):
                res = 1
            elif(colonne<=8):
                res = 2
        elif(ligne<=5):
            if(colonne<=2):
                res = 3
            elif(colonne<=5):
                res = 4
            elif(colonne<=8):
                res = 5
        elif(ligne<=8):
            if(colonne<=2):
                res = 6
            elif(colonne<=5):
                res = 7
            elif(colonne<=8):
                res = 8
        return res

    def est_valide(self) : # La grille est valide
        total = 0
        total = total + self.valide_ligne()
        total = total + self.valide_colonne()
        total = total + self.valide_region()
        if (total == 3):
            valide = 1
        else :
            valide = 0
        return valide

    def remplir(self): # Methode de resolution d'un sudoku 'simple'
        sudoku_simple=1
        while((self.est_valide()!=1)and(sudoku_simple==1)):
            for x in range(9):
                for y in range(9):
                    if((self.grille[x][y])=='0'): # Si case a remplir
                        chiffres = {'1','2','3','4','5','6','7','8','9'} #Possibilités
                        chiffres = chiffres - self.ChaineVersSet(self.ChaineLigne(x))
                        chiffres = chiffres - self.ChaineVersSet(self.ChaineColonne(y))
                        chiffres = chiffres - self.ChaineVersSet(self.ChaineRegion(x,y))
                        # Si on a une seule possibilité
                        if(len(chiffres)==1):
                            for i in range(1,10):
                                if str(i) in chiffres:
                                    sudoku_simple = 1
                                    self.grille[x][y]=str(i)
                        else :
                            sudoku_simple= 0

        if(sudoku_simple==0):
            print("Ce sudoku n'est pas un sudoku 'simple'")
            return 0


    def nb_absent(self,lin,col,nb): # Voir si le nb peut etre ecrit
        chaine=''
        chaine = chaine + self.ChaineLigne(lin)
        chaine = chaine + self.ChaineColonne(col)
        chaine = chaine + self.ChaineRegion(lin,col)
        if((nb in chaine)==False): # ne doit pas etre dans ligne ni colonne ni region
            return 1

    def remplir_difficile(self,case): # Solution de backtracking : methode brute qui traite toues les possibilités
        if(case==81): # Tout est validé
            return 1
        l = case//9 #division entiere --> voir la ligne correspondante
        c = case%9  # reste de la division entiere --> voir la colonne correspondante
        if (self.grille[l][c]!='0'):
            return self.remplir_difficile(case+1) #Si la case est deja remplie on passe a la suite
        for nb in range(1,10):
            if(self.nb_absent(l,c,str(nb))==1):
                self.grille[l][c]=str(nb)
                if(self.remplir_difficile(case+1)==1): # On explore toutes les possibilités avec ce chiffre
                                                        # On a affaire a une fonction recurrente qui n'arretera pas tant que
                                                        # la grille est possible ou que la solution n'a pas encore ete trouvee
                    return 1
        self.grille[l][c]='0' # Si cette rammification n'a pas abouti, on remet la la case a zero
        return 0

    def ChaineVersSet(self,Chaine): # La conversion d'une chaine vers un set simplifie le traitement
                                    # Avec un set on peut realiser les operations : - , + etc
        Set = set()
        for i in range(len(Chaine)):
            if(Chaine[i]!='0'):
                Set.add(Chaine[i])
        return Set

    def ChaineLigne(self,ligne) :
        ligne_a_retourner=""
        for c in range(9):
            ligne_a_retourner=ligne_a_retourner+self.grille[ligne][c]
        return ligne_a_retourner

    def ChaineColonne(self,colonne) :
        colonne_a_retourner=""
        for l in range(9):
            colonne_a_retourner=colonne_a_retourner+self.grille[l][colonne]
        return colonne_a_retourner

    def ChaineRegion(self,l,c) :
        region_a_retourner =""
        liste_region=self.reperer_region() #On met les regions sous formes de listes dans une liste qui regroupe les regions
        region_a_retourner=liste_region[(self.trouver_region(l,c))] # le chiffre que retourne trouver_region correspond a l'indice de la liste des regions
        return region_a_retourner


# -----------------------------------MAIN------------------------------#
quiter = ''
while ((quiter!='Oui')and(quiter!='oui')and(quiter!='y')):
    jeu = input("Voulez vous jouer au Sudoku ? : ")
    if((jeu == "Oui") or (jeu == "oui")or(jeu=="y")):
        print("Bienvenu au jeu du Sudoku !")
        sudoku1=sudoku()
        choix=input("Voulez vous :    1:Creer votre grille  2:Recuperer une grille dans un fichier : ")
        if(choix=='1'):
            sudoku1.saisir_sudoku()
            Choix_correct=1
        elif(choix=='2'):
            sudoku1.remplir_sudoku(path,random.randint(0,245))
            Choix_correct=1
        else :
            print("Vous ne faites pas le bon choix !")
        if (Choix_correct==1):
            sudoku1.afficher_sudoku()
            choix = input("1 :Resolution Complete  2:Resolution Partielle  3:Resoudre soi-meme : ")
            print("ATTENTION PREND PARFOIS DU TEMPS A RESOUDRE")
            if(choix=='1'): 1920 x 1080
                if(sudoku1.remplir()==0):
                    sudoku1.remplir_difficile(0)
                sudoku1.afficher_sudoku()
            elif(choix=='2'):
                if(sudoku1.remplir()==0):
                    sudoku1.remplir_difficile(0)
                for i in range(12):
                    x=random.randint(0,8)
                    y=random.randint(0,8)
                    if(((x,y) in sudoku1.coordonnees_interdites) == False):
                        sudoku1.grille[x][y]='0'
                sudoku1.remplir_utilisateur()
                print("Voici la solution")
                sudoku1.remplir()
            elif(choix=='3'):
                sudoku1.remplir_utilisateur()
                sudoku1.remplir()
                print("Voici le sudoku rempli")
                sudoku1.afficher_sudoku()

    else :
        print("Dommage")
    quiter=input("Voulez vous quiter ? : ")
