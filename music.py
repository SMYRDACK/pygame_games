import random, pygame, os
pygame.mixer.init()
music_folder = 'music'

def random_music():
    music_files = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]
    return random.choice(music_files)

def play_music():
    if not pygame.mixer.music.get_busy():  # Sprawdzenie czy muzyka jest odtwarzana
        next_song = random_music()
        pygame.mixer.music.load(os.path.join(music_folder, next_song))
        pygame.mixer.music.play()
