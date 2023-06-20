import pygame as pg
from pygame import Vector2
from menu_engine import Menu, Text
from colors import *
from time import time
import anim
from math import floor


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


def on_circ(dir,len,max):
    new = Vector2()
    new.from_polar((len,dir*(360/max)))
    return new





pg.init()
sw = 1920
sh = 1080
screen = pg.display.set_mode((sw, sh), pg.FULLSCREEN)


renders = []

nums = []
line_len = 12
dist = 160
line_height = 50
text_size = 0.5
clock_size = 350

for i in range(line_len):
    t_pos = pos_scr((-(line_len-1)*dist*0.5+i*dist,-200-line_height*2))
    renders.append(anim.Render('line',GR,dist*0.1,(-(line_len-1)*dist*0.5+i*dist,-200-line_height),(-(line_len-1)*dist*0.5+i*dist,-200+line_height)))
    renders[-1].kind = 'tick'
    nums.append(Text(str(i),(None,GR),Vector2(t_pos.x/sw,t_pos.y/sh)-Vector2((dist*text_size*0.5)/sw,(dist*text_size*0.5)/sh),((dist*text_size)/sw,(dist*text_size)/sh)))


for i in range(-1,line_len):
    renders.append(anim.Render('line',GR,dist*0.1,(-(line_len-1)*dist*0.5+i*dist,-200),(-(line_len-1)*dist*0.5+(i+1)*dist,-200)))
    renders[-1].kind = 'connect'

lines = anim.Anim(renders,screen)
num_m = Menu(screen,(0,0),(0,0),sw,sh,None,0,nums)

ease_nums = []
for i in range(line_len):
    t_pos = pos_scr((-(line_len-1)*dist*0.5+i*dist,-200-line_height*2))
    nt_pos = pos_scr(on_circ(-i+3,clock_size+line_height*3,line_len))
    ease_nums.append(anim.EasePoint(9999,2,Vector2(t_pos.x/sw,t_pos.y/sh)-Vector2((dist*text_size*0.5)/sw,(dist*text_size*0.5)/sh),Vector2(nt_pos.x/sw,nt_pos.y/sh)-Vector2((dist*text_size*0.5)/sw,(dist*text_size*0.5)/sh),'sine'))


fps_clock = pg.time.Clock()
fps = 60
running = True
while running:


    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    
    update_pressed()
    screen.fill(DG)

    screen.fill(DG)

    lines.render()
    lines.step(1/fps)
    num_m.full_update(events)

    pg.display.update()

    if key_down(pg.K_BACKSPACE):
        running = False
    
    if key_press('c'):
        for n,i in enumerate(lines.renders):
            i:anim.Render
            if i.kind == 'tick':
                i.p1 = anim.EasePoint(lines.t,2,i.p1,on_circ(-n+3,clock_size,line_len),'sine')
                i.p2 = anim.EasePoint(lines.t,2,i.p2,on_circ(-n+3,clock_size+line_height*2,line_len),'sine')
            else:
                i.p1 = anim.EasePoint(lines.t,2,i.p1,on_circ(-n+3,clock_size+line_height,line_len),'sine')
                i.p2 = anim.EasePoint(lines.t,2,i.p2,on_circ(-n+2,clock_size+line_height,line_len),'sine')
        for i in ease_nums:
            i.start_t = lines.t
    
    for n,i in enumerate(num_m.contents):
        i.pos = ease_nums[n].get(lines.t)

    


    fps_clock.tick(fps)
pg.quit()