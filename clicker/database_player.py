import sqlite3
import sys
import time

from settings import *
import pygame

'''
bede zapisywac kolumny w podanym formacie:

nazwa_pierwszaLiteraTypu

t-text, i-intiger, r-real

'''
pygame.init()

def make_list_of_types(lista):
    values_types = []
    for name in lista:
        typ = name[-1]
        if typ == "i":
            typ = "INTEGER"
        elif typ == "r":
            typ = "REAL"
        elif typ =="t":
            typ = "TEXT"
        values_types.append(typ)
    return values_types

def save_game(state):
    columns = list(state.keys())
    values = list(state.values())
    values_type = make_list_of_types(columns)


    conn = sqlite3.connect('savegame.db')
    c = conn.cursor()
    c.execute('Drop table game_state')
    comand = "CREATE TABLE IF NOT EXISTS game_state("
    for i in range(len(columns)):
        comand += columns[i] + " " + values_type[i]
        if i < len(columns) - 1:
            comand += ", "
        else:
            comand += ")"

    c.execute(comand)
    c.execute('DELETE FROM game_state')  # Wyczyść poprzednie zapisy
    comand ='INSERT INTO game_state ('

    for i in range(len(columns)):
        comand += columns[i]
        if i < len(columns) - 1:
            comand += ", "
        else:
            comand += ")"

    comand += ' VALUES ('

    for i in range(len(values)):
        comand += str(values[i])
        if i < len(values) - 1:
            comand += ", "
        else:
            comand += ")"

    c.execute(comand)
    conn.commit()
    conn.close()

def load_game():
    conn = sqlite3.connect('savegame.db')
    c = conn.cursor()
    c.execute('PRAGMA table_info(game_state)')

    columns = [row[1] for row in c.fetchall()]

    comand = 'SELECT '

    for i in range(len(columns)):
        comand += columns[i]
        if i < len(columns) - 1:
            comand += ", "
        else:
            comand += " "

    comand += "FROM game_state"

    c.execute(comand)
    output = c.fetchone()
    state = list(output)
    conn.close()
    dictionary = dict(zip(columns, state))
    return dictionary

def choose_player():
    #samo okno
    okno_size = (1200,300)
    okno = pygame.surface.Surface(okno_size)
    okno.fill((50,50,50))
    pygame.draw.rect(okno, (230,230,230), (0,0, okno_size[0] - 2, okno_size[1] - 2))
    pygame.draw.rect(okno, (180,180,180), (2,2, okno_size[0] - 4, okno_size[1] - 4))

    screen.fill((130,231,22))
    screen.blit(okno,(20,200))
    pygame.display.update()

    #tekst
    input_box = pygame.Rect(0,0,300,50)
    input_box_surface = pygame.surface.Surface((input_box.w, input_box.h))

    text = ''
    color_inactive = pygame.Color((220,220,20))
    color_active = pygame.Color((220,30,220))
    color = color_inactive
    active = False
    font = pygame.font.SysFont(None, 24)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif event.key == pygame.K_RETURN:
                        print(text)
                        return text
                    else:
                        text += event.unicode
        # Rysowanie
        txt_surface = font.render(text, True, (0,0,0))
        pygame.draw.rect(screen, color, input_box)
        input_box_surface.blit(txt_surface, (5,5))
        screen.blit(input_box_surface, (200,200))
        pygame.display.update()


choose_player()
time.sleep(5)