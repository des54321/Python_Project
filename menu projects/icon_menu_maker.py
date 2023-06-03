import pygame
from random import random
import math


def key_down(key: pygame.key) -> bool:
    return pygame.key.get_pressed()[key]

pressed_letters = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "COMMA",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
]
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
        test = eval("pygame.K_" + i)
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

p = []
snap = 20
screen_width = 800
screen_height = 800
was_left_last = False
line_width = 1
FPS = 60
fpsClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("Sim")
screen = pygame.display.set_mode((screen_width,screen_height))
running = True
while running:
    for i in range(len(p)):
        p[i][0] = (round(p[i][0]/(screen_width/snap)))*(screen_width/snap)
        p[i][1] = (round(p[i][1]/(screen_height/snap)))*(screen_height/snap)
    p_per = p
    for i in range(len(p)):
        p_per[i][0] = (round(p[i][0]/(screen_width/snap)))*(screen_width/snap)
        p_per[i][1] = (round(p[i][1]/(screen_height/snap)))*(screen_height/snap)
    if (pygame.mouse.get_pressed())[0]:
        if not was_left_last:
            p.append([pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]])
            for i in range(len(p)):
                p[i][0] = (round(p[i][0]/(screen_width/snap)))*(screen_width/snap)
                p[i][1] = (round(p[i][1]/(screen_height/snap)))*(screen_height/snap)
            #pygame.draw.polygon(screen, (button_color[0]/2,button_color[1]/2,button_color[2]/2), [b_pos(0,0.2,0.1),b_pos(0,0.9,0.5),b_pos(0,0.2,0.9)])
            text = '['
            for i in range(len(p)-1):
                text +=  f'{p[i][0]/screen_width,p[i][1]/screen_height},'
            text += f'{p[-1][0]/screen_width,p[-1][1]/screen_height}]'
            print(text)
        was_left_last = True
    else:
        was_left_last = False
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))
    for i in range(snap):
        if i%5 == 0:
            pygame.draw.line(screen,(255,255,255),[(screen_width/snap)*i,0],[(screen_width/snap)*i,screen_height],line_width)
        else:
            pygame.draw.line(screen,(128,128,128),[(screen_width/snap)*i,0],[(screen_width/snap)*i,screen_height],line_width)
    for i in range(snap):
        if i%5 == 0:
            pygame.draw.line(screen,(255,255,255),[0,(screen_height/snap)*i],[screen_width,(screen_height/snap)*i],line_width)
        else:   
            pygame.draw.line(screen,(128,128,128),[0,(screen_height/snap)*i],[screen_width,(screen_height/snap)*i],line_width)
    if len(p) > 2: 
        if key_down(pygame.K_e):
            pygame.draw.polygon(screen,(255,255,255),p,10)
        else:
            pygame.draw.polygon(screen, (255,255,255), p)
    elif len == 2:
        pygame.draw.line(screen,(255,255,255),p[0],p[1],line_width)
    if key_press('z'):
        p.pop()
    update_pressed()
    pygame.display.update()
    fpsClock.tick(FPS)
pygame.quit()
