"""
Best Editor For Soft Body Simulations Omega Extreme
"""


"""
How to use this amazing tool:

 - The first thing to know is how to add a circle, simple just left click
 - If 'b' is held when adding a point, the point will be very heavy and big
 - If you hold shift while pressing left click, you will create a circle everyframe where adding one wouldn't make it intersect with others
 - If you hold ctrl while shifting, it will auto connect the points with a solid line

 
 - You can add a connection between points by just righting clicking and holding on a point, and dragging the cursor to the point you want to connect to
 - If you hold shift while doing this, the connection will be a spring

 - When adding circles or connections, they will be fixed if you hold 'f' whild adding them, and they will not collide if you hold 'g'
 - When adding a connection, it will be a moveable solid line if 'r' is held

 - Middle click to drag points

 - WASD to move the camera
 - 'n' to zoom in, 'm' to zoom out

 - 'p' to pause and unpause the simulation

 -'k' to save the current scene
 -'l' to laod the last saved scene

 -'v' to update line line lengths
"""


import pygame as pg
import soft_body as sb
from math import floor
from pygame import Vector2
from menu_engine import Menu, Text, Toggle
from copy import deepcopy, copy


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


# Draw a circle a point in space
def draw_circle(pos, size: float, color: str, outline=0):
    pg.draw.circle(
        screen,
        color,
        [
            (pos[0] - cam_pos.x) / zoom + (sw / 2),
            sh - ((pos[1] - cam_pos.y) / zoom + (sh / 2)),
        ],
        floor(size / zoom),
        outline,
    )


# Draw a line at point in space
def draw_line(pos1, pos2, width: float, color: str):
    pg.draw.circle(
        screen,
        color,
        [
            (pos1[0] - cam_pos.x) / zoom + (sw / 2),
            sh - ((pos1[1] - cam_pos.y) / zoom + (sh / 2)),
        ],
        floor(width / zoom),
    )
    pg.draw.circle(
        screen,
        color,
        [
            (pos2[0] - cam_pos.x) / zoom + (sw / 2),
            sh - ((pos2[1] - cam_pos.y) / zoom + (sh / 2)),
        ],
        floor(width / zoom),
    )
    pg.draw.line(
        screen,
        color,
        [
            (pos1[0] - cam_pos.x) / zoom + (sw / 2),
            sh - ((pos1[1] - cam_pos.y) / zoom + (sh / 2)),
        ],
        [
            (pos2[0] - cam_pos.x) / zoom + (sw / 2),
            sh - ((pos2[1] - cam_pos.y) / zoom + (sh / 2)),
        ],
        floor(width / zoom) * 2,
    )


def get_m_pos():
    return Vector2(
        [
            ((pg.mouse.get_pos()[0] - (sw / 2)) * zoom) + cam_pos.x,
            ((sh - (pg.mouse.get_pos()[1] + (sh / 2))) * zoom) + cam_pos.y,
        ]
    )


def add_point(pos):
    """
    The function thats called to add a point into the simulation
    """
    sim.points.append(sb.Point(pos, Vector2(0, 0), solid_line_width, point_color, sim))
    if point_fixed:
        sim.points[-1].move = False
    if point_ghost:
        sim.points[-1].solid = False
        sim.points[-1].color = ghost_color
    if big_point:
        sim.points[-1].size = default_point_size
    if heavy_point:
        sim.points[-1].size *= 2
        sim.points[-1].weight *= 5
        sim.points[-1].color = car_color


def add_line(p1, p2, length, form="rigid"):
    if key_down(pg.K_f):
        sim.lines.append(
            sb.Line(
                length,
                p1,
                p2,
                solid_color,
                solid_line_width,
                sim,
                "fsolid",
                default_rigid_strength,
            )
        )
    elif key_down(pg.K_r):
        sim.lines.append(
            sb.Line(
                length,
                p1,
                p2,
                road_color,
                solid_line_width,
                sim,
                "msolid",
                default_rigid_strength,
            )
        )
    else:
        sim.lines.append(
            sb.Line(
                length,
                p1,
                p2,
                line_color,
                line_width,
                sim,
                form,
                default_rigid_strength,
            )
        )


def set_point_type(set):
    global placing_points
    placing_points = set


def set_line_type(set):
    global placing_lines
    placing_lines = set


pg.init()

# Screen
sw = 1920
sh = 1080
screen = pg.display.set_mode((sw, sh), pg.FULLSCREEN)
###

# Camera
cam_pos = Vector2(0, 0)
zoom = 1
line_color = (100, 220, 50)
point_color = (100, 150, 75)
road_color = (120, 190, 80)
solid_color = (200, 130, 20)
ghost_color = (110, 110, 100)
car_color = (120, 140, 220)
spring_color = (240, 210, 30)
line_width = 5
solid_line_width = 15
backdrop = (5, 6, 11)
outside_color = (200, 230, 140)

cam_move_speed = 5
###


# Simulation
sim_speed = 13
start_time = 20

sim = sb.Sim(
    draw_line, draw_circle, get_m_pos, (sw, sh), 1, -2, 1, breaking=False, max_stress=5
)


# Menu stuff
fps_counter = Text(
    "NaN",
    (backdrop, outside_color),
    Vector2(0.1, 0.1),
    Vector2(0.8, 0.4),
    editable=False,
)
things_counter = Text(
    "NaN",
    (backdrop, outside_color),
    Vector2(0.1, 0.6),
    Vector2(0.8, 0.4),
    editable=False,
)

counter_menu = Menu(
    screen,
    Vector2(sw * 0.95, 0),
    Vector2(sw * 0.95, 0),
    80,
    55,
    backdrop,
    0,
    [fps_counter, things_counter],
)


side_bar_size = 250
side_bar_colors = ((140, 50, 20), (120, 200, 120), (220, 220, 80))


fixed_text = Text("Fixed", (None, side_bar_colors[1]), (0.2, 0.02), (0.6, 0.05))
fixed_toggle = Toggle(
    (side_bar_colors[2], side_bar_colors[1], side_bar_colors[0]),
    (0.2, 0.08),
    (0.6, 0.05),
)

ghost_text = Text("Ghost", (None, side_bar_colors[1]), (0.2, 0.16), (0.6, 0.05))
ghost_toggle = Toggle(
    (side_bar_colors[2], side_bar_colors[1], side_bar_colors[0]),
    (0.2, 0.22),
    (0.6, 0.05),
)

size_text = Text("Size", (None, side_bar_colors[1]), (0.2, 0.3), (0.6, 0.05))
size_toggle = Toggle(
    (side_bar_colors[2], side_bar_colors[1], side_bar_colors[0]),
    (0.2, 0.36),
    (0.6, 0.05),
)

big_text = Text("Heavy", (None, side_bar_colors[1]), (0.2, 0.44), (0.6, 0.05))
big_toggle = Toggle(
    (side_bar_colors[2], side_bar_colors[1], side_bar_colors[0]),
    (0.2, 0.5),
    (0.6, 0.05),
)


side_bar = Menu(
    screen,
    (0, 0),
    (-side_bar_size, 0),
    side_bar_size,
    sh,
    side_bar_colors[0],
    20,
    [
        fixed_toggle,
        fixed_text,
        ghost_toggle,
        ghost_text,
        size_toggle,
        size_text,
        big_toggle,
        big_text,
    ],
    0.12,
    (False, True, False, True),
)


# Controls

pre_focus_move = None
pre_focus_pos = Vector2(0, 0)

focus = -1

default_point_size = 30
default_spring_strength = 15
default_rigid_strength = 1


pre_added = None
focus_offset = Vector2(0, 0)

point_fixed = False
point_ghost = False
big_point = False
heavy_point = False


save_sim = None


was_l = False
was_r = False
l_add = 0
fps = 60
dt = (1 / fps) * sim_speed
fps_clock = pg.time.Clock()
running = True
while running:
    # if len(sim.points) > 0:
    #     print((sim.points[0].pos - sim.points[0].pre_pos).length())
    start_time = max(start_time - 1, 0)

    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    if key_down(pg.K_w):
        cam_pos.y += cam_move_speed * zoom

    if key_down(pg.K_s):
        cam_pos.y -= cam_move_speed * zoom

    if key_down(pg.K_d):
        cam_pos.x += cam_move_speed * zoom

    if key_down(pg.K_a):
        cam_pos.x -= cam_move_speed * zoom

    if key_down(pg.K_n):
        zoom *= 1.04

    if key_down(pg.K_m):
        zoom /= 1.04

    if key_press("p"):
        sim.paused = not sim.paused

    if key_press("k"):
        save_sim = deepcopy(sim)

    if key_press("l"):
        if not save_sim == None:
            sim = deepcopy(save_sim)

    if key_press("v"):
        for i in sim.lines:
            i: sb.Line
            i.length = i.point_1.pos.distance_to(i.point_2.pos)
            i.length = solid_line_width*2

    if key_down(pg.K_BACKSPACE):
        running = False

    if not (pg.mouse.get_pos()[0] < side_bar_size and side_bar.slide_progress == 1):
        if pg.mouse.get_pressed()[1]:
            if focus == -1:
                touch = sim.mouse_point_touch()
                if not touch == -1:
                    focus = touch
                    pre_focus_move = sim.points[focus].move
                    sim.points[focus].move = False
                    focus_offset = sim.get_m_pos() - sim.points[focus].pos
            else:
                pre_focus_pos = sim.points[focus].pos
        else:
            if not focus == -1:
                sim.points[focus].move = pre_focus_move
                pre_focus_move = None
                sim.points[focus].pre_pos = pre_focus_pos
                sim.points[focus].accel = Vector2(0, 0)
                pre_focus_pos = Vector2(0, 0)
            focus = -1
            focus_offset = Vector2(0, 0)

        if not focus == -1:
            sim.points[focus].pos = sim.get_m_pos() - focus_offset

        if pg.mouse.get_pressed()[0]:
            if key_down(pg.K_LSHIFT):
                if sim.mouse_point_touch(default_point_size) == -1:
                    if key_down(pg.K_LCTRL):
                        if pre_added == None:
                            add_point(sim.get_m_pos())
                            pre_added = sim.points[-1]
                        else:
                            add_point(sim.get_m_pos())
                            add_line(
                                pre_added,
                                sim.points[-1],
                                sim.points[-1].pos.distance_to(pre_added.pos),
                            )
                            pre_added = sim.points[-1]
                    else:
                        add_point(sim.get_m_pos())
            else:
                if not was_l:
                    add_point(sim.get_m_pos())
                was_l = True
        else:
            pre_added = None
            was_l = False

        if pg.mouse.get_pressed()[2]:
            touch = sim.mouse_point_touch()
            if not touch == -1:
                if not was_r:
                    l_add = sim.points[touch]
            was_r = True
        else:
            if not l_add == 0:
                if was_r:
                    touch = sim.mouse_point_touch()
                    if not touch == -1:
                        if not sim.points[touch] == l_add:
                            if key_down(pg.K_LSHIFT):
                                add_line(
                                    l_add,
                                    sim.points[touch],
                                    sim.points[touch].pos.distance_to(l_add.pos),
                                    "spring",
                                )
                                sim.lines[-1].color = spring_color
                            else:
                                add_line(
                                    l_add,
                                    sim.points[touch],
                                    sim.points[touch].pos.distance_to(l_add.pos),
                                )

            l_add = 0
            was_r = False

    if key_press("e"):
        side_bar.direct *= -1

    screen.fill(backdrop)

    if start_time == 0:
        sim.full_update(events, dt)

    counter_menu.full_update(events)

    point_fixed = fixed_toggle.on
    point_ghost = ghost_toggle.on
    big_point = size_toggle.on
    heavy_point = big_toggle.on

    side_bar.full_update(events)

    update_pressed()
    pg.display.update()
    fps_clock.tick(fps)

    current_fps = fps_clock.get_fps()
    fps_counter.text = f"{int(current_fps)} FPS"
    things_counter.text = f"{len(sim.points)} EN"

    dt = (1 / max(current_fps, 1)) * sim_speed
pg.quit()
