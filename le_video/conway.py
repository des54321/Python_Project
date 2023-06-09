import pygame as pg
import anim
from anim import *
from random import randint
from colors import *
import pen


dirs = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]

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

def do_grid():
    global grid
    new_grid = []
    for x in range(width):
        new_grid.append([])
        for y in range(height):
            new_grid[-1].append(grid[x][y])
            count = sum([grid[(x+i[0])%width][(y+i[1])%height] for i in dirs])
            if count != 2 and count != 3:
                new_grid[x][y] = 0
            if count == 3:
                new_grid[x][y] = 1
    grid = new_grid




pg.init()
sw = 1920
sh = 1080
screen = pg.display.set_mode((sw, sh), pg.FULLSCREEN)

circle_dist = 75
height = 12
width = 20
circle_size = 30
delay = 0.15
duration = 0.6
grid = []

points = []
renders = []
for x in range(width):
    grid.append([])
    for y in range(height):
        grid[x].append(randint(0,1))
        if grid[x][y] == 1:
            renders.append( Render(
                            'circle',
                            Color(((x*x+y*y)**0.5)*delay,duration,[BL,GR],power=3),
                            EaseValue(((x*x+y*y)**0.5)*delay,duration,0,circle_size,'sine'),
                            EasePoint(((x*x+y*y)**0.5)*delay,duration,(0.5*width*circle_dist,0.5*height*circle_dist),(circle_dist*(width-1)*-0.5+x*circle_dist,circle_dist*(height-1)*-0.5+y*circle_dist),'sine')))
        else:
            renders.append( Render(
                            'circle',
                            Color(((x*x+y*y)**0.5)*delay,duration,[GR,BL],power=3),
                            EaseValue(((x*x+y*y)**0.5)*delay,duration,0,circle_size,'sine'),
                            EasePoint(((x*x+y*y)**0.5)*delay,duration,(0.5*width*circle_dist,0.5*height*circle_dist),(circle_dist*(width-1)*-0.5+x*circle_dist,circle_dist*(height-1)*-0.5+y*circle_dist),'sine')))







anim_delay = 0.4
do_sim = True

anim = Anim(renders,screen)
anim.t = -3
pg.mouse.set_visible(False)
last_step = 4
first = True

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

    pen.update_lines(8)

    if anim.t > last_step:
        if do_sim:
            do_grid()
            for n,i in enumerate(anim.renders):
                i:Render
                if grid[n//height][n%height] == 0:
                    i.fade_to(BL,0.2,'sine')
                else:
                    i.fade_to(GR,0.2,'sine')
                if first:
                    i.p1 = i.p1.get(anim.t)
                    i.size = circle_size
            first = False
            last_step += anim_delay



    if key_down(pg.K_BACKSPACE):
        running = False
    

    if key_press('h'):
        pg.mouse.set_visible(True)
        do_sim = False
        for i in anim.renders:
            i.fade_to(DG,1,'sine')
        
    pen.draw_lines(screen,PEN,10) 

    pg.display.update()
    fps_clock.tick(fps)
pg.quit()