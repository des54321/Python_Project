import pygame as pg
import anim
from anim import *
from menu_engine import Menu, Text
from colors import *
from random import random


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


def pos_scr(pos):
    return Vector2(pos[0] + (sw / 2), sh - (pos[1] + (sh / 2)))


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

circle_dist = 55
sqrt_3 = 0.866
trih = 45
delay = 0.06
duration = 0.6
circle_size = 25


ran_color = color_interpolation.ColorLerp((GR, BL), [])


renders = []
for y in range(trih):
    row = pascal(y)
    for x in range(y + 1):
        pos = Vector2(
            x * circle_dist - y * circle_dist * 0.5,
            circle_dist * sqrt_3 * 40 * 0.5 - (y + 0.5) * circle_dist * sqrt_3,
        )
        scr_from_pos = pos_scr(pos)
        renders.append(
            Render(
                "circle",
                Color(
                    (y + x) * delay,
                    duration,
                    [CY, ran_color.get(random())],
                    power="sine",
                ),
                EaseValue((y + x) * delay, duration, 0, circle_size, "sine"),
                EasePoint((y + x) * delay, duration, (400, 0), pos, "sine"),
            )
        )




anim = Anim(renders, screen)

for i in anim.renders:
    i.p1.end.y -= 400
    i.p1.start.y -= 400

num_color = ColorLerp([GR, DG], [])

mod_color = ColorLerp([GR, BL], [])
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
    anim.step(1 / fps)

    for i in anim.renders:
        i.p1.start.y += anim.t / 3
        i.p1.end.y += anim.t / 3
        i.p1.start *= 1.001
        i.p1.end *= 1.001
        i.size.start *= 1.001
        i.size.end *= 1.001

    anim.render()
    if key_down(pg.K_BACKSPACE):
        running = False

    pg.display.update()
    fps_clock.tick(fps)
    print(fps_clock.get_fps())
pg.quit()
