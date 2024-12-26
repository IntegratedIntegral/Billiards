from settings import *
from level import Level
from stick import Stick
from ui import UI

class Main():
    def __init__(self):
        pg.init()
        
        self.running = True
        self.window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.level = Level(self)

        self.stick = Stick(self)

        self.ui = UI()

        self.clock = pg.time.Clock()
        self.delta_t = 0

        self.hits = 0

        self.end_timer = 5000
    
    def update(self):
        pg.display.set_caption(f"{self.clock.get_fps() :.0f}")
        
        self.level.update()
        self.stick.update()
        self.ui.update(self.window)
    
    def update_end_timer(self):
        self.end_timer = max(self.end_timer - self.delta_t, 0)
        if self.end_timer == 0:
            self.running = False

    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    self.stick.hit_white_ball()
            
            self.window.fill((29, 161, 38))
            
            self.update()

            self.delta_t = self.clock.tick(120)

            pg.display.flip()

app = Main()
app.run()