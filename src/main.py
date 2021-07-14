import pygame
import os
from GameObject import *
from Neuron import *
from UI import *

pygame.font.init()
pygame.display.set_caption('Neural Network Builder')
#pygame.display.set_icon(...)

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

EMPTY = pygame.Color(0, 0, 0, 0)

class App:
    def __init__(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, fps=60):
        #Basic window setup
        self.WIDTH = width
        self.HEIGHT = height
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        self.FPS = fps
        self.clock = pygame.time.Clock()

        #Lists that hold all objects of the programm
        self.objects = []
        self.buttons = []
        self.labels = []
            #mabye all surfaces into list -> "big" storage waste?

        self.object_in_hand = None

        #Grid setup and variables
        self.grid_enabled = True
        self.current_grid_size = 40
        self.grid = Grid(self.current_grid_size, color=(65, 65, 65))

        #TODO change depending on grid size
        self.neuron_size = int(self.current_grid_size / 2)

        #Different surfaces to safe fps
        self.background_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.neuron_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), flags=pygame.SRCALPHA)
        self.in_hand_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), flags=pygame.SRCALPHA)

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

                elif(event.type == pygame.MOUSEBUTTONUP and event.button == 1):
                    #Place object in hand on surface
                    if(self.object_in_hand and not self.objects[0].collision_box.clicked(Mouse_x, Mouse_y)):
                        self.place_object_in_hand()
                    else:
                        #Check if item is put in hand -> created by selecting from inventory
                        for obj in self.objects:
                            if(obj.collision_box and obj.collision_box.clicked(Mouse_x, Mouse_y)):
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

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.object_in_hand = None
                        self.in_hand_surface.fill(EMPTY)

            if self.object_in_hand:
                self.make_in_hand_surface()

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
                                    color=(211, 251, 216), type="Input", inv=True)
        self.objects.append(menu_neuron_input)
        menu_neuron_middle = Neuron(neuron_inv_spacing + (neuron_inv_spacing + 40), WINDOW_HEIGHT-60, self.neuron_size, self.neuron_size,
                                    color=(230, 230, 200), type="Middle", inv=True)
        self.objects.append(menu_neuron_middle)
        menu_neuron_output = Neuron(neuron_inv_spacing + 2*(neuron_inv_spacing + 40), WINDOW_HEIGHT-60, self.neuron_size, self.neuron_size,
                                    color=(239, 160, 162), type="Output", inv=True)
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
        self.redraw_window()

    def redraw_object_at_new_location(self):
        self.objects[0].redraw(y=WINDOW_HEIGHT-100, width=WINDOW_WIDTH)
        self.objects[1].redraw(width=WINDOW_WIDTH)
        self.objects[2].redraw(y=WINDOW_HEIGHT-60)
        self.objects[3].redraw(y=WINDOW_HEIGHT-60)
        self.objects[4].redraw(y=WINDOW_HEIGHT-60)

    def make_background_surface(self):
        self.background_surface.fill((48, 48, 48))

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
        #Draw objects
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
        if self.object_in_hand:
            self.in_hand_surface.fill(EMPTY)
            Mouse_x, Mouse_y = pygame.mouse.get_pos()
            self.object_in_hand.redraw(x=Mouse_x, y=Mouse_y)
            self.object_in_hand.draw(self.in_hand_surface)

    def draw_fps(self):
        fps_background = Inventory(WINDOW_WIDTH - 100, 10, 100, 30)
        fps_background.draw(self.WIN)
        fps_label = Label(WINDOW_WIDTH - 75, 15, 100, 15, text=str(round(self.clock.get_fps(), 0)), name="fps_label", color=(0, 230, 0))
        fps_label.draw(self.WIN)
        pygame.display.update()

    def check_grid_button_clicks(self, button):#
        grid_change = 2

        if button.name == "grid_button" and button.is_pressed:
            self.grid_enabled = True
        elif button.name == "grid_button" and not button.is_pressed:
            self.grid_enabled = False

        elif button.name == "grid_smaller":
            for l in self.labels:
                if l.name == "grid_size_label" and self.grid.size > grid_change:
                    l.text = str(int(l.text) - grid_change)
                    self.current_grid_size -= grid_change
                    self.grid.size = self.current_grid_size
                    self.neuron_size = int(self.current_grid_size / 2)
                    self.give_neuron_new_size_and_pos()
        elif button.name == "grid_bigger":
            for l in self.labels:
                if l.name == "grid_size_label":
                    l.text = str(int(l.text) + grid_change)
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
        if(obj.obj_type == "Neuron" and obj.inv):
            new_Neuron = Neuron(obj.x, obj.y, self.neuron_size, self.neuron_size,
                                color=obj.color, type=None)
            self.object_in_hand = new_Neuron
        elif(obj.obj_type == "Neuron" and not obj.inv):
            self.objects.remove(obj)
            self.object_in_hand = obj
            self.make_background_surface()
            self.make_neuron_surface()

if __name__ == "__main__":
    app = App()
    app.run()
