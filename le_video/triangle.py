import pygame as pg
import anim
from anim import *
from menu_engine import Menu, Text
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

def pos_scr(pos):
    return Vector2(pos[0]+(sw/2),sh-(pos[1]+(sh/2)))


def pascal(n):
    prev = 1
    final = [1]
 
    for i in range(1, n + 1):
        curr = (prev * (n - i + 1)) // i
        final.append(curr)
        prev = curr
    return final



pg.init()
sw = 1920
sh = 1080
screen = pg.display.set_mode((sw, sh), pg.FULLSCREEN)

circle_dist = 110
sqrt_3 = 0.866
trih = 10
delay = 0.08
duration = 0.6
circle_size = 50

circle_values = []

points = []
renders = []
for y in range(trih):
    row = pascal(y)
    for x in range(y+1):
        pos = Vector2(x*circle_dist-y*circle_dist*0.5,circle_dist*sqrt_3*trih*0.5-(y+0.5)*circle_dist*sqrt_3)
        scr_from_pos = pos_scr(pos)
        renders.append(Render('circle',
                              Color((y+x)*delay,duration,[CY,GR],power='sine'),
                              EaseValue((y+x)*delay,duration,0,circle_size,'sine'),
                              EasePoint((y+x)*delay,duration,(400,0),pos,'sine')))
        circle_values.append(Text(str(row[x]),(None,DG),Vector2(scr_from_pos.x/sw,scr_from_pos.y/sh)-Vector2(circle_size/sw,circle_size/sh)/2,(circle_size/sw,circle_size/sh),False))
        renders[-1].text_ob = circle_values[-1]



anim = Anim(renders,screen)

nums = Menu(screen,(0,0),(0,0),sw,sh,None,0,circle_values)
for i in nums.contents:
    i.show = False


num_color = ColorLerp([GR,DG],[])

mod_color = ColorLerp([GR,BL],[])
mod = 1

fps = 60
fps_clock = pg.time.Clock()
running = True
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    
    update_pressed()
    screen.fill(DG)
    anim.step(1/fps)
    anim.render()
    if key_down(pg.K_BACKSPACE):
        running = False
    
    nums.full_update(events)

    if key_press('m'):
        mod += 1
        for i in anim.renders:
            i.fade_to(mod_color.get((int(i.text_ob.text)%mod)/mod),0.4,'sine')


    if anim.t > delay * trih * 3:
        for i in nums.contents:
            i.show = True
            i.colors = (None,num_color.get((anim.t-delay*trih*3)))

    pg.display.update()
    fps_clock.tick(fps)
pg.quit()