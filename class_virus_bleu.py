#classe virus bleu
from random import randint, uniform
import pygame
from math import pi, cos, sin, atan2
comportement_possible=["normal", "peureux"]

class Bleu:
    def __init__(self, indice):
        self.duree_vie=0
        self.image_originale = pygame.image.load("bleu.png")  
        self.image = pygame.image.load("bleu.png")
        self.vie = 3
        self.vitesse=uniform(0.6,1.6)
        self.vitesse_speed_up = self.vitesse
        self.comportement=comportement_possible[randint(0,1)]
        self.pos_x=randint(0,1200)
        self.pos_y=randint(0,800)
        self.hitbox=self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.immunite = 0
        self.taille_hauteur=self.image.get_size()[0]
        self.taille_largeur=self.image.get_size()[1]
        evolution=(randint(0,2),randint(0,1))
        if evolution[1] ==0:
            self.image=pygame.transform.scale(self.image,(self.taille_hauteur+evolution[0],self.taille_largeur+evolution[0]))
        else:
            self.image=pygame.transform.scale(self.image,(self.taille_hauteur+evolution[0],self.taille_largeur+evolution[0]))
        self.caracteristiques =[self.vie,self.vitesse,self.comportement,(self.taille_hauteur,self.taille_largeur),self.duree_vie]  
        self.angle=uniform(0,2 * pi)
        self.indice = indice
    
    def outside_screen(self):
        # si l'image sort de l'écran on la fait apparaître de l'autre côté de l'écran
        if self.hitbox.right < 0:
            self.pos_x = 1200
            self.hitbox.topleft = (self.pos_x, self.pos_y)
        elif self.hitbox.left > 1200:
            self.pos_x = 0
            self.hitbox.topleft = (self.pos_x, self.pos_y)
        
        if self.hitbox.bottom < 0:
            self.pos_y = 800
            self.hitbox.topleft = (self.pos_x, self.pos_y)
        elif self.hitbox.top > 800:
            self.pos_y = 0
            self.hitbox.topleft = (self.pos_x, self.pos_y)

    def deplacement_aleatoire(self):
        self.angle += uniform(-0.1, 0.1)  # on ajuste l'angle
        vitesse_x = self.vitesse_speed_up * cos(self.angle)
        vitesse_y = self.vitesse_speed_up * sin(self.angle)
        self.pos_x += vitesse_x # puis on modifie la position
        self.pos_y += vitesse_y
        self.hitbox.topleft=(self.pos_x,self.pos_y)

        # si l'image sort de l'écran on la fait apparaître de l'autre côté de l'écran
        self.outside_screen()

    def deplacement_peureux(self,espece_x,espece_y):
        distance_x = self.pos_x - espece_x
        distance_y = self.pos_y - espece_y
        distance = distance_x ** 2 + distance_y ** 2 # formule pour calculer une distance au carré dans un repère
        if distance < 10000 :
            self.angle = atan2(distance_y, distance_x)  # Calcul de l'angle opposé
            vitesse_x = self.vitesse_speed_up * cos(self.angle)
            vitesse_y = self.vitesse_speed_up * sin(self.angle)
            self.pos_x+=vitesse_x
            self.pos_y+=vitesse_y
        
            self.hitbox.topleft=(self.pos_x,self.pos_y)
        else:
            self.deplacement_aleatoire()

        # si l'image sort de l'écran on la fait apparaître de l'autre côté de l'écran
        self.outside_screen()


    def mutation_aleatoire_caracteristique(self):
        ind_carac=randint(0,3) # quelle caractéristique on modifie
        variation=randint(0,1) # 0 -> on diminue, 1 -> on augmente

        if ind_carac == 0:             # vie
            if variation == 0 and self.caracteristiques[0] > 1:
                self.caracteristiques[0] -= 1
            else:
                self.caracteristiques[0] += 1

        elif ind_carac == 1:           # vitesse
            if variation == 0:
                self.caracteristiques[1] -= uniform(0, 0.3)
            else:
                self.caracteristiques[1] += uniform(0, 0.3)
            if self.caracteristiques[1] < 0.1:
                self.caracteristiques[1] = 0.1

        elif ind_carac == 2:           # comportement
            if variation == 0:
                self.caracteristiques[2] = comportement_possible[randint(0, 1)]

        elif ind_carac == 3:           # taille
            variation_taille = randint(0, 2)
            h, w = self.caracteristiques[3]
            if variation == 0:
                h += variation_taille
                w += variation_taille
            else:
                h = max(1, h - variation_taille)
                w = max(1, w - variation_taille)
            h = max(10, min(h, 60))
            w = max(10, min(w, 60))
            self.caracteristiques[3] = (h, w)
            self.image = pygame.transform.scale(self.image_originale, (h, w))

        # synchronise les attributs de jeu depuis le génome
        self.vie = self.caracteristiques[0]
        self.vitesse = self.caracteristiques[1]
        self.comportement = self.caracteristiques[2]
        self.taille_hauteur = self.caracteristiques[3][0]
        self.taille_largeur = self.caracteristiques[3][1]


    #méthode à appeler à la mort de l'individu
    def dead(self):
        self.vie = 0

    # méthode qui écrit dans un fichier texte les caractéristiques de l'individu pour la sauvegarde
    def save(self):
        with open("save.txt", "a") as f:
            f.write("\n" + "Virus bleu Indice : "+ str(self.indice) + " Vie actuelle : " + str(self.vie) + " Vie de base : " + str(self.caracteristiques[0]) + 
                    " Vitesse : " + str(self.vitesse) + " Hauteur : " + str(self.taille_hauteur) +  
                    " Largeur : " + str(self.taille_largeur) + " Comportement : " + self.comportement + " Duree vie : " + str(self.duree_vie) +
                    " Position X : " + str(self.pos_x) + " Position Y :" + str(self.pos_y) + " Angle : " + str(self.angle))
        
    # méthode qui permet depuis la save de recréer l'individu
    def recover_save(self,ind_ligne):
        with open("save.txt", "r") as f:
            contenu = f.readlines()
            ligne = contenu[ind_ligne]
            if ligne[0:10] == "Virus bleu":
                self.vie = int((ligne.split(":")[2]).split()[0])
                self.caracteristiques[0] = int((ligne.split(":")[3]).split()[0])
                self.vitesse = float((ligne.split(":")[4]).split()[0])
                self.taille_hauteur = int((ligne.split(":")[5]).split()[0])
                self.taille_largeur = int((ligne.split(":")[6]).split()[0])
                self.image=pygame.transform.scale(self.image,(self.taille_hauteur,self.taille_largeur))
                self.comportement = (ligne.split(":")[7]).split()[0]
                self.duree_vie = int((ligne.split(":")[8]).split()[0])
                self.caracteristiques =[self.vie,self.vitesse,self.comportement,(self.taille_hauteur,self.taille_largeur),self.duree_vie]
                self.pos_x = float((ligne.split(":")[9]).split()[0])
                self.pos_y = float((ligne.split(":")[10]).split()[0])
                self.hitbox=self.image.get_rect(topleft=(self.pos_x,self.pos_y))  
                self.angle = float((ligne.split(":")[11]).split()[0])
            else:
                return
            
        #on renvoie si l'individu est vivant ou mort 
        if (self.vie > 0):
            return True
        else:
            return False
        

    #méthode qui change la vitesse de déplacement de l'individu en fonction de la vitesse de la simulation
    def speed(self, multiplicateur_vitesse):
        self.vitesse_speed_up = self.vitesse * multiplicateur_vitesse