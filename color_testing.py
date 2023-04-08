'''
Can be used to test out what the colors will look like of the spetrum with the color_interpolation module
'''


import pygame as pg
from pygame import Vector2
import color_interpolation


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



color = color_interpolation.ColorLerp(((30,240,70),(230,230,40),(220,30,30)),[0.6])


cir_num = 256

pg.init()
s_w = 1000
s_h = 600
screen = pg.display.set_mode((s_w,s_h))
fps = 60
fps_clock = pg.time.Clock()
running = True
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    
    screen.fill((0,0,0))
    
    for i in range(cir_num+1):

        pg.draw.circle(screen,color.get(i/cir_num),(i*s_w/cir_num,s_h/2),20)
    
    update_pressed()
    pg.display.update()
    fps_clock.tick(fps)
pg.quit()