import pygame
import threading
import time

def zadanie_poboczne():
    while True:
        print("Zadanie poboczne działa")
        time.sleep(2)  # symulacja długiej operacji

# Uruchomienie wątku dla zadania pobocznego
thread = threading.Thread(target=zadanie_poboczne)
thread.daemon = True
thread.start()

# Inicjalizacja Pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
running = True

# Główna pętla gry
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    print("petla glowna dziala")
    screen.fill((0, 0, 0))
    pygame.display.flip()

pygame.quit()