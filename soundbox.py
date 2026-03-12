import random, pygame, os
pygame.mixer.init()


def random_music(sound_folder):
    sound_files = [f for f in os.listdir(sound_folder) if f.endswith('.mp3')]
    return random.choice(sound_files)

def play_sound(sound_folder,sound = None, volume = 1.0):

    sound_folder = os.path.join("soundbox", sound_folder)
    if sound == None:
        sound = random_music(sound_folder)
    sound = pygame.mixer.Sound(os.path.join(sound_folder, sound))
    sound.set_volume(volume)
    sound.play()





