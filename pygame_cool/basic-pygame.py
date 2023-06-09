import pygame as pg


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

    
    update_pressed()
    pg.display.update()
    fps_clock.tick(fps)
pg.quit()