
'''
How to use this amazing tool:

 - The first thing to know is how to add a circle, simple just left click
 - If 'b' is held when adding a point, the point will be very heavy and big
 - If you hold shift while pressing left click, you will create a circle everyframe where adding one wouldn't make it intersect with others
 - If you hold ctrl while shifting, it will auto connect the points with a solid line

 
 - You can add a connection between points by just righting clicking and holding on a point, and dragging the cursor to the point you want to connect to
 - If you hold shift while doing this, the connection will be a spring

 - When adding circles or connections, they will be fixed if you hold 'f' whild adding them, and they will not collide if you hold 'g'
 - When adding a connection, it will be a moveable solid line if 'r' is held


 - WASD to move the camera
 - 'n' to zoom in, 'm' to zoom out

 - 'p' to pause and unpause the simulation

 -'k' to save the current scene
 -'l' to laod the last saved scene
'''


import pygame as pg
import soft_body as sb
from math import floor
from pygame import Vector2
from menu_engine import Menu, Text, Button, Slider
from copy import deepcopy, copy
import color_interpolation as clerp


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


#Draw a circle a point in space
def draw_circle(pos ,size : float,color : str,outline = 0):
    pg.draw.circle(screen,color,[(pos[0]-cam_pos.x)/zoom+(sw/2),sh-((pos[1]-cam_pos.y)/zoom+(sh/2))],floor(size/zoom),outline)


#Draw a line at point in space
def draw_line(pos1 , pos2, width : float,color : str):
    pg.draw.circle(screen,color,[(pos1[0]-cam_pos.x)/zoom+(sw/2),sh-((pos1[1]-cam_pos.y)/zoom+(sh/2))],floor(width/zoom))
    pg.draw.circle(screen,color,[(pos2[0]-cam_pos.x)/zoom+(sw/2),sh-((pos2[1]-cam_pos.y)/zoom+(sh/2))],floor(width/zoom))
    pg.draw.line(screen,color,[(pos1[0]-cam_pos.x)/zoom+(sw/2),sh-((pos1[1]-cam_pos.y)/zoom+(sh/2))],[(pos2[0]-cam_pos.x)/zoom+(sw/2),sh-((pos2[1]-cam_pos.y)/zoom+(sh/2))],floor(width/zoom)*2)


def get_m_pos():
    return Vector2([((pg.mouse.get_pos()[0]-(sw/2))*zoom)+cam_pos.x,((sh-(pg.mouse.get_pos()[1]+(sh/2)))*zoom)+cam_pos.y])



def add_point(pos):
    '''
    The function thats called to add a point into the simulation
    '''
    if mode == 'build':
        sim.points.append(sb.Point(pos,Vector2(0,0),node_size,color_pal[3],sim,form='ghost'))
    elif mode == 'test':
        sim.points.append(sb.Point(pos,Vector2(0,0),node_size*3,color_pal[6],sim,20))


def add_line(p1,p2,length):
    if build_material == 'wood':
        sim.lines.append(sb.Line(length,p1,p2,color_pal[1],line_width,sim,max_stress=wood_strength))
        sim.lines[-1].mat = 'wood'
    elif build_material == 'steel':
        sim.lines.append(sb.Line(length,p1,p2,color_pal[4],line_width,sim,max_stress=steel_strength))
        sim.lines[-1].mat = 'steel'
    elif build_material == 'road':
        sim.lines.append(sb.Line(length,p1,p2,color_pal[2],node_size,sim,'msolid',max_stress=road_strength))
        sim.lines[-1].mat = 'road'
    elif build_material == 'spring':
        sim.lines.append(sb.Line(length,p1,p2,color_pal[5],line_width,sim,'spring',default_spring_strength,spring_strength))
        sim.lines[-1].mat = 'spring'
    sim.lines[-1].real_color = copy(sim.lines[-1].color)


def switch_mat(mat):
    global build_material
    build_material = mat


color_pal = ('#F9F7F7','#BBC2CF','#3F72AF','#112D4E',(230,130,140),(240,230,120),(20,30,50))

mode = 'build'

pg.init()

#Screen
sw = 1600
sh = 900
screen = pg.display.set_mode((sw,sh))
###

#Camera
cam_pos = Vector2(0,0)
zoom = 1
line_width = 5
node_size = 15
backdrop = color_pal[0]
outside_color = color_pal[2]

stress_color = clerp.ColorLerp(((30,240,70),(230,230,40),(220,30,30)),[0.6])

view_mode = 'normal'

cam_move_speed = 5
###

#Simulation
sim_speed = 13
start_time = 20
gap_size = 700
ledge_size = 150
gap_height = -100
incline = 200
ledge_width = 10


material_weight = 0.2

steel_strength = 30
wood_strength = 16
spring_strength = 100
road_strength = 20

sim = sb.Sim(draw_line,draw_circle,get_m_pos,(sw,sh),1,-5,2,breaking=True,max_stress=5,stress_carry=0.5)
sim.paused = True


sim.points.append(sb.Point(Vector2(-gap_size,gap_height),Vector2(0,0),ledge_width,color_pal[6],sim,1,'blank'))
sim.points.append(sb.Point(Vector2(gap_size,gap_height+incline),Vector2(0,0),ledge_width,color_pal[6],sim,1,'blank'))
sim.points.append(sb.Point(Vector2(-gap_size-ledge_size,gap_height),Vector2(0,0),ledge_width,color_pal[6],sim,1,'blank'))
sim.points.append(sb.Point(Vector2(gap_size+ledge_size,gap_height+incline),Vector2(0,0),ledge_width,color_pal[6],sim,1,'blank'))
sim.points.append(sb.Point(Vector2(-gap_size,gap_height-ledge_size),Vector2(0,0),ledge_width,color_pal[6],sim,1,'blank'))
sim.points.append(sb.Point(Vector2(gap_size,gap_height-ledge_size+incline),Vector2(0,0),ledge_width,color_pal[6],sim,1,'blank'))
sim.lines.append(sb.Line(ledge_size,sim.points[-1],sim.points[-5],color_pal[6],ledge_width,sim,'fsolid'))
sim.lines[-1].mat = 'fixed'
sim.lines[-1].real_color = color_pal[6]
sim.lines.append(sb.Line(ledge_size,sim.points[-3],sim.points[-5],color_pal[6],ledge_width,sim,'fsolid'))
sim.lines[-1].mat = 'fixed'
sim.lines[-1].real_color = color_pal[6]
sim.lines.append(sb.Line(ledge_size,sim.points[-4],sim.points[-6],color_pal[6],ledge_width,sim,'fsolid'))
sim.lines[-1].mat = 'fixed'
sim.lines[-1].real_color = color_pal[6]
sim.lines.append(sb.Line(ledge_size,sim.points[-2],sim.points[-6],color_pal[6],ledge_width,sim,'fsolid'))
sim.lines[-1].mat = 'fixed'
sim.lines[-1].real_color = color_pal[6]


#Menu stuff
fps_counter = Text('NaN',(backdrop,outside_color),Vector2(0.1,0.1),Vector2(0.8,0.4),editable=False)
things_counter = Text('NaN',(backdrop,outside_color),Vector2(0.1,0.6),Vector2(0.8,0.4),editable=False)

counter_menu = Menu(screen,Vector2(0,0),Vector2(0,0),80,55,backdrop,0,[fps_counter,things_counter])



#Build menu
menu_height = 200

build_material = 'wood'

road_select = Button('Road',(color_pal[2],color_pal[3]),Vector2(0.02,0.1),Vector2(0.2,0.35),switch_mat,'press',3,has_func_arg=True,fucn_arg='road')
wood_select = Button('Wood',(color_pal[2],color_pal[3]),Vector2(0.02,0.55),Vector2(0.2,0.35),switch_mat,'press',3,has_func_arg=True,fucn_arg='wood')
steel_select = Button('Steel',(color_pal[2],color_pal[3]),Vector2(0.24,0.1),Vector2(0.2,0.35),switch_mat,'press',3,has_func_arg=True,fucn_arg='steel')
spring_select = Button('Spring',(color_pal[2],color_pal[3]),Vector2(0.24,0.55),Vector2(0.2,0.35),switch_mat,'press',3,has_func_arg=True,fucn_arg='spring')
selected = Text('Currently placing: None',(None,color_pal[3]),Vector2(0.75,0.05),Vector2(0.2,0.2),False)


material_select_menu = Menu(screen,Vector2(0,sh-menu_height),Vector2(0,sh),sw,menu_height,color_pal[1],8,[road_select,wood_select,steel_select,spring_select,selected],0.05,(True,True,False,False),True)


#Controls
pre_focus_move = None
pre_focus_pos = Vector2(0,0)
focus = -1
default_spring_strength = 15
focus_offset = Vector2(0,0)


save_sim = None


was_l = False
was_r = False
l_add = 0
fps = 60
dt = (1/fps)*sim_speed
fps_clock = pg.time.Clock()
current_fps = fps_clock.get_fps()
running = True
while running:
    start_time = max(start_time-1,0)

    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False
    

    if key_down(pg.K_w):
        cam_pos.y += cam_move_speed*zoom
    
    if key_down(pg.K_s):
        cam_pos.y -= cam_move_speed*zoom
    
    if key_down(pg.K_d):
        cam_pos.x += cam_move_speed*zoom
    
    if key_down(pg.K_a):
        cam_pos.x -= cam_move_speed*zoom
    
    if key_down(pg.K_n):
        zoom *= 1.04
    
    if key_down(pg.K_m):
        zoom /= 1.04
    
    if key_press('v'):
        if view_mode == 'normal':
            view_mode = 'stress'
        elif view_mode == 'stress':
            view_mode = 'normal'
        
        if view_mode == 'normal':
            for i in sim.lines:
                i.color = copy(i.real_color)
    
    if view_mode == 'stress':
        for i in sim.lines:
            i.color = stress_color.get(min(max(i.stress/i.real_max_stress,0),1))
    
    
    if key_press('p'):
        if mode == 'build':
            save_sim = deepcopy(sim)
            sim.paused = False
            mode = 'test'
            material_select_menu.direct = -1
            for i in sim.points:
                i.weight = 1
                i.local_stress = 0
                i.stress = 0
            
            for i in sim.lines:
                line:sb.Line = i
                line.length = line.point_1.pos.distance_to(line.point_2.pos)
                line.point_1.weight += (line.length/100)*material_weight
                line.point_2.weight += (line.length/100)*material_weight

        elif mode == 'test':
            sim = deepcopy(save_sim)
            sim.paused = True
            mode = 'build'
            material_select_menu.direct = 1
    
    if mode == 'build':
        if pg.mouse.get_pressed()[1]:
            if focus == -1:
                touch = sim.mouse_point_touch(node_size)
                if not touch == -1:
                    focus = touch
                    pre_focus_move = sim.points[focus].move
                    sim.points[focus].move = False
                    focus_offset = sim.get_m_pos()-sim.points[focus].pos
            else:
                pre_focus_pos = sim.points[focus].pos
        else:
            if not focus == -1:
                sim.points[focus].move = pre_focus_move
                pre_focus_move = None
                sim.points[focus].pre_pos = pre_focus_pos
                sim.points[focus].accel = Vector2(0,0)
                pre_focus_pos = Vector2(0,0)
            focus = -1
            focus_offset = Vector2(0,0)
    
        if not focus == -1:
            sim.points[focus].pos = sim.get_m_pos()-focus_offset
    


    if pg.mouse.get_pressed()[0]:
        if not (mode == 'build' and pg.mouse.get_pos()[1] > sh-menu_height):
            if sim.mouse_point_touch(node_size*3) == -1:
                if not was_l:
                    add_point(sim.get_m_pos())
            was_l = True
    else:
        was_l = False
    
    
    if mode == 'build':
        if pg.mouse.get_pressed()[2]:
            touch = sim.mouse_point_touch(node_size)
            if not touch == -1:
                if not was_r:
                    l_add = sim.points[touch]
            was_r = True
        else:
            if not l_add == 0:
                if was_r:
                    touch = sim.mouse_point_touch(node_size)
                    if not touch == -1:
                        if not sim.points[touch] == l_add:
                            add_line(l_add,sim.points[touch],sim.points[touch].pos.distance_to(l_add.pos))
            
            l_add = 0
            was_r = False

    screen.fill(backdrop)
    if start_time == 0:
        sim.full_update(events,dt)
    
    fps_counter.text = f'{int(current_fps)} FPS'
    things_counter.text = f'{len(sim.points)} EN'
    counter_menu.full_update(events)

    material_select_menu.full_update(events)
    selected.text = f'Currently Placing: {build_material}'

    update_pressed()

    pg.display.update()

    fps_clock.tick(fps)
    current_fps = fps_clock.get_fps()


    dt = (1/max(current_fps,1))*sim_speed
pg.quit()