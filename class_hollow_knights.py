import pygame
from math import pi, cos, sin, atan2
from random import randint, uniform
comportement_possible=["gourmand", "gourmand", "gourmand"]
#"déviant" -> il bouge dans tout les sens sans réfléchir
#"gourmand" -> il veut juste manger sans se soucier des monstres, apres avoir mangé 10 fois il gagne une vie même s'il est à 3
# "peureux" -> il fuit le plus possible les monstres

all_img_hk = ["img_hollow_knight/img_hk_1.png",  # toutes les images d'hollow knights
              "img_hollow_knight/img_hk_2.png",
              "img_hollow_knight/img_hk_3.png",
              "img_hollow_knight/img_hk_4.png",
              "img_hollow_knight/img_hk_5.png",
              "img_hollow_knight/img_hk_6.png",
              "img_hollow_knight/img_hk_7.png",
              "img_hollow_knight/img_hk_8.png",
              "img_hollow_knight/img_hk_9.png",
              "img_hollow_knight/img_hk_10.png"
]

#Peut être mettre des valeurs par défaut comme à chaque fois qu'on appelle ça réinitialise avec des valeurs aléatoires
class Hollow_knights:
    def __init__(self, ind_img):
        self.image_name = all_img_hk[ind_img].split("/")[1]
        self.image_originale = pygame.image.load(all_img_hk[ind_img])
        self.image = pygame.image.load(all_img_hk[ind_img])  
        self.small_img = pygame.transform.scale(self.image_originale,(14,15))
        self.vie = 3
        self.faim = randint(5,10) # plus la valeur est faible plus il a faim
        self.vitesse = uniform(1,2) 
        self.vitesse_speed_up = self.vitesse
        self.manger = 0 # combien de fois il a mangé
        self.immunite = 0
        self.rassasier = 0
        self.virus_ignorees = {}  
        self.taille_hauteur=self.image.get_size()[0]
        self.taille_largeur=self.image.get_size()[1]
        size_evolution=(randint(0,2),randint(0,1))
         # si c'est 0 la taille diminuera, si c'est 1 la taille augmentera selon la première valeur du tuple
        if size_evolution[1] ==0:
            self.image=pygame.transform.scale(self.image,(self.taille_hauteur-size_evolution[0],self.taille_largeur-size_evolution[0]))
        else:
            self.image=pygame.transform.scale(self.image,(self.taille_hauteur+size_evolution[0],self.taille_largeur+size_evolution[0]))
        self.comportement = comportement_possible[randint(0,2)]
        self.duree_vie=0
        self.caracteristiques =[self.vie,self.vitesse,self.comportement,(self.taille_hauteur,self.taille_largeur),self.duree_vie]
        self.pos_x=randint(0,1200)
        self.pos_y=randint(0,800)
        self.hitbox=self.image.get_rect(topleft=(self.pos_x,self.pos_y))  
        self.angle=uniform(0,2 * pi) # on initialise un angle en radians
    
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
    
    def deplacement_peureux(self,virus_x,virus_y):
        
        distance_x = self.pos_x - virus_x
        distance_y = self.pos_y - virus_y
        distance = distance_x ** 2 + distance_y ** 2 # formule pour calculer une distance au carré dans un repère
        if distance < 10000 :

            angle = atan2(distance_y, distance_x)  # Calcul de l'angle opposé
            vitesse_x = self.vitesse_speed_up * cos(angle)
            vitesse_y = self.vitesse_speed_up * sin(angle)
            self.pos_x+=vitesse_x
            self.pos_y+=vitesse_y
        
            self.hitbox.topleft=(self.pos_x,self.pos_y)
        else:
            self.deplacement_aleatoire()

        # si l'image sort de l'écran on la fait apparaître de l'autre côté de l'écran
        self.outside_screen()
    
    def deplacement_gourmand(self,food_x,food_y):
        if self.manger >=10:
            self.vie +=1
            self.manger =0
        distance_x = food_x - self.pos_x
        distance_y = food_y - self.pos_y
        distance = distance_x ** 2 + distance_y ** 2 # formule pour calculer une distance au carré dans un repère
        if distance < 10000 :

            angle = atan2(distance_y, distance_x)  # Calcul de l'angle opposé
            vitesse_x = self.vitesse_speed_up * cos(angle)
            vitesse_y = self.vitesse_speed_up * sin(angle)
            self.pos_x+=vitesse_x
            self.pos_y+=vitesse_y
        
            self.hitbox.topleft=(self.pos_x,self.pos_y)
        else:
            self.deplacement_aleatoire()

        # si l'image sort de l'écran on la fait apparaître de l'autre côté de l'écran
        self.outside_screen()
    
    def mutation_aleatoire_caracteristique(self):
        ind_carac=randint(0,3) #quelle caractéristique on modifie
        variation=randint(0,1) #0 -> on diminue, 1 -> on augmente

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
            if self.caracteristiques[1] < 0.5:
                self.caracteristiques[1] = 0.5

        elif ind_carac == 2:           # comportement
            if variation == 0:
                self.caracteristiques[2] = comportement_possible[randint(0, 2)]

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
            f.write("\n" + self.image_name + " Vie actuelle : " + str(self.vie) + " Vie de base : " + str(self.caracteristiques[0]) + " Faim actuelle : " + str(self.faim) +
                    " Vitesse : " + str(self.vitesse) + " Manger : " + str(self.manger) + " Hauteur : " + str(self.taille_hauteur) +
                    " Largeur : " + str(self.taille_largeur) + " Comportement : " + self.comportement + " Duree vie : " + str(self.duree_vie) +
                    " Position X : " + str(self.pos_x) + " Position Y :" + str(self.pos_y) + " Angle : " + str(self.angle))

    # méthode qui permet depuis la save de recréer l'individu
    def recover_save(self, ind_ligne):
        with open("save.txt", "r") as f:
            contenu = f.readlines()
            ligne = contenu[ind_ligne]
            if ligne[0:7] == "img_hk_":
                self.image_name = ligne[0:13].split()[0]
                self.image_originale = pygame.image.load("img_hollow_knight/" + self.image_name)
                self.image = pygame.image.load("img_hollow_knight/" + self.image_name)
                self.small_img = pygame.transform.scale(self.image_originale,(14,15))
                self.vie = int((ligne.split(":")[1]).split()[0])
                self.caracteristiques[0] = int((ligne.split(":")[2]).split()[0])
                self.faim = int((ligne.split(":")[3]).split()[0])
                self.vitesse = float((ligne.split(":")[4]).split()[0])
                self.manger = int((ligne.split(":")[5]).split()[0])
                self.taille_hauteur = int((ligne.split(":")[6]).split()[0])
                self.taille_largeur = int((ligne.split(":")[7]).split()[0])
                self.image=pygame.transform.scale(self.image,(self.taille_hauteur,self.taille_largeur))
                self.comportement = (ligne.split(":")[8]).split()[0]
                self.duree_vie = int((ligne.split(":")[9]).split()[0])
                self.caracteristiques =[self.vie,self.vitesse,self.comportement,(self.taille_hauteur,self.taille_largeur),self.duree_vie]
                self.pos_x = float((ligne.split(":")[10]).split()[0])
                self.pos_y = float((ligne.split(":")[11]).split()[0])
                self.hitbox=self.image.get_rect(topleft=(self.pos_x,self.pos_y))
                self.angle = float((ligne.split(":")[12]).split()[0])
            else:
                print("Fichier corrompu ou sauvegarde inexistante")
                return 
        
        #on renvoie si l'individu est vivant ou mort 
        if (self.vie > 0):
            return True
        else:
            return False

    # méthode pour récupérer le texte à afficher à l'écran
    def show_state(self):
        return  "Vie: " + str(self.vie) + " Faim: " + str(self.faim) + \
                " Vit: " + "{:.2f}".format(self.vitesse) + " H: " + str(self.taille_hauteur) +  \
                " L: " + str(self.taille_largeur) + " C: " + self.comportement +  \
                " X: " + str(round(self.pos_x)) + " Y:" + str(round(self.pos_y)) + " Ang: " + "{:.2f}".format(self.angle) + \
                "Duree vie (s): " + ("?" if(self.caracteristiques[-1] == 0) else str(self.caracteristiques[-1]))
        

    #méthode qui change la vitesse de déplacement de l'individu en fonction de la vitesse de la simulation
    def speed(self, multiplicateur_vitesse):
        self.vitesse_speed_up = self.vitesse * multiplicateur_vitesse
        