import pygame as pg
from pygame import Vector2
import numpy as np
import color_interpolation as clerp
from math import floor, cos
from color_interpolation import lerp


pressed_letters = ['SPACE','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o','p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'COMMA', '1', '2', '3','4', '5', '6', '7', '8', '9', '0']
pressed = []
last = []

for i in pressed_letters:
    pressed.append(False)
    last.append(False)


def d_cos(i):
    return cos(i*0.0174533)


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




def in_grid(x,y):
    if x >= gw:
            return False
    if x < 0:
        return False
    if y >= gh:
        return False
    if y < 0:
        return False
    return True


def do_layer(layer):
    global grid
    for i in range(len(grid[:,layer])):
        count = 0
        for n,x in enumerate(pattern):
            if in_grid(i+x[0],layer-1-x[1]):
                count += grid[i+x[0]][layer-1-x[1]]*multi[n]
        
        grid[i][layer] = count%colors
                


def do_pattern(below = 0):
    for i in range(gh)[below+1:]:
        do_layer(i)


def touch(pos):
    return grid[floor(pos[0])][floor(pos[1])] == colors-1


def send_ray(dir_i,step,start:Vector2):
    dir = Vector2()
    dir.from_polar((1,dir_i))
    pos = start.copy()
    hit_marker = False
    for i in range(fog)[0:]:
        pos.x += (dir*step).x
        if in_grid(pos[0],pos[1]):
            if touch(pos):
                count = 0
                while touch(pos) and count < mini_step_size:
                    pos -= dir*step/mini_step_size
                    count += 1
                pos.y += (dir*step).y
                if in_grid(pos[0],pos[1]):
                    if touch(pos):
                        pos.y -= (dir*step).y
                        return [pos.distance_to(start),0.5 + int(hit_marker)]
                pos.x += (dir*step).x
                if in_grid(pos[0],pos[1]):
                    if touch(pos):
                        pos -= (dir*step)
                        return [pos.distance_to(start),0 + int(hit_marker)]
        else:
            break

        pos.y += (dir*step).y
        if in_grid(pos[0],pos[1]):
            if touch(pos):
                count = 0
                while touch(pos) and count < mini_step_size:
                    pos -= dir*step/mini_step_size
                    count += 1
                pos.x += (dir*step).x
                if in_grid(pos[0],pos[1]):
                    if touch(pos):
                        pos.x -= (dir*step).x
                        return [pos.distance_to(start),0.5 + int(hit_marker)]
                pos.y += (dir*step).y
                if in_grid(pos[0],pos[1]):
                    if touch(pos):
                        pos -= (dir*step)
                        return [pos.distance_to(start),1 + int(hit_marker)]
        else:
            break

        if grid[floor(pos[0])][floor(pos[1])] == colors:
            count = 0
            while grid[floor(pos[0])][floor(pos[1])] == colors and count < mini_step_size:
                pos -= dir*step/mini_step_size
                count += 1
            pos.x += (dir*step).x
            if in_grid(pos[0],pos[1]):
                if grid[floor(pos[0])][floor(pos[1])] == colors:
                    pos.x -= (dir*step).x
                    return [pos.distance_to(start),1.5]
            pos.y += (dir*step).y
            if in_grid(pos[0],pos[1]):
                if grid[floor(pos[0])][floor(pos[1])] == colors:
                    pos -= (dir*step)
                    return [pos.distance_to(start),2]

    return [fog,0.5 + int(hit_marker)]


def find_rays(fov:float,step:float,dir:Vector2,start:Vector2,num:int):
    rays = []
    cur_dir = dir - fov/2
    for i in range(num):
        ray_in = send_ray(cur_dir,step,start)
        ray = ray_in[0]*d_cos((dir - cur_dir))
        ray /= wall_height
        ray = max(ray,step_size)
        pg.draw.line(screen,color.get(ray_in[1]/2),(i*res,sh/2 + (sh/2)/ray),(i*res,sh/2 - (sh/2)/ray),res)
        cur_dir += fov/num
    return rays







pattern = [[0,1],[-2,2],[2,2],[-1,0],[1,0]]
pattern = [[-1,1],[1,1],[-1,2],[1,2],[-1,0],[1,0]]
# pattern = [[0,2],[-1,0],[1,0]]
multi = [1,1,1,1,1,1]
gw = 640
gh = 360





colors = 2
color = clerp.ColorLerp(((90,220,40),(40,60,10),(110,20,220)),[0.5])


grid = np.array([[0 for __ in range(gh)] for _ in range(gw)])
grid[gw//2][0] = 1

do_pattern()




pg.init()
sw = 1600
sh = 900
p_pos = Vector2(gw//2 + 0.5,270.5)
p_dir = 45
dir_vec = Vector2()
dir_vec.from_polar((1,p_dir))
fov = 90
fog = 40

rot_speed = 2
move_speed = 0.05
step_size = 0.25
mini_step_size = 10

res = 6



sky_color = (140,160,250)
floor_color = (120,60,10)

wall_height = 1

screen = pg.display.set_mode((sw,sh))
fps = 60
fps_clock = pg.time.Clock()

rays = [0 for i in range(sw//res)]

running = True
while running:
    if key_down(pg.K_LEFT):
        p_dir -= rot_speed
    
    if key_down(pg.K_RIGHT):
        p_dir += rot_speed
    
    if key_down(pg.K_UP):
        p_pos.x += (dir_vec*move_speed).x
        if touch(p_pos):
            p_pos.x -= (dir_vec*move_speed).x

        p_pos.y += (dir_vec*move_speed).y
        if touch(p_pos):
            p_pos.y -= (dir_vec*move_speed).y
    
    if key_down(pg.K_DOWN):
        p_pos.x -= (dir_vec*move_speed).x
        if touch(p_pos):
            p_pos.x += (dir_vec*move_speed).x

        p_pos.y -= (dir_vec*move_speed).y
        if touch(p_pos):
            p_pos.y += (dir_vec*move_speed).y
    
    
    if key_press('SPACE'):
        grid[floor(p_pos[0])][floor(p_pos[1])] = colors

    




    
    p_dir %= 360
    dir_vec = Vector2()
    dir_vec.from_polar((1,p_dir))
    
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False
    
    if key_down(pg.K_r):
        running = False

    
    pg.draw.rect(screen,sky_color,pg.Rect(0,0,sw,sh/2))
    pg.draw.rect(screen,floor_color,pg.Rect(0,sh/2,sw,sh/2))
    find_rays(fov,step_size,p_dir,p_pos,sw//res)
    update_pressed()
    pg.display.update()
    fps_clock.tick(fps)
    print(int(fps_clock.get_fps()))
pg.quit()