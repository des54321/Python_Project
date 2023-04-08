import pygame as pg
from pygame import Vector2, draw, Rect
from menu_engine import Menu, Button, Slider, Text


particles = []
particle_size = 10
particle_add_delay = 2
particle_add_timer = 0

lines = []


pressed_letters = ['ESCAPE','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o','p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'COMMA', '1', '2', '3','4', '5', '6', '7', '8', '9', '0']
pressed = []
last = []



def nearset_point_to_line(p: Vector2,sp: Vector2,ep: Vector2):
    '''
    Gives the nearest point on the line [sp to ep] to p
    '''
    x,y = p
    sx,sy = sp
    ex,ey = ep
    if sy == ey:
        rx = x
        ry = sy
        if sx > ex:
            if rx > sx:
                rx = sx
            elif rx < ex:
                rx = ex
        else:
            if rx > ex:
                rx = ex
            elif rx < sx:
                rx = sx
        return (rx,ry)
    elif sx == ex:
        rx = sx
        ry = y
        if sy > ey:
            if ry > sy:
                ry = sy
            elif ry < ey:
                ry = ey
        else:
            if ry > ey:
                ry = ey
            elif ry < sy:
                ry = sy
        return (rx,ry)
    else:
        slope = slope_of([sx,sy],[ex,ey])
        in_slope = 1/slope
        rx = (((sx+((y-sy)*in_slope))*(slope*slope))+x)/((slope*slope)+1)
        ry = (((sy+((x-sx)*slope))*(in_slope*in_slope))+y)/((in_slope*in_slope)+1)
        if sx > ex:
            if rx > sx:
                rx = sx
                ry = sy
            elif rx < ex:
                rx = ex
                ry = ey
        else:
            if rx > ex:
                rx = ex
                ry = ey
            elif rx < sx:
                rx = sx
                ry = sy
        return Vector2(rx,ry)



def slope_of(p1,p2):
    '''
    The slope between points p1 and p2
    '''
    try:
        return (p1[1]-p2[1])/(p1[0]-p2[0])
    except:
        return 99999999999999999999999999


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


def liquid_particles_sim():
    global particles

    for i,par1 in enumerate(particles):
        for line in lines:
            near_p = nearset_point_to_line(par1[0],line[0],line[1])
            dist = par1[0].distance_to(near_p)
            if (dist < line_repel) and (not dist == 0):
                pre_pos = particles[i][0]
                particles[i][0] = near_p+(((par1[0] - near_p)/dist)*line_repel)
                particles[i][1] =  particles[i][0] - (pre_pos-par1[1])
        
        par_num = 0
        par_sum = Vector2(0,0)
        for n,par2 in enumerate(particles):
            if not par1[0] == par2[0]:
                if abs(par1[0].x-par2[0].x) < sense_range:
                    if abs(par1[0].y-par2[0].y) < sense_range:
                        dist = par1[0].distance_to(par2[0])
                        if dist < sense_range:
                            par_num += 1
                            par_sum += par2[1]
                            particles[i][1] += ((par2[0]-par1[0])*(dist-sense_range)*repel_power)/dist
            elif not i == n:
                particles[n][0].x += 1
        if not par_num == 0:
            particles[i][1] = (particles[i][1]*(1-visco))+((par_sum/par_num)*visco)
                


def move_particles():
    global particles
    for i in range(len(particles)):
        particles[i][0] += particles[i][1]
        particles[i][1] += Vector2(0,grav)


def render_lines():
    for i in lines:
        draw.line(screen,color_pal[4],i[0],i[1],10)


def render_particles():
    for i in particles:
        draw.circle(screen,color_pal[5],i[0],particle_size)




pg.init()

color_pal = [(3,5,2),(2,4,20),(4,8,30),(245,246,234),(120,110,170),(50,40,120),(200,195,210)]

s_w = 1600
s_h = 960
screen = pg.display.set_mode((s_w,s_h))
fps = 60
fps_clock = pg.time.Clock()
background_color = color_pal[0]
drawing_line = False
mouse_was_pressed = False

lines.append([Vector2(0,0),Vector2(0,s_h)])
lines.append([Vector2(0,s_h),Vector2(s_w,s_h)])
lines.append([Vector2(s_w,0),Vector2(s_w,s_h)])
lines.append([Vector2(s_w,0),Vector2(0,0)])

visco = 0.05
def visco_slider_func(set_get):
    global visco

    var_min = 0
    var_max = 0.5
    if set_get == 'get':
        return (visco-var_min)/(var_max-var_min)
    else:
        visco = var_min+((var_max-var_min)*set_get)


sense_range = 100
def sense_range_slider_func(set_get):
    global sense_range

    var_min = 0
    var_max = 200
    if set_get == 'get':
        return (sense_range-var_min)/(var_max-var_min)
    else:
        sense_range = var_min+((var_max-var_min)*set_get)


repel_power = 0.03
def repel_power_slider_func(set_get):
    global repel_power
    
    var_min = 0
    var_max = 0.08
    if set_get == 'get':
        return (repel_power-var_min)/(var_max-var_min)
    else:
        repel_power = var_min+((var_max-var_min)*set_get)


line_repel = 20
def line_repel_slider_func(set_get):
    global line_repel
    
    var_min = -1
    var_max = 50
    if set_get == 'get':
        return (line_repel-var_min)/(var_max-var_min)
    else:
        line_repel = var_min+((var_max-var_min)*set_get)


grav = 0.1
def grav_slider_func(set_get):
    global grav
    
    var_min = 0
    var_max = 1
    if set_get == 'get':
        return (grav-var_min)/(var_max-var_min)
    else:
        grav = var_min+((var_max-var_min)*set_get)


def line_button_func():
    global drawing_line
    drawing_line = True


visco_slider = Slider(
    'Thickness'
    ,(color_pal[4],color_pal[5],color_pal[3]), Vector2(0.03,0.1), Vector2(0.16,0.35), visco_slider_func, 5
)

sense_range_slider = Slider(
    'Sight Dist'
    ,(color_pal[4],color_pal[5],color_pal[3]), Vector2(0.20,0.1), Vector2(0.16,0.35), sense_range_slider_func, 5
)

repel_power_slider = Slider(
    'Par Repel'
    ,(color_pal[4],color_pal[5],color_pal[3]), Vector2(0.37,0.1), Vector2(0.16,0.35), repel_power_slider_func, 5
)

line_repel_slider = Slider(
    'Line Repel'
    ,(color_pal[4],color_pal[5],color_pal[3]), Vector2(0.54,0.1), Vector2(0.16,0.35), line_repel_slider_func, 5
)

grav_slider = Slider(
    'Gravity'
    ,(color_pal[4],color_pal[5],color_pal[3]), Vector2(0.71,0.1), Vector2(0.16,0.35), grav_slider_func, 5
)

line_button = Button(
    [[(0.25, 0.35),(0.2, 0.3),(0.1, 0.3),(0.05, 0.35),(0.05, 0.65),(0.1, 0.7),(0.2, 0.7),(0.25, 0.65),(0.25, 0.55),(0.75, 0.55),(0.75, 0.65),(0.8, 0.7),(0.9, 0.7),(0.95, 0.65),(0.95, 0.35),(0.9, 0.3),(0.8, 0.3),(0.75, 0.35),(0.75, 0.45),(0.25, 0.45)]]
    ,(color_pal[4],color_pal[5]), Vector2(0.03,0.55), Vector2(0.12,0.35), line_button_func, 'press', 5
)

fps_couter = Text(
    'NaN'
    ,(color_pal[6],color_pal[5]),Vector2(0.9,0.8),Vector2(0.08,0.1),False
)

particle_couter = Text(
    'NaN'
    ,(color_pal[6],color_pal[5]),Vector2(0.9,0.7),Vector2(0.08,0.1),False
)




main_menu = Menu(screen,Vector2(0,s_h-250), Vector2(0,s_h), s_w, 250, color_pal[6], 20, [grav_slider,visco_slider,line_button,sense_range_slider,repel_power_slider,line_repel_slider,fps_couter,particle_couter], 0.1, (True,True,False,False),False)



running = True
while running:
    events = pg.event.get()

    liquid_particles_sim()
    move_particles()

    screen.fill(background_color)
    render_particles()
    render_lines()
    main_menu.full_update(events)

    if not main_menu.focused():
        if key_press('m'):
            main_menu.direct *= -1
    
    if key_press('ESCAPE'):
        running=False
    

    if not ((pg.mouse.get_pos()[1] > main_menu.up_pos.y) and (main_menu.slide_progress == 1)):
        if pg.mouse.get_pressed()[0]:
            if drawing_line:
                if mouse_was_pressed[0]:
                    lines[-1][1] = Vector2(pg.mouse.get_pos())
                else:
                    lines.append([Vector2(pg.mouse.get_pos()),Vector2(pg.mouse.get_pos())])
            else:
                if particle_add_timer == 0:
                    particle_add_timer = particle_add_delay
                    particles.append([Vector2(pg.mouse.get_pos()),Vector2(0,0)])
        else:
            if drawing_line and mouse_was_pressed[0]:
                drawing_line = False
        mouse_was_pressed = pg.mouse.get_pressed()



    for event in events:
        if event.type == pg.QUIT:
            running = False

    
    particle_add_timer = max(particle_add_timer-1,0)
    update_pressed()
    pg.display.update()
    fps_couter.text = str(int(fps_clock.get_fps())) + ' FPS'
    particle_couter.text = str(len(particles)) + ' Particles'
    fps_clock.tick(fps)
pg.quit()