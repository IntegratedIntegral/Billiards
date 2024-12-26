from settings import pg, WHITE_BALL_SENSITIVITY, HIT_THRESHOLD
from path import Path

#you don't actually see a stick, it is just a class for handling the white ball
class Stick:
    def __init__(self, app):
        self.app = app
        self.ball = app.level.white_ball
        self.rel_mouse_pos = None

        self.path = Path(self.app.level)
    
    def get_rel_mouse_pos(self):
        #get the mouse position relative to the white ball
        mouse_pos = pg.mouse.get_pos()
        rel_mouse_pos = mouse_pos - self.ball.pos
        return pg.Vector2(rel_mouse_pos)
    
    def update(self):
        self.rel_mouse_pos = self.get_rel_mouse_pos()
        self.can_hit = self.ball.vel.magnitude_squared() < HIT_THRESHOLD * HIT_THRESHOLD

        if self.can_hit:
            #draw the trajectory of the white ball if its speed is low enough
            self.path.draw(self.app.window, self.rel_mouse_pos, self.app.level.coloured_balls)
    
    def hit_white_ball(self):
        #strike the white ball if its speed is low enough
        if self.can_hit:
            self.ball.vel = WHITE_BALL_SENSITIVITY * self.rel_mouse_pos
            self.app.hits += 1
            self.app.ui.hits = self.app.hits