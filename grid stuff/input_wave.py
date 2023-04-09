import pygame as pg
from pygame import draw




def draw_grid(grid):
    #Das a lotta for loops
    screen.fill((0,0,0))
    grid_w = len(grid)
    grid_h = len(grid[0])
    for x in range(grid_w):
        for y in range(grid_h):
            for i in range(piece_size):
                for n in range(piece_size):
                    draw.rect(screen, colors[pieces[grid[x][y]][i][n]],pg.Rect(x * (s_w / grid_w) + i * (s_w / (grid_w * piece_size)),y * (s_h / grid_h) + n * (s_h / (grid_h * piece_size)),(s_w / (grid_w * piece_size)), (s_h / (grid_h * piece_size))))




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

def add_piece():
    final = []
    for x in range(piece_size):
        final.append([])
        for y in range(piece_size):
            final[x].append(0)
    global pieces
    pieces.append(final)

def mouse_grid(grid_w,grid_h):
    m_pos = pg.mouse.get_pos()
    return [m_pos[0]//(s_w//grid_w),m_pos[1]//(s_h//grid_h)]

#Settings
input_w = 20
input_h = 20
piece_size = 8
pg.init()


colors = {-1: (0, 0, 0), 0: '#1C2730', 1: '#6C4E23', 2: '#535B60', 3:'#999DA8', 4: '#2D4447'}


pieces = []


want_s_w = 900
want_s_h = 900
s_w = (piece_size*input_w)*(want_s_w//(piece_size*input_w))
s_h = (piece_size*input_h)*(want_s_h//(piece_size*input_h))

input_grid = []
for x in range(input_w):
    input_grid.append([])
    for y in range(input_h):
        input_grid[x].append(0)
        

screen = pg.display.set_mode((s_w, s_h))
fps = 60
fps_clock = pg.time.Clock()
running = True
edit = 0
editing = True
chosen = 0
add_piece()
while running:
    if editing:
        draw_grid([[edit]])
        if pg.mouse.get_pressed()[0]:
            if chosen < len(colors)-1:
                m_pos = mouse_grid(piece_size,piece_size)
                pieces[edit][m_pos[0]][m_pos[1]] = chosen
            else:
                print('Slow down there bro!')
        if key_press('n'):
            chosen -= 1
            print(f'Chosen is now {chosen}')
        if key_press('m'):
            chosen += 1
            print(f'Chosen is now {chosen}')
        if key_press('d'):
            print(f'Now in grid mode, new piece is key {len(pieces)-1}')
            chosen = len(pieces)-1
            print(f'Chosen is now {chosen}')
            editing = False
        if key_press('h'):
            print(pieces)
            print(input_grid)
        if key_press('p'):
            m_pos = mouse_grid(piece_size,piece_size)
            print(m_pos)
            chosen = pieces[edit][m_pos[0]][m_pos[1]]
            print(f'Chosen is now {chosen}')
        
    else:
        draw_grid(input_grid)
        if pg.mouse.get_pressed()[0]:
            if chosen < len(pieces):
                m_pos = mouse_grid(input_w,input_h)
                input_grid[m_pos[0]][m_pos[1]] = chosen
            else:
                print('Slow down there bro!')
        if key_press('n'):
            chosen -= 1
            print(f'Chosen is now {chosen}')
        if key_press('m'):
            chosen += 1
            print(f'Chosen is now {chosen}')
        if key_press('e'):
            add_piece()
            print(f'Now in peice edit mode')
            chosen = 1
            print(f'Chosen is now {chosen}')
            edit = len(pieces)-1
            editing = True
        if key_press('h'):
            print('')
            print(f'pieces = {pieces}')
            print('')
            print(f'ex_grid = {input_grid}')
            print('')
            print(f'colors = {colors}')
            print('')
            print(f'piece_size = {piece_size}')
        if key_press('p'):
            m_pos = mouse_grid(input_w,input_h)
            chosen = input_grid[m_pos[0]][m_pos[1]]
            print(f'Chosen is now {chosen}')

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    update_pressed()
    pg.display.update()
    fps_clock.tick(fps)
    print(int(fps_clock.get_fps()))
pg.quit()
