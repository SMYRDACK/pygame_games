import pygame, sys
from settings import *

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


