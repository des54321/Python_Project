import pygame as pg
from pygame import Vector2


class Tile:

    def __init__(self,points,screen_pos) -> None:
        self.points = points
        self.screen_pos = screen_pos
        self.connections = []


    def add_connection(self,other):
        self.connections.append(other)
    

    def remove_connection(self,other):
        try:
            del self.connections[self.connections.index(other)]
        except:
            pass
    

    def render(self,screen,fill_color,line_color,line_width):
        if not fill_color == None:
            pg.draw.polygon(screen,fill_color,[self.screen_pos+i for i in self.points])
        pg.draw.polygon(screen,line_color,[self.screen_pos+i for i in self.points],line_width)