import pygame as pg
import ast


def key_down(key : pg.key) -> bool:
    return pg.key.get_pressed()[key]

def draw_circle(pos,size,color):
    pg.draw.circle(screen,color,(pos[0]+(s_w/2),s_h-(pos[1]+(s_h/2))),round(size))

def draw_rect(pos,width,height,color):
    pg.draw.rect(screen,color,pg.Rect(pos[0]+(s_w/2),s_h-(pos[1]+(s_h/2)),width,height))

def draw_line(pos1,pos2,size,color):
    pg.draw.circle(screen,color,(pos1[0]+(s_w/2),s_h-(pos1[1]+(s_h/2))),(pos2[0]+(s_w/2),s_h-(pos2[1]+(s_h/2))),round(size))

def get_m_pos():
    return [pg.mouse.get_pos()[0]-(s_w/2),s_h-(pg.mouse.get_pos()[0]+(s_h/2))]

pressed_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'COMMA', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
pressed = []
for i in pressed_letters:
    pressed.append(False)
def update_pressed():
    global pressed
    global pressed_letters
    keys = pg.key.get_pressed()
    for i in range(len(pressed_letters)):
        pg_key = getattr(pg,'K_'+pressed_letters[i])
        press = keys[pg_key]
        pressed[i] = False
        if press and (not pressed[i]):
            pressed[i] = True

def key_press(key : str):
    return pressed[pressed_letters.index(key)]



pg.init()
s_w = 1000
s_h = 600
circle_pos = False

screen = pg.display.set_mode((s_w,s_h))
fps = 60
fps_clock = pg.time.Clock()
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    if key_press('c'):
        if type(circle_pos) == bool:
            circle_pos = get_m_pos()
            print(circle_pos)
        

    
    update_pressed()
    pg.display.update()
    fps_clock.tick(fps)
pg.quit()