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


gw = 96
gh = 54

grid = np.array([[0]*gh]*gw)

colors = [(5,6,8),(230,240,250)]


m_pos = [0,0]
pre_m_pos = [0,0]

pg.init()
sw = 1920
sh = 1080
screen = pg.display.set_mode((sw, sh), pg.FULLSCREEN)
fps = 60
fps_clock = pg.time.Clock()
running = True
while running:
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
        for i in range_dist(m_pos[0]-pre_m_pos[0]):
            grid[pre_m_pos[0]+i][pre_m_pos[1]] = 1
        for i in range_dist(m_pos[1]-pre_m_pos[1]):
            grid[m_pos[0]][pre_m_pos[1]+i] = 1

    update_pressed()

    draw_grid()

    pg.display.update()
    fps_clock.tick(fps)
pg.quit()