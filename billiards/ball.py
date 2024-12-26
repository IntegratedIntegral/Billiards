from settings import *

class Ball:
    def __init__(self, pos, colour):
        self.pos = pg.Vector2(pos)
        self.vel = pg.Vector2(0)
        self.colour = colour

        self.new_pos = None

        self.surface = pg.surface.Surface((2 * BALL_RADIUS, 2 * BALL_RADIUS))
        pg.draw.circle(self.surface, self.colour, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS) #draws circle on a surface so that it can be copied to the main window every frame instead of redrawing a circle every frame
        self.surface.set_colorkey((0, 0, 0))
    
    def draw(self, window):
        window.blit(self.surface, (self.pos - pg.Vector2(BALL_RADIUS)))
    
    def update(self, delta_t, balls):
        #compute future position
        self.new_pos = self.pos + self.vel * delta_t

        update_pos = True
        
        #check for collisions between edges
        if self.new_pos.x <= BALL_RADIUS or self.new_pos.x >= WINDOW_WIDTH - BALL_RADIUS:
            self.vel.x = -self.vel.x
            update_pos = False
        if self.new_pos.y <= BALL_RADIUS or self.new_pos.y >= WINDOW_HEIGHT - BALL_RADIUS:
            self.vel.y = -self.vel.y
            update_pos = False
        
        #check for collisions between other balls
        for b in balls:
            if self != b and self.collision_detection(b)[0]:
                update_pos = False
                break
        
        #no collisions detected, update position
        if update_pos:
            self.pos = self.new_pos
        
        #stupid friction, always dragging us behind
        self.vel *= (1 - DRAG) ** delta_t
    
    def collision_detection(self, ball):
        rel_x = ball.pos.x - self.new_pos.x
        rel_y = ball.pos.y - self.new_pos.y

        dist_sqrd = rel_x * rel_x + rel_y * rel_y

        #outputs information about some other ball, including whether or not they collided, its relative position and the distance (well distance squared as it's cheaper to compute)
        return dist_sqrd <= 4 * BALL_RADIUS * BALL_RADIUS, rel_x, rel_y, dist_sqrd
    
    def collide(self, ball):
        collision_results = self.collision_detection(ball)

        #have the two balls collided?
        if collision_results[0]:
            #does some mathemagic to compute the velocity of the ball after collision
            unit_norm = collision_results[1] / collision_results[3] ** 0.5
            unit_tang = collision_results[2] / collision_results[3] ** 0.5

            vel_norm = self.vel.x * unit_norm + self.vel.y * unit_tang
            vel_tang = -self.vel.x * unit_tang + self.vel.y * unit_norm
            ball_vel_norm = ball.vel.x * unit_norm + ball.vel.y * unit_tang
            ball_vel_tang = -ball.vel.x * unit_tang + ball.vel.y * unit_norm

            new_vel_norm = ball_vel_norm
            new_ball_vel_norm = vel_norm

            self.vel.x = new_vel_norm * unit_norm - vel_tang * unit_tang
            self.vel.y = new_vel_norm * unit_tang + vel_tang * unit_norm
            ball.vel.x = new_ball_vel_norm * unit_norm - ball_vel_tang * unit_tang
            ball.vel.y = new_ball_vel_norm * unit_tang + ball_vel_tang * unit_norm