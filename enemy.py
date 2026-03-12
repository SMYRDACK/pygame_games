import pygame, math, os, random
from settings import *

class Ball(pygame.sprite.Sprite):
    def __init__(self, position, player_position, projectal_speed, group):
        super().__init__(group)
        self.position = pygame.math.Vector2(position[0], position[1])
        self.player_position = pygame.math.Vector2(player_position[0], player_position[1])
        self.projectal_speed = projectal_speed
        self.wektor = self.wyznacz_wektor()

        self.image = pygame.image.load("graphic/marble.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.center = self.position + self.wektor


    def wyznacz_wektor(self):
        p1 = self.position
        p2 = self.player_position

        wektor_kierunkowy = p2 - p1
        dlugosc_kierunkowego = wektor_kierunkowy.length()
        wektor_znormalizowany = wektor_kierunkowy / dlugosc_kierunkowego
        wektor = wektor_znormalizowany * self.projectal_speed
        return pygame.math.Vector2(int(wektor.x), int(wektor.y))

    def update(self, direction, walls_speed):
        self.rect.topleft += direction * walls_speed
        self.rect.center += self.wektor



class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, sprite_sheet_path, player, walls, group, frame_size= (48,48), speed=7, view_distance = 200):
        super().__init__(group)
        self.player = player
        self.walls_group = walls

        self.healf = 100

        self.position = position
        self.size = frame_size
        self.speed = speed
        self.sheet = pygame.image.load(sprite_sheet_path)
        self.frames = get_frames(self.sheet, frame_size[0], frame_size[1])
        self.frame_index = 0
        self.frame_direction = 0
        self.rect = pygame.Rect(self.position,self.size)

        self.image =  self.frames[self.frame_direction][self.frame_index]

        #dane ruchu
        self.walls_speed = basic_move_speed
        self.distance = None
        self.move_direction = pygame.math.Vector2()
        self.direction = pygame.math.Vector2()
        self.view_distance = view_distance
        self.last_direction = self.move_direction
        self.opuznienie = 0
        self.counter = 0

        self.ball_group = pygame.sprite.Group()
        self.cooldown = 0
    def player_is_visible(self):
        collision_detected = False

        #sprawdzamczy jest w zasiegu
        dx = self.player.rect.center[0] - self.rect.center[0]
        dy = self.player.rect.center[1] - self.rect.center[1]
        squer_distance = dx**2 + dy**2
        distance = math.sqrt(squer_distance)

        if distance > self.view_distance:
            return False

        for wall in self.walls_group:
            # Check if the line collides with this wall
            if wall.rect.clipline(self.player.rect.center, self.rect.center):
                # If there is a collision, change the ray color to red and break
                collision_detected = True
                break
        return not collision_detected

    def move(self):
        #kiedy nie widzi gracza to idzie w losowym kierunku lub stoi
        if self.player_is_visible() == False:
            if self.counter == 10:
                self.move_direction.x = random.choice([-1, 0, 1]) * self.speed
                self.move_direction.y = random.choice([-1, 0, 1]) * self.speed
                self.counter = 0
            else:
                self.counter += 1
        elif self.player_is_visible():
            if self.cooldown == 0:
                Ball(self.rect.center, self.player.rect.center, 20, self.ball_group)
                self.cooldown = random.randint(10,50)
            else:
                self.cooldown -=1
            #juz bymto zrobił na wektorach a nie xdd
            #jesli widzi gracza obiera najlepszy kierunek
            #wybierz kierunek z większą różnicą x czy y
            if abs(self.rect.center[0] - self.player.rect.center[0]) > abs(self.rect.center[1] - self.player.rect.center[1]):
                self.move_direction.y = 0
                if self.rect.center[0] - self.player.rect.center[0] > 0:
                    self.move_direction.x = -1 * self.speed
                else:
                    self.move_direction.x = 1 * self.speed
            else:
                self.move_direction.x = 0
                if self.rect.center[1] - self.player.rect.center[1] > 0:
                    self.move_direction.y = -1 * self.speed
                else:
                    self.move_direction.y = 1 * self.speed

        #animowanie

        if self.move_direction.x > 0:
            self.frame_direction = 2
        elif self.move_direction.x < 0:
            self.frame_direction = 1

    #    if self.move_direction.y > 0:
    #        self.frame_direction = 0
    #    elif self.move_direction.y < 0:
    #        self.frame_direction = 3

        if self.last_direction != self.frame_direction:
            self.frame_index = 0
        elif self.opuznienie == 5 and self.last_direction == self.frame_direction:
            self.frame_index = (self.frame_index + 1) % 4
            self.opuznienie = 0
        else:
            self.opuznienie += 1
        self.last_direction = self.frame_direction

    def healf_bar(self):
        if self.healf < 100:
            bar = pygame.surface.Surface((104, 14))
            bar.fill((128, 128, 128))
            pygame.draw.rect(bar, (255, 0, 0), (2, 2, 100, 10))
            pygame.draw.rect(bar, (0, 255, 0), (2, 2, self.healf, 10))
            font_healf = pygame.font.SysFont(None, 20)
            draw_text(bar, f"{self.healf}/100", font_healf, (0, 0, 0), (30, 2))
            screen.blit(bar, (self.rect.center[0] - self.size[0] - 8, self.rect.center[1] - self.size[1]))

    def input(self):
        #ten sam kod co przy scianach
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

        self.healf_bar()
        #update ruchu przeciwnika
        self.input()

        self.rect.topleft += self.direction * self.walls_speed

        self.ball_group.update(self.direction, self.walls_speed)
        self.ball_group.draw(screen)
        self.move()
        #animacja
        self.image = self.frames[self.frame_direction][self.frame_index]
        self.rect.topleft += self.move_direction

        for wall in self.walls_group:
            if wall.rect.colliderect(self.rect):
                self.rect.topleft -= self.move_direction
                break


class Drop_items(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)
        self.position = pygame.math.Vector2(position[0], position[1])
        self.type = random.choice(["health", "armor", "magazine"])
        path = f"graphic/drop_items/{self.type}.png"
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.direction = pygame.math.Vector2(0,0)
        self.walls_speed = 0
        self.up = True
        self.cooldown = 0

    def input(self):
        # ten sam kod co przy scianach
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

    def effect(self, player):
        if self.type == "health":
            player.healf += 20
            if player.healf > 100:
                player.healf = 100
        elif self.type == "armor":
            player.armor += 50
        elif self.type == "magazine":
            player.gun.ammo_size += 1
            player.gun.actual_ammo += 1


    def update(self):
        self.input()


        if self.cooldown > 0:
            self.cooldown -= 1

        if self.up and self.cooldown == 0:
            if self.position.y - 3 < self.rect.centery:
                self.rect.centery -= 1
            elif self.position.y - 3 == self.rect.centery:
                self.up = False
            self.cooldown = 3
        elif not self.up and self.cooldown == 0:
            if self.position.y + 3 > self.rect.centery:
                self.rect.centery += 1
            elif self.position.y + 3 == self.rect.centery:
                self.up = True
            self.cooldown = 3
        #dodanie cienia
        shadow_size = (38 , 8 )
        shadow_position_topleft = (self.rect.left - 3, self.position.y + 20)
        shadow = pygame.surface.Surface(shadow_size, pygame.SRCALPHA)
        shadow.set_alpha(90)
        pygame.draw.ellipse(shadow, (0,0,0), shadow.get_rect())
        screen.blit(shadow, shadow_position_topleft)

        self.rect.topleft += self.direction * self.walls_speed
        self.position += self.direction * self.walls_speed

