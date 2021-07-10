import pygame
from GameObject import *

class Neuron(GameObject):
    def __init__(self, x, y, width, height, color=(230, 230, 230), type=None,
                 text_color=(230, 230, 230), text_margin=10, inv=False):
        super().__init__(x, y, width, height)
        self.obj_type = "Neuron"
        self.color = color
        self.type = type
        self.text_color = text_color
        self.text_margin = text_margin
        self.inv = inv
        self.add_collision_box()

    def draw(self, WIN):
        pygame.draw.circle(WIN, self.color, (self.x, self.y), self.width)
        self.draw_label(WIN)

    def draw_label(self, WIN):
        #initialize font
        label_font = pygame.font.SysFont("rubik", 25)

        #render text
        if self.type:
            label = label_font.render(str(self.type), 1, self.text_color)
            WIN.blit(label, (self.x - int(label.get_width() / 2), self.y + self.height + self.text_margin))
