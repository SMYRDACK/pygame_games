import time

from settings import *
import pygame, math, random, sys
from soundbox import  *
from button import Button

pygame.init()
pygame.mixer.init()

font = pygame.font.SysFont(None, 48)

def game_over():
    pygame.mouse.set_visible(True)
    end_surface = pygame.surface.Surface((window_width, window_height), pygame.SRCALPHA)
    end_surface.fill((150,0,0))
    end_surface.set_alpha(90)

    screen.blit(end_surface, (0, 0))

    font_game_over = pygame.font.Font("fonts/RubikMonoOne-Regular.ttf", 128)
    end_text = pygame.surface.Surface((window_width, window_height), pygame.SRCALPHA)
    draw_text(end_text, "game over", font_game_over, (0,0,0), (250, 200))
    screen.blit(end_text, (0,0))


    pygame.display.update()
    time.sleep(3)
    sys.exit()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, distance, speed, gun_position, player_position, angle, group):
        super().__init__(group)
        play_sound(sound_folder="gun", sound="gun_shoot.mp3", volume=0.1)
        self.angle = angle
        self.position = gun_position
        self.speed = speed
        self.image = pygame.image.load('graphic/bullet.png')
        self.image = pygame.transform.scale(self.image,(4 * 5, 3 * 5))
        self.image = pygame.transform.rotate(self.image, -math.degrees(self.angle))
        self.rect = self.image.get_rect(center=self.position)

        self.velocity = pygame.math.Vector2(
            math.cos(-self.angle),
            math.sin(self.angle)
        ) * self.speed

        self.direction = pygame.math.Vector2()
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

        self.position += self.direction * self.move_speed

    def update(self):
        self.input()
        self.position += self.velocity
        self.rect.center = (self.position[0], self.position[1])
        screen.blit(self.image, self.rect.topleft)

class Gun():
    def __init__(self, position, frame_size = (32,16), distance_from_player = 10*scale, frames_path = 'graphic/gun_with_shoot.png', ammo_size = 7):
        self.size = frame_size
        self.position = position
        self.player_postion = position
        self.distance_from_player = distance_from_player * 2

        self.gun_frames = pygame.image.load(frames_path).convert_alpha()
        self.gun_frames = get_frames(self.gun_frames, self.size[0], self.size[1])
        self.gun_frame_index = 0

        self.gun_rotated = None
        self.angle=0
        self.opuznienie = -1
        self.image = self.gun_frames[0][self.gun_frame_index]
        self.rect = self.image.get_rect()

        self.ammo_size = ammo_size
        self.actual_ammo = self.ammo_size
        self.ammo_frames = get_frames(pygame.image.load('graphic/ammo_pack_sheet.png').convert_alpha(), 16, 16)
        self.ammo_actual_frame = 0
        self.bullet_group = pygame.sprite.Group()

        self.animacja_strzalu = False
        self.damage = 50
    def rotate(self, position):
        self.position = (position[0], position[1])
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.angle = math.atan2(mouse_y - self.position[1], mouse_x - self.position[0])

        if self.angle > math.pi / 2 or self.angle < - math.pi / 2:
            gun_fliped = pygame.transform.flip(self.image, False, True)
        else:
            gun_fliped = self.image

        gun_fliped = pygame.transform.scale(gun_fliped,(self.size[0] * scale * 2, self.size[1] * scale * 2))

        self.gun_rotated = pygame.transform.rotate(gun_fliped, -math.degrees(self.angle))

        self.position =(
            self.position[0] + (48 + self.distance_from_player) * math.cos(self.angle) - self.gun_rotated.get_width() // 2,
            self.position[1] + (48 + self.distance_from_player) * math.sin(self.angle) - self.gun_rotated.get_height() // 2
        )
        self.rect = self.gun_rotated.get_rect(topleft=(self.position[0], self.position[1] - 4))

    def shoot(self):
        mouse_bottons = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        if (self.actual_ammo == 0 or  keys[pygame.K_r]) and self.opuznienie > -10 and not self.animacja_strzalu:
            self.opuznienie = -100
            self.gun_frame_index = 0
        elif  self.opuznienie < -10:
            self.opuznienie += 1
        elif self.opuznienie == -10:
            self.actual_ammo = self.ammo_size
            self.opuznienie = -1


        if self.gun_frame_index == 0 and mouse_bottons[0] and self.opuznienie == -1 and self.actual_ammo > 0:
            Bullet(100, 50, self.rect.center, self.player_postion,self.angle, self.bullet_group)

            self.opuznienie = 2
            self.actual_ammo -= 1
            self.animacja_strzalu = True
            ##generuj_pocisk
        elif  self.opuznienie > 0:
            self.opuznienie = (self.opuznienie + 1) % 3
        elif self.opuznienie == 0:
            self.gun_frame_index = (self.gun_frame_index + 1) % 5
            self.opuznienie = 1
        if self.gun_frame_index == 0 and self.opuznienie == 1:
            self.gun_frame_index = 0
            self.animacja_strzalu = False
            self.opuznienie = -1


        self.image = self.gun_frames[0][self.gun_frame_index]


    def gun_menu(self):
        #draw_text(screen, str(self.actual_ammo), font, (255, 255, 255), (0, 0))
       # draw_text(screen, str(self.opuznienie), font, (255, 255, 255), (50, 0))

        menu_size = pygame.math.Vector2()
        menu_size.x = 250
        menu_size.y = 100

        self.menu = pygame.surface.Surface(menu_size)
        self.menu.fill((144, 91, 39))

        pygame.draw.rect(self.menu, (0, 0, 0), (-4, 0, menu_size.x + 4, menu_size.y + 4), width=4)

        #ikona pistoletu
        gun_image = pygame.transform.scale(self.gun_frames[0][0], (100,50))

        pygame.draw.rect(self.menu, (150,150,150), (10, 25, 50 + 20, 50 + 10))
        pygame.draw.rect(self.menu, (200,200,100), (12, 27, 50 + 16, 50 + 6))
        self.menu.blit(gun_image, (10,25))

        #ikona amunicji
        if self.actual_ammo >= 3:
            ammo_image = self.ammo_frames[0][0]
        elif self.actual_ammo == 2:
            ammo_image = self.ammo_frames[0][1]
        elif self.actual_ammo == 1:
            ammo_image = self.ammo_frames[0][2]
        else:
            ammo_image = self.ammo_frames[0][3]

        ammo_image = pygame.transform.scale(ammo_image, (50,50))

        pygame.draw.rect(self.menu, (150, 150, 150), (100, 25, 110 + 20, 50 + 10))
        pygame.draw.rect(self.menu, (200, 200, 100), (102, 27, 110 + 16, 50 + 6))
        self.menu.blit(ammo_image, (110, 32))
        ammo_font = pygame.font.SysFont(None, 32)
        #ilosc amunicji
        pygame.draw.rect(self.menu, (0,0,0), (168, 45, 45, 20))

        dy = 0
        if 10 <= self.ammo_size < 100:
            ammo_font = pygame.font.SysFont(None, 20)
            dy = 4


        draw_text(self.menu, f"{self.actual_ammo} / {self.ammo_size}", font=ammo_font, color=(255,255,255), position=(170, 45 + dy))

        #animowanie przeładowania
        if self.opuznienie < -1:
            shadow = pygame.surface.Surface((int((-66/90) * self.opuznienie + (-66/9)), 50 + 6), pygame.SRCALPHA)
            shadow.fill((0,0,0))
            shadow.set_alpha(100)
            self.menu.blit(shadow, (12,27))



        screen.blit(self.menu, (0, window_height-menu_size.y))


    def update(self, player_position):

        self.rotate(player_position)
        self.shoot()
        self.gun_menu()

        self.bullet_group.update()
        self.bullet_group.draw(screen)
        screen.blit(self.gun_rotated, self.position)

class Player(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)

        self.healf = 100
        self.kills_counter = 0

        self.frames = 4
        self.types = 1
        self.size = (48, 48)
        self.scale = scale
        #animacja
        self.full_sheet = pygame.image.load("graphic/kaczka.png").convert_alpha()
        kaczka = self.select_character()
        self.sheet = self.full_sheet.subsurface(pygame.Rect(kaczka[0], kaczka[1], self.size[0] * 3, self.size[1] * 4))
        self.frames = get_frames(self.sheet, self.size[0], self.size[1])
        self.frame_index = 0
        self.frame_direction = 0
        self.opuznienie = 0

        self.image = self.frames[self.frame_direction][self.frame_index]
        self.image = pygame.transform.scale(self.image, (self.size[0] * self.scale, self.size[1] * self.scale))
        self.rect = self.image.get_rect(topleft = position)

        self.is_honk = False

        #hitbox maska
        self.mask = pygame.mask.from_surface(self.image)


        #bron
        self.gun = Gun(self.rect.center)

        self.keys_history = pygame.key.get_pressed()

        self.armor = 0

    def select_character(self):
        pygame.mouse.set_visible(True)
        #okienko
        size_okna = pygame.math.Vector2(1250, 250)
        karta_wyboru = pygame.surface.Surface((size_okna.x + 2 + 2, size_okna.y + 2 + 2))
        karta_wyboru.fill((50,50,50))
        pygame.draw.rect(karta_wyboru, (200,200,200), (0, 0, size_okna.x + 2, size_okna.y + 2))
        pygame.draw.rect(karta_wyboru, (150, 150, 150), (2, 2, size_okna.x, size_okna.y))

        font_okna = pygame.font.Font("fonts/RubikMonoOne-Regular.ttf", 36)
        draw_text(karta_wyboru, "CHOOSE YOUR DUCK", font_okna, (0, 0, 0), (374, 28))
        draw_text(karta_wyboru, "CHOOSE YOUR DUCK", font_okna, (0, 0, 0), (373, 27))
        draw_text(karta_wyboru, "CHOOSE YOUR DUCK", font_okna, (0, 0, 0), (372, 26))
        draw_text(karta_wyboru, "CHOOSE YOUR DUCK", font_okna, (0, 0, 0), (371, 25))
        draw_text(karta_wyboru, "CHOOSE YOUR DUCK", font_okna, (220,220,220), (370, 25))

        pygame.draw.rect(karta_wyboru, (50, 50, 50), (18,78,1224,143))
        pygame.draw.rect(karta_wyboru, (170,170,170), (20,80,1220,139))

        pozycja_karty = (123, 350)
        screen.blit(karta_wyboru, (pozycja_karty))

        #grafiki kaczek
        obrazy_kaczek_pozycje = [(0,0), (0, 192), (144,0), (144,192), (288,0), (288,192), (432,0), (432,192)]
        obrazy_kaczek = []
        for x, y in obrazy_kaczek_pozycje:
            kaczka = self.full_sheet.subsurface(pygame.Rect(x, y, self.size[0], self.size[1]))
            pygame.transform.scale(kaczka, (100,100))
            obrazy_kaczek.append(kaczka)

        kaczki_buttons =[]
        przeskok = 50 + pozycja_karty[0]

        button_dict = {}

        for dack in obrazy_kaczek:
            pozycja_startowa = (przeskok, 450)
            pygame.draw.rect(screen, (50,50,50), (pozycja_startowa[0] - 2, pozycja_startowa[1] - 2, 104, 104))
            pygame.draw.rect(screen, (250,250,250), (pozycja_startowa[0] - 2, pozycja_startowa[1] - 2, 102, 102))

            button = Button(position=pozycja_startowa, size=(100, 100), color=(200, 200, 200), grafic=dack, shadow_r=0, shadow_g=0, shadow_b=0)
            kaczki_buttons.append(button)
            button_dict[button]=obrazy_kaczek_pozycje[len(button_dict)]
            przeskok += 50 + 100

        while True:
            for dack_button in kaczki_buttons:
                if dack_button.draw_button():
                    pygame.mouse.set_visible(False)
                    return button_dict[dack_button]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            pygame.display.update()


    def input(self):
        keys= pygame.key.get_pressed()
        self.last_direction = self.frame_direction
        brak_ruchu_x, brak_ruchu_y = (False, False)

        if keys[pygame.K_w]:
            self.frame_direction = 3
        elif keys[pygame.K_s]:
            self.frame_direction = 0
        else:
            brak_ruchu_y = True

        if keys[pygame.K_a]:
            self.frame_direction = 1
        elif keys[pygame.K_d]:
            self.frame_direction = 2
        elif brak_ruchu_y:
            brak_ruchu_x = True
            self.frame_index = 0

        if self.last_direction != self.frame_direction:
            self.frame_index = 0
        elif brak_ruchu_y and brak_ruchu_x:
            self.frame_index = 0
            self.opuznienie = 0
        elif self.opuznienie == 5 and self.last_direction == self.frame_direction:
            self.frame_index = (self.frame_index + 1) % 3
            self.opuznienie = 0
        else:
            self.opuznienie += 1

        if keys[pygame.K_q] and keys[pygame.K_q] != self.keys_history[pygame.K_q]:
            play_sound("quack")
            self.is_honk = True
        elif self.keys_history[pygame.K_q]:
            self.is_honk = True
        else:
            self.is_honk = False

        self.keys_history = pygame.key.get_pressed()

    def healf_bar(self):
        if self.healf < 0:
            self.healf = 0

        if self.healf < 100 or self.armor > 0:
            bar = pygame.surface.Surface((104, 14))
            bar.fill((128, 128, 128))
            pygame.draw.rect(bar, (255, 0, 0), (2, 2, 100, 10))
            pygame.draw.rect(bar, (0, 255, 0), (2, 2, self.healf, 10))
            if self.armor > 100:
                self.armor = 100
            if self.armor > 0:
                pygame.draw.rect(bar, (0, 200, 200), (2, 2, self.armor, 10))
            font_healf = pygame.font.SysFont(None, 20)
            draw_text(bar, f"{self.healf}/100", font_healf, (0,0,0), (30, 2))
            screen.blit(bar, (self.rect.center[0] - self.size[0] - 8, self.rect.center[1] - self.size[1]))

    def update(self):
        print(self.healf)
        self.healf_bar()
        self.input()
        self.image = self.frames[self.frame_direction][self.frame_index]
        self.image = pygame.transform.scale(self.image, (self.size[0] * self.scale, self.size[1] * self.scale))
        self.mask = pygame.mask.from_surface(self.image)
        if self.healf <= 0:
            self.kill()
            game_over()

    def update_gun(self):
        self.gun.update(self.rect.center)

