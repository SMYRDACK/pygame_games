import pygame

# Inicjalizacja Pygame
pygame.init()

# Stałe
FRAME_WIDTH = 64
FRAME_HEIGHT = 64
SPRITE_SHEET_PATH = 'kaczka.png'
FPS = 10
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Ładowanie sprite sheet
sprite_sheet = pygame.image.load(SPRITE_SHEET_PATH)

# Funkcja do wyodrębniania klatek animacji
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

# Uzyskiwanie klatek animacji
frames = get_frames(sprite_sheet, FRAME_WIDTH, FRAME_HEIGHT)

# Tworzenie okna Pygame do wyświetlenia animacji
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Animacja Sprite Sheet')

# Główna pętla programu
running = True
clock = pygame.time.Clock()
frame_index = 0
direction = 0  # 0 = w prawo, 1 = w górę, 2 = w dół, 3 = w lewo
x, y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
speed = 5

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Pobieranie stanu klawiatury
    keys = pygame.key.get_pressed()
    stop=False
    if keys[pygame.K_d]:
        direction = 2
        x += speed
    elif keys[pygame.K_w]:
        direction = 3
        y -= speed
    elif keys[pygame.K_s]:
        direction = 0
        y += speed
    elif keys[pygame.K_a]:
        direction = 1
        x -= speed
    else:
        stop=True

    # Ograniczanie ruchu postaci do obszaru okna
    x = max(0, min(SCREEN_WIDTH - FRAME_WIDTH, x))
    y = max(0, min(SCREEN_HEIGHT - FRAME_HEIGHT, y))

    # Wyświetlanie odpowiedniej klatki animacji
    screen.fill((0, 0, 0))  # Wypełnianie tła kolorem czarnym
    screen.blit(frames[direction][frame_index], (x, y))

    # Aktualizacja ekranu
    pygame.display.flip()

    # Następna klatka animacji
    if not stop:
        frame_index = (frame_index + 1) % len(frames[direction])
    else:
        frame_index = 0

    # Czekanie na następną klatkę
    clock.tick(FPS)

# Zakończenie programu
pygame.quit()
