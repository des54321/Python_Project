import numpy as np
from pygame import draw, Rect, Surface

class TileMap:

    def __init__(self, colors, tile_size, grid_width, grid_height, pixel_size) -> None:
        self.tiles = [[0 for __ in range(grid_height)] for _ in range(grid_width)]
        self.colors = colors
        self.tile_size = tile_size
        self.pixel_size = pixel_size
        self.tile_pal = []
        self.w = grid_width
        self.h = grid_height
        self.tile_sur = []
    

    def add_tile(self, value):
        self.tile_pal.append(value)
        self.update_sur()
    

    def get_tile(self,x,y):
        return self.tiles[x][y]
    

    def get_pixel(self,px,py,tile_id):
        return self.colors[self.tile_pal[tile_id][px][py]]


    def update_sur(self):
        self.tile_sur = []
        for n,i in enumerate(self.tile_pal):
            new = Surface((self.tile_size*self.pixel_size,self.tile_size*self.pixel_size))
            for px in range(self.tile_size):
                    for py in range(self.tile_size):
                        draw.rect(new,self.get_pixel(px,py,n),Rect(px*self.pixel_size,py*self.pixel_size,self.pixel_size,self.pixel_size))
            self.tile_sur.append(new)


    def render(self, screen: Surface):

        for x in range(self.w):
            for y in range(self.h):
                if not self.get_tile(x,y) == -1:
                    screen.blit(self.tile_sur[self.get_tile(x,y)],(self.pixel_size*x*self.tile_size,self.pixel_size*y*self.tile_size))
                    # for px in range(self.tile_size):
                    #     for py in range(self.tile_size):
                    #         draw.rect(screen, self.get_pixel(px,py,self.get_tile(x,y)), Rect(self.pixel_size*(px+x*self.tile_size),self.pixel_size*(py+y*self.tile_size),self.pixel_size,self.pixel_size))
