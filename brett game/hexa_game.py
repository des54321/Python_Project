import hexa
import pygame as pg
from pygame import Vector2
from math import floor
from menu_engine import Text, Menu, Slider, Button


pressed_letters = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "COMMA",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
]
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
        test = eval("pg.K_" + i)
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
    if tile == touching or show_moves_of in tile.connections or tile.selected:
        tile.render(screen, color_pal[2], color_pal[2], line_width)
    else:
        tile.render(screen, color_pal[3], color_pal[2], line_width)

    if tile.build == "base":
        hexa.Tile(hexagon, tile.screen_pos).render(
            screen, player_build_colors[tile.build_color], None
        )

    if tile.build == "factory":
        hexa.Tile(square, tile.screen_pos).render(
            screen, player_build_colors[tile.build_color], None
        )

    if tile.build == "bank":
        hexa.Tile(triangle, tile.screen_pos).render(
            screen, player_build_colors[tile.build_color], None
        )

    if tile.troop_num > 0:
        if tile.troop_num == 1 and tile.captain == None:
            pg.draw.circle(
                screen,
                player_troop_colors[tile.troop_color],
                tile.screen_pos,
                tile_size // 5,
            )
        else:
            for i in hexa.shape(tile.troop_num, tile_size // 1.8):
                pg.draw.circle(
                    screen,
                    player_troop_colors[tile.troop_color],
                    tile.screen_pos + i,
                    tile_size // 5,
                )

    if tile.captain != None:
        if tile.captain == "speed":
            hexa.Tile(double_arrow, tile.screen_pos).render(
                screen, player_troop_colors[tile.troop_color], None
            )
        if tile.captain == "sniper":
            pg.draw.circle(
                screen,
                player_troop_colors[tile.troop_color],
                tile.screen_pos,
                tile_size * 0.25,
                round(tile_size * 0.08),
            )
            pg.draw.line(
                screen,
                player_troop_colors[tile.troop_color],
                tile.screen_pos + Vector2(0, tile_size * 0.2),
                tile.screen_pos + Vector2(0, -tile_size * 0.2),
                round(tile_size * 0.08),
            )
            pg.draw.line(
                screen,
                player_troop_colors[tile.troop_color],
                tile.screen_pos + Vector2(tile_size * 0.2, 0),
                tile.screen_pos + Vector2(-tile_size * 0.2, 0),
                round(tile_size * 0.08),
            )


def update_turns():
    global tiles, show_moves_of, builder_moves, kind_selected
    show_moves_of = None
    for i in tiles:
        i.selected = False
        i.moves_left = 0
        if i.troop_num == 0 and i.captain == None:
            i.troop_color = None
        if i.build == None:
            i.build_color = None
    if current_action == 0:
        kind_selected = None
        new = [action_text, done_button]
        action_menu.new_contents(new)
        bank_num = 0
        for i in tiles:
            if i.build_color == turn and i.build == "bank":
                bank_num += 1
        player_squares[turn] += base_square_gen + bank_num
        for i in tiles:
            i: hexa.Tile
            if i.build_color == turn and i.build == "factory":
                i.troop_num = min(i.troop_num + 1, max_troops_per_square)
                i.troop_color = turn

            if i.troop_color == turn:
                if i.captain == "speed":
                    i.moves_left = 2
                else:
                    i.moves_left = 1
            else:
                i.moves_left = 0
    if current_action == 1:
        kind_selected = [None, 0]
        new = [action_text, done_button]
        for n, i in enumerate(buildings):
            new.append(
                Button(
                    i[0],
                    (color_pal[1], color_pal[2]),
                    (n * 0.13 + 0.03, 0.35),
                    (0.1, 0.3),
                    new_kind_selected,
                    "press",
                    5,
                    True,
                    True,
                    i,
                )
            )
        action_menu.new_contents(new)
        for n, i in enumerate(builder_moves):
            for y, x in enumerate(i):
                if n == turn:
                    builder_moves[n][y] = 2

    if current_action == 2:
        kind_selected = None
        new = [action_text, done_button]
        for n, i in enumerate(captains):
            new.append(
                Button(
                    i,
                    (color_pal[1], color_pal[2]),
                    (n * 0.13 + 0.03, 0.35),
                    (0.1, 0.3),
                    new_kind_selected,
                    "press",
                    5,
                    True,
                    True,
                    i,
                )
            )
        action_menu.new_contents(new)
        for i in tiles:
            if i.captain == "sniper" and i.troop_color == turn:
                i.moves_left = 1


def move_troops(start: hexa.Tile, end: hexa.Tile):
    if end.troop_color != None:
        end_value = value_of(end)
        start_value = value_of(start)
        if end.troop_color == start.troop_color:
            if end.captain == None:
                end.captain = start.captain
                start.captain = None

            pre_end_troop_num = end.troop_num
            end.troop_num = min(
                start.troop_num + pre_end_troop_num, max_troops_per_square
            )
            start.troop_num = start.troop_num - (
                min(start.troop_num + pre_end_troop_num, max_troops_per_square)
                - pre_end_troop_num
            )
            if start.troop_num == 0:
                start.troop_color = None
        else:
            if end_value == start_value:
                start.moves_left = 0
                start.troop_num = 0
                start.troop_color = None
                start.captain = None
                end.moves_left = 0
                end.troop_num = 0
                end.troop_color = None
                end.captain = None
            elif start_value > end_value:
                if end.build_color != start.troop_color:
                    end.build = None
                    end.build_color = None
                end.troop_color = start.troop_color
                if (start.captain != None) and (
                    start_value - end_value >= captain_value
                ):
                    end.captain = start.captain
                    end.troop_num = start_value - end_value - captain_value
                else:
                    end.captain = None
                    end.troop_num = start_value - end_value
            else:
                if (end.captain != None) and (end_value - start_value >= captain_value):
                    end.troop_num = end_value - start_value - captain_value
                else:
                    end.captain = None
                    end.troop_num = end_value - start_value
            start.troop_num = 0
            start.troop_color = None
            start.captain = None

    else:
        if end.build_color != start.troop_color:
            end.build = None
            end.build_color = None
        end.troop_num = start.troop_num
        end.troop_color = start.troop_color
        end.captain = start.captain
        start.troop_num = 0
        start.troop_color = None
        start.captain = None


def value_of(tile):
    return tile.troop_num + int(tile.captain != None) * captain_value


def damage_tile(tile: hexa.Tile, damage):
    if value_of(tile) > damage:
        value = value_of(tile)
        if (tile.captain != None) and (value - damage >= captain_value):
            tile.troop_num = value - damage - captain_value
        else:
            tile.captain = None
            tile.troop_num = value - damage


def draw_builders():
    for n, i in enumerate(player_builders):
        for x in i:
            x: hexa.Tile
            x.render(screen, None, player_troop_colors[n], line_width)


def check_builders():
    for n, i in enumerate(player_builders):
        for y, x in enumerate(i):
            x: hexa.Tile
            if n != x.troop_color and x.troop_color != None:
                del player_builders[n][y]


def next_action():
    global buildings, kind_selected, turn, current_action
    current_action += 1
    if current_action >= len(action_order):
        turn += 1
        turn %= len(player_build_colors)
        current_action = 0
    update_turns()


def new_kind_selected(new):
    global kind_selected
    kind_selected = new


pg.init()
# sw = 1600
# sh = 900
# screen = pg.display.set_mode((sw, sh))
sw = 1920
sh = 1080
screen = pg.display.set_mode((sw, sh), pg.FULLSCREEN)

fps = 60
fps_clock = pg.time.Clock()


color_pal = (
    (255, 212, 212),
    (105, 105, 155),
    (205, 233, 144),
    (170, 203, 115),
    (150, 150, 230),
)

player_build_colors = ("#E62C5E", "#FEDB39")
player_troop_colors = ("#B6132E", "#EECB19")


gw = 15
gh = 7
tile_size = sh * 0.0566
line_width = round(sh * 0.00666)
tiles = hexa.hex_grid_l(gw, gh, tile_size, (sw / 2, sh / 1.7))


tiles[floor(gh / 2) * gw].build = "base"
tiles[floor(gh / 2) * gw].build_color = 0


tiles[floor(gh / 2) * gw + gw - 1].build = "base"
tiles[floor(gh / 2) * gw + gw - 1].build_color = 1

player_builders = [
    [tiles[floor(gh / 2) * gw + 1]],
    [tiles[floor(gh / 2) * gw - 2 + gw]],
]

builder_moves = [[0], [0]]


kind_selected = None
buildings = [[None, 0], ["factory", 5], ["bank", 9]]
captains = [None, "sniper", "speed", "builder"]

base_square_gen = 3
starting_squares = 10
player_squares = [starting_squares - base_square_gen, starting_squares]

octagon = hexa.shape(8, tile_size // 2, True)
triangle = hexa.shape(3, tile_size // 2)
hexagon = hexa.shape(6, tile_size // 2)
square = hexa.shape(4, tile_size // 2, True)
double_arrow = ((-1, 1), (-1, -1), (0, 0), (0, -1), (1, 0), (0, 1), (0, 0))
double_arrow = [Vector2(i) * tile_size * 0.25 for i in double_arrow]


max_troops_per_square = 5
captain_value = 4
captain_cost = 5
sniper_damage = 2
sniper_range = 5.1


first_mouse = [False, False, False]
mouse = [False, False, False]

action_order = ("Move Troops", "Build", "Use specials")

current_action = 0

using = None

turn = 0

# Menus
p1_square_counter = Text(
    f"{player_squares[0]}",
    (None, player_build_colors[0]),
    (0.02, 0.3),
    (0.2, 0.4),
    False,
    text_pos=["left", "center"],
)
p2_square_counter = Text(
    f"Player 2 squares: {player_squares[1]}",
    (None, player_build_colors[1]),
    (0.78, 0.3),
    (0.2, 0.4),
    False,
    text_pos=["right", "center"],
)


counter_menu = Menu(
    screen,
    (0, sh / 2),
    (0, sh / 2),
    sw,
    sh / 2,
    None,
    0,
    [p1_square_counter, p2_square_counter],
)


menu_size = sh * 0.2

action_text = Text("None", (None, color_pal[0]), (0.4, 0.015), (0.2, 0.2), False)
done_button = Button(
    "Done",
    (color_pal[0], color_pal[1]),
    (0.78, 0.4),
    (0.2, 0.3),
    next_action,
    "press",
    5,
)


action_menu = Menu(
    screen,
    (0, 0),
    (0, -menu_size),
    sw,
    menu_size,
    color_pal[4],
    25,
    [action_text, done_button],
    1,
    (False, False, True, True),
)

update_turns()
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
    first_mouse = mouse
    mouse = pg.mouse.get_pressed()
    first_mouse = [mouse[i] and not first_mouse[i] for i in range(3)]

    for i in tiles:
        draw_tile(i)

    draw_builders()

    counter_menu.full_update(events)
    action_menu.full_update(events)

    p1_square_counter.text = f"{player_squares[0]}"
    p2_square_counter.text = f"{player_squares[1]}"

    if not touching == None:
        if mouse[0]:
            if current_action == 0:
                if show_moves_of == None:
                    if (
                        value_of(touching) > 0
                        and touching.troop_color == turn
                        and touching.moves_left > 0
                    ):
                        show_moves_of = touching
                else:
                    if not show_moves_of == touching:
                        if show_moves_of in touching.connections:
                            move_troops(show_moves_of, touching)
                            touching.moves_left = show_moves_of.moves_left - 1
                        show_moves_of = None

            elif current_action == 1:
                if show_moves_of != None:
                    other_builder = False
                    for i in player_builders:
                        for x in i:
                            if x == touching:
                                other_builder = True
                    if (
                        (show_moves_of in touching.connections)
                        and (
                            touching.troop_color == turn or touching.troop_color == None
                        )
                        and (
                            touching.build_color == turn or touching.build_color == None
                        )
                        and (not other_builder)
                    ):
                        num = player_builders[turn].index(show_moves_of)
                        player_builders[turn][num] = touching
                        builder_moves[turn][num] -= 1
                    show_moves_of = None

                if touching in player_builders[turn]:
                    if builder_moves[turn][player_builders[turn].index(touching)] > 0:
                        show_moves_of = touching

            elif current_action == 2:
                if kind_selected == None:
                    if touching.selected:
                        for i in tiles:
                            i.selected = False
                        using.moves_left -= 1
                        if value_of(touching) <= sniper_damage:
                            touching.troop_color = None
                            touching.troop_num = 0
                            touching.captain = None
                            touching.moves_left = 0
                        else:
                            damage_tile(touching, sniper_damage)
                    else:
                        if (
                            touching.captain == "sniper"
                            and touching.troop_color == turn
                        ):
                            if touching.moves_left > 0 and first_mouse[0]:
                                using = touching
                                for i in tiles:
                                    i: hexa.Tile
                                    if (
                                        (i.troop_color != turn)
                                        and (i.troop_color != None)
                                        and (
                                            i.screen_pos.distance_to(
                                                touching.screen_pos
                                            )
                                            / tile_size
                                            < sniper_range
                                        )
                                    ):
                                        i.selected = True
                                    else:
                                        i.selected = False
                        else:
                            for i in tiles:
                                i.selected = False
                else:
                    if (
                        touching.troop_color == turn
                        and touching.troop_num == max_troops_per_square
                        and player_squares[turn] >= captain_cost
                    ):
                        if kind_selected == "builder":
                            has_builder = False
                            for i in player_builders:
                                for x in i:
                                    if x == touching:
                                        has_builder = True
                            if not has_builder:
                                touching.troop_num = 0
                                player_builders[turn].append(touching)
                                builder_moves[turn].append(0)
                                player_squares[turn] -= captain_cost
                        else:
                            if touching.captain == None:
                                touching.troop_num = 0
                                touching.captain = kind_selected
                                player_squares[turn] -= captain_cost

        if touching.build == None and mouse[0]:
            if current_action == 1:
                if (
                    touching.troop_color == None or touching.troop_color == turn
                ) and kind_selected != None:
                    if touching in player_builders[turn]:
                        if player_squares[turn] >= kind_selected[1]:
                            touching.build = kind_selected[0]
                            touching.build_color = turn
                            player_squares[turn] -= kind_selected[1]

    check_builders()

    if key_press("d"):
        next_action()

    action_text.text = f"Player {turn+1} {action_order[current_action]}"

    update_pressed()
    pg.display.update()
    fps_clock.tick(fps)

    if key_down(pg.K_BACKSPACE):
        running = False
pg.quit()
