import math
from math import floor
import pygame as pg
from battle_new import closest_player, players, screen
from menus import boundary_size
from graphics_settings import sw, sh
from pygame import Vector2
from graphics_settings import green_team_hue, blue_team_hue, yellow_team_hue


# Camera
cam_x = 0
cam_y = 0
zoom = 2
zoom_radius = 500
cam_move_speed = 0.15
cam_zoom_speed = 0.1


#Creating background sprites
has_background = False
background = pg.image.load("Background/background.png")
fan = pg.image.load("Background/fan.png")
fan_still = pg.image.load("Background/fan_still.png")
fan_speed = 6
fan_rot = 0





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
