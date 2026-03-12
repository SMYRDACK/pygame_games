from settings import *
import numpy as np
import pygame, random

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

