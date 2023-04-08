from sim_run import sim, Cell, interate
import pygame as pg
from pygame import draw
from grid_class import Grid
from random import randrange, random, randint



c_w = 32
c_h = 32
c_size = 25
s_w = 800
s_w = c_w * c_size
s_h = c_h * c_size
rule = [  (0,0,1,0) , (1,0,1,0.1) , (-1,0,1,0.1) , (0,1,1,-0.1) , (0,-1,1,-0.1)  ]
max_value = 50
min_value = 50


def color_of(value : float) -> tuple:
    # if value > 0:
    #     return tuple([0,max(min(int(((value - min_value)/(max_value-min_value))*255), 255), 0),0])
    # else:
    #     return tuple([max(min(int(((value - min_value)/(max_value-min_value))*255), 255), 0),0,0])
    if value > 0:
        return tuple([0,max(min(int((value/max_value)*255), 255), 0),0])
    else:
        return tuple([max(min(int(((value)/(-min_value))*255), 255), 0),0,0])

def draw_grid(grid : object) -> None:
    for x in range(grid.width):
        for y in range(grid.height):
            draw.rect(screen, color_of(grid.get(x,y).value), pg.Rect(x*c_size,y*c_size,c_size,c_size))

def random_rule():
    return (randint(-4,4),randint(-4,4),4*random()-2)

def key_down(key : pg.key):
    return pg.key.get_pressed()[key]



rule = [ 0 , (0,0,1)  ]

for i in range(4):
    rule.append(random_rule())


rule = [-0.08948954253475944, [0, 0, 1.1336456835506528], [3, -3, 1.1899776892686071]] 
pg.init()
screen = pg.display.set_mode((s_w,s_h))
pg.display.set_caption('Learning Test')
fps = 20
fps_clock = pg.time.Clock()
running = True

board = Grid(c_w,c_h,Cell)
board.get(8,8).value = 100
board.get(24,24).value = -100
# board.get(19,9).value = -10
# board.get(19,19).value = 
interations = 0

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    

    draw_grid(board)
    board = interate(board, rule, max_val=50)
    board.get(8,8).value = 50
    board.get(24,24).value = -50

    if key_down(pg.K_r):
        board = Grid(c_w,c_h,Cell)
        board.get(8,8).value = 50
        board.get(24,24).value = -50
        rule = [ random()-0.5 , (0,0,4*random()-2)  ]

        for i in range(5):
            rule.append(random_rule())


    interations += 1
    pg.display.update()
    fps_clock.tick(fps)
pg.quit()