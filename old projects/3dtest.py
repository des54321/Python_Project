import numpy as np
import pygame as pg
from pygame import Vector2, Vector3
import math
from random import random, randint



circles = [[Vector3(10,5,10),5],[Vector3(-5,0,4),2]]
for i in range(10):
    circles.append([Vector3(randint(-10,10),randint(-10,10),randint(-10,10)),randint(2,4)])




def ray_trace():
    cam_dir_x = cam_dir.as_spherical()[1]
    cam_dir_y = cam_dir.as_spherical()[2]
    x_dir = -1*(x_fov/2)
    x_pos = -1*(s_w/2)
    for x in range(x_rays):
        y_dir = -1*(y_fov/2)
        y_pos = -1*(s_h/2)
        for y in range(y_rays):
            angle = Vector3()
            angle.from_spherical((1, (cam_dir_x + x_dir)%360, (cam_dir_y + y_dir)%360))
            dist = 0
            pos = Vector3(0,0,0)
            run = True
            for i in range(step_count):
                if run:
                    dist += step
                    pos += angle*step
                    for n in circles:
                        if pos.distance_squared_to(n[0]-cam_pos) < (n[1]*n[1]):
                            run = False
                    if pos.y < floor_height:
                        run = False
            
            color = (255*(1-(dist/(step_count*step))),0,0)
            draw_rect((x_pos,y_pos),s_w/x_rays,color)
            y_pos += s_h/y_rays
            y_dir += y_fov/y_rays
        x_pos += s_w/x_rays
        x_dir += x_fov/x_rays
        
        




def draw_rect(pos,size,color):
    pg.draw.rect(screen,color,pg.Rect(pos[0]+(s_w/2),s_h-(pos[1]+(s_h/2)),size,size))



def key_down(key : pg.key):
    return pg.key.get_pressed()[key]


a = Vector3()
a.from_spherical((1,0,0))
a.rotate_z_ip(10)
print(a.as_spherical())


#Cam setup
cam_dir = Vector3(1,0,0)
x_fov = 100
y_fov = 100
x_rays = 20
y_rays = 20
cam_pos = Vector3(0,5,0)


#Raytracing Settings
step = 2
step_count = 10
floor_height = -2



#Screen setup
pg.init()
s_w = 800
s_h = 800
screen = pg.display.set_mode((s_w,s_h))
fps = 60
fps_clock = pg.time.Clock()
running = True
while running:
    print(cam_dir.as_spherical()[1])

    if key_down(pg.K_LEFT):
        cam_dir_x = cam_dir.as_spherical()[1]
        cam_dir_y = cam_dir.as_spherical()[2]
        cam_dir.from_spherical((1,(cam_dir_x-5)%180,cam_dir_y))
    if key_down(pg.K_RIGHT):
        cam_dir_x = cam_dir.as_spherical()[1]
        cam_dir_y = cam_dir.as_spherical()[2]
        cam_dir.from_spherical((1,(cam_dir_x+5)%180,cam_dir_y))
    if key_down(pg.K_UP):
        cam_dir_x = cam_dir.as_spherical()[1]
        cam_dir_y = cam_dir.as_spherical()[2]
        cam_dir.from_spherical((1,cam_dir_x,max((min((cam_dir_y+5,170)),20))))
    if key_down(pg.K_DOWN):
        cam_dir_x = cam_dir.as_spherical()[1]
        cam_dir_y = cam_dir.as_spherical()[2]
        cam_dir.from_spherical((1,cam_dir_x,max((min((cam_dir_y-5,170)),20))))


    screen.fill((0,0,0))
    ray_trace()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    pg.display.update()
    fps_clock.tick(fps)
pg.quit()