import pygame as pg
import anim
from anim import *
import pen
from colors import *


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


def get_m_pos():
    return Vector2([pg.mouse.get_pos()[0]-(sw/2),sh-(pg.mouse.get_pos()[1]+(sh/2))])



pg.init()
sw = 1920
sh = 1080
screen = pg.display.set_mode((sw, sh), pg.FULLSCREEN)

circle_dist = 75
circle_size = 30
length = 20
delay = 0.05
duration = 0.8

points = []
renders = []
for i in range(length):
    renders.append( Render(
                    'circle',
                    Color((i)*delay,duration,[CY,GR],power='sine'),
                    EaseValue((i)*delay,duration,0,circle_size,'sine'),
                    EasePoint((i)*delay,duration,(0,400),(circle_dist*length*-0.5+i*circle_dist,-200),'sine')))


anim = Anim(renders,screen)


fps = 60
fps_clock = pg.time.Clock()
running = True
while running:
    if pg.mouse.get_pressed()[2]:
        for i in renders:
            if i.p1.get(anim.t).distance_to(get_m_pos()) < circle_size:
                i.fade_to(GR,0.1,'sine')
    
    touch = False
    
    for i in renders:
        if i.p1.get(anim.t).distance_to(get_m_pos()) < circle_size:
            if pg.mouse.get_pressed()[0]:
                i.fade_to(BL,0.1,'sine')
            touch = True
            pen.was_drawing = False
            pen.last_dir = None
    
    if not touch:
        pen.update_lines(8)
    
    if key_press('s'):
        pen.was_drawing = False
        pen.last_dir = None
        pen.lines.append([])
        circle_res = 30
        for i in range(circle_res+1):
            new = Vector2()
            new.from_polar((25,i*360/circle_res))
            new.y *= 1.6
            pen.lines[-1].append(new+Vector2(pg.mouse.get_pos()))
    
    if key_press('a'):
        pen.was_drawing = False
        pen.last_dir = None
        pos = pg.mouse.get_pos()
        pen.lines.append([[pos[0],pos[1]+40],[pos[0],pos[1]-40]])
    
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    
    update_pressed()
    screen.fill(DG)
    anim.step(1/fps)
    anim.render()
    print(pen.drawing_arrow)

    pen.draw_lines(screen,PEN,10)


    if key_down(pg.K_BACKSPACE):
        running = False

    pg.display.update()
    fps_clock.tick(fps)
pg.quit()