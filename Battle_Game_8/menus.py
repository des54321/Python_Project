import pygame as pg
from pygame import Vector2
from menu_engine import Text, Button, Menu, Slider
from battle_new import players, Player, all_chars, screen, reset_players
from render import draw_tank_base
from graphics_settings import sw, sh, color_pal, backdrop, outside_color
from random_presets import team_names


# Settings
declare_box_length = 100
declare_box_fade = 10
declare_box_timer = 0



def declare(txt):
    global declare_box_timer
    declare_box_timer = declare_box_length
    declare_box.text = txt
    delcare_menu.slide_progress = 0


# Menu functions


def go_to_char_select():
    global current_page
    current_page = "char_select"


def go_to_pause_menu():
    global current_page
    current_page = "pause"


def go_to_game(reset=True):
    global current_page, controllers, controller_input
    if len(players) < 2:
        declare("Set-up chars first")
    else:
        if reset:
            controller_input = []
            controllers = []
            for i in range(pg.joystick.get_count()):
                controllers.append(pg.joystick.Joystick(i))
                controller_input.append(
                    [
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        [0, 0],
                        [0, 0],
                        [False, False],
                    ]
                )

            for controller in controllers:
                controller.init()
            reset_players()
        current_page = "game"


def go_to_settings():
    global current_page
    current_page = "settings"


def go_to_start():
    global current_page
    current_page = "start"


# Slider funcs
boundary_size = 1500


def boundary_size_slider_func(set_get):
    global boundary_size

    var_min = 500
    var_max = 3000
    if set_get == "get":
        return (boundary_size - var_min) / (var_max - var_min)
    else:
        boundary_size = var_min + ((var_max - var_min) * set_get)


bot_target_dist = 400


def bot_target_dist_slider_func(set_get):
    global bot_target_dist

    var_min = 150
    var_max = 1200
    if set_get == "get":
        return (bot_target_dist - var_min) / (var_max - var_min)
    else:
        bot_target_dist = var_min + ((var_max - var_min) * set_get)


controller_barrel_rot_speed = 8


def controller_barrel_rot_speed_slider_func(set_get):
    global controller_barrel_rot_speed

    var_min = 3
    var_max = 16
    if set_get == "get":
        return (controller_barrel_rot_speed - var_min) / (var_max - var_min)
    else:
        controller_barrel_rot_speed = var_min + ((var_max - var_min) * set_get)


keyboard_barrel_rot_speed = 3


def keyboard_barrel_rot_speed_slider_func(set_get):
    global keyboard_barrel_rot_speed

    var_min = 3
    var_max = 16
    if set_get == "get":
        return (keyboard_barrel_rot_speed - var_min) / (var_max - var_min)
    else:
        keyboard_barrel_rot_speed = var_min + ((var_max - var_min) * set_get)


respawn_immunity = 200


def respawn_immunity_slider_func(set_get):
    global respawn_immunity

    var_min = 0
    var_max = 500
    if set_get == "get":
        return (respawn_immunity - var_min) / (var_max - var_min)
    else:
        respawn_immunity = var_min + ((var_max - var_min) * set_get)


bots = 0


def bots_slider_func(set_get):
    global bots

    var_min = 0
    var_max = 7
    if set_get == "get":
        return (bots - var_min) / (var_max - var_min)
    else:
        bots = var_min + ((var_max - var_min) * set_get)

    bots = round(bots)


# Char select funcs


def add_player():
    if not len(players) > 7:
        players.append(Player(all_chars[0], "red", 0, 0, ["keyboard", 0]))


def remove_player(player):
    del players[players.index(player)]


def next_char(player):
    if player < len(players):
        players[player].type = all_chars[
            (all_chars.index(players[player].type) + 1) % len(all_chars)
        ]


def pre_char(player):
    if player < len(players):
        players[player].type = all_chars[
            (all_chars.index(players[player].type) - 1) % len(all_chars)
        ]


def next_team(player):
    if player < len(players):
        players[player].team = team_names[
            (team_names.index(players[player].team) + 1) % len(team_names)
        ]


def draw_player_menus():
    for n, i in enumerate(players):
        draw_tank_base(
            0.11 * sh,
            i.type,
            Vector2(0, 80),
            i.team,
            sw * ((n % 4) * 0.2 + 0.2),
            sh * ((n // 4) * 0.4 + 0.21),
            True,
        )


def update_player_menus():
    if len(players) > 7:
        add_player_button.icon = "Max Players"
    else:
        add_player_button.icon = "Add Player"

    joy_num = pg.joystick.get_count()
    for n, i in enumerate(player_menus):
        if len(players) > n // player_menu_num:
            i.show = True
            if n % player_menu_num == 3:
                i: Text
                i.text = players[n // player_menu_num].type.name
            if n % player_menu_num == 4:
                i: Text
                if joy_num > n // player_menu_num:
                    players[n // player_menu_num].movement = [
                        "controller",
                        n // player_menu_num,
                    ]
                    i.text = f"Controller {n//player_menu_num + 1}"
                elif joy_num + bots > n // player_menu_num:
                    players[n // player_menu_num].movement = [
                        "bot",
                        n // player_menu_num - joy_num,
                    ]
                    i.text = f"Bot {n//player_menu_num - joy_num + 1}"
                else:
                    players[n // player_menu_num].movement = [
                        "keyboard",
                        n // player_menu_num - joy_num - bots,
                    ]
                    i.text = f"Keyboard {n//player_menu_num - joy_num - bots + 1}"

        else:
            i.show = False


# Declare box
declare_box = Text("Nan", (None, color_pal[2]), (0, 0), ((1, 1)), False)
delcare_menu = Menu(
    screen,
    (sw * 0.5, sh * 0.9),
    (sw * 0.5, sh),
    sw * 0.5,
    sh * 0.1,
    None,
    0,
    [declare_box],
    1 / declare_box_fade,
)


# Start menu
start_button = Button(
    "Play ",
    (color_pal[1], color_pal[2]),
    (-0.05, 0.4),
    (0.3, 0.1),
    go_to_game,
    "press",
    15,
    text_pos=["right", "center"],
)
settings_button_main = Button(
    "Options ",
    (color_pal[1], color_pal[2]),
    (-0.05, 0.7),
    (0.3, 0.1),
    go_to_settings,
    "press",
    15,
    text_pos=["right", "center"],
)
char_select_button = Button(
    "Chars ",
    (color_pal[1], color_pal[2]),
    (-0.05, 0.55),
    (0.3, 0.1),
    go_to_char_select,
    "press",
    15,
    text_pos=["right", "center"],
)
title_text = Text(
    "Battle Game", (color_pal[0], color_pal[2]), (0.4, 0.1), (0.4, 0.2), False
)

start_menu = Menu(
    screen,
    (0, 0),
    (0, sh),
    sw,
    sh,
    color_pal[0],
    0,
    [start_button, title_text, settings_button_main, char_select_button],
)


# Character select
add_player_button = Button(
    "Add Player",
    (color_pal[1], color_pal[2]),
    (0.15, 0.88),
    (0.25, 0.08),
    add_player,
    "press",
    5,
)
done_char_button = Button(
    "Done",
    (color_pal[1], color_pal[2]),
    (0.6, 0.88),
    (0.25, 0.08),
    go_to_start,
    "press",
    5,
)

# The player menus
player_menu_num = 5
player_menus = []
for i in range(8):
    player_menus.append(
        Button(
            "Pre",
            (color_pal[1], color_pal[2]),
            ((i % 4) * 0.2 + 0.125, (i // 4) * 0.4 + 0.4),
            (0.05, 0.04),
            pre_char,
            "press",
            5,
            True,
            True,
            i,
        )
    )
    player_menus.append(
        Button(
            "Next",
            (color_pal[1], color_pal[2]),
            ((i % 4) * 0.2 + 0.225, (i // 4) * 0.4 + 0.4),
            (0.05, 0.04),
            next_char,
            "press",
            5,
            True,
            True,
            i,
        )
    )
    player_menus.append(
        Button(
            "Change Team",
            (color_pal[1], color_pal[2]),
            ((i % 4) * 0.2 + 0.125, (i // 4) * 0.4 + 0.28),
            (0.15, 0.04),
            next_team,
            "press",
            5,
            True,
            True,
            i,
        )
    )
    player_menus.append(
        Text(
            "None",
            (color_pal[2], color_pal[1]),
            ((i % 4) * 0.2 + 0.125, (i // 4) * 0.4 + 0.335),
            (0.15, 0.05),
            False,
            15,
        )
    )
    player_menus.append(
        Text(
            "None",
            (color_pal[2], color_pal[1]),
            ((i % 4) * 0.2 + 0.125, (i // 4) * 0.4 + 0.05),
            (0.15, 0.04),
            False,
            5,
        )
    )

char_select = Menu(
    screen,
    Vector2(0, 0),
    Vector2(0, sh),
    sw,
    sh,
    color_pal[0],
    0,
    [add_player_button, done_char_button] + player_menus,
)


# Pause menu
resume_button = Button(
    "Resume",
    (color_pal[1], color_pal[2]),
    Vector2(0.35, 0.45),
    Vector2(0.3, 0.1),
    go_to_game,
    "press",
    10,
    True,
    True,
    False,
)
quit_to_main_pause = Button(
    "Quit",
    (color_pal[1], color_pal[2]),
    Vector2(0.35, 0.6),
    Vector2(0.3, 0.1),
    go_to_start,
    "press",
    10,
)
pause_text = Text(
    "Pause", (color_pal[0], color_pal[2]), Vector2(0.2, 0.1), Vector2(0.6, 0.2), False
)

pause_menu = Menu(
    screen,
    Vector2(0, 0),
    Vector2(0, sh),
    sw,
    sh,
    color_pal[0],
    0,
    [resume_button, quit_to_main_pause, pause_text],
)


# Settings menu
boundary_size_slider = Slider(
    "Wall size",
    (color_pal[1], color_pal[3], color_pal[2]),
    Vector2(0.05, 0.2),
    Vector2(0.3, 0.1),
    boundary_size_slider_func,
    5,
)
con_rot_slider = Slider(
    "Joy Rot",
    (color_pal[1], color_pal[3], color_pal[2]),
    Vector2(0.05, 0.50),
    Vector2(0.3, 0.1),
    controller_barrel_rot_speed_slider_func,
    5,
)
key_rot_slider = Slider(
    "Key Rot",
    (color_pal[1], color_pal[3], color_pal[2]),
    Vector2(0.05, 0.65),
    Vector2(0.3, 0.1),
    keyboard_barrel_rot_speed_slider_func,
    5,
)
rep_imm_slider = Slider(
    "Immune Time",
    (color_pal[1], color_pal[3], color_pal[2]),
    Vector2(0.05, 0.80),
    Vector2(0.3, 0.1),
    respawn_immunity_slider_func,
    5,
)
bot_target_dist_slider = Slider(
    "Bot Target Dist",
    (color_pal[1], color_pal[3], color_pal[2]),
    Vector2(0.55, 0.2),
    Vector2(0.3, 0.1),
    bot_target_dist_slider_func,
    5,
)
bots_slider = Slider(
    "Bot Number",
    (color_pal[1], color_pal[3], color_pal[2]),
    Vector2(0.55, 0.35),
    Vector2(0.3, 0.1),
    bots_slider_func,
    5,
)


back_button_settings = Button(
    [
        [
            (0.9, 0.4),
            (0.9, 0.6),
            (0.35, 0.6),
            (0.35, 0.85),
            (0.05, 0.55),
            (0.05, 0.45),
            (0.35, 0.15),
            (0.35, 0.4),
        ]
    ],
    (color_pal[0], color_pal[1]),
    Vector2(0.05, 0.05),
    Vector2(0.075, 0.1),
    go_to_start,
    "press",
    5,
)
settings_text = Text(
    "Settings",
    (color_pal[0], color_pal[2]),
    Vector2(0.2, 0.05),
    Vector2(0.6, 0.1),
    False,
)

settings_menu = Menu(
    screen,
    Vector2(0, 0),
    Vector2(0, sh),
    sw,
    sh,
    color_pal[0],
    0,
    [
        boundary_size_slider,
        settings_text,
        back_button_settings,
        con_rot_slider,
        key_rot_slider,
        rep_imm_slider,
        bot_target_dist_slider,
        bots_slider,
    ],
)


# Game menu
fps_counter = Text(
    "NaN",
    (backdrop, outside_color),
    Vector2(0.1, 0.6),
    Vector2(0.8, 0.2),
    editable=False,
)
things_counter = Text(
    "NaN",
    (backdrop, outside_color),
    Vector2(0.1, 0.8),
    Vector2(0.8, 0.2),
    editable=False,
)
pause_button = Button(
    [
        [(0.45, 0.1), (0.3, 0.1), (0.3, 0.9), (0.45, 0.9)],
        [(0.55, 0.1), (0.7, 0.1), (0.7, 0.9), (0.55, 0.9)],
    ],
    (backdrop, outside_color),
    Vector2(0.1, 0.05),
    Vector2(0.8, 0.5),
    go_to_pause_menu,
    "press",
)

game_menu = Menu(
    screen,
    Vector2(0, 0),
    Vector2(0, 0),
    80,
    80,
    backdrop,
    0,
    [fps_counter, things_counter, pause_button],
)
