import pygame
from GameObject import *

class Inventory(GameObject):
    def __init__(self, x, y, width, height, color=(80, 80, 80)):
        super().__init__(x, y, width, height)
        self.color = color
        self.add_collision_box()

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.color, pygame.Rect(self.x, self.y, self.width, self.height))
