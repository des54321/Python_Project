import hexa
import pygame as pg
from pygame import Vector2
from math import floor
from menu_engine import Text, Menu, Slider, Button


pressed_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                   'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'COMMA', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
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


def draw_tile(tile: hexa.Tile):
    if tile == touching or show_moves_of in tile.connections:
        tile.render(screen, color_pal[2], color_pal[2], round(sh*0.00666))
    else:
        tile.render(screen, color_pal[3], color_pal[2], round(sh*0.00666))

    if tile.troop_num > 0:
        if tile.troop_num == 1:
            pg.draw.circle(
                screen, player_colors[tile.troop_color], tile.screen_pos, tile_size//5)
        else:
            for i in hexa.shape(tile.troop_num, tile_size//2):
                pg.draw.circle(
                    screen, player_colors[tile.troop_color], tile.screen_pos+i, tile_size//5)

    if tile.build == 'base':
        hexa.Tile(hexagon, tile.screen_pos).render(
            screen, player_colors[tile.build_color], None)


pg.init()
sw = 1600
sh = 900
screen = pg.display.set_mode((sw, sh))
fps = 60
fps_clock = pg.time.Clock()


color_pal = ((255, 212, 212), (169, 174, 210),
             (205, 233, 144), (170, 203, 115))

player_colors = ('#D61C4E', '#FEDB39')


gw = 15
gh = 7
tile_size = sh*0.0666
tiles = hexa.hex_grid_l(gw, gh, tile_size, (sw/2, sh/2))


tiles[floor(gh/2)*gw].build = 'base'
tiles[floor(gh/2)*gw].build_color = 0


tiles[floor(gh/2)*gw+gw-1].build = 'base'
tiles[floor(gh/2)*gw+gw-1].build_color = 1


tiles[50].troop_num = 2
tiles[50].troop_color = 1

tiles[76].troop_num = 4
tiles[76].troop_color = 0


player_squares = [0, 0]

octagon = hexa.shape(8, tile_size//2, True)
hexagon = hexa.shape(6, tile_size//2)


max_troops_per_square = 5

action_order = ('Move Troops', 'Build', 'Use special buildings')

current_action = 0


turn = 0

# Menus
p1_square_counter = Text(f'Player 1 squares: {player_squares[0]}', (
    None, player_colors[0]), (0.02, 0.015), (0.2, 0.05), False, text_pos=['left', 'center'])
p2_square_counter = Text(f'Player 2 squares: {player_squares[1]}', (
    None, player_colors[1]), (0.78, 0.015), (0.2, 0.05), False, text_pos=['right', 'center'])
action_text = Text(
    'None', (None, color_pal[0]), (0.4, 0.015), (0.2, 0.05), False)


counter_menu = Menu(screen, (0, 0), (0, 0), sw, sh, None, 0, [
                    p1_square_counter, p2_square_counter, action_text])

show_moves_of = None

running = True
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    screen.fill(color_pal[1])

    touching = hexa.p_touching(pg.mouse.get_pos(), tiles)
    touching: hexa.Tile
    mouse = pg.mouse.get_pressed()

    for i in tiles:
        draw_tile(i)

    counter_menu.full_update(events)

    p1_square_counter.text = f'Player 1 squares: {player_squares[0]}'
    p2_square_counter.text = f'Player 2 squares: {player_squares[1]}'

    if mouse[0]:
        if current_action == 0:
            if touching.troop_num > 0 and touching.troop_color == turn and touching.troop_moves > 0:
                show_moves_of = touching

    if key_press('d'):
        current_action += 1
        if current_action >= len(action_order):
            turn += 1
            turn %= len(player_colors)
            current_action = 0

    action_text.text = f'Player {turn+1} {action_order[current_action]}'

    update_pressed()
    pg.display.update()
    fps_clock.tick(fps)
pg.quit()
