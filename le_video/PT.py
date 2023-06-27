import pygame as pg
import anim
from anim import *
from menu_engine import Menu, Text
from colors import *
import pen


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
pen.arrow_length /= 1.5




circle_values = []


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
        renders[-1].text = circle_values[-1].text



anim = Anim(renders,screen)

nums = Menu(screen,(0,0),(0,0),sw,sh,None,0,circle_values)
for i in nums.contents:
    i.show = False


num_color = ColorLerp([GR,DG],[])

mod_color = ColorLerp([GR,BL],[])
mod = 1


fade_time = 0
faded = False


fps = 60
fps_clock = pg.time.Clock()
running = True
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    
    pen.update_lines(8)

    update_pressed()
    screen.fill(DG)
    if faded:
        fade_time += 1/fps
    anim.step(1/fps)
    anim.render()
    if faded:
        pen.draw_lines(screen,PEN,10)
    else:
        pen.draw_lines(screen,BL,10)
    if key_down(pg.K_BACKSPACE):
        running = False
    
    nums.full_update(events)

    if key_press('s'):
        pen.was_drawing = False
        pen.last_dir = None
        pen.lines.append([])
        circle_res = 30
        for i in range(circle_res+1):
            new = Vector2()
            new.from_polar((18,i*360/circle_res))
            new.y *= 1.6
            pen.lines[-1].append(new+Vector2(pg.mouse.get_pos()))
    
    if key_press('m'):
        mod += 1
        for i in anim.renders:
            i.fade_to(mod_color.get((int(i.text)%mod)/(mod-1)),0.4,'sine')
    
    


    if anim.t > delay * trih * 3:
        for i in nums.contents:
            i.show = True
            i.colors = (None,num_color.get((anim.t-delay*trih*3)))
    

    if key_press('b'):
        nums.contents = []
        for i in anim.renders:
            i.p1 = EasePoint(anim.t,2,i.p1.get(anim.t),i.p1.get(anim.t)/4+Vector2(0,358),'sine')
            i.size = EaseValue(anim.t,2,i.size.get(anim.t),i.size.get(anim.t)/4,'sine')
        

        trih *= 4
        circle_dist /= 4
        circle_size //= 4
        for y in range(trih//4,trih):
            row = pascal(y)
            for x in range(y+1):
                pos = Vector2(x*circle_dist-y*circle_dist*0.5,circle_dist*sqrt_3*trih*0.5-(y+0.5)*circle_dist*sqrt_3)
                renders.insert(0,Render('circle',
                                    Color(anim.t+2,2,[DG,mod_color.get((row[x]%mod)/(mod-1))],power='sine'),
                                    circle_size,
                                    pos))
                renders[0].text = str(row[x])
        anim.update_renders()
    

    if key_down(pg.K_z):
        for i in anim.renders:
            if not type(i.p1) == Vector2:
                i.p1 = i.p1.get(anim.t)
            i.p1 *= 1.001
            if not (type(i.size) == float or type(i.size) == int):
                i.size = i.size.get(anim.t)
            i.size *= 1.001


    if key_press('f'):
        faded = True
        for i in anim.renders:
            i.fade_to(DG,0.4,'sine')
    
    if fade_time > 0.4:
        anim.renders = []
    

    

    pg.display.update()
    fps_clock.tick(fps)
pg.quit()