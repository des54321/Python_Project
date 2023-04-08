import math
import pygame as pg
from pygame.math import Vector2
from random import random
import os
if __name__ == '__main__':
    import battle_gameplay
    import menu_engine
    from menu_engine import Menu, Button, Slider, Text

'''
Setting up the window and stuff
'''


def key_down(key : pg.key):
    return pg.key.get_pressed()[key]



if __name__ == '__main__':
    pg.init()
    os.chdir('Battle Game 8')
    game_icon = pg.image.load('play.png')
    pg.display.set_icon(game_icon)
    pg.display.set_caption('Battle Game!')
    print(pg.joystick.get_count())
    buttons_pressed = []
    controllers = []
    for i in range(pg.joystick.get_count()):
        controllers.append(pg.joystick.Joystick(i))
        buttons_pressed.append([False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,[0,0],[0,0],[False,False]])

    for controller in controllers:
        controller.init()


players_num = 1
# color_pal = ((147, 125, 194),(198, 137, 198),(232, 160, 191),(252, 197, 192))
color_pal = ((33, 33, 33),(15, 76, 117),(50, 130, 184),(187, 225, 250))
aim_type = 2
s_w = 1920
s_h = 1080
screen = pg.display.set_mode((s_w,s_h), pg.FULLSCREEN)

'''
Setting up controller support
'''

key_mapping = {
  "x": 0,
  "circle": 1,
  "square": 2,
  "triangle": 3,
  "share": 4,
  "PS": 5,
  "options": 6,
  "left_stick_click": 7,
  "right_stick_click": 8,
  "L1": 9,
  "R1": 10,
  "up_arrow": 11,
  "down_arrow": 12,
  "left_arrow": 13,
  "right_arrow": 14,
  "touchpad": 15

}



#up,right,down,left,fire,aim1,aim2,special
controls = ((pg.K_w,pg.K_d,pg.K_s,pg.K_a,pg.K_SPACE,pg.K_e,pg.K_f,pg.K_LSHIFT),(pg.K_UP,pg.K_RIGHT,pg.K_DOWN,pg.K_LEFT,pg.K_COMMA,pg.K_v,pg.K_b,pg.K_RSHIFT),(pg.K_i,pg.K_l,pg.K_k,pg.K_j,pg.K_LEFTBRACKET,pg.K_o,pg.K_p,pg.K_u))

def go_to_char_select():
    global current_page
    current_page = 'char_select'


#Gotta love UI, right, RIGHT?


start_button = Button('Play', (color_pal[1],color_pal[2]),Vector2(0.3,0.6),Vector2(0.4,0.2),go_to_char_select,'press',10)
title_text = Text('/think of name', (color_pal[0],color_pal[2]),Vector2(0.2,0.1),Vector2(0.6,0.2),False)

start_menu = Menu(screen, Vector2(0,0), Vector2(0,s_h),s_w,s_h,color_pal[0],0,[start_button,title_text])



char_select = Menu(screen, Vector2(0,0), Vector2(0,s_h),s_w,s_h,color_pal[1],0,[])






fps = 60
fps_clock = pg.time.Clock()
if __name__ == '__main__':
    running = True
    current_page = 'start'
    while running:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.JOYBUTTONUP:
                buttons_pressed[event.joy][event.button] = False
            if event.type == pg.JOYBUTTONDOWN:
                buttons_pressed[event.joy][event.button] = True
            if event.type == pg.JOYAXISMOTION:
                if event.axis > 3:
                    if event.value < 0:
                        buttons_pressed[event.joy][17][event.axis-4] = False
                    else:
                        buttons_pressed[event.joy][17][event.axis-4] = True
                elif event.axis > 1:
                    if aim_type == 1:
                        if  not abs(event.value) < 0.4:
                            buttons_pressed[event.joy][16][event.axis-2] = round(event.value*20)/20
                    elif aim_type == 2:
                        buttons_pressed[event.joy][16][event.axis-2] = round(event.value*20)/20
                        if abs(event.value) < 0.4:
                            buttons_pressed[event.joy][16][event.axis-2] = 0
                else:
                    buttons_pressed[event.joy][15][event.axis] = round(event.value*20)/20
                    if abs(event.value) < 0.4:
                        buttons_pressed[event.joy][15][event.axis] = 0
        
        screen.fill((0,0,0))
        if current_page == 'start':
            start_menu.full_update(events)
        elif current_page == 'char_select':
            char_select.full_update(events)
        elif current_page == 'game':
            battle_gameplay.game_tick(buttons_pressed,screen,controls,aim_type)
        pg.display.update()
        fps_clock.tick(fps)
        if key_down(pg.K_BACKSPACE):
            running = False
    pg.quit()