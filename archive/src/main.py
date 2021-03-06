#Import python standard libraries
import pygame
import importlib
import sys
import os

#Import own libraries for game
from Constants import *
from GameObject import *
from Neuron import *
from UI import *

#Import surfaces
#TODO

pygame.font.init()
pygame.display.set_caption('Neural Network Builder')
#pygame.display.set_icon(...)

class App:
    def __init__(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, fps=60):
        #Basic window setup
        self.WIDTH = width
        self.HEIGHT = height
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        self.FPS = fps
        self.clock = pygame.time.Clock()
        self.temp = None

        #Visual variables ?
        self.line_width = 2

        #Lists that hold all objects of the programm
        self.objects = []
        self.buttons = []
        self.labels = []
            #mabye all surfaces into list -> "big" storage waste?

        #seems like too many selection variables?
        self.object_in_hand = None
        self.objects_are_in_hand = False
        self.select = SelectBox(0, 0, 0, 0)
        self.select2 = SelectBox(0, 0, 0, 0)
        self.objects_selected = []
        self.is_selected = False
        self.still_selected = False

        #Grid setup and variables
        self.grid_enabled = True
        self.current_grid_size = 40
        self.grid = Grid(self.current_grid_size, color=LIGHT_GRAY)

        self.neuron_size = int(self.current_grid_size / 2)

        #Different surfaces to safe fps
        self.background_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.neuron_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), flags=pygame.SRCALPHA)
        self.in_hand_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), flags=pygame.SRCALPHA)
        self.selected_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), flags=pygame.SRCALPHA)

        self.setup()

    def run(self):
        global WINDOW_WIDTH, WINDOW_HEIGHT
        run = True
        #Main Game Loop
        while run:
            self.draw_fps()
            self.clock.tick(self.FPS)
            #self.clock.tick()

            Mouse_x, Mouse_y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                elif event.type == pygame.VIDEORESIZE:
                    #If Windowsize changes
                    WINDOW_WIDTH, WINDOW_HEIGHT = event.dict["size"]
                    self.background_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                    self.in_hand_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), flags=pygame.SRCALPHA)
                    self.neuron_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), flags=pygame.SRCALPHA)
                    self.make_and_redraw_window()

                elif(event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    #Check if line is beginning to be drawn
                    for obj in self.objects:
                        if(obj.collision_box and obj.collision_box.clicked(Mouse_x, Mouse_y) and obj.obj_type=="Neuron" and not obj.inv):
                            self.temp = obj
                            break
                    else:
                        self.is_selected = True
                        self.still_selected = True
                        self.select.x, self.select.y = Mouse_x, Mouse_y
                        self.make_in_hand_surface()


                elif(event.type == pygame.MOUSEBUTTONUP and event.button == 1):
                    if self.is_selected:
                        self.is_selected = False
                        #self.select = SelectBox(0, 0, 0, 0)
                        self.check_for_selected_items()

                    #End line drawn from another neuron
                    elif self.temp:
                        for obj in self.objects:
                            if(obj != self.temp and obj.collision_box and obj.collision_box.clicked(Mouse_x, Mouse_y)
                                                 and obj.obj_type=="Neuron" and not obj.inv):
                                # Add neurons to connect list
                                if(obj in self.temp.connect_to and self.temp in obj.connect_from):
                                    self.temp.connect_to.remove(obj)
                                    obj.connect_from.remove(self.temp)
                                elif(obj not in self.temp.connect_to and self.temp not in obj.connect_from):
                                    self.temp.connect_to.append(obj)
                                    obj.connect_from.append(self.temp)
                                self.make_neuron_surface()
                                break
                        #If the line is not released on a neuron it is dropped
                        #Otherwhise is kept, so no other object can be picked up
                        else:
                            self.temp = None

                    if self.objects_are_in_hand:
                        print("objects are now out of hand")
                        self.objects_are_in_hand = False

                    #Place object in hand on surface
                    if(self.object_in_hand and not self.objects[0].collision_box.clicked(Mouse_x, Mouse_y)):
                        self.place_object_in_hand()
                    else:
                        #Check if item is put in hand -> created by selecting from inventory
                        for obj in self.objects:
                            if(obj.collision_box and obj.collision_box.clicked(Mouse_x, Mouse_y) and not self.temp):
                                self.put_neuron_in_hand(obj)

                        #Check for button presses
                        for button in self.buttons:
                            if(button.collision_box and button.collision_box.clicked(Mouse_x, Mouse_y)):
                                if button.is_toggle and not button.is_pressed:
                                    button.is_pressed = True
                                elif button.is_toggle and button.is_pressed:
                                    button.is_pressed = False

                                button.draw(self.WIN)
                                self.check_grid_button_clicks(button)

                    self.temp = None

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.object_in_hand = None
                        self.in_hand_surface.fill(EMPTY)

            if self.object_in_hand or self.is_selected:
                self.make_in_hand_surface()

            if len(self.objects_selected) > 0:
                self.make_selected_surface()

            self.redraw_window()

    def setup(self):
        #Inventories (top and bottom)
        inv = Inventory(0, WINDOW_HEIGHT-100, WINDOW_WIDTH, 100)
        self.objects.append(inv)
        menu = Inventory(0, 0, WINDOW_WIDTH, 50)
        self.objects.append(menu)

        #Neuron in Inventory
        neuron_inv_spacing = 70
        menu_neuron_input = Neuron(neuron_inv_spacing, WINDOW_HEIGHT-60, self.neuron_size, self.neuron_size,
                                    color=LIGHT_GREEN, type="Input", inv=True)
        self.objects.append(menu_neuron_input)
        menu_neuron_middle = Neuron(neuron_inv_spacing + (neuron_inv_spacing + 40), WINDOW_HEIGHT-60, self.neuron_size, self.neuron_size,
                                    color=LIGHT_YELLOW, type="Middle", inv=True)
        self.objects.append(menu_neuron_middle)
        menu_neuron_output = Neuron(neuron_inv_spacing + 2*(neuron_inv_spacing + 40), WINDOW_HEIGHT-60, self.neuron_size, self.neuron_size,
                                    color=LIGHT_RED, type="Output", inv=True)
        self.objects.append(menu_neuron_output)

        #Path to image files
        mediapath = os.path.abspath(os.path.join(os.getcwd(), os.pardir) + str("\\media\\"))

        #Grid Button
        grid_button = ImgButton(10, 10, 30, 30, img=str(mediapath + "\\grid_off.png"), img_pressed=str(mediapath + "\\grid_on.png"),
                                                toggle=True, name ="grid_button", is_pressed=True)
        self.buttons.append(grid_button)
        #Arrow buttons and size number display
        arrow_left_button = ImgButton(60, 10, 30, 30, img=str(mediapath + "\\arrow_left.png"), name="grid_smaller")
        self.buttons.append(arrow_left_button)
        grid_detail_label = Label(95, 10, 30, 30, text=str(self.current_grid_size), name="grid_size_label")
        self.labels.append(grid_detail_label)
        arrow_right_button = ImgButton(130, 10, 30, 30, img=str(mediapath + "\\arrow_right.png"), name="grid_bigger")
        self.buttons.append(arrow_right_button)

        #Draw all Surfaces for the first time
        self.make_background_surface()
        self.make_in_hand_surface()
        self.redraw_window()

    def redraw_window(self):
        self.WIN.blit(self.background_surface, (0, 0))
        self.WIN.blit(self.in_hand_surface, (0, 0))
        self.WIN.blit(self.neuron_surface, (0, 0))
        self.draw_fps()

        pygame.display.update()

    def make_and_redraw_window(self):
        self.redraw_object_at_new_location()
        self.make_background_surface()
        self.make_neuron_surface()
        self.make_in_hand_surface()
        self.make_selected_surface()
        self.redraw_window()

    def redraw_object_at_new_location(self):
        self.objects[0].redraw(y=WINDOW_HEIGHT-100, width=WINDOW_WIDTH)
        self.objects[1].redraw(width=WINDOW_WIDTH)
        self.objects[2].redraw(y=WINDOW_HEIGHT-60)
        self.objects[3].redraw(y=WINDOW_HEIGHT-60)
        self.objects[4].redraw(y=WINDOW_HEIGHT-60)

    def make_background_surface(self):
        self.background_surface.fill(GRAY)

        if self.grid_enabled:
            self.grid.draw(self.background_surface, WINDOW_WIDTH, WINDOW_HEIGHT)

        #Draw objects
        for obj in self.objects:
            if(obj.obj_type != "Neuron" or (obj.obj_type == "Neuron" and obj.inv)):
                obj.draw(self.background_surface)
            if obj.collision_box:
                #obj.collision_box.draw(self.background_surface)
                pass

        #Draw buttons
        for b in self.buttons:
            b.draw(self.background_surface)
            if b.collision_box:
                #b.collision_box.draw(self.background_surface)
                pass

        #Draw labels
        for l in self.labels:
            l.draw(self.background_surface)
            if l.collision_box:
                #l.collision_box.draw(self.background_surface)
                pass

    def make_neuron_surface(self):
        self.neuron_surface.fill(EMPTY)

        #Draw Lines
        for obj in self.objects:
            if obj.obj_type == "Neuron" and not obj.inv:
                for end in obj.connect_to:
                    pygame.draw.line(self.neuron_surface, WHITE, (obj.x, obj.y), (end.x, end.y), self.line_width)

        #Draw Neurons
        for obj in self.objects:
            if obj.obj_type == "Neuron":
                obj.draw(self.neuron_surface)
            if obj.collision_box:
                #obj.collision_box.draw(self.background_surface)
                pass

        inv = self.objects[0]
        pygame.draw.rect(self.neuron_surface, EMPTY, pygame.Rect(inv.x, inv.y, inv.width, inv.height))

    def give_neuron_new_size_and_pos(self):
        for obj in self.objects:
            if obj.obj_type == "Neuron" and not obj.inv:
                obj.width, obj.height = self.neuron_size, self.neuron_size
                obj.x, obj.y, obj.grid_x, obj.grid_y = self.grid.place_at_grid_pos(obj)
                obj.add_collision_box()


    def make_in_hand_surface(self):
        self.make_neuron_surface() #is needed so synapses are drawn correctly
        self.in_hand_surface.fill(EMPTY)

        if self.object_in_hand:
            Mouse_x, Mouse_y = pygame.mouse.get_pos()
            if self.object_in_hand.obj_type == "Neuron":
                for point in self.object_in_hand.connect_from:
                    pygame.draw.line(self.in_hand_surface, WHITE, (self.object_in_hand.x, self.object_in_hand.y), (point.x, point.y), self.line_width)
                for point in self.object_in_hand.connect_to:
                    pygame.draw.line(self.in_hand_surface, WHITE, (self.object_in_hand.x, self.object_in_hand.y), (point.x, point.y), self.line_width)
            self.object_in_hand.redraw(x=Mouse_x, y=Mouse_y)
            self.object_in_hand.draw(self.in_hand_surface)

        elif self.is_selected or self.still_selected: #what is still_selected?!
            self.draw_selection_box()

        inv1, inv2 = self.objects[0], self.objects[1]
        pygame.draw.rect(self.in_hand_surface, EMPTY, pygame.Rect(inv1.x, inv1.y, inv1.width, inv1.height))
        pygame.draw.rect(self.in_hand_surface, EMPTY, pygame.Rect(inv2.x, inv2.y, inv2.width, inv2.height))

    def draw_fps(self):
        fps_background = Inventory(WINDOW_WIDTH - 100, 10, 100, 30)
        fps_background.draw(self.WIN)
        fps = self.clock.get_fps()
        if fps > 40:
            fps_label = Label(WINDOW_WIDTH - 75, 15, 100, 15, text=str(round(fps, 0)), name="fps_label", color=CONTRAST_GREEN)
        elif fps > 24:
            fps_label = Label(WINDOW_WIDTH - 75, 15, 100, 15, text=str(round(fps, 0)), name="fps_label", color=CONTRAST_YELLOW)
        else:
            fps_label = Label(WINDOW_WIDTH - 75, 15, 100, 15, text=str(round(fps, 0)), name="fps_label", color=CONTRAST_RED)
        fps_label.draw(self.WIN)
        pygame.display.update()

    def check_grid_button_clicks(self, button):
        grid_change = 2

        #grid on/off
        if button.name == "grid_button" and button.is_pressed:
            self.grid_enabled = True
        elif button.name == "grid_button" and not button.is_pressed:
            self.grid_enabled = False

        #Grid size changes
        elif(button.name == "grid_smaller" or button.name == "grid_bigger"):
            if button.name == "grid_smaller":
                #negative change = smaller
                grid_change *= -1
            for l in self.labels:
                if l.name == "grid_size_label" and self.grid.size > grid_change:
                    #change grid size label
                    l.text = str(int(l.text) + grid_change)
                    #change grid size
                    self.current_grid_size += grid_change
                    self.grid.size = self.current_grid_size
                    self.neuron_size = int(self.current_grid_size / 2)
                    self.give_neuron_new_size_and_pos()
        else:
            return

        self.make_background_surface()
        self.make_neuron_surface()

    def place_object_in_hand(self):
        if self.grid_enabled:
            self.object_in_hand.x, self.object_in_hand.y, self.object_in_hand.grid_x, self.object_in_hand.grid_y = self.grid.get_best_xy(self.object_in_hand.x, self.object_in_hand.y)
            self.object_in_hand.add_collision_box()
        self.objects.append(self.object_in_hand)
        self.object_in_hand = None
        self.make_background_surface()
        self.make_neuron_surface()
        self.in_hand_surface.fill(EMPTY)

    def put_neuron_in_hand(self, obj):
        if obj in self.objects_selected:
            self.objects_are_in_hand = True

        elif(obj.obj_type == "Neuron" and obj.inv):
            new_Neuron = Neuron(obj.x, obj.y, self.neuron_size, self.neuron_size,
                                color=obj.color, type=None)
            self.object_in_hand = new_Neuron
        elif(obj.obj_type == "Neuron" and not obj.inv):
            self.objects.remove(obj)
            self.object_in_hand = obj
            self.make_background_surface()
            self.make_neuron_surface()

    def draw_selection_box(self):
        #Smart xD
        Mouse_x, Mouse_y = pygame.mouse.get_pos()
        self.select2 = SelectBox(self.select.x, self.select.y, abs(Mouse_x - self.select.x), abs(Mouse_y - self.select.y))
        if Mouse_x >= self.select.x and Mouse_y < self.select.y:
            self.select2.y = Mouse_y
        elif Mouse_x < self.select.x and Mouse_y >= self.select.y:
            self.select2.x = Mouse_x
        elif Mouse_x < self.select.x and Mouse_y < self.select.y:
            self.select2.x = Mouse_x
            self.select2.y = Mouse_y
        self.select2.draw(self.in_hand_surface)

    def check_for_selected_items(self):
        self.object_selected = []
        for obj in self.objects:
            if(obj.x > self.select2.x and obj.y > self.select2.y and obj.x + obj.width < self.select2.x + self.select2.width
                                                                 and obj.y + obj.height < self.select2.y + self.select2.height):
                self.objects_selected.append(obj)

    def make_selected_surface(self):
        if self.objects_are_in_hand:
            self.selected_surface.fill(EMPTY)
            print("objects are now in hand")
            #that a task for tomorrow? #TODO draw selected at hand


"""
NOTES:
------
for obj in self.objects_selected:
    self.object_in_hand = obj
    self.place_object_in_hand()
"""

if __name__ == "__main__":
    app = App()
    app.run()
