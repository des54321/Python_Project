import pygame as pg
import color_interpolation
from color_interpolation import lerp,ColorLerp
from pygame import Vector2
from math import cos, pi


def draw_circle(screen,color,pos,size):
    pg.draw.circle(screen,color,(pos[0]+(screen.get_width()/2),screen.get_height()-(pos[1]+(screen.get_height()/2))),round(size))

def draw_rect(screen,pos,width,height,color):
    pg.draw.rect(screen,color,pg.Rect(pos[0]+(screen.get_width()/2),screen.get_height()-(pos[1]+(screen.get_height()/2)),width,height))

def draw_line(screen,color,pos1,pos2,size):
    pg.draw.line(screen,color,(pos1[0]+(screen.get_width()/2),screen.get_height()-(pos1[1]+(screen.get_height()/2))),(pos2[0]+(screen.get_width()/2),screen.get_height()-(pos2[1]+(screen.get_height()/2))),round(size))


class Anim:

    def __init__(self,renders,screen) -> None:
        self.renders = renders
        self.t = 0
        self.screen = screen

        for i in self.renders:
            i.anim = self
    

    def step(self,size):
        self.t += size
    
    def reset(self):
        self.t = 0
    
    def render(self):
        for i in self.renders:
            i.render(self.t)
    
    def update_renders(self):
        for i in self.renders:
            i.anim = self



class EaseValue:

    def __init__(self,start_t,duration,start,end,power=1) -> None:
        self.start_t = start_t
        self.duration = duration
        self.start = start
        self.end = end
        self.power = power
    
    def get(self,t):
        if t < self.start_t:
            return self.start
        if t > self.start_t + self.duration:
            return self.end
        if self.power == 'sine':
            return lerp(self.start,self.end,(cos(((t-self.start_t)/self.duration)*pi+pi)+1)/2)
        return lerp(self.start,self.end,((t-self.start_t)/self.duration)**self.power)



class EasePoint:

    def __init__(self,start_t,duration,start,end=None,power=1) -> None:
        self.start_t = start_t
        self.duration = duration
        self.start = Vector2(start)
        self.end = Vector2(end)
        self.power = power
    

    def get(self,t):
        if t < self.start_t:
            return self.start
        if t > self.start_t + self.duration:
            return self.end
        return Vector2(EaseValue(self.start_t,self.duration,self.start.x,self.end.x,self.power).get(t),EaseValue(self.start_t,self.duration,self.start.y,self.end.y,self.power).get(t))



class Color:

    def __init__(self,start_t,duration,colors,power=1,pos=[]) -> None:
        self.start_t = start_t
        self.duration = duration
        self.power = power
        self.lerper = ColorLerp(colors,pos)
    

    def get(self,t):
        if self.power == 'sine':
            return self.lerper.get((cos((min(max((t-self.start_t)/self.duration,0),1))*pi+pi)+1)/2)
        return self.lerper.get(min(max((t-self.start_t)/self.duration,0),1)**self.power)



class Render:

    def __init__(self,type,color:Color,size:EaseValue,p1:EasePoint,p2:EasePoint = None) -> None:
        self.type = type
        self.color = color
        self.p1 = p1
        self.p2 = p2
        self.size = size
        self.anim = None
    
    def render(self,t):
        if type(self.size) == EaseValue:
            size = self.size.get(t)
        else:
            size = self.size
        if size <= 0:
            return 0
        if type(self.p1) == EasePoint:
            p1 = self.p1.get(t)
        else:
            p1 = self.p1
        if type(self.p2) == EasePoint:
            p2 = self.p2.get(t)
        else:
            p2 = self.p2
        if type(self.color) == Color:
            color = self.color.get(t)
        else:
            color = self.color
        if self.type == 'line':
            draw_line(self.anim.screen,color,p1,p2,round(size))
        if self.type == 'circle':
            draw_circle(self.anim.screen,color,p1,round(size))
    

    def fade_to(self,new_color,duration,power):
        self.color = Color(self.anim.t,duration,(self.color.get(self.anim.t),new_color),power)
