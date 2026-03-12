import pygame
from settings import *

class object(pygame.sprite.Sprite):
    def __init__(self, position, type, group):
        super().__init__(group)
        self.type=type
        self.image = 