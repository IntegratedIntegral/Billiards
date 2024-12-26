from settings import *

class Path:
    def __init__(self, level):
        self.white_ball = level.white_ball
        self.coloured_balls = level.coloured_balls
    
    def collision_position(self, ball, start_pos, vel):
        cx = ball.pos.x - start_pos.x
        cy = ball.pos.y - start_pos.y
        if vel.x != 0:
            slope = vel.y / vel.x
        else:
            slope = 800
        determinant = cx * slope * (2 * cy - cx * slope) - cy * cy + 4 * BALL_RADIUS * BALL_RADIUS * (slope * slope + 1)
        if determinant < 0:
            #no collision detected. return nothing
            return None
        
        coll_x1 = (slope * cy + cx + determinant ** 0.5) / (slope * slope + 1)
        coll_y1 = slope * coll_x1

        coll_x2 = (slope * cy + cx - determinant ** 0.5) / (slope * slope + 1)
        coll_y2 = slope * coll_x2
        
        if (vel.x > 0) ^ (cx > 0):
            #line intersects ball, but it is in the opposite direction. return nothing
            return None
        
        #there are two intersections between the line and the ball. return the intersection that is closer
        intersection1 = pg.Vector2(coll_x1, coll_y1)
        intersection2 = pg.Vector2(coll_x2, coll_y2)
        if intersection1.magnitude_squared() < intersection2.magnitude_squared(): return intersection1
        else: return intersection2
    
    def draw_line(self, window, start_pos, vel, balls, previously_collided_balls, colour):
        coll_vel = pg.Vector2(0)
        min_coll_dist = None
        min_coll_pos = None
        coll_ball = None
        vel_norm = pg.Vector2(0)
        #this loop will find the ball that the white ball will collide with
        #min_coll_dist is the shortest of the distances between the white ball and other balls that it COULD collide with should there be nothing else blocking the way
        for ball in balls:
            if ball.pos != start_pos:
                #loop over all balls and check if there will be a collision
                coll_pos = self.collision_position(ball, start_pos, vel) #coll_pos is measured relative to the white ball
                if coll_pos == None:
                    #no collision. next ball!
                    continue
                
                coll_dist = coll_pos.magnitude()
                if (min_coll_dist == None or coll_dist < min_coll_dist) and not ball in previously_collided_balls:
                    min_coll_dist = coll_dist
                    min_coll_pos = coll_pos
                    coll_ball = ball
        
        length = vel.magnitude() / DRAG #length of trajectory. ball will eventually stop due to friction
        vel_dir = vel.normalize() if not (vel.x == 0 and vel.y == 0) else pg.Vector2(0)

        if min_coll_pos != None:
            if min_coll_dist < length: #collision will shorten the length of path
                length = min_coll_dist
                rel_pos = coll_ball.pos - min_coll_pos - start_pos
                coll_vel = vel - vel_dir * length * DRAG #velocity of white ball imediately before collision
                vel_norm = coll_vel.dot(rel_pos) * rel_pos / (4 * BALL_RADIUS * BALL_RADIUS) #component of velocity parallel to rel_pos
                coll_vel -= vel_norm #velocity imediately after collision
        
        end_pos = start_pos + vel_dir * length

        #if end_pos goes over border, shorten the line
        if end_pos.x > WINDOW_WIDTH:
            length = (WINDOW_WIDTH - BALL_RADIUS - start_pos.x) / vel_dir.x
            end_pos = start_pos + vel_dir * length
            
            coll_vel = vel - vel_dir * length * DRAG
            coll_vel.x *= -1
        elif end_pos.x < 0:
            length = (BALL_RADIUS - start_pos.x) / vel_dir.x
            end_pos = start_pos + vel_dir * length

            coll_vel = vel - vel_dir * length * DRAG
            coll_vel.x *= -1
        if end_pos.y > WINDOW_HEIGHT:
            length = (WINDOW_HEIGHT - BALL_RADIUS - start_pos.y) / vel_dir.y
            end_pos = start_pos + vel_dir * length

            coll_vel = vel - vel_dir * length * DRAG
            coll_vel.y *= -1
        elif end_pos.y < 0:
            length = (BALL_RADIUS - start_pos.y) / vel_dir.y
            end_pos = start_pos + vel_dir * length

            coll_vel = vel - vel_dir * length * DRAG
            coll_vel.y *= -1
        
        #draw the line
        pg.draw.line(window, colour, start_pos, end_pos)

        #return end_pos and, if they exist, velocity just after collision, collided ball and the component of velocity that the white ball lost to the collided ball
        return end_pos, coll_vel, coll_ball, vel_norm
    
    def draw(self, window, rel_mouse_pos, balls):
        end_pos, coll_vel, coll_ball, vel_norm = self.draw_line(window, self.white_ball.pos, WHITE_BALL_SENSITIVITY * rel_mouse_pos, balls, [], self.white_ball.colour)
        i = 0
        collided_balls = [] #list of balls that the white ball will collide with. This prevents the path tracing algorithm to predict that the same ball will be collided more than once

        while coll_vel.x != 0 and coll_vel.y != 0 and i < 4:
            if coll_ball != None:
                #if a collision was detected, draw the path of the coloured ball
                collided_balls.append(coll_ball)
                self.draw_line(window, coll_ball.pos, vel_norm, balls, [], coll_ball.colour)
            end_pos, coll_vel, coll_ball, vel_norm = self.draw_line(window, end_pos, coll_vel, balls, collided_balls, self.white_ball.colour)
            
            i += 1