import pygame
from settings import *
from music import *
from button import Button

pygame.init()

#przyciski
maze_button = Button(position = (100, 100), size = (200, 100), message = 'MAZE DACK', message_color = (255, 255, 255),
                     grafic = pygame.image.load('graphic/better_duck_maze.jpg').subsurface(pygame.Rect(0, 0, 1000, 500)))

clicker_button = Button(position=(400, 100), size = (200, 100), message="DACK *CLICK*", message_color = (0, 0, 255), color=(255,255,255))

lan_button = Button(position=(700, 100), size = (200, 100), message="LAN DACK", message_color = (200, 0, 200), color=(255,255,255), )

parking_button =  Button(position=(1000, 100), size = (200, 100), message="PARKING MASTER", message_color = (0, 0, 255), color=(255,255,255))

#wygląd
background_image = pygame.image.load('graphic/taterki.jpg')
background_image = pygame.transform.scale(background_image,(window_width, window_height))
screen.blit(background_image, (0,0))

running = True
while running:
    play_music()

    if clicker_button.draw_button():
        from clicker.clicker_main import *
    elif maze_button.draw_button():
        from maze_game_main import *
    elif lan_button.draw_button():
        from shooting_game_main import *
    elif parking_button.draw_button():
        from parking_master_main import *

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()