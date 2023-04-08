import pygame as pg
from pygame import Vector2
from menu_engine import Menu, Text


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

pg.init()
color_pal = [(3,5,2),(2,4,20),(4,8,30),(245,246,234),(120,110,170),(50,40,120),(200,195,210)]
s_w = 1600
s_h = 960
screen = pg.display.set_mode((s_w,s_h))
fps = 60
fps_clock = pg.time.Clock()

test_box = Text(
    'NaN'
    ,(color_pal[6],color_pal[5]),Vector2(0.1,0.1),Vector2(0.8,0.8)
)
main_menu = Menu(screen,Vector2(0,s_h-250), Vector2(0,s_h), s_w, 250, color_pal[6], 20, [test_box], 0.1, (True,True,False,False),False)
texting = ''
running = True
while running:
    # texting += pg.event.get()
    pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_WAIT)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.fill(color_pal[0])
    
    if key_press('m'):
        main_menu.direct *= -1
    # main_menu.full_update()

    
    update_pressed()
    pg.display.update()
    fps_clock.tick(fps)
pg.quit()