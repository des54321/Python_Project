import pygame as pg
from pygame import Vector2
from menu_engine import Menu, Text
from colors import *
from time import time


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


def square_step():
    global squares, square_size
    square_size /= 3
    new = []
    for i in squares:
        for x in dirs:
            new.append(i+Vector2(x)*square_size)
    squares = new


def draw_rect(pos,width,height,color):
    pg.draw.rect(screen,color,pg.Rect(pos[0]+(sw/2)-width/2,sh-(pos[1]+(sh/2)+height/2),width,height))





dirs = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]





pg.init()
sw = 1920
sh = 1080
screen = pg.display.set_mode((sw, sh), pg.FULLSCREEN)

start = time()

cur_start = 0

delay = 0.5

squares = [Vector2(0,0)]
square_size = 1000





fps_clock = pg.time.Clock()
fps = 60
running = True
while running:

    if time()-start > cur_start*delay:
        cur_start += 1
        if cur_start < 6:
            screen.fill(DG)

            for i in squares:
                draw_rect(i,square_size+1,square_size+1,GR)
            pg.display.update()
            
            square_step()
        elif cur_start == 6:
            screen.fill(DG)

            for i in squares:
                draw_rect(i,square_size+1,square_size+1,GR)
            pg.display.update()


    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    
    update_pressed()
    screen.fill(DG)
    

    if key_down(pg.K_BACKSPACE):
        running = False
    


    fps_clock.tick(fps)
pg.quit()