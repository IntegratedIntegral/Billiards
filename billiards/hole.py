from settings import pg, HOLE_RADIUS

class Hole:
    def __init__(self, pos):
        self.pos = pg.Vector2(pos)
        self.surface = pg.surface.Surface((2 * HOLE_RADIUS, 2 * HOLE_RADIUS))
        pg.draw.circle(self.surface, (31, 71, 33), (HOLE_RADIUS, HOLE_RADIUS), HOLE_RADIUS)
        self.surface.set_colorkey((0, 0, 0))
    
    def draw(self, window):
        window.blit(self.surface, self.pos - pg.Vector2(HOLE_RADIUS))
    
    def detect_ball(self, ball):
        rel_pos = ball.pos - self.pos
        
        #has the ball entered the hole?
        if rel_pos.magnitude_squared() <= HOLE_RADIUS * HOLE_RADIUS:
            return True
        
        return False