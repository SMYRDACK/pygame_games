import pygame

p1 = pygame.math.Vector2(0,0)
p2 = pygame.math.Vector2(3, 4)

wektor_kierunkowy = p2 - p1
print(wektor_kierunkowy.length())