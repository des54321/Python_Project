import pygame as pg
import os




os.chdir('Battle Game 8')

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
s_w = 1000
s_h = 600
screen = pg.display.set_mode((s_w,s_h))
fps = 60
fps_clock = pg.time.Clock()
running = True


red_tank_base = pg.image.load('Tanks/tank_bottom.png')
green_tank_base = red_tank_base.copy()
blue_tank_base = red_tank_base.copy()
yellow_tank_base = red_tank_base.copy()
#Make green tank green
pixels_green = pg.PixelArray(green_tank_base)
pixels_blue = pg.PixelArray(blue_tank_base)
pixels_yellow = pg.PixelArray(yellow_tank_base)
                                           
for x in range(green_tank_base.get_width()):
    for y in range(green_tank_base.get_height()):
        #Make green tank green
        rgb = green_tank_base.unmap_rgb(pixels_green[x][y])
        color = pg.Color(*rgb)
        h, s, l, a = color.hsla
        color.hsla = (int(h) + 110) % 360, int(s), int(l), int(a)
        pixels_green[x][y] = color

        #Make blue tank blue
        rgb = blue_tank_base.unmap_rgb(pixels_blue[x][y])
        color = pg.Color(*rgb)
        h, s, l, a = color.hsla
        color.hsla = (int(h) + 200) % 360, int(s), int(l), int(a)
        pixels_blue[x][y] = color

        #Make yellow tank yellow
        rgb = yellow_tank_base.unmap_rgb(pixels_yellow[x][y])
        color = pg.Color(*rgb)
        h, s, l, a = color.hsla
        color.hsla = (int(h) + 60) % 360, int(s), int(l), int(a)
        pixels_yellow[x][y] = color
del pixels_green
del pixels_blue
del pixels_yellow

red_tank_base = pg.transform.scale(red_tank_base,(100,200))
red_tank_base = pg.transform.rotate(red_tank_base,247)
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False


    screen.fill((210,70,102))
    blue_tank_base = pg.transform.scale(blue_tank_base,(100,200))
    screen.blit(blue_tank_base,(s_w//2,s_h//2))
    green_tank_base = pg.transform.scale(green_tank_base,(100,200))
    screen.blit(green_tank_base,(0,0))
    yellow_tank_base = pg.transform.scale(yellow_tank_base,(100,200))
    screen.blit(yellow_tank_base,(s_w//2,0))
    size = red_tank_base.get_size()
    screen.blit(red_tank_base,(0,s_h//2))
    pg.draw.circle(screen,(0,0,0),(size[0]//2,(s_h//2)+size[1]//2),10)

    
    
    update_pressed()
    pg.display.update()
    fps_clock.tick(fps)
pg.quit()