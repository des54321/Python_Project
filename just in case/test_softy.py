import pygame as pg
from pygame import Vector2
from math import floor,ceil


di_dirs = [
    [1,0],
    [1,1],
    [0,1],
    [-1,1],
    [-1,0],
    [-1,-1],
    [0,-1],
    [1,-1]
]

def possible_around(grid_size,pos):
    '''
    Gives coordinates in the surrounding 8 squares around the point in the grid, that are not outside of the bounds
    '''
    pos = [int(pos[0]),int(pos[1])]
    total = []
    for i in di_dirs:
        possible = [pos[0]+i[0],pos[1]+i[1]]
        if not (possible[0] < 0 or possible[0] >= grid_size[0] or possible[1] < 0 or possible[1] >= grid_size[1]):
            total.append(possible)
    return total



def slope_of(p1,p2):
    '''
    Gives the slope between p1 and p2
    '''
    try:
        return (p1.y-p2.y)/(p1.x-p2.x)
    except:
        return float(99999999999)



def closest_point_to(point, p1, p2):
    '''
    Favorite equation I have ever made btw, returns the closest point on a line to another point
    '''
    if p1.y == p2.y:
        final = Vector2(point.x,p1.y)
        if p1.x > p2.x:
            final.x = max(final.x,p2.x)
            final.x = min(final.x,p1.x)
        else:
            final.x = max(final.x,p1.x)
            final.x = min(final.x,p2.x)
        return final
    elif p1.x == p2.x:
        final = Vector2(p1.x,point.y)
        if p1.y > p2.y:
            final.y = max(final.y,p2.y)
            final.y = min(final.y,p1.y)
        else:
            final.y = max(final.y,p1.y)
            final.y = min(final.y,p2.y)
        return final
    else:
        slope = slope_of(p1,p2)
        in_slope = 1/slope
        final = Vector2(0,0)
        final.x = (((p1.x+((point.y-p1.y)*in_slope))*(slope*slope))+point.x)/((slope*slope)+1)
        final.y = (((p1.y+((point.x-p1.x)*slope))*(in_slope*in_slope))+point.y)/((in_slope*in_slope)+1)
        if p1.x > p2.x:
            if final.x > p1.x:
                final = p1
            elif final.x < p2.x:
                final = p2
        else:
            if final.x < p1.x:
                final = p1
            elif final.x > p2.x:
                final = p2
        return final



def point_in_box(p:Vector2,b1:Vector2,b2:Vector2,radius=0):
    if (p.x > b1.x+radius) == (p.x > b2.x) and (p.x > b1.x-radius) == (p.x > b2.x) and (p.x > b1.x) == (p.x > b2.x+radius) and (p.x > b1.x) == (p.x > b2.x-radius):
        return False
    if (p.y > b1.y+radius) == (p.y > b2.y) and (p.y > b1.y-radius) == (p.y > b2.y) and (p.y > b1.y) == (p.y > b2.y+radius) and (p.y > b1.y) == (p.y > b2.y-radius):
        return False
    return True




class Sim:
    
    def __init__(self, draw_line, draw_circle, get_m_pos, size:tuple, friction:float, gravity: float, resolve_times : int,debug: bool = False, debugging: str = None, breaking = False, max_stress = 0, stress_carry = 0.9) -> None:
        '''
        The softbody simulation class, holds all the components

        draw_line: Function to be called to draw a line (pos1,pos2,width,color)
        draw_circle: Function to be called to draw a circle (pos,size,color,#outline)
        get_m_pos: Should give the position of the cursor relative to the simulation
        size: (width of area, height of area)
        friction: The frictiony the sim is
        gravity: How large the force of gravity is
        resolve_times: How many times the simulation will try to resovle rigid lines
        debug: If the sim is in debug mode
        debbugging: What the sim should print for debug
        stress_carry: How much stress carries over each frame
        '''
        self.draw_line = draw_line
        self.draw_circle = draw_circle
        self.size = size
        self.points = []
        self.lines = []
        self.near_grid = {}
        self.friction = friction
        self.grav = gravity
        self.debug = debug
        self.debugging  = debugging
        self.resovle_times = resolve_times
        self.get_m_pos = get_m_pos
        self.paused = False
        self.breaking = breaking
        self.max_stress = max_stress
        self.stress_carry = stress_carry
    

    def update_points(self,dt):
        for i in self.points:
            i.full_update(dt)
    
    
    def update_lines(self,dt):
        for i in self.lines:
            if i.form == 'spring':
                i.full_update(dt)
    

    def resolve(self,dt):
        for i in self.lines:
            if not i.form == 'spring':
                    i.full_update(dt)
        

        self.update_near_grid()
        for i in self.points:
            i.collide()
        


    def render(self):
        for i in self.lines:
            i.render()
        for i in self.points:
            i.render()
    

    def full_update(self,events,dt):
        if not self.paused:
            self.update_near_grid()
            self.update_points(dt)
            self.update_lines(dt)
            for _ in range(self.resovle_times):
                self.resolve(dt)
        self.render()
    

    def mouse_point_touch(self, size = 0):
        '''
        Gives -1 if the mouse is not touching a point, gives the index of the first point else

        size: How large the cursor's hit box is
        '''
        pos = self.get_m_pos()
        for n,i in enumerate(self.points):
            if i.pos.distance_to(pos) < i.size+size:
                return n
        return -1
    

    def update_near_grid(self):
        solids = []
        for i in self.points:
                if i.solid:
                    solids.append(i)
        if not len(solids) < 1:
            mid = Vector2(0,0)
            max_size = 0
            for i in solids:
                mid += i.pos
                max_size = max(max_size,i.size)
            
            max_size *= 2
            
            self.near_grid = {}
            

            for i in solids:
                near_grid_pos = str([floor(i.pos.x/max_size),floor(i.pos.y/max_size)])
                if near_grid_pos in self.near_grid:
                    self.near_grid[near_grid_pos].append(i)
                else:
                    self.near_grid[near_grid_pos] = [i]
                i.near_grid_pos = near_grid_pos
            

            for i in solids:
                for n in di_dirs:
                    tup = eval(i.near_grid_pos)
                    val = str([tup[0]+n[0],tup[1]+n[1]])
                    if val in self.near_grid:
                        self.near_grid[val].append(i)
            
            
            if self.debug:
                for i in range(grid_size[0]+1):
                    self.draw_line((bounds.left+box_size.x*i,bounds.top),(bounds.left+box_size.x*i,bounds.bottom),2,(255,255,255))
                for i in range(grid_size[1]+1):
                    self.draw_line((bounds.left,bounds.top+box_size.y*i),(bounds.right,bounds.top+box_size.y*i),2,(255,255,255))
                
                self.draw_circle(bound_tl,10,(255,0,0))
                self.draw_circle(bound_br,10,(255,0,0))
                self.draw_circle(mid,10,(255,0,0))
                if self.debugging == "near grid":
                    print(f'{self.near_grid} {len(self.near_grid)} {len(self.near_grid[0])}')
        else:
            self.near_grid = {}






class Point:


    def __init__(self, pos:Vector2, velocity:Vector2, size:int, color:tuple, sim:Sim, weight: float = 1, form = 'normal') -> None:
        '''
        The simple base of the entire simulation, a point in space

        pos: Where the point will be
        velocity: Its speed coming out
        size: How big it is
        color: What color it is
        sim: The points parent simulation
        weight: How heavy it is
        form: What kind of point it is: normal (collides and moves), fixed (collides, not moves), blank (no colliding or moving), ghost (moves, does not collide)
        '''
        self.pos = pos
        self.pre_pos = pos - velocity
        self.size = size
        self.color = color
        self.draw = sim.draw_circle
        self.sim = sim
        self.weight = weight
        self.accel = Vector2()
        self.near_grid_pos = [0,0]
        self.set_form(form)
        self.near_grid_pos = [0,0]
    

    def set_form(self, form):
        if form == 'normal':
            self.move = True
            self.solid = True
        elif form == 'fixed':
            self.move = False
            self.solid = True
        elif form == 'blank':
            self.move = False
            self.solid = False
        elif form == 'ghost':
            self.move = True
            self.solid = False
    

    def render(self):
        self.draw(self.pos,self.size,self.color)
    

    def __repr__(self) -> str:
        return f'ID: {self.sim.points.index(self)}'


    def __str__(self) -> str:
        return self.__repr__()
    

    def update_pos(self, dt):
        vel = self.pos - self.pre_pos
        self.pre_pos = self.pos
        self.pos = self.pos + vel * self.sim.friction + self.accel * dt * dt / (self.weight)
        self.accel = Vector2(0,0)
    

    def apply_grav(self):
        self.accel += Vector2(0,self.sim.grav*self.weight)


    def full_update(self,dt):
        if self.move:
            self.update_pos(dt)
            self.apply_grav()
    

    def collide(self):
        if self.move and self.solid:
            for i in self.sim.near_grid[self.near_grid_pos]:
                if (not i == self) and i.solid:
                    pother:Point = i
                    dist = pother.pos.distance_to(self.pos)
                    if dist < self.size + pother.size:
                        if not dist < 1:
                            if not pother.move:
                                bias = 0
                            else:
                                bias = (self.weight)/(pother.weight+self.weight)
                            mid = (self.pos*bias+pother.pos*(1-bias))
                            dis = (dist - (self.size + pother.size))/dist
                            self.pos += (mid-self.pos)*dis
                            pother.pos += (mid-pother.pos)*dis



class Line:


    def __init__(self,length:float,start:Point,end:Point,color:tuple,width:int,sim:Sim,form:str = 'rigid',strength:float = 1,max_stress = None) -> None:
        '''
        A simple connection between two points, will exert force on them to be the correct length

        length: How long the line wants to be
        start: One of the points its connected to
        end: The other point
        color: ;)
        width: How wide the line will appear, has no effect of strength
        sim: The lines parent simulation
        form: What kind of connectin it is: rigid (will be very stiff), spring (will simply pull on its points), fsolid (a solid line that points will bounce off of, it won't move), m-solid
        strength: How strong the spring will pull, or how far the rigid line will get to the correct distance
        max_stress: How much stress the line can take until it breaks
        '''
        self.length = length
        self.point_1 = start
        self.point_2 = end
        self.color = color
        self.width = width
        self.strength = strength
        self.draw = sim.draw_line
        self.form = form
        if self.form == 'fsolid':
            self.point_1.set_form('blank')
            self.point_1.size = self.width
            self.point_1.color = self.color
            self.point_2.set_form('blank')
            self.point_2.size = self.width
            self.point_2.color = self.color
        self.sim = sim
        self.local_stress = 0
        self.stress = 0
        if max_stress == None:
            self.max_stress = self.sim.max_stress
        else:
            self.max_stress = max_stress
        self.real_max_stress = (self.max_stress/(1-self.sim.stress_carry))*max(1,self.sim.resovle_times)
    

    def render(self):
        self.draw(self.point_1.pos,self.point_2.pos,self.width,self.color)
    

    def full_update(self,dt):
        self.local_stress = 0
        if self.form == 'spring':
            self.update_spring()
        elif self.form == 'rigid':
            self.update_rigid()
        elif self.form == 'fsolid':
            self.update_fsolid()
        elif self.form == 'msolid':
            self.update_msolid()
        
        self.stress *= self.sim.stress_carry
        self.stress += self.local_stress
        if self.sim.breaking:
            if self.stress > self.real_max_stress:
                del self.sim.lines[self.sim.lines.index(self)]
    
    
    def update_spring(self):
        p1 = self.point_1.pos
        p2 = self.point_2.pos
        dist = p1.distance_to(p2)
        if not dist == 0:
            dis_frac = (dist-self.length)/dist
            self.local_stress = max(self.local_stress, abs(dist-self.length))
            mid = (p1+p2)/2
            self.point_1.accel += (mid-p1)*dis_frac*self.strength
            self.point_2.accel += (mid-p2)*dis_frac*self.strength
    

    def update_rigid(self):
        if self.point_1.move or self.point_2.move:
            p1 = self.point_1.pos
            p2 = self.point_2.pos
            dist = p1.distance_to(p2)
            if not dist == 0:
                if not self.point_1.move:
                    bias = 1
                elif not self.point_2.move:
                    bias = 0
                else:
                    bias = (self.point_1.weight)/(self.point_1.weight+self.point_2.weight)
                mid = (p1*bias+p2*(1-bias))
                dis = (dist - self.length)/dist
                self.local_stress += abs(dist-self.length)*(self.point_1.weight+self.point_2.weight)
                self.point_1.pos += (mid-self.point_1.pos)*dis*self.strength
                self.point_2.pos += (mid-self.point_2.pos)*dis*self.strength
    

    def update_fsolid(self):
        for i in self.sim.points:
            point:Point = i
            if point.move and point.solid:
                if point_in_box(point.pos,self.point_1.pos,self.point_2.pos,point.size+self.width):
                    closest = closest_point_to(point.pos,self.point_1.pos,self.point_2.pos)
                    dist = closest.distance_to(point.pos)
                    if dist < self.width + point.size:
                        point.pos = closest - ((closest - point.pos) * ((self.width + point.size) / dist))
    

    def update_msolid(self):
        if not (self.point_1.move or self.point_2.move):
            self.point_1.set_form('blank')
            self.point_1.size = self.width
            self.point_1.color = self.color
            self.point_2.set_form('blank')
            self.point_2.size = self.width
            self.point_2.color = self.color
            self.form = 'fsolid'
            return None

        for i in self.sim.points:
            if not (i == self.point_1 or i == self.point_2):
                point:Point = i
                if point.solid and point.move:
                    if point_in_box(point.pos,self.point_1.pos,self.point_2.pos,point.size+self.width):
                        closest = closest_point_to(point.pos,self.point_1.pos,self.point_2.pos)
                        dist = closest.distance_to(point.pos)
                        if dist < self.width + point.size:
                            p1_dist = self.point_1.pos.distance_to(closest)
                            p2_dist = self.point_2.pos.distance_to(closest)
                            hit_frac = p1_dist / (p1_dist+p2_dist)
                            if not (self.point_1.move and self.point_2.move):
                                p_frac = 1
                            else:
                                p_frac = (2 * ((self.point_1.weight * (1-hit_frac)) + (self.point_1.weight * hit_frac)))/(point.weight + (2 * ((self.point_1.weight * (1-hit_frac)) + (self.point_1.weight * hit_frac))))
                            
                            if not self.point_1.move:
                                p1_frac = 1
                            else:
                                p1_frac = (2 * self.point_1.weight)/(point.weight + (2 * self.point_1.weight))
                            
                            if not self.point_2.move:
                                p2_frac = 1
                            else:
                                p2_frac = (2 * self.point_2.weight)/(point.weight + (2 * self.point_2.weight))
                            
                            m_frac = ((self.width + point.size) / dist)
                            multi = (closest-closest*m_frac+point.pos*m_frac-point.pos)
                            point.pos += multi*p_frac
                            self.point_1.pos -= multi*(1-p1_frac)*(1-hit_frac)
                            self.point_2.pos -= multi*(1-p2_frac)*(hit_frac)
        
        self.update_rigid()

