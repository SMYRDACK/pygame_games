import random
import pygame
from settings import *
from map import Map
from player import Player
from walls import Walls, Grass
from music import *
from enemy import Enemy, Drop_items
from soundbox import *
from portal import Portal, Box, Gem
"""
załozenia gry:
mamy mapę i gracza.
gracz porusza sie po mapie typu labirynt i pokonuje przeciwnikow za monety
znajduje skrzynki z roznymi przedmiotami broniami
przechodzi labirynt znajdując wejscie wyzej
kazde pietro coraz ciezsze
"""
"""
main task:
ogarnij postać gracza oraz mapę

zrób animacje ruchu i sterowanie

dodaj pociski

dodaj przeciwnika

zrob widocznosc pola widzenia gracza

zrob ruch przeciwnikow
"""

pygame.init()

#kursor
pygame.mouse.set_visible(False)
celownik_kursor = pygame.image.load("graphic/celownik.png")
kursor = pygame.surface.Surface(celownik_kursor.get_size(), pygame.SRCALPHA)
kursor.set_alpha(100)

#sprites groups
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
        play_sound("get_hit")
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


