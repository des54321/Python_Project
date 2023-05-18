from pygame import Vector2, draw, Surface
from copy import copy

move_speed = 0.5
thrust = -0.6
friction = 0.95
grav = 0.3
player_size = 100
time = 1000
area_w = 1200
area_h = 675

player_size_s = player_size*player_size*4

RED = 'red'
BLUE = 'blue'

start_x = 100
start_y = 200


class Agent:

    def __init__(self, color, x, y, time) -> None:
        self.pos_x = x
        self.pos_y = y
        self.color = color
        self.vel_x = 0
        self.vel_y = 0
        self.time = time
    
    def left_input(self):
        self.vel_x -= move_speed
    
    def right_input(self):
        self.vel_x += move_speed
    
    def up_input(self):
        self.vel_y += thrust
    
    def update(self):
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        self.vel_x *= friction
        self.vel_y += grav



class Match:

    def __init__(self) -> None:
        self.red = Agent(RED,start_x,start_y,time)
        self.blue = Agent(BLUE,area_w-start_x,start_y,time)
        self.it = RED
        self.was_t = False
        self.winner = None
    
    def update(self):
        self.blue.update()
        self.red.update()

        self.blue.pos_x = min(max(self.blue.pos_x,0),area_w)
        self.blue.pos_y = min(max(self.blue.pos_y,0),area_h)
        self.red.pos_x = min(max(self.red.pos_x,0),area_w)
        self.red.pos_y = min(max(self.red.pos_y,0),area_h)

        if self.blue.pos_y == area_h:
            self.blue.vel_y = 0
        if self.red.pos_y == area_h:
            self.red.vel_y = 0

        if (self.red.pos_x-self.blue.pos_x)**2 + (self.red.pos_y-self.blue.pos_y)**2 < player_size_s:
            if not self.was_t:
                if self.it == BLUE:
                    self.it = RED
                else:
                    self.it = BLUE
            self.was_t = True
        else:
            self.was_t = False
        if self.it == BLUE:
            self.blue.time -= 1
            if self.blue.time == 0:
                self.winner = RED
        else:
            self.red.time -= 1
            if self.red.time == 0:
                self.winner = BLUE
        
        return self.winner
    

    def render(self,screen:Surface):
        draw.circle(screen,(30,40,220),(self.blue.pos_x,self.blue.pos_y),player_size)
        draw.circle(screen,(230,40,30),(self.red.pos_x,self.red.pos_y),player_size)
        draw.line(screen,(240,240,240),(area_w,0),(area_w,area_h),10)
        draw.line(screen,(240,240,240),(0,area_h),(area_w,area_h),10)
        draw.line(screen,(30,40,220),(0,screen.get_height()),((screen.get_width()/2)-((screen.get_width()*(1-(self.blue.time/time)))/2),screen.get_height()),30)
        draw.line(screen,(230,40,30),(screen.get_width(),screen.get_height()),((screen.get_width()/2)+((screen.get_width()*(1-(self.red.time/time)))/2),screen.get_height()),30)
