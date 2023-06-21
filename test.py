import pygame as pg
from pygame import Vector2


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


def point_in_box(p:Vector2,b1:Vector2,b2:Vector2,radius=0):
    if (p.x > b1.x+radius) == (p.x > b2.x) and (p.x > b1.x-radius) == (p.x > b2.x) and (p.x > b1.x) == (p.x > b2.x+radius) and (p.x > b1.x) == (p.x > b2.x-radius):
        return False
    if (p.y > b1.y+radius) == (p.y > b2.y) and (p.y > b1.y-radius) == (p.y > b2.y) and (p.y > b1.y) == (p.y > b2.y+radius) and (p.y > b1.y) == (p.y > b2.y-radius):
        return False
    return True



pg.init()
sw = 1000
sh = 600
screen = pg.display.set_mode((sw,sh))
fps = 60
fps_clock = pg.time.Clock()
running = True
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False
    


    print(point_in_box(Vector2(pg.mouse.get_pos()),Vector2(100,300),Vector2(800,300),50))
    print(pg.mouse.get_pos())

    
    update_pressed()
    pg.display.update()
    fps_clock.tick(fps)
pg.quit()