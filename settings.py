"""
tutaj są dane niezmienne dla naszej gry, wykorzystywane w projekcie
"""
import random
import pygame


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
COLS= 51
ROWS = 51
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
