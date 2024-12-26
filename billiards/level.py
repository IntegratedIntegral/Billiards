from settings import *
from ball import Ball
from hole import Hole

class Level:
    def __init__(self, app):
        #starting condition of the table. contains information about the positions of all of the balls and holes
        self.app = app
        self.white_ball = Ball((500, 400), (255, 255, 255))
        ball_positions = [
            (800, 520), (840, 520), (880, 520), (920, 520), (960, 520),
            (820, 485), (860, 485), (900, 485), (940, 485),
            (840, 450), (880, 450), (920, 450),
            (860, 415), (900, 415),
            (880, 380)
        ]
        ball_colours = [
            (199, 24 , 24 ), (54 , 155, 209), (227, 207, 25 ), (155, 52 , 179), (55 , 71 , 219),
            (20 , 217, 141), (232, 143, 26 ), (159, 224, 45 ), (237, 66 , 180),
            (46 , 46 , 46 ), (117, 84 , 30 ), (235, 148, 151),
            (13 , 74 , 23 ), (121, 139, 217),
            (17 , 144, 158)
        ]
        self.generate_coloured_balls(ball_positions, ball_colours)
        hole_positions = [
            (CORNER_HOLE_OFFSET, CORNER_HOLE_OFFSET),
            (WINDOW_WIDTH / 2, 0),
            (WINDOW_WIDTH - CORNER_HOLE_OFFSET, CORNER_HOLE_OFFSET),
            (WINDOW_WIDTH - CORNER_HOLE_OFFSET, WINDOW_HEIGHT - CORNER_HOLE_OFFSET),
            (WINDOW_WIDTH / 2, WINDOW_HEIGHT),
            (CORNER_HOLE_OFFSET, WINDOW_HEIGHT - CORNER_HOLE_OFFSET)
        ]
        self.generate_holes(hole_positions)

        self.end_reached = False
    
    def generate_coloured_balls(self, ball_positions, ball_colours):
        self.coloured_balls = []
        for pos, colour in zip(ball_positions, ball_colours):
            self.coloured_balls.append(Ball(pos, colour))
    
    def generate_holes(self, hole_positions):
        self.holes = []
        for pos in hole_positions:
            self.holes.append(Hole(pos))

    def update(self):
        #have any balls entered a hole?
        for h in self.holes:
            h.draw(self.app.window)

            for b in self.coloured_balls:
                if h.detect_ball(b):
                    #yes! a coloured ball has entered. it shall be deleted
                    self.coloured_balls.remove(b)
            
            if h.detect_ball(self.white_ball):
                #yes! the white ball has entered. game over!
                self.app.running = False
        
        self.white_ball.draw(self.app.window)
        self.white_ball.update(self.app.delta_t, self.coloured_balls)

        #have any balls collided with each other?
        for b in self.coloured_balls:
            b.draw(self.app.window)
            b.update(self.app.delta_t, self.coloured_balls)
            
            for b2 in self.coloured_balls:
                if b2 != b:
                    b.collide(b2)
            self.white_ball.collide(b)
        
        self.check_end()
    
    def check_end(self):
        if len(self.coloured_balls) == 0 and not self.end_reached:
            self.app.ui.end_reached = True
            self.end_reached = True
        elif self.end_reached:
            self.app.update_end_timer()