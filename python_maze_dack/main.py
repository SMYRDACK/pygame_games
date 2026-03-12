import random
import pygame, math, time


pygame.init()


#settings.py
def zmien_wymiary_plaszy(x,y):
    global COLS, ROWS
    if x % 2 == 0:
        COLS = x + 1
    else:
        COLS = x
    if y % 2 == 0:
        ROWS = y + 1
    else:
        ROWS = y

def zoom(zooming):
    global scale
    scale = zooming

#liczba kolumn i wierszy mapy (musi byc nieparzysta)
COLS= 11
ROWS = 11
tile_size = 128

#wymiary okna
window_height = 750
window_width = 1500

#zmienne uzywane stale
screen = pygame.display.set_mode((window_width,window_height))
clock = pygame.time.Clock()

try:
    brick_wall = pygame.image.load("graphic/brickwall_1080x1080.jpg").convert_alpha()
    background = pygame.image.load("graphic/big_grass.jpeg").convert_alpha()
    background = pygame.transform.scale(background, (window_width, window_height))
except:
    pass

scale = 2
tile_size = tile_size * scale
basic_move_speed = 5 * scale
start_position = (3 * tile_size / 2, 3 * tile_size / 2)





def get_frames(sheet, frame_width, frame_height):
    frames = []
    sheet_width, sheet_height = sheet.get_size()
    for y in range(0, sheet_height, frame_height):
        row_frames = []
        for x in range(0, sheet_width, frame_width):
            frame = sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
            row_frames.append(frame)
        frames.append(row_frames)
    return frames


def draw_text(surface, text, font, color, position):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)


#map.py ______________________________________________________________________________________________________
import numpy as np

class Map:
    def __init__(self):
        self.width = COLS
        self.height = ROWS
        self.map_size = (tile_size * self.width, tile_size * self.height)
        self.grid = np.zeros((COLS, ROWS), dtype=int)

        self.zapisana_pozycja_konca = None

    def closed_tile(self, x, y):
        wall_counter = 0
        # sprawdzam kratki w poziomie i w pionie

        if self.grid[x - 1, y] > 0:
           wall_counter += 1

        if self.grid[x + 1, y] > 0:
            wall_counter += 1

        if self.grid[x, y + 1] > 0:
            wall_counter += 1

        if self.grid[x, y - 1] > 0:
            wall_counter += 1

        if wall_counter == 4:
            return True
        elif wall_counter < 4:
            return False

    def generate_map(self):
        new_tile=True
        first_tile=True

        temp_x, temp_y = (None,None)

        directions=[(0, 1), (1, 0), (0, -1), (-1, 0)]   #mozliwe kierunki ruchu
        self.grid = np.zeros((COLS, ROWS), dtype=int)

        for x in range(self.width):
            for y in range(self.height):

                #uzupelnij bazowo w kratke
                if x % 2 == 0 or y % 2 == 0:
                    self.grid[x, y]=1

        #teraz ponownie przechodze po pozycjach szukając zabudowanych miejsc

        for x in range(self.width):
            for y in range(self.height):

                if self.grid[x,y] == 1: #jezeli wybrana jest sciana to skip
                    continue

                if not self.closed_tile( x, y):  #jesli jest otwarta pozycja skip
                    continue

                #jesli tu doszedł, to mamy pusta kratke otoczoną scianami
                #bierzemy losową kolejnosc kierunkow i sprawdzamy czy sąsiad jest domkniety
                random.shuffle(directions)

                #jesli to początkowa
                if first_tile:
                    first_tile = False
                    new_tile = False
                    for move_x, move_y in directions:
                        if move_x > 0 or move_y > 0:
                            self.grid[x + move_x, y + move_y] = 0
                            #zniszcozna sciana, zapisuje pozycje tymczasowe w nowej kratce
                            temp_x, temp_y = (2 * move_x + x, 2 * move_y + y)

                if new_tile:
                    temp_x, temp_y = (x, y)
                    for move_x, move_y in directions:
                        if not (2 * move_x + temp_x in range(1, self.width -1) and  2 * move_y + temp_y in range(1, self.height -1)):
                            continue
                        #jesli znajdziesz otwartą kratke obok a takowa musi byc to zrob tam przejscie
                        if not self.closed_tile(2 * move_x + x, 2 * move_y + y):
                            self.grid[x + move_x, y + move_y] = 0
                            new_tile = False
                            break

                #wyjątki za nami. trzeba teraz stworzyć główny generator
                generowanie = True

                while generowanie:
                    random.shuffle(directions) #przelosuj kierunki
                    znalazl_kierunek = False
                    for move_x, move_y in directions:
                        #pomin jesli docelowo wyjdziemy poza granice
                        if not (2 * move_x + temp_x in range(1, self.width -1) and  2 * move_y + temp_y in range(1, self.height -1)):
                            continue

                        if self.closed_tile(2 * move_x + temp_x, 2 * move_y + temp_y):
                            self.grid[temp_x + move_x, temp_y + move_y] = 0
                            temp_x += 2 * move_x
                            temp_y += 2 * move_y
                            znalazl_kierunek = True
                            break

                    if znalazl_kierunek == False:
                        self.grid[temp_x][temp_y] = -2
                        self.zapisana_pozycja_konca = (temp_x, temp_y)
                        new_tile=True
                        generowanie=False

        #wybor miejsca konca gry
        self.grid[self.zapisana_pozycja_konca[0]][self.zapisana_pozycja_konca[1]] = -3

    def walls_data(self):
        walls_positions = []
        for x in range(self.width):
            for y in range(self.height):
                tile_x = x * tile_size
                tile_y = y * tile_size


                if self.grid[x][y]== 1:
                    walls_positions.append((tile_x, tile_y))
        return walls_positions

    def paths_data(self):
        paths_positions = []
        for x in range(self.width):
            for y in range(self.height):
                tile_x = x * tile_size
                tile_y = y * tile_size

                if self.grid[x][y] <= 0:
                    paths_positions.append((tile_x, tile_y))
        return paths_positions

    def ends_data(self):
        ends_positions = []
        for x in range(self.width):
            for y in range(self.height):
                tile_x = x * tile_size
                tile_y = y * tile_size

                if self.grid[x][y] == -3 or self.grid[x][y] == -2:
                    ends_positions.append((tile_x, tile_y))
        return ends_positions

    def portal_data(self):
        tile_x = self.zapisana_pozycja_konca[0] * tile_size
        tile_y = self.zapisana_pozycja_konca[1] * tile_size
        return [tile_x, tile_y]

    def render(self, screen = screen):

        minimap = pygame.surface.Surface((self.width * 10 + 8, self.height * 10 + 8), pygame.SRCALPHA)
        minimap.set_alpha(200)
        minimap.fill((0,0,0))
        pygame.draw.rect(minimap, (200,200,200), (0, 0, self.width * 10 + 6, self.height * 10 + 6))
        pygame.draw.rect(minimap, (100, 100, 100), (2, 2, self.width * 10 + 4, self.height * 10 + 4))
        for x in range(self.width):
            for y in range(self.height):
                tile_x = x * 10 + 4
                tile_y = y * 10 + 4

                if self.grid[x][y] == 0:
                    pygame.draw.rect(minimap, (255,255,255), (tile_x, tile_y, 10 - 1, 10 - 1))
                elif self.grid[x][y]== 1:
                    pygame.draw.rect(minimap, (0,0,0), (tile_x, tile_y, 10 - 1, 10 - 1))
                elif self.grid[x][y] == -1:
                    pygame.draw.rect(minimap, (255, 0, 0), (tile_x, tile_y, 10 - 1, 10 - 1))
                elif self.grid[x][y] == -2:
                    pygame.draw.rect(minimap, (0, 255, 0), (tile_x, tile_y, 10 - 1, 10 - 1))
                elif self.grid[x][y] == -3:
                    pygame.draw.rect(minimap, (0, 200, 200), (tile_x, tile_y, 10 - 1, 10 - 1))

        screen.blit(minimap, (20,20))


#soundbox.py________________________________________________________________________________________________
import os
pygame.mixer.init()

def random_music(sound_folderr):
    sound_file_v = [f for f in os.listdir(sound_folderr) if f.endswith('.mp3')]
    return random.choice(sound_file_v)

def play_sound(sound_folderr,sound = None, volume = 1.0):

    sound_folderr = os.path.join("soundbox", sound_folderr)
    if sound == None:
        try:
            sound = random_music(sound_folderr)
        except:
            sound = "(1).mp3"
    sound = pygame.mixer.Sound(os.path.join(sound_folderr, sound))
    sound.set_volume(volume)
    sound.play()


#button.py_________________________________________________________________________________________________
import sys

class Button:
    def __init__(self, position, size, message = None, message_color = (0,0,0), font_size = 30, color = (255, 0, 0), grafic = None, alpha = 100, shadow_r = 0, shadow_g = 0, shadow_b = 0):
        pygame.init()
        self.position = position
        self.size = size
        self.color = color
        self.shadow = pygame.Surface(self.size, pygame.SRCALPHA)
        self.alpha = alpha
        self.shadow.fill((0, 0, 0, self.alpha))
        self.grafic = grafic
        if self.grafic != None:
            self.grafic = pygame.transform.scale(self.grafic, self.size)

        self.text = message
        self.button_rect = pygame.Rect(self.position, self.size)
        if self.text != None:
            self.font = pygame.font.Font(None, font_size)
            self.rendered_text = self.font.render(self.text, True, message_color)
            self.text_rect = self.rendered_text.get_rect(center=self.button_rect.center)
            self.text_surface = pygame.Surface((self.text_rect[2], self.text_rect[3]), pygame.SRCALPHA)
            self.text_surface.fill((0,0,0, alpha))

        self.shadow_r = shadow_r
        self.shadow_g = shadow_g
        self.shadow_b = shadow_b

    def draw_button(self, mouse_position = None, mouse_click = None):
        if mouse_position == None and mouse_click == None:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
        else:
            mouse = mouse_position
            click = mouse_click
        pressed = False



        if self.position[0] + self.size[0] > mouse[0] > self.position[0] and self.position[1] + self.size[1] > mouse[1] > self.position[1]:
            pygame.draw.rect(screen, self.color, (self.position, self.size))
            if self.grafic != None:
                screen.blit(self.grafic, self.position)
            screen.blit(self.shadow, self.button_rect.topleft)

            if click[0] == 1:
                print("Przycisk został naciśnięty")
                pressed = True
                pygame.draw.rect(screen, self.color, (self.position, self.size))

                if self.grafic != None:
                    screen.blit(self.grafic, self.position)
                self.alpha = 60
                self.shadow.fill((self.shadow_r, self.shadow_g, self.shadow_b, self.alpha))
                screen.blit(self.shadow, self.button_rect.topleft)


                if self.text != None:
                    screen.blit(self.text_surface, self.text_rect.topleft)
                    screen.blit(self.rendered_text, self.text_rect.topleft)

                pygame.display.update()
                self.alpha = 100
                self.shadow.fill((0, 0, 0, self.alpha))
        else:
            pygame.draw.rect(screen, self.color, (self.position, self.size))
            if self.grafic != None:
                screen.blit(self.grafic, self.position)

        if self.text != None:
            screen.blit(self.text_surface, self.text_rect.topleft)
            screen.blit(self.rendered_text, self.text_rect.topleft)
        return pressed

#player.py

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
        play_sound(sound_folderr="gun", sound="gun_shoot.mp3", volume=0.1)
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

#walls.py_____________________________________________________________________________________________________________________

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

#music.py_____________________________________________________________________________________________
music_folder = 'music'

def random_music():
    music_files = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]
    return random.choice(music_files)

def play_music():
    if not pygame.mixer.music.get_busy():  # Sprawdzenie czy muzyka jest odtwarzana
        next_song = random_music()
        pygame.mixer.music.load(os.path.join(music_folder, next_song))
        pygame.mixer.music.play()


#enemy.py_________________________________________________________________________________________________________

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


#portal.py__________________________________________________________________________________________________________________

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



#main part maze_game_main.py __________________________________________________________________________________________

play_music()

#kursor
pygame.mouse.set_visible(False)
celownik_kursor = pygame.image.load("graphic/celownik.png")
kursor = pygame.surface.Surface(celownik_kursor.get_size(), pygame.SRCALPHA)
kursor.set_alpha(100)

players_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
paths_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
drop_items_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
gem_group = pygame.sprite.Group()

map = Map()
show_map = -1
keys_history = pygame.key.get_pressed()


player = Player((screen.get_size()[0]/2, screen.get_size()[1]/2), players_group)


map.generate_map()
walls_position = map.walls_data()
paths_position = map.paths_data()
portal_position = map.portal_data()
box_position = map.ends_data()

for x, y in walls_position:
    x += (player.rect.topleft[0] - start_position[0])
    y += (player.rect.topleft[1] - start_position[1])
    Walls((x,y), walls_group)

for x, y in paths_position:
    x += (player.rect.topleft[0] - start_position[0])
    y += (player.rect.topleft[1] - start_position[1])
    Grass((x,y), paths_group)

    if random.randint(0,100) >70 and (x>1500 or y>800) :
        Enemy(position=(x + (tile_size/2), y + (tile_size/2)), frame_size=(64,64), speed = basic_move_speed/2,
            sprite_sheet_path=random.choice(['graphic/SLIME_BLUE.png', 'graphic/SLIME_GREEN.png', 'graphic/SLIME_GOLD.png', 'graphic/SLIME_VIOLET.png']),
            view_distance=500, player=player,
            walls=walls_group, group= enemies_group)

portal_position[0] += (player.rect.topleft[0] - start_position[0])
portal_position[1] += (player.rect.topleft[1] - start_position[1])
Portal(portal_position, portal_group)

for x, y in box_position:
    x += (player.rect.topleft[0] - start_position[0])
    y += (player.rect.topleft[1] - start_position[1])
    if x == portal_position[0] and y == portal_position[1]:
        with_portal = True
    else:
        with_portal = False
    Box((x,y), with_portal, box_group)


clock = pygame.time.Clock()


portal_box_destroed = False

while True:
    clock.tick(30)
    play_music()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((0,0,0))
    #redukcja wchodzenia w sciane
    if pygame.sprite.spritecollide(player, walls_group, False):
        while pygame.sprite.spritecollide(player, walls_group, False):      ##, pygame.sprite.collide_mask
            back_direction = None
            for walls in walls_group:
                if back_direction == None:
                    back_direction = walls.direction
                walls.rect.topleft -= back_direction * 5
            for paths in paths_group:
                paths.rect.topleft -= back_direction * 5
            for enemy in enemies_group:
                enemy.rect.topleft -= back_direction * 5
                for ball in enemy.ball_group:
                    ball.rect.topleft -= back_direction * 5
            for bullet in player.gun.bullet_group:
                bullet.position -= back_direction * 5
            for drops in drop_items_group:
                drops.position -= back_direction * 5
                drops.rect.center -= back_direction * 5
            for portal in portal_group:
                portal.rect.center -= back_direction * 5
            for box in box_group:
                box.rect.center -= back_direction * 5
            for gems in gem_group:
                gems.rect.center -= back_direction * 5


    if pygame.sprite.spritecollide(player, enemies_group, True):
        play_sound(sound_folderr="get_hit", sound="hit.mp3")
        player.healf -= 10
        player.armor = 0

    for drops in drop_items_group:
        if pygame.sprite.spritecollide(drops, players_group, False):
            drops.effect(player)
            drops.kill()

    for portal in portal_group:
        if pygame.sprite.spritecollide(portal, players_group, False, pygame.sprite.collide_mask) and portal.has_opened:
            portal.start_closing = True
            player.kill()
        if portal.start_opening:
            gem.kill()

    for box in box_group:
        if pygame.sprite.spritecollide(box, player.gun.bullet_group, True, pygame.sprite.collide_mask) and not box.hitted:
            box.hitted = True
            if box.with_portal:
                portal_box_destroed = True
                gem = Gem(box.rect.center, gem_group)


    #jesli sciana/enemy styka sie z pociskiem -> zabij
    for wall in walls_group:
        pygame.sprite.spritecollide(wall, player.gun.bullet_group, True)
    for enemy in enemies_group:
        #bullets_players
        if pygame.sprite.spritecollide(enemy, player.gun.bullet_group, True):
            enemy.healf -= player.gun.damage
            enemy.view_distance = 1000
            if enemy.healf <= 0:
                player.kills_counter += 1
                if random.randint(0,100)<100:
                    Drop_items(position=enemy.rect.center, group=drop_items_group)
                enemy.kill()
        #balls_enemies
        if pygame.sprite.spritecollide(player, enemy.ball_group, True):
            if player.armor > 0:
                player.armor -= random.randint(5, 20)
                if player.armor < 0:
                    player.armor = 0
            else:
                player.healf -= random.randint(5,10)
        #zabij pocisk o sciane
        for ball in enemy.ball_group:
            if pygame.sprite.spritecollide(ball, walls_group, False):
                ball.kill()




    walls_group.draw(screen)
    paths_group.draw(screen)
    drop_items_group.draw(screen)
    gem_group.draw(screen)
    portal_group.draw(screen)
    players_group.draw(screen)
    enemies_group.draw(screen)
    box_group.draw(screen)
    for gem in gem_group:
        gem.draw()

    drop_items_group.update()
    players_group.update()
    walls_group.update()
    paths_group.update()
    enemies_group.update()
    box_group.update()
    gem_group.update()
    portal_group.update(player.is_honk, portal_box_destroed, player.rect.center)

    for players in players_group:
        players.update_gun()

    kursor_rect = celownik_kursor.get_rect(center=pygame.mouse.get_pos())
    kursor.blit(celownik_kursor, (0,0))
    screen.blit(kursor, kursor_rect.topleft)
    print(player.kills_counter)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_m] and keys[pygame.K_m] != keys_history[pygame.K_m]:
        show_map *= -1
    keys_history = pygame.key.get_pressed()
    if show_map == 1:
        map.render()

    pygame.display.update()