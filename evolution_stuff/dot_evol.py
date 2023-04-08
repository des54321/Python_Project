import pygame as pg
from pygame import Vector2, draw
from random import random
from copy import deepcopy


pressed_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                   'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'COMMA', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
pressed = []
last = []




#Sim settings

#Costs
min_photo_rate = 0
max_photo_rate = 14

min_move_cost = 0.5
max_move_cost = 3

attack_rate_cost = 0.3

min_damage_cost = 0.001

max_damage_cost = 0.005

min_sight_cost = 0.01

max_sight_cost = 0.03

split_cost = 1600

#Rand
damage_effe = 0.4

min_dist = 4

dot_add_rate = 3
dot_add_timer = 0
max_dots = 200
new_dot_energy = 1000

#Physics
split_force = 0.2

friction = 0.95




def dots_do_the_thingy_awwww_yeah_baby_this_is_cool():
    for i in dots:
        i.full_update()




def ranran(start,end):
    return start+(random()*(end-start))


def evolve_trait(org,down,up,mini,maxi):
    return min(max(mini,org + ranran(down,up)),maxi)


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


def lerp(x,min,max):
    return min + ((max-min)*x)


class DNA:

    def __init__(self) -> None:
        self.repel_fore = ranran(-0.8,0.8)
        self.repel_side = ranran(-0.8,0.8)
        self.photo_trade_off = ranran(0,1)
        self.sight_trade_off = ranran(0,1)
        self.attack_rate = ranran(30,110)
        self.damage = ranran(0,1000)
        self.size = ranran(6,10)
        self.split_size = ranran(1800,2500)
        self.sight_range = ranran(50,70)
        self.cost_photo_eval()
        self.distance_from_random = 0
        self.color = (round(ranran(0,255)),round(ranran(0,255)),round(ranran(0,255)))
        # self.repel_fore = -0.4
        # self.repel_side = 0.2
        # self.photo_trade_off = 1
        # self.attack_rate = 120
        # self.damage = 4
        # self.size = 4
        # self.split_size = 1000000
        # self.sight_range = 100
        # self.sight_trade_off = 0
        # self.cost_photo_eval()
        # self.distance_from_random = 0
        # self.color = (round(ranran(0,255)),round(ranran(0,255)),round(ranran(0,255)))
    

    def cost_photo_eval(self):
        total_cost = 0

        total_cost += (abs(self.repel_fore) + abs(self.repel_side)) * lerp(self.photo_trade_off,min_move_cost,max_move_cost)
        total_cost += (abs(self.repel_fore) + abs(self.repel_side)) * lerp(self.photo_trade_off,min_move_cost,max_move_cost)
        total_cost += self.damage * lerp(self.sight_trade_off,min_damage_cost,max_damage_cost)
        total_cost += (60/self.attack_rate)*attack_rate_cost
        total_cost += self.sight_range * lerp(1-self.sight_trade_off,min_sight_cost,max_sight_cost)


        photo_total = lerp(self.photo_trade_off,min_photo_rate,max_photo_rate)

        self.photo_rate = photo_total - total_cost
    

    def mutate(self):
        new = deepcopy(self)
        new.attack_rate = evolve_trait(new.attack_rate,-4,4,5,200)
        new.damage = evolve_trait(new.damage,-10,10,0,1200)
        new.photo_trade_off = evolve_trait(new.photo_trade_off,-0.05,0.05,0,1)
        new.repel_fore = evolve_trait(new.repel_fore,-0.04,0.04,-2,2)
        new.repel_side = evolve_trait(new.repel_side,-0.04,0.04,-2,2)
        new.sight_trade_off = evolve_trait(new.sight_trade_off,-0.05,0.05,0,1)
        new.size = evolve_trait(new.size,-0.5,0.5,5,20)
        new.split_size = evolve_trait(new.split_size,-100,100,split_cost,100000)
        new.sight_range = evolve_trait(new.sight_range,-10,10,0,100)
        new.color = (round(evolve_trait(new.color[0],-10,10,0,255)),round(evolve_trait(new.color[1],-10,10,0,255)),round(evolve_trait(new.color[2],-10,10,0,255)))
        new.distance_from_random += 1
        new.cost_photo_eval()
        return new
    

    def __str__(self) -> str:
        st = ''
        st += ' Attack rate:'+str(round(self.attack_rate))
        st += ' Damage:'+str(round(self.damage))
        st += ' Repel Fore:'+str(self.repel_fore)
        st += ' Repel Side:'+str(self.repel_side)
        st += ' Photo trade off:'+str(self.photo_trade_off)
        st += ' Sight trade off:'+str(self.sight_trade_off)
        st += ' Sight:'+str(round(self.sight_range))
        st += ' Photo Rate:'+str(self.photo_rate)
        st += ' Gen:'+str(round(self.distance_from_random))
        st += ' Split Size:'+str(round(self.split_size))
        return st



class Dot:

    def __init__(self, dna: DNA, energy,pos: Vector2, vel: Vector2) -> None:
        self.dna = dna
        self.pos = pos
        self.vel = vel
        self.energy = energy
        self.in_radius_rel = Vector2(0,0)
        self.attack_timer = self.dna.attack_rate
        self.attack_stack = []
    

    def render(self):
        draw.circle(screen,self.dna.color,self.pos,self.dna.size)
    

    def update_position(self):
        self.pos += self.vel
    

    def add_energy(self):
        self.energy += self.dna.photo_rate


    def check_die(self):
        if self.energy <= 0:
            self.slash_kill()


    def check_split(self):
        if self.energy > self.dna.split_size:
            if not len(dots) > max_dots:
                self.energy -= split_cost
                dir = ranran(0,360)
                force = Vector2(0,0)
                force.from_polar([self.dna.size*split_force,dir])
                dots.append(Dot(self.dna.mutate(),self.energy/2,self.pos+force*6,force))
                dots.append(Dot(self.dna.mutate(),self.energy/2,self.pos+force*-6,force*-1))
                self.slash_kill()
    

    def full_update(self):
        self.add_energy()
        self.check_die()
        self.check_split()
        self.update_vel()
        self.update_position()
        self.update_with_other_dots()
        self.defend_the_homeland()
        self.render()


    def slash_kill(self):
        del dots[dots.index(self)]


    def check_for_adding(self,other_dot):
        dist = max(self.pos.distance_to(other_dot.pos),min_dist)
        if dist < self.dna.sight_range:
            self.in_radius_rel += (self.pos-other_dot.pos)/(dist*dist)

            if dist < self.dna.size+other_dot.dna.size:
                self.attack_stack.append(other_dot)


    def defend_the_homeland(self):
        self.attack_timer = max(self.attack_timer-1,0)
        if len(self.attack_stack) > 0:
            if self.attack_timer == 0:
                self.attack_timer = self.dna.attack_rate
                for i in self.attack_stack:
                    i.energy -= self.dna.damage
                    self.energy += self.dna.damage * damage_effe
        
        self.attack_stack = []


    def update_vel(self):
        self.vel *= friction
        self.apply_force((self.dna.repel_fore,self.dna.repel_side),1,0,self.in_radius_rel)
        
    
    def apply_force(self,rule:tuple,div:float,pos:Vector2,rel_pos_ar = None):

        if rel_pos_ar == None:
            rel_pos = ((self.pos - pos)/div)
        else:
            rel_pos = rel_pos_ar
        #Fore movement
        self.vel += rel_pos*rule[0]
        #Side movement
        self.vel += Vector2(rel_pos.y,rel_pos.x*-1)*rule[1]
    

    def update_with_other_dots(self):
        self.in_radius_rel = Vector2(0,0)
        for i in dots:
            if not i == self:
                self.check_for_adding(i)



        

dots = []


pg.init()
s_w = 1000
s_h = 600

for i in range(0):
    dots.append(Dot(DNA(),new_dot_energy,Vector2(ranran(0,s_w),ranran(0,s_h)),Vector2(0,0)))

for i in dots:
        print(i.dna.photo_rate)


screen = pg.display.set_mode((s_w, s_h))
fps = 60
run_self = False
fps_clock = pg.time.Clock()
running = True
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    screen.fill((0,0,0))

    if run_self:
        for i in dots:
            i.apply_force((-2,0),900,Vector2(pg.mouse.get_pos()))
        
        if len(dots) < 20:
            dots.append(Dot(DNA(),new_dot_energy,Vector2(pg.mouse.get_pos())+Vector2(ranran(-200,200),ranran(-200,200)),Vector2(0,0)))
    
    else:

        if pg.mouse.get_pressed()[0]:
            for i in dots:
                i.apply_force((-2,0),900,Vector2(pg.mouse.get_pos()))
        
        if pg.mouse.get_pressed()[2]:
            for i in dots:
                i.apply_force((3,0),900,Vector2(pg.mouse.get_pos()))
        

        if pg.mouse.get_pressed()[1]:
            if dot_add_timer == 0:
                dots.append(Dot(DNA(),new_dot_energy,Vector2(pg.mouse.get_pos())+Vector2(ranran(-10,10),ranran(-10,10)),Vector2(0,0)))
                dot_add_timer = dot_add_rate
    

    update_pressed()
    dots_do_the_thingy_awwww_yeah_baby_this_is_cool()
    dot_add_timer = max(dot_add_timer-1,0)
    pg.display.update()
    fps_clock.tick(fps)
    if key_press('q'):
        print(dots[0].dna)
    if key_press('f'):
        print(fps_clock.get_fps())
    if key_press('n'):
        print(len(dots))
    if key_press('w'):
        print(dots[-1].dna)
    if key_press('d'):
        dots.append(Dot(DNA(),new_dot_energy,Vector2(pg.mouse.get_pos()),Vector2(0,0)))
        dots[-1].dna.attack_rate = 5
        dots[-1].dna.damage = 1500
        dots[-1].dna.repel_fore = -4
        dots[-1].dna.repel_side = 0
        dots[-1].dna.photo_trade_off = 0
        dots[-1].dna.sight_trade_off = 0
        dots[-1].dna.sight_range = 300
        dots[-1].dna.size = 20
        dots[-1].dna.cost_photo_eval()
        print(dots[-1].dna)
        dots[-1].attack_timer = dots[-1].dna.attack_rate
pg.quit()
