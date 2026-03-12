from settings import *
import pygame

class Powerup(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super.__init__(group)
        self.position = position
        self.sheet =