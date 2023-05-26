import pygame as pg
from pygame import Vector2
from color_interpolation import ColorLerp as Clerp

debug_color = Clerp(
    ((0, 0, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)), (0.33, 0.66))
debug_num = 6


class Tile:

    def __init__(self, points, screen_pos) -> None:
        self.points = points
        self.screen_pos = screen_pos
        self.connections = []
        self.connect_type = []
        self.build = 'blank'
        self.build_color = None
        self.uses = 0
        self.troop_color = None
        self.troop_num = 0
        self.troop_moves = 0
        self.captain = None

    def add_connection(self, other, type):
        self.connections.append(other)
        self.connect_type.append(type)

    def remove_connection(self, other):
        try:
            del self.connections[self.connections.index(other)]
        except:
            pass

    def render(self, screen, fill_color, line_color, line_width=0, connects=False):
        if not fill_color == None:
            pg.draw.polygon(screen, fill_color, [
                            self.screen_pos+i for i in self.points])
        if not line_color == None:
            pg.draw.polygon(screen, line_color, [
                            self.screen_pos+i for i in self.points], line_width)
        if connects:
            for n, i in self.connections, self.connect_type:
                pg.draw.line(screen, debug_color.get(
                    i/debug_num), self.screen_pos, (n.screen_pos+self.screen_pos)/2, line_width//2)


def p_touching(i_point: Vector2, grid):
    point = Vector2(i_point)
    for i in grid:
        if point_in_tile(point, i):
            return i
    return None


def point_in_tile(pos: Vector2, tile: Tile):
    return bool(sum([point_left_of_line(pos, tile.points[i]+tile.screen_pos, tile.points[(i+1) % len(tile.points)]+tile.screen_pos) for i in range(len(tile.points))]) % 2)


def point_left_of_line(point, l1, l2):
    if ((point.x > l1.x) == (point.x > l2.x)):
        return False
    if l1.x > l2.x:
        return (((l2.x-l1.x)*(point.y-l1.y)-(l2.y-l1.y)*(point.x-l1.x)) > 0)
    else:
        return (((l2.x-l1.x)*(point.y-l1.y)-(l2.y-l1.y)*(point.x-l1.x)) < 0)


def shape(sides, size, rot=False):
    final = []
    for i in range(sides):
        new = Vector2()
        if rot:
            new.from_polar((size, (i+0.5)*360/sides))
        else:
            new.from_polar((size, i*360/sides))
        final.append(new)
    return final


def hex_grid_l(w, h, tile_size, pos):
    tiles = []
    real_pos = pos-Vector2((w-1)*tile_size*0.75, (h-0.5)*0.866*tile_size)
    for i in range(h):
        for n in range(w):
            tile_pos = Vector2(
                n*tile_size*1.5, (i+(n % 2)*0.5)*1.732*tile_size)
            tiles.append(Tile(shape(6, tile_size), tile_pos+real_pos))
    for i in range(h):
        for n in range(w):
            if i+1 < h:
                tiles[i*w+n].add_connection(tiles[(i+1)*w+n], 0)
            if i-1 >= 0:
                tiles[i*w+n].add_connection(tiles[(i-1)*w+n], 3)
            if n+1 < w:
                tiles[i*w+n].add_connection(tiles[i*w+n+1], 1+n % 2)
                if n % 2 == 0:
                    if i-1 >= 0:
                        tiles[i*w+n].add_connection(tiles[(i-1)*w+n+1], 2)
                else:
                    if i+1 < h:
                        tiles[i*w+n].add_connection(tiles[(i+1)*w+n+1], 1)
            if n-1 >= 0:
                tiles[i*w+n].add_connection(tiles[i*w+n-1], 5-n % 2)
                if n % 2 == 0:
                    if i-1 >= 0:
                        tiles[i*w+n].add_connection(tiles[(i-1)*w+n-1], 4)
                else:
                    if i+1 < h:
                        tiles[i*w+n].add_connection(tiles[(i+1)*w+n-1], 5)

    return tiles
