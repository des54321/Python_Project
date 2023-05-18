import pygame as pg
from pygame import Vector2
from random import random, randint
from math import floor, sqrt, ceil



# Game Setup
pg.init()
sw = 1850
sh = 1000
screen = pg.display.set_mode((sw,sh))
fps = 60
fps_clock = pg.time.Clock()
running = True
###

#Camera Setup
cam_pos = Vector2(0,0)
zoom = 4
cam_move_rate = 0.2
dying_color = (150,40,20)
###

#Player setup
ppos = Vector2(1000,1000)
pvel = Vector2((-2,0))
psize = 50
player_color = (25,230,100)
collide_friction = 0.8
size_of_area = 20000
pox = 300
player_got_ox = False
player_ox_use = 0.35
dying_ox = 300
player_max_ox = 300
###

#Gun setup
gun_dist = 30
gun_length = 60
gun_color = (20,150,60)
gun_charged_color = (230,20,100)
gun_angle = Vector2(0,1)
gun_width = 10
m_down_time = 0
power_shot_time = 30
power_shot_power = 30
normal_shot_power = 4
###


#Bullets
bullet_size = 10
bullet_color = (160,70,230)
bullet_damage = 10
bullet_speed = 4
bullet_speed_char = 6
###

#Planet stuff
max_ox = 60

min_ox = 30
max_ox_size = 0.5
add_planet_size = 250
min_planet_size = 100
add_chance = 0.4
spot_density = 0.0002
spot_size = 40
spot_size_tolerance = 0.2
spot_color_percentage = 0.7
planet_pull = 0.65
oxygen_color = (200,200,255)
ox_gain = 0.1
planet_ox_deplete = 1

planets = []
bullets = []



#Planet Class
class Planet:

    #Startup Function
    def __init__(self, pos : Vector2, size : int, color : tuple, rot_speed : float) -> None:
        self.pos = pos
        self.size = size
        self.tot_ox = min_ox + (((size-min_planet_size)/(max_ox-min_ox))*(max_ox-min_ox))
        self.ox = 0
        self.color = color
        self.rot_speed = rot_speed

        self.spots = []
        self.spots_size = []
        for i in range(ceil((size**2)*spot_density)):
            self.spots_size.append(spot_size*(1 + ( (random()*(spot_size_tolerance*2)) - spot_size_tolerance) ))
            self.spots.append(rand_point_in_cricle(size-self.spots_size[-1]))
            touching = True
            repeat = 0
            while touching and (repeat < 100):
                touching = False
                for i in range(len(self.spots)-1):
                    if self.spots[i].distance_to(self.spots[-1]) < (self.spots_size[i] + self.spots_size[-1]) :
                        self.spots[-1] = rand_point_in_cricle(size-self.spots_size[-1])
                        touching = True
                repeat += 1
            

    def update(self) -> None:
        global pox,player_got_ox
        for i in self.spots:
            i.rotate_ip(self.rot_speed)
        if self.pos.distance_to(ppos) < self.size*(1+max_ox_size):
            if not self.ox == 0:
                self.ox = max(0,self.ox-planet_ox_deplete)
                player_got_ox = True
                pox += planet_ox_deplete
        else:
            self.ox = min(self.tot_ox,self.ox+ox_gain)

    
    #Draw 
    def draw(self) -> None:
        draw_circle(self.pos, self.size*(1+(self.ox/self.tot_ox)*max_ox_size), oxygen_color)
        draw_circle(self.pos, self.size, self.color)
        for i in range(len(self.spots)):
            draw_circle(self.pos+self.spots[i],self.spots_size[i],[self.color[0]*spot_color_percentage,self.color[1]*spot_color_percentage,self.color[2]*spot_color_percentage])



class PlayerBullet:

    def __init__(self,pos,dir,power) -> None:
        self.pos = pos
        self.vel = Vector2()
        self.vel.from_polar((dir,power))

    
    def remove(self):
        if planet_touching(bullet_size,self.pos) != -1:
            del bullets[bullets.index(self)]
        if self.pos.x < 0 or self.pos.y < 0 or self.pos.x > size_of_area or self.pos.y > size_of_area:
            del bullets[bullets.index(self)]
    

    def move(self):
        self.pos += self.vel
    

    def render(self):
        draw_circle(self.pos,bullet_size,bullet_color)
    

    def full_update(self):
        self.render()
        self.remove()
        self.move()


#Draws all the planets
def draw_planets():
    for i in planets:
        i.draw()
        i.update()



#Updates bullets
def update_bullets():
    for i in bullets:
        i.full_update()


#Draw a circle a point in space
def draw_circle(pos ,size : float,color : str,outline = 0):
    pg.draw.circle(screen,color,[(pos[0]-cam_pos.x)/zoom+(sw/2),sh-((pos[1]-cam_pos.y)/zoom+(sh/2))],floor(size/zoom),outline)


#Draw a line at point in space
def draw_line(pos1 , pos2, width : float,color : str):
    pg.draw.circle(screen,color,[(pos1[0]-cam_pos.x)/zoom+(sw/2),sh-((pos1[1]-cam_pos.y)/zoom+(sh/2))],floor(width/zoom))
    pg.draw.circle(screen,color,[(pos2[0]-cam_pos.x)/zoom+(sw/2),sh-((pos2[1]-cam_pos.y)/zoom+(sh/2))],floor(width/zoom))
    pg.draw.line(screen,color,[(pos1[0]-cam_pos.x)/zoom+(sw/2),sh-((pos1[1]-cam_pos.y)/zoom+(sh/2))],[(pos2[0]-cam_pos.x)/zoom+(sw/2),sh-((pos2[1]-cam_pos.y)/zoom+(sh/2))],floor(width/zoom)*2)


#Gives a random signed value
def ran_s():
    return random()*2-1


#Tells if a key is pressed
def key_down(key : pg.key):
    return pg.key.get_pressed()[key]


#Gives a point in a circle
def rand_point_in_cricle(size : float):
    place = pg.Vector2()
    place.from_polar((sqrt(random())*size,random()*360))
    return place


#Gives the pos of the mouse on screen
def get_m_pos_screen():
    return Vector2(pg.mouse.get_pos()[0]-(sw/2),sh-(pg.mouse.get_pos()[0]+(sh/2)))


#Gives the pos of the mouse in space
def get_m_pos_space():
    return Vector2(cam_pos.x+((pg.mouse.get_pos()[0]-(sw/2))*zoom),cam_pos.y+((sh-(pg.mouse.get_pos()[1]+(sh/2)))*zoom))


#Moves the camera towards the player
def cam_update():
    global cam_pos
    cam_pos += (ppos-cam_pos)*cam_move_rate


#Gives a random color
def ran_color():
    return (floor(random()*255),floor(random()*255),floor(random()*255))


#Calculates the effect of planets on an object at a point
def calc_planet_pull(pos):
    new = pos
    if not type(new) == Vector2:
        new = Vector2(new[0],new[1])
    total = Vector2()
    for i in planets:
        total += (i.pos-new).normalize()*((i.size**2)/(new.distance_to(i.pos)**2))
    return total*planet_pull


#Checks if a point of some size is touching a planet
def planet_touching(size, pos):
    new = pos
    if not type(new) == Vector2:
        new = Vector2(new[0],new[1])
    touch = -1
    for i in range(len(planets)):
        if new.distance_to(planets[i].pos) < planets[i].size+size:
            touch = i
            return planets[touch]
    return touch


#Moves the player
def player_move():
    global ppos
    global pvel
    global gun_angle
    gun_angle = (get_m_pos_space()-ppos).normalize()
    pvel += calc_planet_pull(ppos)
    ppos += pvel
    touching = planet_touching(psize,ppos)
    if not touching == -1:
        new = ppos - touching.pos
        new.scale_to_length(touching.size+psize)
        new += touching.pos
        pvel = (new-(ppos - pvel))*collide_friction
        ppos = new
    
    ppos.x = ((ppos.x+size_of_area)%(size_of_area*2))-size_of_area
    ppos.y = ((ppos.y+size_of_area)%(size_of_area*2))-size_of_area


#Draws the player
def player_draw():
    draw_circle(ppos,psize,player_color)
    if m_down_time > power_shot_time:
        draw_line(ppos+(gun_angle*gun_dist),ppos+(gun_angle*(gun_dist+gun_length)),gun_width,gun_charged_color)
    else:
        draw_line(ppos+(gun_angle*gun_dist),ppos+(gun_angle*(gun_dist+gun_length)),gun_width,gun_color)



def rand_planet_size():
    current = min_planet_size
    current += randint(0,add_planet_size)
    while random() < add_chance:
        current += randint(0,add_planet_size)
    return current
        

largest = 0
for i in range(60):
    planets.append(Planet(Vector2(ran_s()*size_of_area,ran_s()*size_of_area),rand_planet_size(),ran_color(),ran_s()*2))
    if planets[-1].size > largest:
        largest = planets[-1].size

print(largest)




left_m_down = False




while running:
    
    if pg.mouse.get_pressed()[0]:
        m_down_time += 1
        left_m_down = True
    else:
        if left_m_down:
            if m_down_time > power_shot_time:
                pvel -= gun_angle*power_shot_power
                #bullets.append(PlayerBullet(ppos,Vector2().angle_to(gun_angle),bullet_speed_char))
            else:
                pvel -= gun_angle*normal_shot_power
        m_down_time = 0
        left_m_down = False
    
    screen.fill((10,6,15))
    player_got_ox = False
    player_move()
    cam_update()
    draw_planets()
    player_draw()
    update_bullets()
    if not player_got_ox:
        pox -= player_ox_use
    
    pox = min(pox,player_max_ox)
    
    if pox < dying_ox:
        pg.draw.circle(screen,dying_color,(sw//2,sh//2),sw,int((1-(pox/dying_ox))*sw))
    if pox < 0:
        pg.quit()
    

    # Game quit, fps, display update
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    
    pg.display.update()
    fps_clock.tick(fps)
    ###

pg.quit()