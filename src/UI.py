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
    def __init__(self, size, color=(130, 130, 130)):
        self.size = size
        self.color = color
        self.draw_start_x, self.draw_star_y = 0, 50
        self.WIN_width, self.WIN_height = None, None

    def draw(self, WIN, WIN_width, WIN_height):
        self.WIN_width, self.WIN_height = WIN_width, WIN_height
        grid_x, grid_y = self.draw_start_x, self.draw_star_y
        while grid_y <= WIN_height:
            line = pygame.draw.line(WIN, self.color, (grid_x, grid_y), (WIN_width, grid_y), width=1)
            grid_y += self.size

        grid_y = 0

        while grid_x <= WIN_width:
            pygame.draw.line(WIN, self.color, (grid_x, grid_y), (grid_x, WIN_height), width=1)
            grid_x += self.size

    def get_best_xy(self, current_x, current_y):
        grid_x, grid_y = self.draw_start_x, self.draw_star_y
        while grid_x < self.WIN_width:
            if grid_x - current_x > 0:
                break
            grid_x += self.size

        while grid_y < self.WIN_height:
            if grid_y - current_y > 0:
                break
            grid_y += self.size


        return grid_x - self.size / 2, grid_y - self.size / 2

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

    def change_text(self, text):
        self.text = text
