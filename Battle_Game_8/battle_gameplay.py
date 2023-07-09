import math
from math import floor
import pygame as pg
import os
from pygame.math import Vector2
from random import random
import copy
import menu_engine
from menu_engine import Menu, Button, Slider, Text


pg.init()
# os.chdir("C:\\Users\\robin\\Documents\\Python_Project\\Battle_Game_8")
os.chdir("C:\\Users\\angela\\Documents\\Python_Project\\Battle_Game_8")
menu_engine.default_font = "Fonts/Orbitron-Medium.ttf"
game_icon = pg.image.load("play.png")
pg.display.set_icon(game_icon)
pg.display.set_caption("Battle Game!")


print(pg.joystick.get_count())
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


color_pal = ((33, 33, 33), (15, 76, 117), (50, 130, 184), (187, 225, 250))
aim_type = 2
sw = 1920
sh = 1080
screen = pg.display.set_mode((sw, sh), pg.FULLSCREEN)
# sw = 1600
# sh = 900
# screen = pg.display.set_mode((sw,sh))
green_team_hue = 130
blue_team_hue = 210
yellow_team_hue = 40

bot_happy_dist = 50
smart_bot_avoidance = 4


red_tank_base = pg.image.load("Tanks/tank_bottom.png")
green_tank_base = red_tank_base.copy()
blue_tank_base = red_tank_base.copy()
yellow_tank_base = red_tank_base.copy()
immune_tank_base = red_tank_base.copy()

# Make the tanks their color

pixels_green = pg.PixelArray(green_tank_base)
pixels_blue = pg.PixelArray(blue_tank_base)
pixels_yellow = pg.PixelArray(yellow_tank_base)
pixels_immune = pg.PixelArray(immune_tank_base)

for x in range(green_tank_base.get_width()):
    for y in range(green_tank_base.get_height()):
        # Make green tank green
        rgb = green_tank_base.unmap_rgb(pixels_green[x][y])
        color = pg.Color(*rgb)
        h, s, l, a = color.hsla
        color.hsla = (int(h) + green_team_hue) % 360, int(s), int(l), int(a)
        pixels_green[x][y] = color

        # Make blue tank blue
        rgb = blue_tank_base.unmap_rgb(pixels_blue[x][y])
        color = pg.Color(*rgb)
        h, s, l, a = color.hsla
        color.hsla = (int(h) + blue_team_hue) % 360, int(s), int(l), int(a)
        pixels_blue[x][y] = color

        # Make yellow tank yellow
        rgb = yellow_tank_base.unmap_rgb(pixels_yellow[x][y])
        color = pg.Color(*rgb)
        h, s, l, a = color.hsla
        color.hsla = (int(h) + yellow_team_hue) % 360, int(s), int(l), int(a)
        pixels_yellow[x][y] = color

        # Make immune tank gray
        rgb = immune_tank_base.unmap_rgb(pixels_immune[x][y])
        color = pg.Color(*rgb)
        h, s, l, a = color.hsla
        color.hsla = int(h), 0, int(l), int(a)
        pixels_immune[x][y] = color


del pixels_green
del pixels_blue
del pixels_yellow
del pixels_immune








"""
Setting up controller support
"""


key_mapping = {
    "x": 0,
    "circle": 1,
    "square": 2,
    "triangle": 3,
    "share": 4,
    "PS": 5,
    "options": 6,
    "left_stick_click": 7,
    "right_stick_click": 8,
    "L1": 9,
    "R1": 10,
    "up_arrow": 11,
    "down_arrow": 12,
    "left_arrow": 13,
    "right_arrow": 14,
    "touchpad": 15,
}


# up,right,down,left,fire,aim1,aim2,special
keyboard_controls = (
    (pg.K_w, pg.K_d, pg.K_s, pg.K_a, pg.K_SPACE, pg.K_n, pg.K_m, pg.K_LSHIFT),
    (pg.K_i, pg.K_l, pg.K_k, pg.K_j, pg.K_RALT, pg.K_KP1, pg.K_KP3, pg.K_KP_ENTER),
    (pg.K_UP, pg.K_RIGHT, pg.K_DOWN, pg.K_LEFT, pg.K_t, pg.K_r, pg.K_h, pg.K_KP0)
)


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


def go_to_stats():
    global current_page
    current_page = 'stats'


def reset_stats():
    global team_stats
    team_stats = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in players:
        team_stats[team_to_num(i.team)][2] += 1


# Settings/set-up

# Graphics
outside_color = (20, 5, 13)
backdrop = (240, 250, 230)
healthbar_color = (50, 240, 100)
special_ready_color = (160, 30, 150)
declare_box_length = 100
declare_box_fade = 10
declare_box_timer = 0

# Camera
cam_x = 0
cam_y = 0
zoom = 2
respawn_immunity = 200
zoom_radius = 500
grid_spacing = 100
cam_move_speed = 0.15
cam_zoom_speed = 0.1



#Creating background sprites
has_background = False
background = pg.image.load("Background/background.png")
fan = pg.image.load("Background/fan.png")
fan_still = pg.image.load("Background/fan_still.png")
fan_speed = 6
fan_rot = 0

bound_max = 2000
bound_min = 500

        






# Slider funcs
boundary_size = 1500


def boundary_size_slider_func(set_get):
    global boundary_size

    var_min = bound_min
    var_max = bound_max
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


developer_art_val = 0
developer_art = False


def developer_art_slider_func(set_get):
    global developer_art_val
    global developer_art

    var_min = 0
    var_max = 1
    if set_get == "get":
        return (developer_art_val - var_min) / (var_max - var_min)
    else:
        developer_art_val = round(var_min + ((var_max - var_min) * set_get))

    developer_art = developer_art_val > 0.5


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


bot_rand = 2


def bot_rand_slider_func(set_get):
    global bot_rand

    var_min = 0
    var_max = 10
    if set_get == "get":
        return (bot_rand - var_min) / (var_max - var_min)
    else:
        bot_rand = var_min + ((var_max - var_min) * set_get)


smart_bots_val = 0
smart_bots = False


def smart_bots_slider_func(set_get):
    global smart_bots_val
    global smart_bots

    var_min = 0
    var_max = 1
    if set_get == "get":
        return (smart_bots_val - var_min) / (var_max - var_min)
    else:
        smart_bots_val = round(var_min + ((var_max - var_min) * set_get))

    smart_bots = smart_bots_val > 0.5



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


# Class lists
bullets = []
players = []
specials = []


# Team data (red,green,blue,yellow) (kills,killed,players)
team_names = ("red", "green", "blue", "yellow")
team_stats = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]


# Gotta love UI, right, RIGHT?

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
stats_button = Button(
    "Stats ",
    (color_pal[1], color_pal[2]),
    (-0.05, 0.85),
    (0.3, 0.1),
    go_to_stats,
    "press",
    15,
    text_pos=["right", "center"],
)

start_menu = Menu(
    screen,
    (0, 0),
    (0, sh),
    sw,
    sh,
    color_pal[0],
    0,
    [start_button, title_text, settings_button_main, char_select_button,stats_button],
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
developer_art_slider = Slider(
    "'Wow' art",
    (color_pal[1], color_pal[3], color_pal[2]),
    Vector2(0.05, 0.35),
    Vector2(0.3, 0.1),
    developer_art_slider_func,
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
bot_rand_slider = Slider(
    "Bot Rand",
    (color_pal[1], color_pal[3], color_pal[2]),
    Vector2(0.55, 0.5),
    Vector2(0.3, 0.1),
    bot_rand_slider_func,
    5,
)
smart_bots_slider = Slider(
    "Smart Bots",
    (color_pal[1], color_pal[3], color_pal[2]),
    Vector2(0.55, 0.65),
    Vector2(0.3, 0.1),
    smart_bots_slider_func,
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
        developer_art_slider,
        con_rot_slider,
        key_rot_slider,
        rep_imm_slider,
        bot_target_dist_slider,
        bots_slider,
        bot_rand_slider,
        smart_bots_slider
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



#Stats menu

red_team_lable = Text('Red',(None,color_pal[2]),(0.2,0.15),(0.1,0.1),False)
green_team_lable = Text('Green',(None,color_pal[2]),(0.4,0.15),(0.1,0.1),False)
blue_team_lable = Text('Blue',(None,color_pal[2]),(0.6,0.15),(0.1,0.1),False)
yellow_team_lable = Text('Yellow',(None,color_pal[2]),(0.8,0.15),(0.1,0.1),False)

kills_lable = Text('Kills:',(None,color_pal[1]),(0,0.3),(0.2,0.1),False,0,True,('right','center'))

team_kills = []
for i in range(4):
    team_kills.append(Text('0',(None,color_pal[3]),(i*0.2+0.2,0.3),(0.1,0.1),False))

deaths_lable = Text('Deaths:',(None,color_pal[1]),(0,0.5),(0.2,0.1),False,0,True,('right','center'))

team_deaths = []
for i in range(4):
    team_deaths.append(Text('0',(None,color_pal[3]),(i*0.2+0.2,0.5),(0.1,0.1),False))


reset_stats_button = Button('Reset',(color_pal[1],color_pal[2]),(0.4,0.8),(0.2,0.1),reset_stats,'press',10)
    


back_button_stats = Button(
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

stats_menu = Menu(
    screen,
    Vector2(0, 0),
    Vector2(0, sh),
    sw,
    sh,
    color_pal[0],
    0,
    [red_team_lable,green_team_lable,blue_team_lable,yellow_team_lable,back_button_stats,kills_lable,deaths_lable,reset_stats_button]+team_kills+team_deaths
)


# Viva el fuctions, yay


def update_stats():
    for n,i in enumerate(team_kills):
        i.text = str(team_stats[n][0])
    for n,i in enumerate(team_deaths):
        i.text = str(team_stats[n][1])



def reset_players():
    global bullets, specials
    teams = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    bullets = []
    specials = []
    for n, i in enumerate(players):
        i: Player
        teams[team_to_num(i.team)][2] += 1
        i.reset()
        pos = Vector2()
        pos.from_polar((boundary_size - 100, 360 * n / len(players)))
        i.x = pos.x
        i.y = pos.y


def declare(txt):
    global declare_box_timer
    declare_box_timer = declare_box_length
    declare_box.text = txt
    delcare_menu.slide_progress = 0


def players_in_radius(pos, radius: float, not_included=0):
    in_radius = []
    for i in players:
        if not i.team == not_included:
            if math.dist([i.x, i.y], pos) < radius:
                in_radius.append(i)
    return in_radius


def closest_player(pos, not_included=0, is_max=False,is_rand=False,rand=0):
    distances = []
    for i in players:
        if i.team == not_included:
            distances.append(10000000)
        else:
            if is_rand:
                distances.append(math.dist([i.x, i.y], pos)+random()*rand)
            else:
                distances.append(math.dist([i.x, i.y], pos))
    if is_max:
        return players[distances.index(max(distances))]
    else:
        return players[distances.index(min(distances))]


def closest_bullet(pos, not_included=0, is_max=False,is_rand=False,rand=0):
    distances = []
    for i in bullets:
        i:Bullet
        if i.came_from.team == not_included:
            distances.append(10000000)
        else:
            if is_rand:
                distances.append(math.dist([i.x, i.y], pos)+random()*rand)
            else:
                distances.append(math.dist([i.x, i.y], pos))
    if is_max:
        return bullets[distances.index(max(distances))]
    else:
        return bullets[distances.index(min(distances))]


def fire_bullet(
    x: float,
    y: float,
    type: str,
    dir: float,
    spread: float,
    amount: int,
    player: object,
    add_vel: bool = True,
):
    global bullets
    for i in range(amount):
        bullets.append(
            Bullet(
                x, y, (dir) + ((i - (amount / 2) + 0.5) * spread), type, player, add_vel
            )
        )

        # Cool bullet stuff

        if type == rotator:
            bullets[-1].vel = Vector2(0, 0)


def draw_bullets():
    for i in bullets:
        i.draw()


def draw_grid():
    for i in range(math.ceil(sw / grid_spacing)):
        x = (grid_spacing - ((cam_x / zoom) % grid_spacing)) + (i * grid_spacing)
        pg.draw.line(screen, [i * 0.4 for i in backdrop], [x, 0], [x, sh], 5)
    for i in range(math.ceil(sw / grid_spacing)):
        y = ((cam_y / zoom) % grid_spacing) + (i * grid_spacing)
        pg.draw.line(screen, [i * 0.4 for i in backdrop], [0, y], [sw, y], 5)


def all_colors_of(surface: pg.Surface):
    """
    Gives a list of that surface in all the team colors
    """
    red_top = surface
    green_top = red_top.copy()
    blue_top = red_top.copy()
    yellow_top = red_top.copy()
    immune_top = red_top.copy()

    # Make the surfaces their color

    pixels_green = pg.PixelArray(green_top)
    pixels_blue = pg.PixelArray(blue_top)
    pixels_yellow = pg.PixelArray(yellow_top)
    pixels_immune = pg.PixelArray(immune_top)

    for x in range(green_top.get_width()):
        for y in range(green_top.get_height()):
            # Make green tank green
            rgb = green_top.unmap_rgb(pixels_green[x][y])
            color = pg.Color(*rgb)
            h, s, l, a = color.hsla
            color.hsla = (int(h) + green_team_hue) % 360, int(s), int(l), int(a)
            pixels_green[x][y] = color

            # Make blue tank blue
            rgb = blue_top.unmap_rgb(pixels_blue[x][y])
            color = pg.Color(*rgb)
            h, s, l, a = color.hsla
            color.hsla = (int(h) + blue_team_hue) % 360, int(s), int(l), int(a)
            pixels_blue[x][y] = color

            # Make yellow tank yellow
            rgb = yellow_top.unmap_rgb(pixels_yellow[x][y])
            color = pg.Color(*rgb)
            h, s, l, a = color.hsla
            color.hsla = (int(h) + yellow_team_hue) % 360, int(s), int(l), int(a)
            pixels_yellow[x][y] = color

            # Make immune tank gray
            rgb = immune_top.unmap_rgb(pixels_immune[x][y])
            color = pg.Color(*rgb)
            h, s, l, a = color.hsla
            color.hsla = int(h), 0, int(l), int(a)
            pixels_immune[x][y] = color

    del pixels_green
    del pixels_blue
    del pixels_yellow
    del pixels_immune

    return [red_top, green_top, blue_top, yellow_top, immune_top]


def collide_bullets():
    for b in bullets:
        for p in players:
            if not p.immunity > 0:
                if not b.came_from.team == p.team:
                    if math.dist([b.x, b.y], [p.x, p.y]) < (
                        p.type.size + b.bullet_type.size
                    ):
                        p.health -= b.bullet_type.damage

                        # Death message + death counter
                        if p.health <= 0 and not p.dead:
                            declare(f"{b.came_from.team} killed a {p.team}")
                            team_stats[team_to_num(b.came_from.team)][0] += 1
                            team_stats[team_to_num(p.team)][1] += 1
                            p.dead = True

                        if b in bullets:
                            del bullets[bullets.index(b)]
    for i in specials:
        if i.type.bullet_collide:
            for b in bullets:
                if not b.came_from.team == i.came_from.team:
                    if math.dist([b.x, b.y], [i.x, i.y]) < (
                        i.type.size + b.bullet_type.size
                    ):
                        i.collide_bullet(b)


def team_to_num(team):
    """
    Will give the number of a team given its name
    """
    if team == "red":
        return 0
    if team == "green":
        return 1
    if team == "blue":
        return 2
    if team == "yellow":
        return 3


def player_specials_update():
    for i in players:
        i.type.use_special(i)


def bullet_despawn():
    for i in bullets:
        if i.time_left <= 0:
            if i in bullets:
                # Stuff certain bullets do on despawn

                if i.bullet_type == shotgun_bomb:
                    fire_bullet(i.x, i.y, shrapnel, 0, 5, 72, i.came_from)

                del bullets[bullets.index(i)]


def player_respawn():
    for i in players:
        i.respawn()


def adjust_camera():
    global cam_x
    global cam_y
    global zoom
    x = []
    for i in players:
        x.append(i.x)
    cam_x += ((min(x) + max(x)) / 2 - cam_x) * cam_move_speed
    y = []
    for i in players:
        y.append(i.y)
    cam_y += ((min(y) + max(y)) / 2 - cam_y) * cam_move_speed
    farthest_player = closest_player((cam_x, cam_y), 0, True)
    most_dist = math.dist((farthest_player.x, farthest_player.y), (cam_x, cam_y))
    zoom += (
        (((math.ceil(most_dist / zoom_radius) * zoom_radius) / sh) * 2) - zoom
    ) * cam_zoom_speed


def move_bullets():
    for i in bullets:
        i.move()


def tick_specials():
    for i in specials:
        i.tick()


def draw_specials():
    for i in specials:
        i.draw()


def draw_players():
    for i in players:
        i.draw()


def move_players():
    for i in players:
        i.move()


def key_down(key: pg.key):
    return pg.key.get_pressed()[key]


def draw_circle(pos, size: float, color: str, outline=0):
    pg.draw.circle(
        screen,
        color,
        [(pos[0] - cam_x) / zoom + (sw / 2), sh - ((pos[1] - cam_y) / zoom + (sh / 2))],
        round(size / zoom),
        outline,
    )


def draw_line(pos1, pos2, size: float, color: str):
    pg.draw.line(
        screen,
        color,
        [
            (pos1[0] - cam_x) / zoom + (sw / 2),
            sh - ((pos1[1] - cam_y) / zoom + (sh / 2)),
        ],
        [
            (pos2[0] - cam_x) / zoom + (sw / 2),
            sh - ((pos2[1] - cam_y) / zoom + (sh / 2)),
        ],
        round(size / zoom),
    )


def draw_rect(pos1, size, color: str, corners: int):
    pg.draw.rect(
        screen,
        color,
        pg.Rect(
            (pos1[0] - cam_x) / zoom + (sw / 2),
            sh - ((pos1[1] - cam_y) / zoom + (sh / 2)),
            size[0] / zoom,
            size[1] / zoom,
        ),
        0,
        round(corners / zoom),
    )


def draw_tank_base(size, type, barrel: Vector2, team, x, y, scr=False):
    if scr:
        s_x = x
        s_y = y
        s_size = size
    else:
        s_x = (x - cam_x) / zoom + (sw / 2)
        s_y = sh - ((y - cam_y) / zoom + (sh / 2))
        s_size = round(size / zoom) * 2
    if team == "red":
        base = pg.transform.scale(red_tank_base, (floor(s_size), floor(s_size * 2)))
        index = 0
    elif team == "green":
        base = pg.transform.scale(green_tank_base, (floor(s_size), floor(s_size * 2)))
        index = 1
    elif team == "blue":
        base = pg.transform.scale(blue_tank_base, (floor(s_size), floor(s_size * 2)))
        index = 2
    elif team == "yellow":
        base = pg.transform.scale(yellow_tank_base, (floor(s_size), floor(s_size * 2)))
        index = 3
    elif team == "immune":
        base = pg.transform.scale(immune_tank_base, (floor(s_size), floor(s_size * 2)))
        index = 4

    base = pg.transform.rotate(base, (barrel.angle_to(Vector2(0, 0)) * -1) - 90)
    screen.blit(base, (s_x - (base.get_width() // 2), s_y - (base.get_height() // 2)))

    top = pg.transform.scale(type.tops[index], (floor(s_size), floor(s_size)))
    screen.blit(top, (s_x - (top.get_width() // 2), s_y - (top.get_height() // 2)))


def draw_sprite_team(x, y, dir, size, team, surfaces, rotate: bool = True):
    if team == "red":
        index = 0
    elif team == "green":
        index = 1
    elif team == "blue":
        index = 2
    elif team == "yellow":
        index = 3
    draw_sprite(x,y,dir,size,surfaces[index],rotate)
    


def draw_sprite(x, y, dir, size, surface, rotate: bool = True, alpha = 255, has_alpha = False):
    s_x = (x - cam_x) / zoom + (sw / 2)
    s_y = sh - ((y - cam_y) / zoom + (sh / 2))
    s_size = floor(round(size / zoom) * 2)


    if not (
        s_x - s_size > sw or s_x + s_size < 0 or s_y - s_size > sh or s_y + s_size < 0
    ):
        image = pg.transform.scale(surface,(floor(s_size),floor(s_size * (surface.get_height() / surface.get_width()))))
        

        if rotate:
            image = pg.transform.rotate(image, dir)
        if has_alpha:
            image.set_alpha(alpha)
        screen.blit(
            image, (s_x - (image.get_width() // 2), s_y - (image.get_height() // 2))
        )


def draw_background():
    global fan_rot, fan_speed
    fan_rot += fan_speed
    fan_rot %= 90
    draw_sprite(0,0,0,boundary_size,background)
    draw_sprite(0,0,fan_rot,boundary_size,fan,True,140,True)
    draw_sprite(0,0,0,boundary_size,fan_still,alpha=220,has_alpha=True)



"""
Stuff in the special class is stuff that does not really fit as a bullet or a player, it can be anything
from a turret to a sheild. If they collide with bullets or players, they need their own function to call
when that should happen. The 'tick' function for the specials will be called every frame.
"""


class SpecialGroup:
    def __init__(self, player_collide, bullet_collide, kind) -> None:
        self.bullet_collide = bullet_collide
        self.player_collide = player_collide

        if kind == "small_turret":
            self.size = 20
            self.fire_rate = 30
            self.life_time = 1000
            self.color = (50, 200, 200)
            self.max_health = 40
            self.fires = turret_bullet

        if kind == "damage_orb":
            self.speed = 8
            self.damage = 0.5
            self.life_time = 1000
            self.radius = 230
            self.size = 35
            self.color = (80, 10, 20)
            self.damage_color = (130, 20, 80)

        if kind == "large_sheild":
            self.lenth = 150
            self.life_time = 1000
            self.width = 10
            self.color = (80, 10, 20)
            self.size = 100

        if not kind == None:
            self.images = all_colors_of(
                pg.image.load("Projectiles/Specials/" + kind + ".png")
            )


class Special:
    def __init__(self, type: SpecialGroup, x, y, extra=None, extra2=None) -> None:
        self.x = x
        self.y = y
        self.type = type

        # Special inits

        if type == small_turret:
            self.health = type.max_health
            self.barrel = Vector2(0, self.type.size * 2)
            self.timer = type.fire_rate
            self.came_from = extra
            self.time_left = type.life_time
        if type == damage_orb:
            self.time_left = type.life_time
            self.came_from = extra
            new = Vector2(0, 0)
            new.from_polar((self.type.speed, extra2))
            self.vel = new

    def tick(self) -> None:
        # Runs once every frame
        global specials

        if self.type == small_turret:
            # Turret aiming
            toward = closest_player([self.x, self.y], self.came_from.team)
            toward_pos = (
                Vector2(toward.x, toward.y)
                + (toward.vel / self.type.fires.speed)
                * Vector2((toward.x - self.x), (toward.y - self.y)).length()
            )
            between = toward_pos - Vector2(self.x, self.y)
            between.scale_to_length(8)
            new = self.barrel + between
            new.scale_to_length(self.type.size * 2)
            self.barrel = new

            # Decreasing timers
            if self.timer > 0:
                self.timer -= 1

            if self.time_left > 0:
                self.time_left -= 1

            # Firing
            if self.timer <= 0:
                self.timer = self.type.fire_rate
                fire_bullet(
                    self.x + self.barrel.x,
                    self.y + self.barrel.y,
                    self.type.fires,
                    Vector2(0, 0).angle_to(self.barrel),
                    0,
                    1,
                    self.came_from,
                    False,
                )

            # Running out of time
            if self.time_left <= 0 or self.health <= 0:
                del specials[specials.index(self)]

        if self.type == damage_orb:
            # Move
            self.x += self.vel.x
            self.y += self.vel.y

            # Zapping!
            closest = players_in_radius(
                [self.x, self.y], self.type.radius, self.came_from.team
            )
            for i in closest:
                if not i.immunity > 0:
                    i.health -= self.type.damage
                    draw_line(
                        [i.x, i.y],
                        [self.x, self.y],
                        self.type.size // 3,
                        self.type.damage_color,
                    )

            # Decreasing timers
            if self.time_left > 0:
                self.time_left -= 1

            # Running out of time
            if self.time_left <= 0:
                del specials[specials.index(self)]

    def draw(self) -> None:
        # Runs every frame, but only the way that specials are drawn should go here, all the rest goes in 'tick'

        if developer_art:
            if self.type == small_turret:
                draw_circle(
                    [self.x, self.y],
                    self.type.size,
                    [i * (self.health / self.type.max_health) for i in self.type.color],
                )
                draw_line(
                    [self.x, self.y],
                    [self.x + self.barrel.x, self.y + self.barrel.y],
                    self.type.size // 3,
                    [i * (self.health / self.type.max_health) for i in self.type.color],
                )
                draw_circle(
                    [self.x + self.barrel.x, self.y + self.barrel.y],
                    self.type.size // 6,
                    [i * (self.health / self.type.max_health) for i in self.type.color],
                )

            if self.type == damage_orb:
                draw_circle([self.x, self.y], self.type.size, self.type.color)
                # draw_circle([self.x,self.y],self.type.radius,self.type.damage_color,self.type.size//2)
        else:
            if self.type == small_turret:
                draw_sprite_team(
                    self.x,
                    self.y,
                    (self.barrel.angle_to(Vector2(0, 0)) * -1) - 90,
                    self.type.size,
                    self.came_from.team,
                    self.type.images,
                )

            if self.type == damage_orb:
                draw_sprite_team(
                    self.x,
                    self.y,
                    (self.vel.angle_to(Vector2(0, 0)) * -1) - 90,
                    self.type.size,
                    self.came_from.team,
                    self.type.images,
                )
                # draw_circle([self.x,self.y],self.type.radius,self.type.damage_color,self.type.size//2)

    def collide_bullet(self, bullet) -> None:
        # Runs when a bullet collide with the special ( they will only collide if that special type says so)

        if self.type == small_turret:
            self.health -= bullet.bullet_type.damage
            del bullets[bullets.index(bullet)]


class BulletGroup:
    def __init__(self, image, damage, speed, size, color, homing, life_span) -> None:
        self.damage = damage
        self.speed = speed
        self.size = size
        self.color = color
        self.homing = homing
        self.life_span = life_span
        self.images = []
        if not image == None:
            self.images = all_colors_of(
                pg.image.load("Projectiles/Bullets/" + image + ".png")
            )


class Bullet:
    def __init__(self, x, y, dir, bullet_type, came_from, add_vel=True) -> None:
        self.x = x
        self.y = y
        self.vel = Vector2()
        self.vel.from_polar((bullet_type.speed, dir))
        self.bullet_type = bullet_type
        if not self.bullet_type.speed == 0:
            if add_vel:
                self.vel += came_from.vel * 0.5
        self.came_from = came_from
        self.time_left = bullet_type.life_span
        if bullet_type == mini_mine:
            self.vel.scale_to_length((1 - (random() ** 2)) * 40)

    def move(self) -> None:
        if self.bullet_type == mini_mine:
            self.x += round(self.vel.x)
            self.y += round(self.vel.y)
        else:
            self.x += self.vel.x
            self.y += self.vel.y
        self.time_left -= 1
        if not self.bullet_type.homing == 0:
            if not len(players) == 1:
                toward = closest_player([self.x, self.y], self.came_from.team)
                between = Vector2((toward.x - self.x), (toward.y - self.y))
                between.scale_to_length(self.bullet_type.homing)
                new = self.vel + between
                new.scale_to_length(self.vel.length())
                self.vel = new
        if not self.bullet_type == rotator:
            if (
                math.dist((0, 0), (self.x, self.y))
                > boundary_size - self.bullet_type.size
            ):
                self.vel *= -1
                new = Vector2(self.x, self.y)
                new.scale_to_length(boundary_size - self.bullet_type.size)
                self.x = new.x
                self.y = new.y

        # Special Bullets Cool Stuff

        if self.bullet_type == mini_mine or self.bullet_type == mine:
            self.vel *= 0.9

        if self.bullet_type == rotator:
            self.vel.x = (self.vel.x + 5) % 360
            old = Vector2()
            old.from_polar((rotator.speed, self.vel.x))
            self.x = self.came_from.x + old.x
            self.y = self.came_from.y + old.y

    def draw(self) -> None:
        if developer_art:
            if self.bullet_type == mine:
                if self.time_left > 600:
                    draw_circle(
                        [self.x, self.y], self.bullet_type.size, self.bullet_type.color
                    )
                else:
                    draw_circle(
                        [self.x, self.y],
                        self.bullet_type.size // 4,
                        self.bullet_type.color,
                    )
            else:
                draw_circle(
                    [self.x, self.y], self.bullet_type.size, self.bullet_type.color
                )
        else:
            if self.bullet_type == mine:
                if self.time_left > 600:
                    draw_sprite_team(
                        self.x,
                        self.y,
                        (self.vel.angle_to(Vector2(0, 0)) * -1) - 90,
                        self.bullet_type.size,
                        self.came_from.team,
                        self.bullet_type.images,
                        not (self.bullet_type == mine or self.bullet_type == mini_mine),
                    )
                else:
                    draw_sprite_team(
                        self.x,
                        self.y,
                        (self.vel.angle_to(Vector2(0, 0)) * -1) - 90,
                        self.bullet_type.size // 4,
                        self.came_from.team,
                        self.bullet_type.images,
                        not (self.bullet_type == mine or self.bullet_type == mini_mine),
                    )
            else:
                draw_sprite_team(
                    self.x,
                    self.y,
                    (self.vel.angle_to(Vector2(0, 0)) * -1) - 90,
                    self.bullet_type.size,
                    self.came_from.team,
                    self.bullet_type.images,
                    not (self.bullet_type == mine or self.bullet_type == mini_mine),
                )


class PlayerCharacter:
    def __init__(
        self,
        top_image: str,
        size: int,
        max_health: int,
        move_speed: float,
        drift: float,
        reload_time: int,
        color: tuple,
        bullet_type: BulletGroup,
        special_cooldown: int,
        amount: int,
        spread: int,
        name: str,
    ) -> None:
        """
        Top image is the file name of the image that its top is
        """
        self.size = size
        self.name = name
        self.max_health = max_health
        self.move_speed = move_speed
        self.drift = drift
        self.reload_time = reload_time
        self.color = color
        self.fires = bullet_type
        self.special_cooldown = special_cooldown
        self.amount = amount
        self.spread = spread
        self.tops = []
        all_chars.append(self)
        if not top_image == None:
            self.tops = all_colors_of(pg.image.load("Tanks/Tops/" + top_image + ".png"))

    def init_special_use(self, player) -> None:
        player: Player
        if self == shotgun_char:
            fire_bullet(
                player.x + player.barrel.x,
                player.y + player.barrel.y,
                shotgun_bomb,
                Vector2(0, 0).angle_to(player.barrel),
                0,
                1,
                player,
            )
        if self == mine_layer:
            player.left = 18
        if self == cloner_char:
            for i, n in enumerate(players):
                n: Player
                if n.team == player.team:
                    players[i].immunity = 130
                    if not n == player:
                        players[i].cool_down = 0

        if self == speed_char:
            player.left = 12
        if self == tank_char:
            player.left = 300
        if self == spin_char:
            player.left = 12
        if self == blaster_char:
            player.left = 3
        if self == turret_layer:
            specials.append(Special(small_turret, player.x, player.y, player))
        if self == orb_char:
            specials.append(
                Special(
                    damage_orb,
                    player.x + player.barrel.x,
                    player.y + player.barrel.y,
                    player,
                    Vector2(0, 0).angle_to(player.barrel),
                )
            )

    def use_special(self, player) -> None:
        if self == mine_layer:
            if player.left > 0:
                player.left -= 1
                fire_bullet(
                    player.x,
                    player.y,
                    mini_mine,
                    player.left * 20 + (random() * 20),
                    0,
                    4,
                    player,
                )
        if self == speed_char:
            if player.left > 0:
                player.left -= 1
                if player.movement[0] == "controller":
                    player.vel.x += 4 * controller_input[player.movement[1]][15][0]
                    player.vel.y -= 4 * controller_input[player.movement[1]][15][1]
                elif player.movement[0] == "keyboard":
                    if key_down(keyboard_controls[player.movement[1]][0]):
                        player.vel.y += 4
                    if key_down(keyboard_controls[player.movement[1]][1]):
                        player.vel.x += 4
                    if key_down(keyboard_controls[player.movement[1]][2]):
                        player.vel.y -= 4
                    if key_down(keyboard_controls[player.movement[1]][3]):
                        player.vel.y -= 4
                fire_bullet(
                    player.x,
                    player.y,
                    speed_big_pellet,
                    Vector2(0, 0).angle_to(player.vel),
                    180,
                    2,
                    player,
                )
        if self == tank_char:
            if player.left > 0:
                player.left -= 1
                player.vel = Vector2(0, 0)
                player.timer -= 4
        if self == spin_char:
            if player.left > 0:
                if player.wait <= 0:
                    player.left -= 1
                    player.wait = 6
                    fire_bullet(
                        player.x + rotator.speed, player.y, rotator, 0, 0, 1, player
                    )
        if self == blaster_char:
            if player.left > 0:
                if player.wait <= 0:
                    player.left -= 1
                    player.wait = 10
                    fire_bullet(player.x, player.y, blaster_bolt, 0, 36, 10, player)


class Player:
    def __str__(self) -> str:
        return f"{self.x,self.y} pos, {self.vel} vel, {players.index(self)+1} number"

    def __init__(self, group: PlayerCharacter, team, x, y, control_scheme) -> None:
        self.team = team
        self.type = group
        self.x = x
        self.y = y
        self.health = group.max_health
        self.movement = control_scheme
        self.vel = Vector2(0, 0)
        self.barrel = Vector2(0, self.type.size * 2)
        self.timer = 0
        self.left = 0
        self.wait = 0
        self.cool_down = self.type.special_cooldown
        self.immunity = respawn_immunity // 3
        self.dead = False
        team_stats[team_to_num(team)][2] += 1

    def move(self) -> None:
        self.x += self.vel.x
        self.y += self.vel.y
        self.vel.x *= self.type.drift
        self.vel.y *= self.type.drift
        if self.movement[0] == "keyboard":
            self.control_keyboard()
        elif self.movement[0] == "controller":
            self.control_controller()
        elif self.movement[0] == "bot":
            if smart_bots:
                self.control_mid()
            else:
                self.control_dumb()

        if math.dist((0, 0), (self.x, self.y)) > boundary_size - self.type.size:
            new = Vector2(self.x, self.y)
            new.scale_to_length(boundary_size - self.type.size)
            self.x = new.x
            self.y = new.y
        if self.timer > 0:
            self.timer -= 1
        if self.cool_down > 0:
            self.cool_down -= 1
        if self.immunity > 0:
            self.immunity -= 1
        if self.wait > 0:
            self.wait -= 1
    

    def control_keyboard(self):
        if key_down(keyboard_controls[self.movement[1]][0]):
            self.vel.y += self.type.move_speed
        if key_down(keyboard_controls[self.movement[1]][1]):
            self.vel.x += self.type.move_speed
        if key_down(keyboard_controls[self.movement[1]][2]):
            self.vel.y -= self.type.move_speed
        if key_down(keyboard_controls[self.movement[1]][3]):
            self.vel.x -= self.type.move_speed
        if key_down(keyboard_controls[self.movement[1]][5]):
            self.barrel.rotate_ip(keyboard_barrel_rot_speed)
        if key_down(keyboard_controls[self.movement[1]][6]):
            self.barrel.rotate_ip(-keyboard_barrel_rot_speed)
        if self.immunity <= 0:
            if key_down(keyboard_controls[self.movement[1]][4]):
                if self.timer <= 0:
                    self.timer = self.type.reload_time
                    fire_bullet(
                        self.x + self.barrel.x,
                        self.y + self.barrel.y,
                        self.type.fires,
                        Vector2(0, 0).angle_to(self.barrel),
                        self.type.spread,
                        self.type.amount,
                        self,
                    )
            if key_down(keyboard_controls[self.movement[1]][7]):
                if self.cool_down <= 0:
                    self.cool_down = self.type.special_cooldown
                    self.type.init_special_use(self)
    

    def control_controller(self):
        if self.immunity <= 0:
            if controller_input[self.movement[1]][17][1]:
                if self.timer <= 0:
                    self.timer = self.type.reload_time
                    fire_bullet(
                        self.x + self.barrel.x,
                        self.y + self.barrel.y,
                        self.type.fires,
                        Vector2(0, 0).angle_to(self.barrel),
                        self.type.spread,
                        self.type.amount,
                        self,
                    )
            if controller_input[self.movement[1]][17][0]:
                if self.cool_down <= 0:
                    self.cool_down = self.type.special_cooldown
                    self.type.init_special_use(self)
        if aim_type == 1:
            if (
                controller_input[self.movement[1]][16][0] == 0
                and controller_input[self.movement[1]][16][1] == 0
            ):
                self.barrel = Vector2(0, self.type.size * 2)
            else:
                new = Vector2(
                    controller_input[self.movement[1]][16][0],
                    -controller_input[self.movement[1]][16][1],
                )
                new.scale_to_length(self.type.size * 2)
                self.barrel = new
        else:
            self.barrel.rotate_ip(
                controller_input[self.movement[1]][16][0]
                * -controller_barrel_rot_speed
            )
        self.vel.x += (
            self.type.move_speed * controller_input[self.movement[1]][15][0]
        )
        self.vel.y -= (
            self.type.move_speed * controller_input[self.movement[1]][15][1]
        )


    def control_dumb(self):
        target = closest_player(Vector2(self.x, self.y), self.team,is_rand=True,rand=bot_rand)
        dist = Vector2(self.x, self.y).distance_to(Vector2(target.x, target.y))
        dir = Vector2(target.x, target.y) - Vector2(self.x, self.y)
        self.bot_move(dist,target)
        if dir.length() < 1:
            dir = Vector2(1,0)
        dir.normalize_ip()
        dot = self.barrel.x*(dir.y)+self.barrel.y*(-dir.x)
        if abs(dot) > self.type.size * 0.2:
            if dot > 0:
                self.barrel.rotate_ip(keyboard_barrel_rot_speed)
            else:
                self.barrel.rotate_ip(-keyboard_barrel_rot_speed)

        
        if self.immunity <= 0:
            if self.timer <= 0:
                self.timer = self.type.reload_time
                fire_bullet(
                    self.x + self.barrel.x,
                    self.y + self.barrel.y,
                    self.type.fires,
                    Vector2(0, 0).angle_to(self.barrel),
                    self.type.spread,
                    self.type.amount,
                    self,
                )
            if self.cool_down <= 0:
                self.cool_down = self.type.special_cooldown
                self.type.init_special_use(self)
    

    def control_mid(self):
        target:Player = closest_player(Vector2(self.x, self.y), self.team,is_rand=True,rand=bot_rand)
        dist = Vector2(self.x, self.y).distance_to(Vector2(target.x, target.y))
        if len(bullets) > 0:
            near:Bullet = closest_bullet(Vector2(self.x, self.y), self.team,is_rand=True,rand=bot_rand)
            dist_bul = Vector2(self.x, self.y).distance_to(Vector2(near.x, near.y))
            if dist_bul < (near.bullet_type.size+near.bullet_type.speed) * smart_bot_avoidance and near.came_from.team != self.team:
                if near.y < self.y:
                    self.vel.y += self.type.move_speed
                if near.x < self.x:
                    self.vel.x += self.type.move_speed
                if near.y > self.y:
                    self.vel.y -= self.type.move_speed
                if near.x > self.x:
                    self.vel.x -= self.type.move_speed
            else:
                self.bot_move(dist,target)
        else:
            self.bot_move(dist,target)
        toward_pos = (
            Vector2(target.x, target.y)
            + (target.vel / (self.type.fires.speed**1.5))
            * Vector2((target.x - self.x), (target.y - self.y)).length()
        )
        dir = toward_pos - Vector2(self.x, self.y)
        if dir.length() < 1:
            dir = Vector2(1,0)
        dir.normalize_ip()
        dot = self.barrel.x*(dir.y)+self.barrel.y*(-dir.x)
        if abs(dot) > self.type.size * 0.2:
            if dot > 0:
                self.barrel.rotate_ip(keyboard_barrel_rot_speed)
            else:
                self.barrel.rotate_ip(-keyboard_barrel_rot_speed)
        if self.immunity <= 0:
            if self.timer <= 0:
                self.timer = self.type.reload_time
                fire_bullet(
                    self.x + self.barrel.x,
                    self.y + self.barrel.y,
                    self.type.fires,
                    Vector2(0, 0).angle_to(self.barrel),
                    self.type.spread,
                    self.type.amount,
                    self,
                )
            if self.cool_down <= 0:
                self.cool_down = self.type.special_cooldown
                self.type.init_special_use(self)
    

    def bot_move(self,dist,target):
        if abs(dist - bot_target_dist) > bot_happy_dist:
            if dist > bot_target_dist:
                if target.y > self.y:
                    self.vel.y += self.type.move_speed
                if target.x > self.x:
                    self.vel.x += self.type.move_speed
                if target.y < self.y:
                    self.vel.y -= self.type.move_speed
                if target.x < self.x:
                    self.vel.x -= self.type.move_speed
            else:
                if target.y < self.y:
                    self.vel.y += self.type.move_speed
                if target.x < self.x:
                    self.vel.x += self.type.move_speed
                if target.y > self.y:
                    self.vel.y -= self.type.move_speed
                if target.x > self.x:
                    self.vel.x -= self.type.move_speed
    

    def draw(self) -> None:
        if self.health > 0:
            if self.immunity <= 0:
                if developer_art:
                    draw_circle(
                        [self.x, self.y],
                        self.type.size,
                        [
                            i * (self.health / self.type.max_health)
                            for i in self.type.color
                        ],
                    )
                    draw_line(
                        [self.x, self.y],
                        [self.x + self.barrel.x, self.y + self.barrel.y],
                        self.type.size // 3,
                        [
                            i * (self.health / self.type.max_health)
                            for i in self.type.color
                        ],
                    )
                    draw_circle(
                        [self.x + self.barrel.x, self.y + self.barrel.y],
                        self.type.size // 6,
                        [
                            i * (self.health / self.type.max_health)
                            for i in self.type.color
                        ],
                    )
                else:
                    draw_tank_base(
                        self.type.size,
                        self.type,
                        self.barrel,
                        self.team,
                        self.x,
                        self.y,
                    )
                draw_rect(
                    (self.x - self.type.size, self.y + self.type.size * 1.5),
                    (
                        self.type.size * 2 * (self.health / self.type.max_health),
                        self.type.size * 0.2,
                    ),
                    healthbar_color,
                    self.type.size * 0.05,
                )
            else:
                if developer_art:
                    draw_circle([self.x, self.y], self.type.size, tuple([128] * 3))
                    draw_line(
                        [self.x, self.y],
                        [self.x + self.barrel.x, self.y + self.barrel.y],
                        self.type.size // 3,
                        tuple([128] * 3),
                    )
                    draw_circle(
                        [self.x + self.barrel.x, self.y + self.barrel.y],
                        self.type.size // 6,
                        tuple([128] * 3),
                    )
                else:
                    draw_tank_base(
                        self.type.size, self.type, self.barrel, "immune", self.x, self.y
                    )

            if self.cool_down <= 0:
                if developer_art:
                    draw_circle(
                        [self.x, self.y],
                        self.type.size / 2,
                        [
                            i * ((self.health / self.type.max_health) * 0.5)
                            for i in self.type.color
                        ],
                    )
                else:
                    draw_circle(
                        (self.x - self.type.size * 1.4, self.y + self.type.size * 1.4),
                        self.type.size * 0.3,
                        special_ready_color,
                    )

    def respawn(self) -> None:
        if self.immunity <= 0:
            if self.health <= 0:
                self.dead = False
                self.x = cam_x
                self.y = cam_y
                self.health = self.type.max_health
                self.immunity = respawn_immunity

    def reset(self):
        self.health = self.type.max_health
        self.vel = Vector2(0, 0)
        self.barrel = Vector2()
        self.barrel.from_polar((self.type.size * 2, 0))
        self.timer = 0
        self.left = 0
        self.wait = 0
        self.cool_down = self.type.special_cooldown
        self.immunity = respawn_immunity // 3
        self.dead = False


# Bullet Types
blaster_bolt = BulletGroup("blaster_bolt", 8, 13, 12, (40, 200, 40), 0.4, 240)
tank_shell = BulletGroup("tank_shell", 18, 12, 15, (40, 60, 100), 0.1, 300)
spin_char_bullet = BulletGroup("spin_char_bullet", 6, 15, 20, (50, 200, 50), 1.4, 100)
shotgun_pellet = BulletGroup("shotgun_pellet", 4, 16, 8, (150, 150, 150), 0, 40)
mine = BulletGroup("mine", 100, 10, 35, (240, 50, 50), 0, 800)
mini_mine = BulletGroup("mini_mine", 20, 30, 25, (230, 150, 150), 0, 500)
shotgun_bomb = BulletGroup("shotgun_bomb", 75, 12, 50, (210, 240, 100), 0, 60)
shrapnel = BulletGroup("shrapnel", 30, 20, 15, (105, 120, 50), 0, 40)
speed_pellet = BulletGroup("speed_pellet", 4, 12, 6, (200, 40, 200), 0, 120)
speed_big_pellet = BulletGroup("speed_big_pellet", 10, 15, 10, (100, 20, 100), 1, 25)
rotator = BulletGroup("rotator", 35, 100, 20, (120, 200, 255), 0, 350)
cloner_bullet = BulletGroup("cloner_bullet", 3, 12, 6, (20, 20, 20), 0.2, 200)
turret_bullet = BulletGroup("turret_bullet", 4, 18, 10, (20, 128, 128), 0, 100)
small_orb = BulletGroup("small_orb", 12, 13, 20, (80, 0, 200), 0.75, 130)


# Player Characters
all_chars = []
shotgun_char = PlayerCharacter(
    "shotgun_char",
    30,
    60,
    5,
    0.4,
    50,
    (240, 240, 40),
    shotgun_pellet,
    1200,
    10,
    4,
    "Shotgun",
)
blaster_char = PlayerCharacter(
    "blaster_char",
    25,
    40,
    3,
    0.7,
    30,
    (200, 30, 30),
    blaster_bolt,
    1200,
    1,
    0,
    "Blaster",
)
tank_char = PlayerCharacter(
    "tank_char", 40, 120, 3, 0.65, 80, (60, 20, 200), tank_shell, 1100, 1, 0, "Tank"
)
cloner_char = PlayerCharacter(
    "cloner_char",
    20,
    25,
    2,
    0.8,
    9,
    (60, 255, 30),
    cloner_bullet,
    1300,
    1,
    0,
    "Support"
)
mine_layer = PlayerCharacter(
    "mine_layer", 40, 100, 2, 0.6, 60, (255, 128, 20), mine, 600, 1, 0, "Mines"
)
speed_char = PlayerCharacter(
    "speed_char", 20, 35, 3, 0.8, 10, (255, 100, 255), speed_pellet, 600, 2, 20, "Speed"
)
spin_char = PlayerCharacter(
    "spin_char",
    40,
    60,
    1,
    0.95,
    35,
    (230, 255, 50),
    spin_char_bullet,
    1200,
    1,
    0,
    "Spinner",
)
turret_layer = PlayerCharacter(
    "turret_layer",
    25,
    75,
    2,
    0.8,
    50,
    (100, 255, 255),
    turret_bullet,
    600,
    3,
    5,
    "Turrets",
)
orb_char = PlayerCharacter(
    "orb_char", 40, 50, 3, 0.8, 70, (100, 10, 140), small_orb, 150, 1, 0, "Orbulator"
)





# Special types
small_turret = SpecialGroup(False, True, "small_turret")
damage_orb = SpecialGroup(False, False, "damage_orb")


def game_tick(events):
    screen.fill(outside_color)
    if developer_art or (not has_background):
        draw_circle((0, 0), boundary_size, backdrop)
    else:
        draw_background()
    # draw_grid()
    adjust_camera()
    move_players()
    move_bullets()
    bullet_despawn()
    collide_bullets()
    tick_specials()
    player_specials_update()
    draw_bullets()
    player_respawn()
    draw_players()
    draw_specials()
    fps_counter.text = str(int(fps_clock.get_fps())) + " FPS"
    things_counter.text = str(len(players) + len(bullets) + len(specials)) + " EN"
    game_menu.full_update(events)


fps = 60
fps_clock = pg.time.Clock()

if __name__ == "__main__":
    running = True
    current_page = "start"

    while running:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False

            # Controller stuff
            if event.type == pg.JOYBUTTONUP:
                controller_input[event.joy][event.button] = False
            if event.type == pg.JOYBUTTONDOWN:
                controller_input[event.joy][event.button] = True
            if event.type == pg.JOYAXISMOTION:
                if event.axis > 3:
                    if event.value < 0:
                        controller_input[event.joy][17][event.axis - 4] = False
                    else:
                        controller_input[event.joy][17][event.axis - 4] = True
                elif event.axis > 1:
                    if aim_type == 1:
                        if not abs(event.value) < 0.4:
                            controller_input[event.joy][16][event.axis - 2] = (
                                round(event.value * 20) / 20
                            )
                    elif aim_type == 2:
                        controller_input[event.joy][16][event.axis - 2] = (
                            round(event.value * 20) / 20
                        )
                        if abs(event.value) < 0.4:
                            controller_input[event.joy][16][event.axis - 2] = 0
                else:
                    controller_input[event.joy][15][event.axis] = (
                        round(event.value * 20) / 20
                    )
                    if abs(event.value) < 0.4:
                        controller_input[event.joy][15][event.axis] = 0

        screen.fill((0, 0, 0))
        if current_page == "start":
            start_menu.full_update(events)
        elif current_page == "char_select":
            update_player_menus()
            char_select.full_update(events)
            draw_player_menus()
        elif current_page == "game":
            game_tick(events)
        elif current_page == "pause":
            pause_menu.full_update(events)
        elif current_page == "settings":
            settings_menu.full_update(events)
        elif current_page == 'stats':
            update_stats()
            stats_menu.full_update(events)

        declare_box_timer = max(declare_box_timer - 1, 0)
        if not declare_box_timer == 0:
            if declare_box_timer < declare_box_fade:
                delcare_menu.direct = -1
            elif declare_box_timer > declare_box_length - declare_box_fade:
                delcare_menu.direct = 1
            else:
                delcare_menu.direct = 0
            delcare_menu.full_update(events)

        pg.display.update()
        fps_clock.tick(fps)
        if key_down(pg.K_BACKSPACE):
            running = False
    pg.quit()
