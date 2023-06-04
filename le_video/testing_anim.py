import pygame as pg
import anim
from anim import *


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






pg.init()
sw = 1600
sh = 900
screen = pg.display.set_mode((sw,sh))

circle_dist = 40
sqrt_3 = 0.866
trih = 20
delay = 0.03
duration = 0.6

points = []
renders = []
for y in range(trih):
    for x in range(y+1):
        renders.append(Render('circle',
                              Color((y+x)*delay,duration,[(50,220,220),(120,240,120)],power='sine'),
                              EaseValue((y+x)*delay,duration,0,15,'sine'),
                              EasePoint((y+x)*delay,duration,(400,0),(x*circle_dist-y*circle_dist*0.5,circle_dist*sqrt_3*trih*0.5-y*circle_dist*sqrt_3),'sine')))


anim = Anim(renders,screen)


fps = 60
fps_clock = pg.time.Clock()
running = True
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    
    update_pressed()
    screen.fill((20,30,15))
    anim.step(1/fps*(int(pg.mouse.get_pressed()[0])*-4+1))
    anim.render()

    pg.display.update()
    fps_clock.tick(fps)
pg.quit()