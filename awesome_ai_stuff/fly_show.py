import pygame as pg
import fly_game_classes as fg
import pickle

fg.move_speed *= 3
fg.thrust *= 3

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




game = fg.Match()

game.it = fg.BLUE

game.blue.pos_x, game.red.pos_x = game.red.pos_x, game.blue.pos_x

with open('best.pkl','rb') as load:
    best = pickle.load(load)

print(best.bias)

pg.init()
sw = 1600
sh = 900
screen = pg.display.set_mode((sw,sh))
fps = 60
fps_clock = pg.time.Clock()
running = True
while running:
    screen.fill((6,7,6))
    game.update()
    game.render(screen)


    blue_chose = best.big_brain([float(game.it == fg.BLUE),game.blue.pos_x,game.blue.pos_y,game.blue.pos_x-game.red.pos_x,game.blue.pos_y-game.red.pos_y,game.blue.vel_x,game.blue.vel_y,game.red.vel_x,game.red.vel_y])
    if blue_chose[0] > 0:
        game.blue.up_input()
    if blue_chose[1] > 0:
        game.blue.right_input()
    if blue_chose[2] > 0:
        game.blue.left_input()
    
    if key_down(pg.K_UP):
        game.red.up_input()
    if key_down(pg.K_LEFT):
        game.red.left_input()
    if key_down(pg.K_RIGHT):
        game.red.right_input()
    


    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    
    update_pressed()
    pg.display.update()
    fps_clock.tick(fps)
pg.quit()