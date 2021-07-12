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

class App:
    def __init__(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, fps=60):
        self.WIDTH = width
        self.HEIGHT = height
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        self.FPS = fps
        self.clock = pygame.time.Clock()
        self.objects = []
        self.buttons = []
        self.labels = []
        self.object_in_hand = None

        self.setup()

    def run(self):
        global WINDOW_WIDTH, WINDOW_HEIGHT, CLICK_DOWN
        run = True
        while run:
            self.clock.tick(self.FPS)
            Mouse_x, Mouse_y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                elif event.type == pygame.VIDEORESIZE:
                    WINDOW_WIDTH, WINDOW_HEIGHT = event.dict["size"]
                    self.objects[0].redraw(y=WINDOW_HEIGHT-100, width=WINDOW_WIDTH)
                    self.objects[1].redraw(width=WINDOW_WIDTH)
                    self.objects[2].redraw(y=WINDOW_HEIGHT-60)
                    self.objects[3].redraw(y=WINDOW_HEIGHT-60)
                    self.objects[4].redraw(y=WINDOW_HEIGHT-60)

                elif(event.type == pygame.MOUSEBUTTONUP and event.button == 1):
                    if(self.object_in_hand and not self.objects[0].collision_box.clicked(Mouse_x, Mouse_y)):
                        self.objects.append(self.object_in_hand)
                        self.object_in_hand = None
                    else:
                        for obj in self.objects:
                            if(obj.collision_box and obj.collision_box.clicked(Mouse_x, Mouse_y)):
                                if(obj.obj_type == "Neuron" and obj.inv):
                                    new_Neuron = Neuron(obj.x, obj.y, obj.width, obj.height,
                                                        color=obj.color, type=None)
                                    self.object_in_hand = new_Neuron
                                elif(obj.obj_type == "Neuron" and not obj.inv):
                                    self.object_in_hand = obj

                        for button in self.buttons:
                            if(button.collision_box and button.collision_box.clicked(Mouse_x, Mouse_y)):
                                if button.is_toggle and not button.is_pressed:
                                    button.is_pressed = True
                                    button.draw(self.WIN)
                                elif button.is_toggle and button.is_pressed:
                                    button.is_pressed = False
                                    button.draw(self.WIN)

                                elif button.name == "grid_smaller":
                                    for l in self.labels:
                                        if l.name == "grid_size_label":
                                            l.text = str(int(l.text) - 1)
                                            l.draw(self.WIN)
                                elif button.name == "grid_bigger":
                                    for l in self.labels:
                                        if l.name == "grid_size_label":
                                            l.text = str(int(l.text) + 1)
                                            l.draw(self.WIN)


                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.object_in_hand = None

            for obj in self.objects:
                obj.move()

            self.redraw_window()

    def setup(self):
        #Inventory
        inv = Inventory(0, WINDOW_HEIGHT-100, WINDOW_WIDTH, 100)
        self.objects.append(inv)
        menu = Inventory(0, 0, WINDOW_WIDTH, 50)
        self.objects.append(menu)

        #Neuron in Inventory
        neuron_inv_spacing = 70
        menu_neuron_input = Neuron(neuron_inv_spacing, WINDOW_HEIGHT-60, 20, 20,
                                    color=(211, 251, 216), type="Input", inv=True)
        self.objects.append(menu_neuron_input)
        menu_neuron_middle = Neuron(neuron_inv_spacing + (neuron_inv_spacing + 40), WINDOW_HEIGHT-60, 20, 20,
                                    color=(230, 230, 200), type="Middle", inv=True)
        self.objects.append(menu_neuron_middle)
        menu_neuron_output = Neuron(neuron_inv_spacing + 2*(neuron_inv_spacing + 40), WINDOW_HEIGHT-60, 20, 20,
                                    color=(239, 160, 162), type="Output", inv=True)
        self.objects.append(menu_neuron_output)

        #Img Buttons
        mediapath = os.path.abspath(os.path.join(os.getcwd(), os.pardir) + str("\\media\\"))

        grid_button = ImgButton(10, 10, 30, 30, img=str(mediapath + "\\grid_off.png"), img_pressed=str(mediapath + "\\grid_on.png"), toggle=True)
        self.buttons.append(grid_button)

        arrow_left_button = ImgButton(60, 10, 30, 30, img=str(mediapath + "\\arrow_left.png"), name="grid_smaller")
        self.buttons.append(arrow_left_button)
        grid_detail_label = Label(95, 10, 30, 30, text="10", name="grid_size_label")
        self.labels.append(grid_detail_label)
        arrow_right_button = ImgButton(130, 10, 30, 30, img=str(mediapath + "\\arrow_right.png"), name="grid_bigger")
        self.buttons.append(arrow_right_button)

    def redraw_window(self):
        self.WIN.fill((48, 48, 48))
        #draw stuff
        for obj in self.objects:
            obj.draw(self.WIN)
            if obj.collision_box:
                #obj.collision_box.draw(self.WIN)
                pass

        self.draw_buttons()
        self.draw_labels()

        if self.object_in_hand:
            Mouse_x, Mouse_y = pygame.mouse.get_pos()
            self.object_in_hand.redraw(x=Mouse_x, y=Mouse_y)
            self.object_in_hand.draw(self.WIN)

        pygame.display.update()

    def draw_buttons(self):
        for b in self.buttons:
            b.draw(self.WIN)
            if b.collision_box:
                #b.collision_box.draw(self.WIN)
                pass

    def draw_labels(self):
        for l in self.labels:
            l.draw(self.WIN)
            if l.collision_box:
                #l.collision_box.draw(self.WIN)
                pass

if __name__ == "__main__":
    app = App()
    app.run()
