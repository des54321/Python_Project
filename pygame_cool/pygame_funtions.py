
def key_down(key : pg.key) -> bool:
    return pg.key.get_pressed()[key]

def draw_circle(pos,size,color):
    pg.draw.circle(screen,color,(pos[0]+(s_w/2),s_h-(pos[1]+(s_h/2))),round(size))

def draw_rect(pos,width,height,color):
    pg.draw.rect(screen,color,pg.Rect(pos[0]+(s_w/2),s_h-(pos[1]+(s_h/2)),width,height))

def draw_line(pos1,pos2,size,color):
    pg.draw.circle(screen,color,(pos1[0]+(s_w/2),s_h-(pos1[1]+(s_h/2))),(pos2[0]+(s_w/2),s_h-(pos2[1]+(s_h/2))),round(size))

def get_m_pos():
    return [pg.mouse.get_pos()[0]-(s_w/2),s_h-(pg.mouse.get_pos()[1]+(s_h/2))]

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



pg.init()
s_w = 1000
s_h = 600
screen = pg.display.set_mode((s_w,s_h))
fps = 60
fps_clock = pg.time.Clock()
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    
    update_pressed()
    pg.display.update()
    fps_clock.tick(fps)
pg.quit()