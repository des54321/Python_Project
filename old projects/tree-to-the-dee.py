import pygame as pg
from pygame import Vector3, Vector2
from math import sin, cos, pi
from copy import copy, deepcopy


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

def get_m_pos():
    return [pg.mouse.get_pos()[0]-(s_w/2),s_h-(pg.mouse.get_pos()[1]+(s_h/2))]

def draw_circle(pos,size,color):
    pg.draw.circle(screen,color,(pos[0]+(s_w/2),s_h-(pos[1]+(s_h/2))),round(size))



class OrnoPoints:

    def __init__(self , is_list : bool = False , given_list : list = [] , is_grid : bool = False , specs : list = [] , is_cube : bool = False ,center : bool = True) -> None:
        new_list = []
        if is_list:
            new_list = given_list
        if is_grid:
            for x in range(specs[0]):
                for y in range(specs[1]):
                    new_list.append(Vector3(x*specs[2],y*specs[3],0))
        if is_cube:
            for x in range(specs[0]):
                for y in range(specs[1]):
                    for z in range(specs[2]):
                        new_list.append(Vector3(x*specs[3],y*specs[4],z*specs[5]))
        self.points = new_list
        if center:
            if is_grid:
                self.translate(Vector3(-specs[2]*(specs[0]-1)/2,-specs[3]*(specs[1]-1)/2,0))
            if is_cube:
                self.translate(Vector3(-specs[3]*(specs[0]-1)/2,-specs[4]*(specs[1]-1)/2,-specs[5]*(specs[2]-1)/2))
    
    def __add__(self, other):
        new_list = []
        if type(other) == OrnoPoints:
            if len(other.points) == len(self.points):
                new_list = []
                for num, i in enumerate(self.points):
                    new_list.append(i+other.points[num])
        if type(other) == Vector3:
            new_list = []
            for i in self.points:
                new_list.append(i+other)
        return OrnoPoints(given_list = new_list, is_list=True)
    
    def __mul__(self, other):
        new_list = []
        if type(other) == float or type(other) == int:
            new_list = []
            for i in self.points:
                new_list.append(i*other)
        return new_list
    
    def translate(self, translation):
        self += translation
    
    def scale(self, scale_factor):
        self.points = self * scale_factor
    
    def rotate_x_ip(self, degrees, y = 0, z = 0):
        for num, i in enumerate(self.points):
            self.points[num].y = y + (((i.y - y) * cos(degrees)) - ((i.z - z) * sin(degrees)))
            self.points[num].z = z + (((i.y - y) * sin(degrees)) + ((i.z - z) * cos(degrees)))
    
    def rotate_y_ip(self, degrees, x = 0, z = 0):
        for num, i in enumerate(self.points):
            self.points[num].x = x + (((i.x - x) * cos(degrees)) - ((i.z - z) * sin(degrees)))
            self.points[num].z = z + (((i.x - x) * sin(degrees)) + ((i.z - z) * cos(degrees)))
        
    def rotate_z_ip(self, degrees, x = 0, y = 0):
        for num, i in enumerate(self.points):
            self.points[num].x = x + (((i.x - x) * cos(degrees)) - ((i.y - y) * sin(degrees)))
            self.points[num].y = y + (((i.x - x) * sin(degrees)) + ((i.y - y) * cos(degrees)))
    
    def rotate_x(self, degrees, y = 0, z = 0):
        new_points = deepcopy(self)
        for num, i in enumerate(self.points):
            new_points.points[num].y = y + (((i.y - y) * cos(degrees)) - ((i.z - z) * sin(degrees)))
            new_points.points[num].z = z + (((i.y - y) * sin(degrees)) + ((i.z - z) * cos(degrees)))
        return new_points
    
    def rotate_y(self, degrees, x = 0, z = 0):
        new_points = deepcopy(self)
        for num, i in enumerate(self.points):
            new_points.points[num].x = x + (((i.x - x) * cos(degrees)) - ((i.z - z) * sin(degrees)))
            new_points.points[num].z = z + (((i.x - x) * sin(degrees)) + ((i.z - z) * cos(degrees)))
        return new_points
    
    def rotate_z(self, degrees, x = 0, y = 0):
        new_points = deepcopy(self)
        for num, i in enumerate(self.points):
            new_points.points[num].x = x + (((i.x - x) * cos(degrees)) - ((i.y - y) * sin(degrees)))
            new_points.points[num].y = y + (((i.x - x) * sin(degrees)) + ((i.y - y) * cos(degrees)))
        return new_points
        

    def render(self, point_size, color):
        for i in self.points:
            if not i.z <= 0:
                draw_circle([i.x/i.z*100,i.y/i.z*100],point_size,color)

    

    
        
        
        


        


scene = OrnoPoints(is_cube= True, specs= [2,2,2,80,80,80])
print(len(scene.points))
rot_x = 0
rot_y = 0
rot_z = 0
tau = pi*2
m_sense = 0.1
looking_y = 0
cam_pos = Vector3(0,0,200)

pg.init()
s_w = 1000
s_h = 600
screen = pg.display.set_mode((s_w,s_h))
fps = 60
fps_clock = pg.time.Clock()

pg.mouse.set_visible(False)

running = True
while running:

    mouse_vel = pg.mouse.get_rel()[0]

    looking_y += (mouse_vel/s_w)*tau*m_sense


    image = (scene.rotate_x(rot_x)).rotate_y(-looking_y)

    screen.fill((0,0,0))
    (image + cam_pos).render(4,(200,50,220))

    
    if key_down(pg.K_UP):
        rot_x += 0.05
    
    if key_down(pg.K_DOWN):
        rot_x -= 0.05
    
    if key_down(pg.K_RIGHT):
        rot_y += 0.05
    
    if key_down(pg.K_LEFT):
        rot_y -= 0.05
    
    if key_down(pg.K_d):
        rot_z += 0.05
    
    if key_down(pg.K_a):
        rot_z -= 0.05
    

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    
    update_pressed()
    pg.display.update()
    pg.mouse.set_pos([s_w/2,s_h/2])
    fps_clock.tick(fps)
pg.quit()