import soft_body as sb
import pygame as pg
from pygame import Vector2
from math import floor
from that_menu_thing import Text, Button, Menu, Slider


pressed_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o','p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'COMMA', '1', '2', '3','4', '5', '6', '7', '8', '9', '0']
pressed = []
last = []

for i in pressed_letters:
    pressed.append(False)
    last.append(False)


def update_pressed():
    global last
    global pressed
    global pressed_letters
    for x, i in enumerate(pressed_letters):
        test = eval('pg.K_' + i)
        press = key_down(test)
        if press and (not last[x]):
            pressed[x] = True
        else:
            pressed[x] = False
        if press:
            last[x] = True
        else:
            last[x] = False


def key_press(key: str):
    return pressed[pressed_letters.index(key)]


def key_down(key: pg.key) -> bool:
    return pg.key.get_pressed()[key]


#Draw a circle a point in space
def draw_circle(pos ,size : float,color : str,outline = 0):
    pg.draw.circle(screen,color,[(pos[0]-cam_pos.x)/zoom+(sw/2),sh-((pos[1]-cam_pos.y)/zoom+(sh/2))],floor(size/zoom),outline)


#Draw a line at point in space
def draw_line(pos1 , pos2, width : float,color : str):
    pg.draw.circle(screen,color,[(pos1[0]-cam_pos.x)/zoom+(sw/2),sh-((pos1[1]-cam_pos.y)/zoom+(sh/2))],floor(width/zoom))
    pg.draw.circle(screen,color,[(pos2[0]-cam_pos.x)/zoom+(sw/2),sh-((pos2[1]-cam_pos.y)/zoom+(sh/2))],floor(width/zoom))
    pg.draw.line(screen,color,[(pos1[0]-cam_pos.x)/zoom+(sw/2),sh-((pos1[1]-cam_pos.y)/zoom+(sh/2))],[(pos2[0]-cam_pos.x)/zoom+(sw/2),sh-((pos2[1]-cam_pos.y)/zoom+(sh/2))],floor(width/zoom)*2)



pg.init()

#Screen
sw = 1800
sh = 1000
screen = pg.display.set_mode((sw,sh))
###

#Camera
cam_pos = Vector2(0,0)
zoom = 1
line_color = (100,220,50)
point_color = (100,150,75)
line_width = 5
backdrop =(5,6,11)
outside_color = (200,230,140)
###




#Menu stuff
fps_counter = Text('NaN',(backdrop,outside_color),Vector2(0.1,0.1),Vector2(0.8,0.8),editable=False)

counter_menu = Menu(screen,Vector2(0,0),Vector2(0,0),80,25,backdrop,0,[fps_counter])





#The sim
sim_speed = 13


was_l = False
was_r = False
fps = 60
dt = (1/fps)*sim_speed
fps_clock = pg.time.Clock()
running = True
while running:

    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False
    
    

    screen.fill(backdrop)
    counter_menu.full_update(events)
    update_pressed()
    pg.display.update()
    fps_clock.tick(fps)
    current_fps = fps_clock.get_fps()
    fps_counter.text = f'{int(current_fps)} FPS'
    dt = (1/max(current_fps,1))*sim_speed
pg.quit()