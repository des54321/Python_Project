import hexa
import pygame as pg
from pygame import Vector2
from math import floor
from menu_engine import Text,Menu,Slider,Button



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


def draw_tile(tile:hexa.Tile):
    if tile == touching:
        tile.render(screen,color_pal[2],color_pal[2],6)
    else:
        tile.render(screen,color_pal[3],color_pal[2],6)

    if tile.has[0] == 'blank':
        return 0

    if tile.has[0] == 'base':
        hexa.Tile(hexagon,tile.screen_pos).render(screen,player_colors[tile.has[1]],None)




pg.init()
sw = 1600
sh = 900
screen = pg.display.set_mode((sw,sh))
fps = 60
fps_clock = pg.time.Clock()


color_pal = ((255, 212, 212),'#A0E4CB',(205, 233, 144),(170, 203, 115))

player_colors = ('#D61C4E','#FEDB39')


gw = 15
gh = 7
tile_size = 60
tiles = hexa.hex_grid_l(gw,gh,tile_size,(sw/2,sh/2))
for i in tiles:
    i.has = ['blank',None]

tiles[floor(gh/2)*gw].has = ['base',0]
tiles[floor(gh/2)*gw+gw-1].has = ['base',1]

player_squares = [0,0]

octagon = hexa.shape(8,tile_size//2,True)
hexagon = hexa.shape(6,tile_size//2)

#Menus
p1_square_counter = Text(f'Player 1 squares: {player_squares[0]}',(None,color_pal[0]),Vector2())



running = True
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    
    screen.fill(color_pal[1])
    touching = hexa.p_touching(pg.mouse.get_pos(),tiles)
    for i in tiles:
        draw_tile(i)
    update_pressed()
    pg.display.update()
    fps_clock.tick(fps)
pg.quit()