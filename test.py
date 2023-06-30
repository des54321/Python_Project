import pygame as pg
import numpy as np
from math import floor


pressed_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o','p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'COMMA', '1', '2', '3','4', '5', '6', '7', '8', '9', '0']
pressed = []
last_letters = []

for i in pressed_letters:
    pressed.append(False)
    last_letters.append(False)


def update_pressed():
    global last_letters
    global pressed
    global pressed_letters
    for x, i in enumerate(pressed_letters):
        test = eval('pg.K_' + i)
        press = key_down(test)
        if press and (not last_letters[x]):
            pressed[x] = True
        else:
            pressed[x] = False
        if press:
            last_letters[x] = True
        else:
            last_letters[x] = False


def key_press(key: str):
    return pressed[pressed_letters.index(key)]


def key_down(key: pg.key) -> bool:
    return pg.key.get_pressed()[key]


def draw_grid():
    for x in range(gw):
        for y in range(gh):
            pg.draw.rect(screen,colors[grid[x][y]],pg.Rect(x*(sw/gw),y*(sh/gh),(sw/gw),(sh/gh)))


def range_dist(i):
    if i == 0:
        return range(0)
    if i > 0:
        return range(1,i)
    if i < 0:
        return range(i+1,0)


def apply_grav():
    global grid, grid_vels
    for x in range(gw):
        for y in range(gh):
            if grid[x][y] == 2:
                grid_vels[x][y][1] += 1


def move_fluid():
    global grid, grid_vels
    for x in range(gw):
        for y in range(gh):
            if grid[x][y] == 2:
                vel = grid_vels[x][y]
                grid[x][y] = 0
                grid_vels[x][y] = [0,0]
                if is_in(x+vel[0],y+vel[1]):
                    grid[x+vel[0]][y+vel[1]] = 2
                    grid_vels[x+vel[0]][y+vel[1]] = vel


def is_in(x : int, y : int) -> bool:
    if x >= gw:
        return False
    if x < 0:
        return False
    if y >= gh:
        return False
    if y < 0:
        return False
    return True


gw = 16
gh = 9

grid = np.zeros((gw,gh),int)
grid_vels = np.zeros((gw,gh,2),int)



colors = [(5,6,8),(230,240,250),(20,40,240)]


m_pos = [0,0]
pre_m_pos = [0,0]


# Grav is applied every X frames, so higher = less grav
grav = 20
grav_timer = 0

sim_cycle = 20
sim_timer = 0



pg.init()
sw = 1920
sh = 1080
screen = pg.display.set_mode((sw, sh), pg.FULLSCREEN)
fps = 60
fps_clock = pg.time.Clock()
running = True
while running:
    grav_timer += 1
    grav_timer %= grav
    if grav_timer == 0:
        apply_grav()
    

    sim_timer += 1
    sim_timer %= sim_cycle
    if sim_timer == 0:
        move_fluid()

    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    pre_m_pos = m_pos
    m_pos = [floor(pg.mouse.get_pos()[0]/(sw/gw)),floor(pg.mouse.get_pos()[1]/(sh/gh))]

    if key_down(pg.K_BACKSPACE):
        running = False
    

    if pg.mouse.get_pressed()[0]:
        grid[m_pos[0]][m_pos[1]] = 1
        grid[m_pos[0]][pre_m_pos[1]] = 1
        for i in range_dist(m_pos[0]-pre_m_pos[0]):
            grid[pre_m_pos[0]+i][pre_m_pos[1]] = 1
        for i in range_dist(m_pos[1]-pre_m_pos[1]):
            grid[m_pos[0]][pre_m_pos[1]+i] = 1
    
    if pg.mouse.get_pressed()[1]:
        if grid[m_pos[0]][m_pos[1]] == 0:
            grid[m_pos[0]][m_pos[1]] = 2
            grid_vels[m_pos[0]][m_pos[1]] = [0,0]

    update_pressed()

    draw_grid()

    pg.display.update()
    fps_clock.tick(fps)
pg.quit()