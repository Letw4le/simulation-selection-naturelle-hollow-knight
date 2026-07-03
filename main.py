from class_hollow_knights import Hollow_knights
from class_virus_jaune import virus_jaune
from class_virus_bleu import Bleu
from random import randint, uniform
from math import pi
import pygame
import threading
from game_time import Horloge
from class_btn_img import Button_img
from menu import Button


#settings de base
pygame.init()
screen = pygame.display.set_mode((1200,800))
font=pygame.font.SysFont("timesnewroman", 20)
title_font = pygame.font.SysFont("timesnewroman", 80)
carac_font = pygame.font.SysFont("timesnewroman", 11)
state = {
    "running": False,
    "menu": True,
    "nb_gen": 0,
    "speed": 1,
}

Horloge = Horloge()
saved = False


#Initialisation des especes
liste_virus_bleu_alive=[Bleu(i) for i in range (10) ]
liste_virus_bleu_dead=[]
liste_hollow_knight_alive=[Hollow_knights(i) for i in range(10)]
liste_hollow_knight_dead=[]
liste_virus_jaune=[virus_jaune(i) for i in range(15)]


# Démarrage de la fonction qui incrémente le temps
lock = threading.Lock()
temps_thread = threading.Thread(target=Horloge.temps_jeu, args =(lock,state))
temps_thread.start()



# fonction qui permet de trier selon la durée de vie
def temps_vie(liste): 
    return int(liste[-1])


#fonction qui gère la sauvegarde dasn un fichier texte
def global_save():
    with open("save.txt", "w") as f:
        f.write("Saved=True\n" +
        "Generation :" + str(state["nb_gen"]) + "\n" +
        "Time :" + str(Horloge.get_actual_time()) + "\n")

    for individu in liste_hollow_knight_alive + liste_hollow_knight_dead:
        individu.save()

    for individu in liste_virus_bleu_alive + liste_virus_bleu_dead:
        individu.save()

    for individu in liste_virus_jaune:
        individu.save()

#bouton de sauvegarde 
Save_btn = Button_img(1155,5,"save_img.png", 0.075,170, screen, global_save)



#fonction qui permet de gérer la vitesse de la simulation
def global_speed(speed):
    state["speed"] = speed
    
    for individu in liste_hollow_knight_alive:
        individu.speed(speed)

    for individu in liste_virus_bleu_alive:
        individu.speed(speed)

    for individu in liste_virus_jaune:
        individu.speed(speed)
    
#bouton x2
speed_up_btn = Button_img(1070, -7, "X2_button.png", 0.35, 170, screen, global_speed)

#fonction qui permet de faire une nouvelle génération de l'espece hollow knight
#elle regarde celui qui a survécu le plus longtemps et mélange la moitié de ses caracteristiques 
#pris au hasard à chaque fois pour la mélanger avec la moitié des caractéristiques de chaque individu 
def nouvelle_generation_hollow_knight(liste_hollow_knight): 
    liste_carac=[]
    new_gen=[]
    for individu in liste_hollow_knight:
        liste_carac.append(individu.caracteristiques)
    liste_carac=sorted(liste_carac, reverse=True, key=temps_vie) # on trie la liste dans l'ordre décroissant selon leur durée de vie
    new_gen.append(liste_carac[0])
    for i in range(1,10):
        best=[None, None, None, None, 0]
        cpt = 0
        while cpt < 2:
            n=randint(0,3)
            if best[n] == None:
                best[n] = liste_carac[0][n] # on stocke la stat
                cpt +=1

        while cpt < 4:
            n=randint(0,3)
            if best[n] == None:
                best[n] = liste_carac[i][n]
                cpt +=1

        new_gen.append(best)

    i=0
    for individu in liste_hollow_knight:
        # changements caractéristiques
        individu.caracteristiques[0] = new_gen[i][0]  # vie
        individu.caracteristiques[1] = new_gen[i][1]  # vitesse
        individu.caracteristiques[2] = new_gen[i][2]  # comportement
        individu.caracteristiques[3] = new_gen[i][3]  # taille
        individu.image = pygame.transform.scale(individu.image_originale, individu.caracteristiques[3])
        individu.caracteristiques[4] = 0              # duree_vie remise à 0

        # reset des données
        individu.duree_vie=0
        individu.faim = randint(5,10)
        individu.manger = 0
        individu.virus_ignorees = {}
        individu.pos_x=randint(100,1100)
        individu.pos_y=randint(100,700)
        individu.angle=uniform(0,2 * pi)
        individu.mutation_aleatoire_caracteristique()
        individu.speed(state["speed"])

        individu.hitbox=individu.image.get_rect(topleft=(individu.pos_x,individu.pos_y))
        i+=1

    return liste_hollow_knight

def nouvelle_generation_virus_bleu(liste_virus_bleu): 
    liste_carac=[]
    new_gen=[]
    for individu in liste_virus_bleu:
        liste_carac.append(individu.caracteristiques)
    liste_carac=sorted(liste_carac, reverse=True, key=temps_vie) # on trie la liste selon leur durée de vie
    new_gen.append(liste_carac[0])
    for i in range(1,10):
        best=[None, None, None, None, 0]  
        cpt =0
        while cpt < 2:
            n=randint(0,3)
            if best[n] == None:
                best[n] = liste_carac[0][n] # on stocke la stat et son indice       
                cpt +=1        

        while cpt < 4:
            n=randint(0,3)
            if best[n] == None: 
                best[n] = liste_carac[i][n]
                cpt +=1 

        new_gen.append(best)

    i=0
    for individu in liste_virus_bleu:
        #changements caractéristiques
        individu.caracteristiques[0] = new_gen[i][0]  # vie 
        individu.caracteristiques[1] = new_gen[i][1]  # vitesse
        individu.caracteristiques[2] = new_gen[i][2]  # comportement
        individu.caracteristiques[3] = new_gen[i][3]  # taille
        individu.image = pygame.transform.scale(individu.image_originale, individu.caracteristiques[3])
        individu.caracteristiques[4] = 0              # duree_vie remise à 0

        #reset des données
        individu.duree_vie=0
        individu.pos_x=randint(100,1100)
        individu.pos_y=randint(100,700)
        individu.angle=uniform(0,2 * pi)
        individu.mutation_aleatoire_caracteristique() 
        individu.speed(state["speed"])

        individu.hitbox=individu.image.get_rect(topleft=(individu.pos_x,individu.pos_y))
        i+=1

    return liste_virus_bleu


# variable pour gérer la faim (tranche de 20 secondes)
derniere_tranche_faim = Horloge.get_actual_time() // 20

#variable pour savoir quand incrémenter la vitesse des virus jaunes
derniere_minute_vitesse = Horloge.min


#boutons pour le menu et leurs fonctions
def start_simulation():
    state["running"] = True
    state["menu"]= False

def quit():
    Horloge.en_cours = False 
    state["menu"]= False

def reload_save():
    with open("save.txt", "r") as f:
        contenu = f.readlines()
        state["nb_gen"] = int(contenu[1].split(":")[1])
        Horloge.recover_time(int(contenu[2].split(":")[1]))

    ind_ligne = 4
    for individu in liste_hollow_knight_alive + liste_hollow_knight_dead:
        alive = individu.recover_save(ind_ligne) # fonction qui recrée l'individu et renvoie s'il est vivant ou non
        if (alive == False):
            liste_hollow_knight_dead.append(individu)
            liste_hollow_knight_alive.remove(individu)
        ind_ligne +=1

    for individu in liste_virus_bleu_alive + liste_virus_bleu_dead:
        alive = individu.recover_save(ind_ligne) # fonction qui recrée l'individu et renvoie s'il est vivant ou non
        if (alive == False):
            liste_virus_bleu_dead.append(individu)
            liste_virus_bleu_alive.remove(individu)
        ind_ligne +=1

    for individu in liste_virus_jaune:
        individu.recover_save(ind_ligne)
        ind_ligne +=1

    state["running"] = True
    state["menu"]= False
    

first_button_y = 300
button_gap = 80

#on regarde s'il y a une save
try:
    with open("save.txt", "r") as f:
        contenu = f.readlines()
    
    if contenu and contenu[0].strip() == "Saved=True":
        saved = True
        btn_reload_save = Button(0, first_button_y, "Continue", screen, reload_save, centrer=True)
        btn_start = Button(0, first_button_y + button_gap, "Restart", screen, start_simulation, centrer=True)
        btn_quit = Button(0, first_button_y + button_gap*2, "Quit", screen, quit, centrer=True)
    else:
        btn_start = Button(0, first_button_y, "Start", screen, start_simulation, centrer=True)
        btn_quit = Button(0, first_button_y + button_gap, "Quit", screen, quit, centrer=True)

except FileNotFoundError:
    # Le fichier n'existe pas
    btn_start = Button(0, first_button_y, "Start", screen, start_simulation, centrer=True)
    btn_quit = Button(0, first_button_y + button_gap, "Quit", screen, quit, centrer=True)

        
#titre menu
text_title = "Simulation Hollow Knight"
surface_title = title_font.render(text_title, True, (255, 255, 255))
x = screen.get_width() // 2 - surface_title.get_width() // 2
y = 60



while state["menu"]:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Horloge.en_cours = False 
            state["menu"]= False
    screen.blit(surface_title, (x, y) )
    
    if (saved):
        btn_reload_save.draw()
    btn_start.draw()
    btn_quit.draw()
    



    pygame.display.flip() 
    pygame.time.delay(60)



while state["running"]:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Horloge.en_cours = False 
            state["running"] = False
            
        

    screen.fill((0,0,0)) # fond noir

    a_supprimer = []

    # boucle qui parcourt la liste des hollow knights encore en vie
    for individu in liste_hollow_knight_alive:   
        for virus in liste_virus_jaune:
            if individu.hitbox.colliderect(virus.hitbox): #si il rencontre un ennemi il perd 1 de vie s'il en a encore sinon il meurt 
                if individu.immunite == 0:
                    if individu.vie > 1:
                        individu.vie -=1
                    else:
                        individu.caracteristiques[-1] = Horloge.get_actual_time()
                        if individu not in a_supprimer:
                            a_supprimer.append(individu)
                    individu.immunite = 10
                    
            
        for virus in liste_virus_bleu_alive:
            if individu.hitbox.colliderect(virus.hitbox): #si il rencontre un virus bleu sa faim augmente de 2 et son compteur d'individu manger augmente
                if individu.rassasier == 0:
                    individu.faim += 2
                    individu.manger += 1
                    individu.rassasier = 30
                    individu.virus_ignorees[id(virus)] = Horloge.get_actual_time() + 30

                    
        if individu.comportement == "deviant":
            individu.deplacement_aleatoire()

        elif individu.comportement == "peureux": 
            menace = None
            distance_min = float('inf')
            for virus in liste_virus_jaune:
                d2 = (individu.pos_x - virus.pos_x)**2 + (individu.pos_y - virus.pos_y)**2
                if d2 < distance_min:
                    distance_min = d2
                    menace = virus
            if menace is not None:
                individu.deplacement_peureux(menace.pos_x, menace.pos_y)
            else:
                individu.deplacement_aleatoire()

        elif individu.comportement == "gourmand":
                food = None
                distance_min = float('inf')
                temps_actuel = Horloge.get_actual_time()
                for f in liste_virus_bleu_alive:
                    if individu.virus_ignorees.get(id(f), 0) > temps_actuel:
                        continue
                    d2 = (individu.pos_x - f.pos_x)**2 + (individu.pos_y - f.pos_y)**2
                    if d2 < distance_min:
                        distance_min = d2
                        food = f
                if food is not None:
                    individu.deplacement_gourmand(food.pos_x, food.pos_y)
                else:
                    individu.deplacement_aleatoire()
        else:
            individu.deplacement_aleatoire()
        
              

        if individu.vie > 0:
            screen.blit(individu.image, (individu.pos_x, individu.pos_y)) 
        if(individu.immunite > 0):
            individu.immunite -= state["speed"]

        if(individu.rassasier > 0):
            individu.rassasier -= state["speed"]


    #gérer la faim de chaque hollow knight
    if Horloge.get_actual_time() // 20 != derniere_tranche_faim:
        derniere_tranche_faim = Horloge.get_actual_time() // 20
        
        for individu in liste_hollow_knight_alive:
            if individu.faim > 1:
                individu.faim -= 1
            else:
                individu.caracteristiques[-1] = Horloge.get_actual_time()
                if individu not in a_supprimer:
                    a_supprimer.append(individu)

    for individu in a_supprimer:
        if individu in liste_hollow_knight_alive:
            individu.dead()
            liste_hollow_knight_dead.append(individu)
            liste_hollow_knight_alive.remove(individu)
    a_supprimer=[]

    # boucle qui parcourt la liste des virus jaunes
    for individu in liste_virus_jaune:
        individu.deplacement_aleatoire()   
        screen.blit(individu.image,(individu.pos_x,individu.pos_y))

    #incrémenter la vitesse des virus jaunes toutes les minues
    if Horloge.min != derniere_minute_vitesse:
        derniere_minute_vitesse = Horloge.min
        
        for individu in liste_virus_jaune:
            individu.vitesse += 0.2


    # boucle qui parcourt la liste des virus bleu encore en vie
    for individu in liste_virus_bleu_alive:
        if individu.comportement=="normal":
            individu.deplacement_aleatoire()
        else:  # peureux : fuit la menace la plus proche
            menace = None
            distance_min = float('inf')
            for m in liste_virus_jaune + liste_hollow_knight_alive:
                d2 = (individu.pos_x - m.pos_x)**2 + (individu.pos_y - m.pos_y)**2
                if d2 < distance_min:
                    distance_min = d2
                    menace = m
            if menace is not None:
                individu.deplacement_peureux(menace.pos_x, menace.pos_y)
            else:
                individu.deplacement_aleatoire()

        for virus in liste_virus_jaune:
            if individu.hitbox.colliderect(virus.hitbox): 
                if individu.immunite == 0:
                    if individu.vie > 1:
                        individu.vie -=1
                    else:
                        individu.caracteristiques[-1] = Horloge.get_actual_time()
                        if individu not in a_supprimer:
                            a_supprimer.append(individu)
                    individu.immunite = 10
                
        for espece in liste_hollow_knight_alive:
            if individu.hitbox.colliderect(espece.hitbox): 
                if individu.immunite == 0:
                    if individu.vie >1:
                        individu.vie -=1
                    else:
                        individu.caracteristiques[-1] = Horloge.get_actual_time()
                        if individu not in a_supprimer:
                            a_supprimer.append(individu)
                    individu.immunite = 10
                

        if individu.vie > 0:
            screen.blit(individu.image, (individu.pos_x, individu.pos_y))
        if(individu.immunite > 0):
            individu.immunite -= state["speed"]

    for individu in a_supprimer:
        if individu in liste_virus_bleu_alive:
            individu.dead()
            liste_virus_bleu_dead.append(individu)
            liste_virus_bleu_alive.remove(individu)


    # affichage de la génération et du temps
    generation=font.render("Generation : " + str(state["nb_gen"]),1,(255,255,255))
    time=font.render("Time : " + Horloge.time_str(),1,(255,255,255))
    screen.blit(generation,(0,0))
    screen.blit(time,(150,0))
    
    #affichage de l'état des hollow knights
    decalage = 25
    for individu in liste_hollow_knight_alive + liste_hollow_knight_dead:
        screen.blit(individu.small_img, (0,decalage-2))
        screen.blit(carac_font.render(individu.show_state(), 1, (255,255,255)), (20,decalage))
        decalage += 20
        

    
    # vérification de l'état des espèces
    if len(liste_virus_bleu_alive)<=1:
        liste_virus_bleu_dead.extend(liste_virus_bleu_alive)
        liste_virus_bleu_alive = nouvelle_generation_virus_bleu(liste_virus_bleu_dead)
        liste_virus_bleu_dead = []

    elif len(liste_hollow_knight_alive)==0:
        #reset de la génération
        liste_hollow_knight_alive = nouvelle_generation_hollow_knight(liste_hollow_knight_dead)
        liste_hollow_knight_dead = [] 

        liste_virus_bleu_dead.extend(liste_virus_bleu_alive)
        liste_virus_bleu_alive = nouvelle_generation_virus_bleu(liste_virus_bleu_dead)
        liste_virus_bleu_dead = [] 

        liste_virus_jaune=[virus_jaune(i) for i in range (15)]
        state["nb_gen"] +=1
        global_speed(state["speed"])
        Horloge.reset_time()

        for individu in liste_hollow_knight_alive:
            individu.save()
    
    speed_up_btn.draw_X2()
    Save_btn.draw_btn()

    pygame.display.flip() #met à jout l'affichage
    pygame.time.delay(60)  #délai de 60 millisecondes donc environ 16 frames par secondes
   
    
pygame.quit()
Horloge.en_cours = False # on arrete le temps


