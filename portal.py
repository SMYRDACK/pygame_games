import pygame
from settings import *

pygame.init()

class Gem(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)
        self.position = pygame.math.Vector2(position[0], position[1])
        self.sheet = pygame.image.load("graphic/gem.png").convert_alpha()
        self.sheet = pygame.transform.scale(self.sheet, (80 * 3, 16 * 3))
        self.frames = get_frames(self.sheet, 16 * 3, 16 * 3)
        self.frame_index = 0
        self.type = 0

        self.image = self.frames[self.type][self.frame_index]
        self.rect = self.image.get_rect(center= self.position)

        self.cooldown = 0
        self.direction = pygame.math.Vector2()
        self.walls_speed = 0

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
            self.walls_speed = 3 / 2 * basic_move_speed
        else:
            self.walls_speed = basic_move_speed

    def update(self):
        self.input()
        self.rect.topleft += self.direction * self.walls_speed

        if self.cooldown > 0:
            self.cooldown -= 1
        else:
            self.frame_index = (self.frame_index + 1) % 4
            self.cooldown = 3

        self.image = self.frames[self.type][self.frame_index]

    def draw(self):
        font = pygame.font.SysFont(None, 32)
        draw_text(screen, "PRESS Q", font, (0,0,0), (self.rect.centerx - 47, self.rect.centery - 48))
        draw_text(screen, "PRESS Q", font, (0,0,0), (self.rect.centerx - 48, self.rect.centery - 47))
        draw_text(screen, "PRESS Q", font, (0, 0, 0), (self.rect.centerx - 46, self.rect.centery - 47))
        draw_text(screen, "PRESS Q", font, (0, 0, 0), (self.rect.centerx - 46, self.rect.centery - 46))
        draw_text(screen, "PRESS Q", font, (255, 255, 255), (self.rect.centerx - 48, self.rect.centery - 48))



class Box(pygame.sprite.Sprite):
    def __init__(self, position, with_portal, group):
        super().__init__(group)
        self.position = pygame.math.Vector2(position[0], position[1])
        self.with_portal = with_portal
        self.sheet = pygame.image.load("graphic/create_2.png").convert_alpha()
        self.sheet = pygame.transform.scale(self.sheet, (160 * 4, 32 * 4))
        self.frames = get_frames(self.sheet, 64 * 2, 64 * 2)
        self.frame_index = 0
        self.type = 0
        self.image = self.frames[self.type][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = pygame.math.Vector2(self.position.x + int(tile_size / 2), self.position.y + int(tile_size / 2))

        self.mask = pygame.mask.from_surface(self.image)

        self.hitted = False
        self.destroyed = False
        self.cooldown = 0

        self.direction = pygame.math.Vector2()
        self.walls_speed = 0
    def destroy_box(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        elif self.frame_index < 4:
            self.cooldown = 3
            self.frame_index += 1
        elif self.frame_index == 4:
            self.destroyed = True

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
            self.walls_speed = 3 / 2 * basic_move_speed
        else:
            self.walls_speed = basic_move_speed

    def update(self):
        if self.hitted:
            self.destroy_box()
        elif self.destroyed and not self.with_portal:
            self.kill()

        self.image = self.frames[self.type][self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)

        self.input()
        self.rect.topleft += self.direction * self.walls_speed

class Portal(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)
        self.position = pygame.math.Vector2(position[0], position[1])
        self.size = (64, 64)

        self.sheet = pygame.image.load("graphic/Green Portal Sprite Sheet.png").convert_alpha()
        self.frames = get_frames(self.sheet, self.size[0], self.size[1])
        self.frame_index = 7
        self.type = {"open" : 0, "closing" : 2, "opening" : 1 }
        self.actual_type = self.type["closing"]

        self.has_opened = False
        self.start_closing = False
        self.escaped = False
        self.start_opening = False
        self.cooldown = 0

        self.image = self.frames[self.actual_type][self.frame_index]
        self.image = pygame.transform.scale(self.image, (256, 256))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.topleft = self.position

        self.direction = pygame.math.Vector2(0,0)
        self.walls_speed = None

    def opening(self):
        if self.actual_type != 1 and self.cooldown == 0:
            self.actual_type = self.type["opening"]
            self.frame_index = 0
            self.cooldown = 3
        elif self.frame_index < 7 and self.cooldown == 0:
            self.frame_index += 1
            self.cooldown = 3
        elif self.frame_index == 7 and self.cooldown == 0:
            self.has_opened = True
            self.cooldown = 3
        elif self.cooldown != 0:
            self.cooldown -= 1

    def closing(self):
        if self.actual_type != 2 and self.cooldown == 0:
            self.actual_type = self.type["closing"]
            self.frame_index = 0
            self.cooldown = 3
        elif self.frame_index < 7 and self.cooldown == 0:
            self.frame_index += 1
            self.cooldown = 3
        elif self.frame_index == 7 and self.cooldown == 0:
            self.escaped = True
            self.cooldown = 3
        elif self.cooldown != 0:
            self.cooldown -= 1

    def open(self):
        if self.actual_type != 0 and self.cooldown == 0:
            self.actual_type = 0
            self.frame_index = 0
            self.cooldown = 3
        elif self.cooldown == 0:
            self.frame_index += 1
            self.frame_index = self.frame_index % 8
            self.cooldown = 3
        elif self.cooldown > 0:
            self.cooldown -= 1

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
            self.walls_speed = 3 / 2 * basic_move_speed
        else:
            self.walls_speed = basic_move_speed

    def distance(self, player_position):
        p1 = self.rect.center
        p2 = pygame.math.Vector2(player_position[0], player_position[1])

        wektor_kierunkowy = p2 - p1
        return wektor_kierunkowy.length()

    def update(self, is_honk, can_open, player_position):
        font = pygame.font.SysFont(None, 48)
        #draw_text(screen, f"{is_honk}, {player_position}, {self.distance(player_position)}", font, (0,0,255), (0,0))
        self.input()
        self.rect.topleft += self.direction * self.walls_speed

        if self.distance(player_position) > 300 and not self.has_opened:
            #działa tylko w odleglosci do 300 px
            return

        if not self.has_opened and is_honk and can_open:
            self.start_opening = True
            self.opening()
        elif not self.has_opened and not is_honk and self.actual_type == 1:
            self.opening()


        if self.has_opened and not self.start_closing:
            self.open()
        elif self.has_opened and self.start_closing:
            self.closing()

        self.image = self.frames[self.actual_type][self.frame_index]
        self.image = pygame.transform.scale(self.image, (256, 256))
        self.mask = pygame.mask.from_surface(self.image)





