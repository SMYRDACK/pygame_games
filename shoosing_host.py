from settings import *
from button import Button
import pygame, time
import subprocess

pygame.init()

host_button = Button(position = (500, 400), size = (200, 100), message = 'HOST GAME', message_color = (255, 255, 255),
                     color= (70,70,70))

join_button = Button(position = (800, 400), size = (200, 100), message = 'JOIN GAME', message_color = (255, 255, 255),
                     color= (70,70,70))

okno_size = (600,200)
okno = pygame.surface.Surface(okno_size)
okno.fill((50,50,50))
pygame.draw.rect(okno, (240,240,240), (0, 0, okno_size[0] - 2, okno_size[1] - 2))
pygame.draw.rect(okno, (170,170,170), (2, 2, okno_size[0] - 4, okno_size[1] - 4))
pygame.draw.rect(okno, (50,50,50), (50, 50, 200 + 2, 100 + 2))
pygame.draw.rect(okno, (50,50,50), (350, 50, 200 + 2, 100 + 2))
pygame.draw.rect(okno, (240,240,240), (48, 48, 200 + 2, 100 + 2))
pygame.draw.rect(okno, (240,240,240), (48 + 300, 48, 200 + 2, 100 + 2))
pygame.draw.rect(okno, (50,50,50), (350, 50, 200 + 2, 100 + 2))
screen.blit(okno,(450,350))
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if host_button.draw_button():
        subprocess.Popen(['python', 'server/server.py'])
        break
    if join_button.draw_button():
        break
    pygame.display.update()
