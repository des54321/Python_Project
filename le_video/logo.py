import pygame as pg
from pygame import draw,Vector2


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

def draw_circle(pos,size,color):
    pg.draw.circle(screen,color,(pos[0]+(sw/2),sh-(pos[1]+(sh/2))),round(size))


def draw_poly(pos,color):
    pg.draw.polygon(screen,color,[(i[0]+(sw/2),sh-(i[1]+(sh/2))) for i in pos])

def draw_rect(pos,width,height,color):
    pg.draw.rect(screen,color,pg.Rect(pos[0]+(sw/2),sh-(pos[1]+(sh/2)),width,height))

def draw_line(pos1,pos2):
    pg.draw.line(screen,line_color,(pos1[0]+(sw/2),sh-(pos1[1]+(sh/2))),(pos2[0]+(sw/2),sh-(pos2[1]+(sh/2))),round(line_width))

def key_press(key: str):
    return pressed[pressed_letters.index(key)]



def key_down(key: pg.key) -> bool:
    return pg.key.get_pressed()[key]

p1 = (0,200)
p2 = (141.4,141.4)
p3 = (200,0)
p4 = (141.4,-141.4)
p5 = (0,-200)
p6 = (-141.4,-141.4)
p7 = (-200,0)
p8 = (-141.4,141.4)
p9 = (100,100)
p10 = (100,-100)
p11 = (-100,-100)
p12 = (-100,100)
pink = (240,190,193)
blue = (150,150,240)

line_width = 5
line_color = (220,240,250)

pg.init()
sw = 500
sh = 500
screen = pg.display.set_mode((sw,sh))
fps = 60
fps_clock = pg.time.Clock()
running = True
while running:
    screen.fill((8,10,9))
    draw_poly((p1,p2,p3,p4,p5,p6,p7,p8),blue)
    draw_line(p9,p8)
    draw_line(p12,p2)

    draw_line(p11,p4)
    draw_line(p4,p9)
    draw_line(p10,p6)
    draw_line(p6,p12)
    draw_line(p8,p11)
    draw_line(p2,p10)

    draw_poly((p1,p6,p5,p4),pink)

    draw_line(p11,p4)
    draw_line(p4,p9)
    draw_line(p10,p6)
    draw_line(p6,p12)
    draw_line(p8,p11)
    draw_line(p2,p10)

    draw_line(p1,p2)
    draw_line(p2,p3)
    draw_line(p3,p4)
    draw_line(p4,p5)
    draw_line(p5,p6)
    draw_line(p6,p7)
    draw_line(p7,p8)
    draw_line(p8,p1)

    draw_line(p1,p6)
    draw_line(p1,p4)


    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    
    update_pressed()
    pg.display.update()
    fps_clock.tick(fps)
pg.quit()