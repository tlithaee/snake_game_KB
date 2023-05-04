import pygame
import button
import easy_game
import medium_game
import hard_game
import sys

def run_game():

    #create display window
    SCREEN_HEIGHT = 500
    SCREEN_WIDTH = 500

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Button Demo')

    BG = pygame.image.load("assets/background-utama.png")

    #load button images
    easy_img = pygame.image.load('assets/easy.png').convert_alpha()
    medium_img = pygame.image.load('assets/medium.png').convert_alpha()
    hard_img = pygame.image.load('assets/hard.png').convert_alpha()
    exit_img = pygame.image.load('assets/exit.png').convert_alpha()

    #create button instances
    easy_button = button.Button(180, 80, easy_img, 0.8)
    medium_button = button.Button(180, 180, medium_img, 0.8)
    hard_button = button.Button(180, 280, hard_img, 0.8)
    exit_button = button.Button(190, 380, exit_img, 0.8)

    #game loop
    run = True
    while run:
        screen.blit(BG, (0, 0))
        if easy_button.draw(screen):
            print('easy')
            easy_game.run_game()
        if medium_button.draw(screen):
            print('medium')
            medium_game.run_game()
        if hard_button.draw(screen):
            print('hard')
            hard_game.run_game()
        if exit_button.draw(screen):
            print('EXIT')
            pygame.quit()
            sys.exit()
        #event handler
        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()

    pygame.quit()
