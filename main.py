import pygame
import random
pygame.init()
X = 600
Y = 800
screen = pygame.display.set_mode((X, Y))
pygame.display.set_caption('pendu')
clock = pygame.time.Clock()

font = pygame.font.SysFont ('arial', 30)
text = ""
essai = ""
echecs = 0
with open('mots.txt', 'r') as f:
    mots = [line.strip() for line in f]
mot_a_deviner = random.choice(mots)
image_pendu = pygame.image.load("images\\pendu_0.png")
texte_3 = font.render ("Vous avez gagné !", True, (255,255,255))
texte_4 = font.render ("Vous avez perdu ...", True, (255,255,255))


images_pendu = [pygame.image.load("images\\pendu_0.png"), pygame.image.load("images\\pendu_1.png"), pygame.image.load("images\\pendu_2.png"),
                pygame.image.load("images\\pendu_3.png"), pygame.image.load("images\\pendu_4.png"), pygame.image.load("images\\pendu_5.png"),
                pygame.image.load("images\\pendu_6.png")]



input_active = True
status = True
while (status):
    display_word = ''.join([(x + " " if x in essai else "_ ") for x in mot_a_deviner])
    image_pendu = images_pendu[echecs]
    for event in pygame.event.get():

        clock.tick(30)
 
        if event.type == pygame.QUIT:
            status = False

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
        elif "_ " not in display_word:
            texte_3 = font.render ("Vous avez gagné !", True, (0,0,0))
        texte_5 = font.render (("Lettres essayées : " + essai + " "), True, (0,0,0))
            
        

    texte_1 = font.render ("Entrez une lettre : ", True, (0,0,0))
    texte_2 = font.render (display_word, True,(0,0,0) )
    
    text_surf = font.render(text, True, (255, 0, 0))
    
    screen.fill ((255, 255, 255))
    screen.blit (texte_1, (0,300))
    screen.blit (texte_2, (300,100))
    screen.blit (texte_3, (250,450))
    screen.blit (texte_4, (250,500))
    screen.blit (texte_5, (0,550))
    screen.blit(image_pendu, (0, 0))
    screen.blit (text_surf, (0, 350))
    
    
    
    
    pygame.display.flip()


pygame.quit()