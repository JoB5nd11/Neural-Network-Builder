import pygame
from GameObject import *

class Inventory(GameObject):
    def __init__(self, x, y, width, height, color=(80, 80, 80)):
        super().__init__(x, y, width, height)
        self.color = color
        self.add_collision_box()

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

class Grid:
    def __init__(self, size):
        self.size = size

    def draw(self, WIN):
        pass

class ImgButton(GameObject):
    def __init__(self, x, y, width, height, img=None, img_pressed=None, toggle=False, name=None):
        super().__init__(x, y, width, height)
        self.img = img
        self.img_pressed = img_pressed
        self.is_pressed = False
        self.is_toggle = toggle
        self.name = name
        self.add_collision_box()

    def draw(self, WIN):
        if self.is_pressed:
            display_img = pygame.image.load(self.img_pressed)
        else:
            display_img = pygame.image.load(self.img)

        display_img = pygame.transform.scale(display_img, (self.width, self.height))
        WIN.blit(display_img, (self.x, self.y))

class Label(GameObject):
    def __init__(self, x, y, width, height, text="", color=(230, 230, 230), name=None):
        super().__init__(x, y, width, height)
        self.text = text
        self.color = color
        self.name = name
        self.add_collision_box()

    def draw(self, WIN):
        i = 1
        label_font = pygame.font.SysFont("rubik", 1)
        while(label_font.size(self.text)[0] < self.width and label_font.size(self.text)[1] < self.height):
            i += 1
            label_font = pygame.font.SysFont("rubik", i)

        label = label_font.render(str(self.text), 1, self.color)
        WIN.blit(label, (self.x + int(self.width / 2 - label_font.size(self.text)[0] / 2), 
                         self.y + int(self.height / 2 - label_font.size(self.text)[1] / 2)))
