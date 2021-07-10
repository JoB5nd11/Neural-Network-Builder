import pygame
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
                    self.objects[1].redraw(y=WINDOW_HEIGHT-60)
                    self.objects[2].redraw(y=WINDOW_HEIGHT-60)
                    self.objects[3].redraw(y=WINDOW_HEIGHT-60)

                elif(event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
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

    def redraw_window(self):
        self.WIN.fill((48, 48, 48))
        #draw stuff
        for obj in self.objects:
            obj.draw(self.WIN)
            if obj.collision_box:
                #obj.collision_box.draw(self.WIN)
                pass

        if self.object_in_hand:
            Mouse_x, Mouse_y = pygame.mouse.get_pos()
            self.object_in_hand.redraw(x=Mouse_x, y=Mouse_y)
            self.object_in_hand.draw(self.WIN)

        pygame.display.update()

if __name__ == "__main__":
    app = App()
    app.run()
