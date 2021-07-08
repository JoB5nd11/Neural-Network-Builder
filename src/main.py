import pygame
pygame.font.init()
pygame.display.set_caption('Neural Network Builder')
#pygame.display.set_icon(...)

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

class GameObject:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, WIN):
        pass

    def move(self):
        pass

    def redraw_size(self, x=None, y=None, width=None, height=None):
        if x:
            self.x = x
        if y:
            self.y = y
        if width:
            self.width = width
        if height:
            self.height = height

class Neuron(GameObject):
    def __init__(self, x, y, width, height, color=(230, 230, 230), type=None,
                 text_color=(230, 230, 230), text_margin=10, inv=False):
        super().__init__(x, y, width, height)
        self.color = color
        self.type = type
        self.text_color = text_color
        self.text_margin = text_margin

    def draw(self, WIN):
        pygame.draw.circle(WIN, self.color, (self.x, self.y), self.width)
        self.draw_label(WIN)

    def draw_label(self, WIN):
        #initialize font
        label_font = pygame.font.SysFont("rubik", 25)

        #render text
        label = label_font.render(str(self.type), 1, self.text_color)
        WIN.blit(label, (self.x - int(label.get_width() / 2), self.y + self.height + self.text_margin))

class Inventory(GameObject):
    def __init__(self, x, y, width, height, color=(80, 80, 80)):
        super().__init__(x, y, width, height)
        self.color = color

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

class App:
    def __init__(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, fps=60):
        self.WIDTH = width
        self.HEIGHT = height
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        self.FPS = fps
        self.clock = pygame.time.Clock()
        self.objects = []

        self.setup()

    def run(self):
        global WINDOW_WIDTH, WINDOW_HEIGHT
        run = True
        while run:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                elif event.type == pygame.VIDEORESIZE:
                    WINDOW_WIDTH, WINDOW_HEIGHT = event.dict["size"]
                    self.objects[0].redraw_size(y=WINDOW_HEIGHT-100, width=WINDOW_WIDTH)
                    self.objects[1].redraw_size(y=WINDOW_HEIGHT-60)
                    self.objects[2].redraw_size(y=WINDOW_HEIGHT-60)
                    self.objects[3].redraw_size(y=WINDOW_HEIGHT-60)

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
                                    color=(134, 133, 239), type="Output", inv=True)
        self.objects.append(menu_neuron_output)

    def redraw_window(self):
        self.WIN.fill((48, 48, 48))
        #draw stuff
        for obj in self.objects:
            obj.draw(self.WIN)

        pygame.display.update()

if __name__ == "__main__":
    app = App()
    app.run()
