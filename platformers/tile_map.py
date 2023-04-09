import numpy as np
from pygame import draw, Rect

class TileMap:

    def __init__(self, colors, tile_size, grid_width, grid_height, pixel_size) -> None:
        self.tiles = []
        self.colors = colors
        self.tile_size = tile_size
        self.pixel_size = pixel_size
        self.tile_pal = []
        self.w = grid_width
        self.h = grid_height
    

    def add_tile(self, value):
        self.tiles.append(value)
    

    def get_tile(self,x,y):
        return self.tiles[x][y]
    

    def get_pixel(self,px,py,tile_id):
        return self.colors[self.tile_pal[tile_id][px][py]]


    def render(self, screen):
        for x in range(self.w):
            for y in range(self.h):
                if not self.get_tile(x,y) == -1:
                    for px in range(self.tile_size):
                        for py in range(self.tile_size):
                            draw.rect(screen, self.get_pixel(px,py,self.get_tile(x,y)), Rect(self.pixel_size*(px+x*self.tile_size),self.pixel_size*(py+y*self.tile_size),self.pixel_size,self.pixel_size))
    