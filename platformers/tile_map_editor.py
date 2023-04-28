import pygame as pg
from pygame import Vector2
import menu_engine as me
import tile_map
from math import floor


pressed_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o','p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'COMMA', '1', '2', '3','4', '5', '6', '7', '8', '9', '0','LEFT','RIGHT']
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
    global temp_tile, mode
    temp_tile = [[0 for __ in range(tile_size)] for _ in range(tile_size)]
    mode  = 'make tile'


def set_tile(tile):
    global placing
    placing = tile


def finish_tile():
    global mode, tiles, tile_select
    mode = 'tile map'
    tiles.add_tile(temp_tile)
    tile_select.contents.append(me.Button(f'Tile {len(tiles.tile_pal)-1}',(color_pal[0],color_pal[2]),Vector2(0.05+0.2*(len(tiles.tile_pal)-1),0.2),Vector2(0.15,0.2),set_tile,'press',3,has_func_arg=True,fucn_arg=len(tiles.tile_pal)-1))
    tile_select.contents[-1].menu = tile_select



mode = 'tile map'
placing = 0


tile_colors = ('#F9F7F7','#BBC2CF','#3F72AF','#112D4E',(230,130,140),(240,230,120),(20,30,50))

#Tiles

tile_size = 4
pixel_size = 7
tw = 32
th = 32
tiles = tile_map.TileMap(tile_colors,tile_size,tw,th,pixel_size)
temp_tile = [[0 for __ in range(tile_size)] for _ in range(tile_size)]
tiles.tile_pal = [[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], [[2, 2, 2, 2], [2, 1, 1, 2], [2, 1, 1, 2], [2, 2, 2, 2]]]
tiles.update_sur()
tiles.tiles = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
placing_color = 0



pg.init()
sw = tw*tile_size*pixel_size
sh = th*tile_size*pixel_size

screen = pg.display.set_mode((sw,sh))

#UI

color_pal = ((33, 33, 33),(15, 76, 117),(50, 130, 184),(187, 225, 250))

tile_select_height = int(0.25*sh)

add_tile_button = me.Button('Add Tile',(color_pal[0],color_pal[2]),Vector2(0.75,0.2),Vector2(0.2,0.2),add_tile,'press',3)

tile_select = me.Menu(screen,Vector2(0,sh-tile_select_height),Vector2(0,sh),sw,tile_select_height,color_pal[1],8,[add_tile_button],0.05,(True,True,False,False),True)
for i in range(len(tiles.tile_pal)):
    tile_select.contents.append(me.Button(f'Tile {i}',(color_pal[0],color_pal[2]),Vector2(0.05+0.2*i,0.2),Vector2(0.15,0.2),set_tile,'press',3,has_func_arg=True,fucn_arg=i))
    tile_select.contents[-1].menu = tile_select


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
    if mode == 'tile map':
        add_tile_button.icon = 'Add Tile'
        add_tile_button.action = add_tile
        tiles.render(screen)

        if pg.mouse.get_pressed()[0] and (pg.mouse.get_pos()[1] < sh-tile_select_height or tile_select.slide_progress == 0):
            tiles.tiles[floor(pg.mouse.get_pos()[0]/(pixel_size*tile_size))][floor(pg.mouse.get_pos()[1]/(pixel_size*tile_size))] = placing
    else:
        add_tile_button.icon = 'Finish'
        add_tile_button.action = finish_tile
        for x in range(tile_size):
            for y in range(tile_size):
                    pg.draw.rect(screen,tile_colors[temp_tile[x][y]],pg.Rect(tw*x*pixel_size,th*y*pixel_size,tw*pixel_size,th*pixel_size))
        
        if pg.mouse.get_pressed()[0] and (pg.mouse.get_pos()[1] < sh-tile_select_height or tile_select.slide_progress == 0):
            temp_tile[floor(pg.mouse.get_pos()[0]/(tw*pixel_size))][floor(pg.mouse.get_pos()[1]/(th*pixel_size))] = placing_color
        

        if key_down(pg.K_p):
            placing_color = temp_tile[floor(pg.mouse.get_pos()[0]/(tw*pixel_size))][floor(pg.mouse.get_pos()[1]/(th*pixel_size))]
        if key_press('LEFT'):
            placing_color -= 1
        if key_press('RIGHT'):
            placing_color += 1
        placing_color %= len(tile_colors)
    
    if key_press('e'):
        print('')
        print('Tile Pal')
        print(tiles.tile_pal)
        print('')
        print('Tiles')
        print(tiles.tiles)

    
    tile_select.full_update(events)

    pg.display.update()
    fps_clock.tick(fps)
pg.quit()