import pygame as pg
from pygame import Vector2
import menu_engine as me
import tile_map


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


def add_tile():
    pass


pg.init()
sw = 1600
sh = 900

screen = pg.display.set_mode((sw,sh))

#UI

color_pal = ((33, 33, 33),(15, 76, 117),(50, 130, 184),(187, 225, 250))

tile_select_height = 220

add_tile_button = me.Button('Add Tile',(color_pal[0],color_pal[2]),Vector2(0.75,0.2),Vector2(0.2,0.4),add_tile,'press',3)

tile_select = me.Menu(screen,Vector2(0,sh-tile_select_height),Vector2(0,sh),sw,tile_select_height,color_pal[1],8,[add_tile_button],0.05,(True,True,False,False),True)


#Tiles

tiles = tile_map.TileMap()




fps = 60
fps_clock = pg.time.Clock()

running = True
while running:
    if pg.mouse.get_pressed()[0] and pg.mouse.get_pos()[1] > sh-tile_select_height:
        pass

    if key_press('m'):
        tile_select.direct *= -1
    

    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    
    update_pressed()
    
    screen.fill((0,0,0))
    tile_select.full_update(events)

    pg.display.update()
    fps_clock.tick(fps)
pg.quit()