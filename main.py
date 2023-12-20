import pygame
import pygame_menu
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
X = 800
Y = 800

# Création de la fenêtre
screen = pygame.display.set_mode((X, Y))
pygame.display.set_caption('pendu')
clock = pygame.time.Clock()

# Paramètres de police
font = pygame.font.SysFont('arial', 30)

# Variables globales
text = ""
essai = ""
echecs = 0
difficultee = ""
pseudo = ""
scores = 0
mots = []
mot_a_ajouter = ''
image_pendu = pygame.image.load("images\\pendu_0.png")
texte_3 = font.render("Vous avez gagné !", True, (255, 255, 255))
texte_4 = font.render("Vous avez perdu ...", True, (255, 255, 255))

# Chargement des images du pendu
images_pendu = [pygame.image.load("images\\pendu_0.png"), pygame.image.load("images\\pendu_1.png"),
                pygame.image.load("images\\pendu_2.png"), pygame.image.load("images\\pendu_3.png"),
                pygame.image.load("images\\pendu_4.png"), pygame.image.load("images\\pendu_5.png"),
                pygame.image.load("images\\pendu_6.png")]

# Fonction principale du menu
def menu():
    global difficultee 
    global mot_a_ajouter
    global pseudo_input
    
    # Création d'un menu avec Pygame Menu
    menu = pygame_menu.Menu('Bienvenue', 800, 800, theme=pygame_menu.themes.THEME_DEFAULT)
    pseudo_input = menu.add.text_input('Pseudo :', default="")
    difficultee = menu.add.selector('Difficultée :', [('Facile', 1), ('Normale', 2), ('Difficile', 3)])
    mot_a_ajouter = menu.add.text_input('Entrez un mot à ajouter : ')
    menu.add.button('Tableau des scores', scoreboard)
    menu.add.button('Jouer', jeu)
    menu.add.button('Quitter', pygame_menu.events.EXIT)

    # Lancement du menu
    menu.mainloop(screen)

# Ajouter un mot à la liste des mots
def ajouter_mot():
    check = True
    mot_ajoute = mot_a_ajouter.get_value()
    with open("mots.txt", "a+") as f:
        f.seek(0)
        lignes = f.readlines()
        for ligne in lignes:            
            if mot_ajoute == ligne.strip():
                check = False
        if mot_ajoute != "" and check == True:            
            f.write("\n")
            f.write(mot_ajoute)

# Changer la difficulté en fonction du choix dans le menu
def changer_difficultee():
    global mots
    global difficultee_selectionnee
    difficultee_selectionnee = difficultee.get_value()[0]

    if difficultee_selectionnee == ('Facile',1):
        with open('mots.txt', 'r') as f:
            for line in f:
                elements = line.strip()
                if len(elements) < 6:
                    mots.append(elements)

    elif difficultee_selectionnee == ('Normale',2):
        with open('mots.txt', 'r') as f:
            for line in f:
                elements = line.strip()
                if 6 < len(elements) < 10:
                    mots.append(elements)

    elif difficultee_selectionnee == ('Difficile',3):
        with open('mots.txt', 'r') as f:
            for line in f:
                elements = line.strip()
                if len(elements) >= 10:
                    mots.append(elements)

# Enregistrer le score dans un fichier
def fonction_score():
    pseudo = pseudo_input.get_value()

    if difficultee_selectionnee == ('Facile',1):
        with open('scores.txt', 'a+') as f:
            print (pseudo, ": ", scores + 1, file=f)
    elif difficultee_selectionnee == ('Normale',2):
        with open('scores.txt', 'a+') as f:
            print (pseudo, ": ", scores + 2, file=f)
    elif difficultee_selectionnee == ('Difficile',3):
        with open('scores.txt', 'a+') as f:
            print (pseudo, ": ", scores + 3, file=f)
        
# Afficher le tableau des scores
def scoreboard():
    status = True
    while (status):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = False
        with open('scores.txt', 'r') as f:
            scores = f.read().splitlines()
            scores = str(scores)
            texte_score = font.render (scores, True, (0,0,0))
        screen.fill((255,255,255))
        screen.blit (texte_score, (0, 50))
        pygame.display.flip()

# Fonction principale du jeu
def jeu():
    global essai
    global echecs
    global text
    global mots
    global scores


    ajouter_mot()
    changer_difficultee()
    texte_3 = font.render("Vous avez gagné !", True, (255,255,255))
    texte_4 = font.render("Vous avez perdu ...", True, (255,255,255))

    mot_a_deviner = random.choice(mots)
    image_pendu = pygame.image.load("images\\pendu_0.png")
    input_active = True
    status = True
    while (status):


        display_word = ''.join([(x + " " if x in essai else "_ ") for x in mot_a_deviner])
        image_pendu = images_pendu[echecs]
        for event in pygame.event.get():

    
            if event.type == pygame.QUIT:
                status = False
                mots = []

            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    if len(text) == 1:
                        if text not in essai:
                            essai += text
                            if text not in mot_a_deviner:
                                if echecs < 6:
                                    echecs += 1
                        else:
                            print("Lettre déjà devinée. Veuillez entrer une nouvelle lettre.")
                    else:
                        print("Veuillez rentrer une seule lettre en minuscule")
                    text = ""
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
            if echecs == 6:
                texte_4 = font.render("Vous avez perdu ...", True, (0, 0, 0))
                essai = ""
                echecs = 0
                display_word = mot_a_deviner
                
            elif "_ " not in display_word:
                texte_3 = font.render("Vous avez gagné !", True, (0,0,0))
                essai = ""
                echecs = 0
                fonction_score()

        texte_1 = font.render("Entrez une lettre : ", True, (0,0,0))
        texte_2 = font.render(display_word, True,(0,0,0) )
        texte_5 = font.render(("Lettres essayées : " + essai + " "), True, (0,0,0))        
        text_surf = font.render(text, True, (255, 0, 0))
        
        screen.fill((255, 255, 255))
        screen.blit(texte_1, (50,150))
        screen.blit(texte_2, (350,50))
        screen.blit(texte_3, (250,500))
        screen.blit(texte_4, (250,550))
        screen.blit(texte_5, (50,600))
        screen.blit(image_pendu, (300, 300))
        screen.blit(text_surf, (50, 650))
        
        pygame.display.flip()

# Lancement du menu
menu()
print(scores)

# Fermeture de Pygame
pygame.quit()
