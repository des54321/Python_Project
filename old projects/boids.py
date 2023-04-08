import math
import random
import pygame as pg
from pygame import Vector2
pg.init()
screen_width = 1400
screen_height = 800
boid_speed = 10
sight_radius = 100
alignment_weight = 2
cohesion_weight = 0.25
separation_weight = 21
previous_weight = 10
randomness = 1
screen = pg.display.set_mode((screen_width,screen_height))
fps = 60
fps_clock = pg.time.Clock()


def draw_circle(pos,size,color):
    pg.draw.circle(screen,color,(pos[0]+(screen_width/2),screen_height-(pos[1]+(screen_height/2))),round(size))



def draw_boids():
    for i in boids:
        i.draw()



def move_boids():
    for i in boids:
        i.move()



class Boid:

    def __init__(self,x,y) -> None:
        self.speed = boid_speed
        self.x = x
        self.y = y
        self.vel = Vector2(0,random.randint(-1,1))
    
    def near_to(self,radius : float) -> list:
        new =[]
        for i in boids:
            if not i == self:
                if self.dist_to(i) < radius:
                    new.append(i)
        return new


    def dist_to(self,other,index = False) -> float:
        new = []
        new.append(math.dist((self.x,self.y),(other.x,other.y)))
        new.append(math.dist((self.x+screen_width,self.y),(other.x,other.y)))
        new.append(math.dist((self.x-screen_width,self.y),(other.x,other.y)))
        new.append(math.dist((self.x,self.y+screen_height),(other.x,other.y)))
        new.append(math.dist((self.x,self.y-screen_height),(other.x,other.y)))
        # new.append(math.dist((self.x+screen_width,self.y+screen_width),(other.x,other.y)))
        # new.append(math.dist((self.x-screen_width,self.y+screen_height),(other.x,other.y)))
        # new.append(math.dist((self.x-screen_width,self.y-screen_height),(other.x,other.y)))
        # new.append(math.dist((self.x+screen_width,self.y-screen_height),(other.x,other.y)))
        if index:
            return [min(new),new.index(min(new))]
        else:
            return min(new)
    
    def draw(self) -> None:
        draw_circle([self.x,self.y],8,(255,0,255))

    def move(self) -> None:
        self.x += self.vel.x
        self.y += self.vel.y
        self.x = ((self.x + screen_width/2)%screen_width)-screen_width/2
        self.y = ((self.y + screen_height/2)%screen_height)-screen_height/2
        alignment = Vector2(0,0)
        cohesion = Vector2(0,0)
        separation = Vector2(0,0)
        near = self.near_to(sight_radius)
        if not len(near) == 0:
            for i in near:
                alignment += i.vel
                i_dist = self.dist_to(i,True)
                distance = i_dist[0]
                if i_dist[1] == 0:
                    diff = Vector2(i.x-self.x,i.y-self.y)
                elif i_dist[1] == 1 or i_dist[1] == 2:
                    diff = Vector2(self.x-i.x,i.y-self.y)
                else:
                    diff = Vector2(i.x-self.x,self.y-i.y)
                cohesion += diff
                new  = -diff
                dist = separation_weight/distance
                separation += new * dist
            new  = separation + (cohesion*cohesion_weight) + (alignment*alignment_weight) + (self.vel*previous_weight) + Vector2((random.random()*2*randomness)-randomness,(random.random()*2*randomness)-randomness)
            new.scale_to_length(self.speed)
            self.vel = new





boids = []
for i in range(100):
    boids.append(Boid(random.randint(-screen_width/2,screen_width/2),random.randint(-screen_height/2,screen_height/2)))


screen = pg.display.set_mode((screen_width,screen_height))
fps = 60
fps_clock = pg.time.Clock()
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((0,0,0))
    draw_boids()
    mouse_x = pg.mouse.get_pos()[0]-(screen_width/2)
    mouse_y = (screen_height-pg.mouse.get_pos()[1])-(screen_height/2)
    # print(boids[0].dist_to(boids[1]))
    move_boids()
    pg.display.update()
    fps_clock.tick(fps)
pg.quit()