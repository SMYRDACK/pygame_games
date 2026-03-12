import pygame
from settings import *

class Walls(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)

        self.position = position
        self.image = brick_wall
        self.size = (tile_size, tile_size)
        self.image = pygame.transform.scale(self.image, self.size).convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
        self.last_player_position = None
        self.mask = pygame.mask.from_surface(self.image)

        self.direction = pygame.math.Vector2()
        self.last_direction = pygame.math.Vector2(-1,0)
        self.move_speed = basic_move_speed

    def resize (self, width, height):
        self.size = (width, height)
        self.image = pygame.transform.scale(self.image, self.size).convert_alpha()

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = 1
        elif keys[pygame.K_s]:
            self.direction.y = -1
        else:
            self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = 1
        elif keys[pygame.K_d]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_LSHIFT]:
            self.move_speed = 3 / 2 * basic_move_speed
        else:
            self.move_speed = basic_move_speed

    def update(self):
        self.input()

        self.rect.topleft += self.direction * self.move_speed




#########################################################################################



class Grass(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)
        self.image = pygame.image.load("graphic/paths_edit.jpeg").convert_alpha()
        self.position = position
        self.size = (tile_size, tile_size)
        self.image = pygame.transform.scale(self.image, self.size).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.direction = pygame.math.Vector2()
        self.move_speed = basic_move_speed

    def resize(self, width, height):
        self.size = (width, height)
        self.image = pygame.transform.scale(self.image, self.size).convert_alpha()

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = 1
        elif keys[pygame.K_s]:
            self.direction.y = -1
        else:
            self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = 1
        elif keys[pygame.K_d]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_LSHIFT]:
            self.move_speed = 3 / 2 * basic_move_speed
        else:
            self.move_speed = basic_move_speed

    def update(self):
        self.input()

        self.rect.topleft += self.direction * self.move_speed


