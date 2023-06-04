import pygame as pg
import numpy as np
import color_interpolation as clerp
from math import floor


pressed_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o','p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'COMMA', '1', '2', '3','4', '5', '6', '7', '8', '9', '0']
pressed = []
last = []

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



def draw_grid():
    for x in range(gw):
        for y in range(gh):
                pg.draw.rect(screen,color.get(grid[x][y]/(colors-1)),pg.Rect(tile_size*x,tile_size*y,tile_size,tile_size))


def in_grid(x,y):
    if x >= gw:
            return False
    if x < 0:
        return False
    if y >= gh:
        return False
    if y < 0:
        return False
    return True


def do_layer(layer):
    global grid
    for i in range(len(grid[:,layer])):
        count = 0
        for n,x in enumerate(pattern):
            if in_grid(i+x[0],layer-1-x[1]):
                count += grid[i+x[0]][layer-1-x[1]]*multi[n]
        
        grid[i][layer] = count%colors
                


def do_pattern(below = 0):
    for i in range(gh)[below+1:]:
        do_layer(i)




# pattern = [[0,1],[-2,2],[2,2],[-1,0],[1,0]]

# pattern = []
# amount = 5
# for i in range(amount+1)[1:]:
#     pattern.append([-(amount-i+1),i-1])
#     pattern.append([(amount-i+1),i-1])

# pattern = []
# amount = 5
# for i in range(amount):
#     pattern.append([-((i%2)+1),i])
#     pattern.append([(i%2)+1,i])

# pattern = []
# amount = 4
# for i in range(amount):
#     pattern.append([-i-1,0])
#     pattern.append([i+1,0])

# pattern = []
# amount = 4
# for i in range(amount):
#     if i%2 == 1:
#         pattern.append([0,i])
#     else:
#         pattern.append([-1,i])
#         pattern.append([1,i])


# pattern = []
# amount = 5
# for i in range(amount+1)[1:]:
#     pattern.append([-i,i-1])
#     pattern.append([i,i-1])


pattern = []
amount = 4
for i in range(amount):
    pattern.append([-1,i])
    pattern.append([1,i])



# pattern = [[0, 0], [-3, 3], [-3, 1], [-3, 2], [-2, 1], [2, 2]]
# pattern = [[0,2],[-1,0],[1,0]]
# pattern = [[2, 2], [-1, 0], [2, 1], [1, 0], [-1, 0]]
# pattern = [[-1,1],[1,1],[-1,2],[1,2],[-1,0],[1,0]]


multi = [1 for _ in range(len(pattern))]
gw = 400
gh = 225
tile_size = 4

colors = 2
color = clerp.ColorLerp(((20,140,40),(220,230,50),(245,60,80),(40,240,220)),[0.33,0.66])
color = clerp.ColorLerp(((0,0,0),(255,255,255)),[])


grid = np.array([[0 for __ in range(gh)] for _ in range(gw)])
grid[gw//2][0] = 1

do_pattern()




pg.init()
sw = gw*tile_size
sh = gh*tile_size
screen = pg.display.set_mode((sw,sh))
fps = 60
fps_clock = pg.time.Clock()

draw_grid()
update_pressed()
pg.display.update()


running = True
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    
    if pg.mouse.get_pressed()[0]:
        grid[floor(pg.mouse.get_pos()[0]/tile_size)][floor(pg.mouse.get_pos()[1]/tile_size)] = 0
        do_pattern(floor(pg.mouse.get_pos()[1]/tile_size))
        draw_grid()
        update_pressed()
        pg.display.update()
    fps_clock.tick(fps)
pg.quit()