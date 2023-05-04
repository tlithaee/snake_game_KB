import pygame
import button
import level

#create display window
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Button Demo')

BG = pygame.image.load("assets/background_snake.png")

#load button images
start_img = pygame.image.load('assets/start_1.png').convert_alpha()

#create button instances
start_button = button.Button(180, 270, start_img, 0.8)

#game loop
run = True
while run:
    screen.blit(BG, (0, 0))
    if start_button.draw(screen):
        print('START')
        level.run_game()

    #event handler
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()