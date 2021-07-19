import pygame
from Constants import *

class GameObject:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.obj_type = None
        self.collision_box = None
        self.grid_x, self.grid_y = None, None

    def draw(self, WIN):
        pass

    def move(self):
        pass

    def redraw(self, x=None, y=None, width=None, height=None):
        if x:
            self.x = x
        if y:
            self.y = y
        if width:
            self.width = width
        if height:
            self.height = height

        if self.collision_box:
            self.add_collision_box()

    def add_collision_box(self):
        self.collision_box = CollisionBox(obj=self)

class CollisionBox(GameObject):
    def __init__(self, x=None, y=None, width=None, height=None, obj=None):
        self.color = WHITE
        if obj:
            if obj.obj_type == "Neuron":
                super().__init__(obj.x - obj.width, obj.y - obj.height, obj.width*2, obj.height*2)
            else:
                super().__init__(obj.x, obj.y, obj.width, obj.height)
        else:
            super().__init__(x, y, width, height)

    def clicked(self, Mouse_x, Mouse_y):
        if(Mouse_x > self.x and Mouse_y > self.y and Mouse_x < self.x + self.width and Mouse_y < self.y + self.height):
            return True
        return False

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.color, pygame.Rect(self.x, self.y, self.width, self.height))
