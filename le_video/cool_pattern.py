import pygame as pg
import numpy as np
import color_interpolation as clerp
from math import floor, ceil
from time import time
from random import randint
import pen
from colors import *


pressed_letters = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "COMMA",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
]
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
        test = eval("pg.K_" + i)
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


def draw_grid(r):
    for y in range(gh)[r - 1 : r]:
        for x in range(gw):
            pg.draw.rect(
                screen,
                color.get(grid[x][y] / (colors - 1)),
                pg.Rect(tile_size * x, tile_size * y+(sh-(gh*tile_size))*0.5, tile_size, tile_size),
            )


def in_grid(x, y):
    if x > gw - 1:
        return False
    if x < 0:
        return False
    if y > gh - 1:
        return False
    if y < 0:
        return False
    return True


def do_layer(layer):
    global grid
    for i in range(len(grid[:, layer])):
        count = 0
        for n, x in enumerate(pattern):
            if in_grid(i + x[0], layer - 1 - x[1]):
                count += (
                    (grid[i + floor(x[0])][layer - 1 - x[1]] * (x[0] % 1))
                    + (grid[i + ceil(x[0])][layer - 1 - x[1]] * (1 - x[0] % 1))
                ) * multi[n]

        grid[i][layer] = count % colors


def do_pattern(below=0):
    for i in range(gh)[below + 1 :]:
        do_layer(i)


# pattern = [[0,1],[-2,2],[2,2],[-1,0],[1,0]]

# pattern = []
# amount = 5
# for i in range(amount+1)[1:]:
#     pattern.append([-(amount-i+1),i-1])
#     pattern.append([(amount-i+1),i-1])

# pattern = []
# amount = 5
# for i in range(amount):
#     pattern.append([-((i%2)+1),i])
#     pattern.append([(i%2)+1,i])

# pattern = []
# amount = 4
# for i in range(amount):
#     pattern.append([-i-1,0])
#     pattern.append([i+1,0])

# pattern = []
# amount = 4
# for i in range(amount):
#     if i%2 == 1:
#         pattern.append([0,i])
#     else:
#         pattern.append([-1,i])
#         pattern.append([1,i])


# pattern = []
# amount = 5
# for i in range(amount+1)[1:]:
#     pattern.append([-i,i-1])
#     pattern.append([i,i-1])


# pattern = []
# amount = 6
# start = 0
# for i in range(start,amount+start):
#     pattern.append([-i,i-1])
#     pattern.append([i,i-1])

# pattern = []
# amount = 1
# for i in range(amount):
#     pattern.append([-i,i])
#     pattern.append([1,i])


# pattern = [[0, 0], [-3, 3], [-3, 1], [-3, 2], [-2, 1], [2, 2]]
# pattern = [[0,2],[-1,0],[1,0]]
# pattern = [[2, 2], [-1, 0], [2, 1], [1, 0], [-1, 0]]
# pattern = [[-1,1],[1,1],[-1,2],[1,2],[-1,0],[1,0]]

# pattern = []
# for i in range(3):
#     y = randint(0, 5)
#     x = randint(0, y + 1)
#     pattern.append([x, y])
#     pattern.append([-x, y])

pattern = [[-1, 0],[1,0]]
# pattern = [[-2,1],[2,1],[0,0]]

multi = [1 for _ in range(len(pattern))]
gw = 192
gh = 96
tile_size = 10

mul = 8
gw //= mul
gh //= mul
tile_size *= mul

colors = randint(3, 4)
colors = 2


color = clerp.ColorLerp([DG, GR], [])


grid = np.array([[0.0 for __ in range(gh)] for _ in range(gw)])
grid[gw // 2][0] = 1

print(pattern)
print(colors)
do_pattern()

delay = 0


doing_pen = False 


pg.init()
sw = 1920
sh = 1080
screen = pg.display.set_mode((sw, sh), pg.FULLSCREEN)
fps = 60
fps_clock = pg.time.Clock()
start = time()

draw_grid(0)
update_pressed()
pg.display.update()
up_to = 0

running = True
while running:

    if doing_pen:
        pen.update_lines(8)
    if time() - start > up_to * delay:
        up_to += 1
    
    if key_press('n'):
        start = time()
        up_to = 0
        colors += 1
        do_pattern()

    if up_to > gh and doing_pen:
        screen.fill((0,0,0))
        for i in range(gh):
            draw_grid(i+1)
    else:
        draw_grid(up_to)

    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    if doing_pen:
        pen.draw_lines(screen,BL,10)
    pg.display.update()
    update_pressed()
    fps_clock.tick(fps)

    if key_down(pg.K_BACKSPACE):
        running = False
pg.quit()
