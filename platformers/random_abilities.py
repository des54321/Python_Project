from plaforming import Ability
from random import random, randint
import pygame as pg

ran_keys = [pg.K_SPACE,pg.K_UP,pg.K_LEFT,pg.K_RIGHT,pg.K_DOWN,pg.K_0,pg.K_LSHIFT]
ran_keys_words = ['space','up','left','right','down','0','shift']




def randrange(min,max):
    return min + random()*(max-min)    


def ranbool():
    return bool(round(random()))


def ranbools(num):
    return [ranbool() for i in range(num)]


def random_abil(show = False):
    operation = randint(0,2)
    if show:
        print(f'operation {operation}')
    if operation == 2:
        x = randrange(-0.1,0.1)
        y = randrange(-0.1,0.1)
    elif operation == 1:
        x = randrange(-0.08,0.08)
        y = randrange(-0.06,0.06)
    elif operation == 0:
        x = randrange(0.8,1.1)
        y = randrange(0.8,1.1)
    if show:
        print(f'[x,y] {[x,y]}')
    press_type = randint(0,2)
    if show:
        print(f'press_type {press_type}')
    if press_type == 0:
        amount = 1
        reset = 'all'
        key = None
        repeat = 0
    elif press_type == 1:
        amount = randint(10,50)
        reset = ranbools(4)
        key = ran_keys[randint(0,len(ran_keys)-1)]
        repeat = randint(0,3)
    elif press_type == 2:
        amount = randint(1,4)
        reset = ranbools(4)
        key = ran_keys[randint(0,len(ran_keys)-1)]
        repeat = randint(0,60)
    if show:
        print(f'amount {amount}')
        print(f'reset {reset}')
        if key != None:
            print(f'key {ran_keys_words[ran_keys.index(key)]}')
        else:
            print(f'key is None')
        print(f'repeat {repeat}')
    affect = ranbools(2)
    condition = ranbools(4)
    if show:
        print(f'affect {affect}')
        print(f'condition {condition}')


    return Ability(operation,condition,press_type,amount,reset,key,x,y,repeat,affect)
