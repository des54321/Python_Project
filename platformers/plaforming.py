import pygame as pg
from pygame import Vector2
from random import random, randint
from math import floor

coyote_time = 10
buffer = 5
mini_steps = 4



def key_down(key : pg.key) -> bool:
    return pg.key.get_pressed()[key]



class AbilAmount:

    def __init__(self,amount) -> None:
        self.amount = amount
        self.amount_num = 0
        self.resolve()
    

    def use(self):
        self.amount_num -= 1
        self.amount_num = max(self.amount_num,0)
    

    def reset(self):
        self.amount_num = self.amount
    

    def resolve(self):
        self.real = self.amount_num



class Ability:

    def __init__(self,operation_type:int,conditions:list,press_type:int,amount:AbilAmount,reset:list,key,x:float,y:float,repeat:int = 0,affect:list = [True,True],at_end:any = None,at_start:any = None):
        '''
        The class that defines a movement ability

        operation_type: 0 (multiply), 1 (add), 2 (set)
        conditions: whether you can use the ability [in air, on ground, on wall, on ceiling], or 'all'
        press_type: 0 (happens every frame), 1 (every frame when key is held), 2 (once when the key is pressed)
        amount: how many times you can use the ability without it being reset
        reset: when the ability is reset [in air, on ground, on wall, on ceiling], or 'all'
        key: what key is pressed to use the ability
        x: the vaule of the operation performed of vx
        y: the vaule of the operation performed of vy
        repeat: how many frames the operation will happen for
        affect: if it affects [x,y]
        at_end: what ability should ativate when the ability ends
        at_start: what ability should ativate when the ability starts
        '''
        self.operation_type = operation_type

        if conditions == 'all':
            self.conditions = [True,True,True,True]
        else:
            self.conditions = conditions
        
        self.press_type = press_type

        if type(amount) == int:
            self.amount_var = AbilAmount(amount)
        else:
            self.amount_var = amount
        
        if reset == 'all':
            self.reset = [True,True,True,True]
        else:
            self.reset = reset
        
        self.key = key
        self.x = x
        self.y = y
        self.repeat = repeat
        self.repeat_num = 0
        self.was_pressed = False
        self.affect = affect
        self.at_end = at_end
        self.at_start = at_start




class Player:
    def __init__(self,start_pos:Vector2,grid:list,abilities:list,player_w:float,player_h:float,vel:Vector2 = Vector2(0,0)) -> None:
        self.pos = start_pos
        self.grid = grid
        self.gw = len(grid)
        self.gh = len(grid[0])
        self.abilities = abilities
        self.vel = vel
        self.pw = player_w
        self.ph = player_h
        self.update_player_hitbox()
        self.coyote_time = [0,0,0,0]
        self.coyote_touch = [False,False,False,False]
        self.real_touch = [False,False,False,False]
    

    def update_player_hitbox(self):
        self.p_hit = []
        self.p_hit.append(Vector2(self.pw/2,self.ph/2))
        self.p_hit.append(Vector2(-self.pw/2,self.ph/2))
        self.p_hit.append(Vector2(self.pw/2,-self.ph/2))
        self.p_hit.append(Vector2(-self.pw/2,-self.ph/2))

    
    def update(self):
        self.real_touch = self.get_touching()
        for i in range(4):
            self.coyote_time[i] = max(0,self.coyote_time[i]-1)
            if self.real_touch[i]:
                self.coyote_time[i] = coyote_time
            if self.coyote_time[i] == 0:
                self.coyote_touch[i] = False
            else:
                self.coyote_touch[i] = True


        for i in self.abilities:
            self.ability_update(i)
        
        for i in self.abilities:
            i:Ability
            i.amount_var.resolve()

        self.move()
    

    def ability_update(self,abil:Ability):
        if abil.repeat_num > 0:
            self.use_abil(abil)
            abil.repeat_num = max(abil.repeat_num-1,0)

            if abil.repeat_num == 0:
                if not abil.at_end == None:
                    self.use_abil(abil.at_end)
                    abil.at_end.repeat_num = abil.at_end.repeat
            return 0

        meets_condition = False
        for i in range(4):
            if abil.reset[i] and self.real_touch[i]:
                abil.amount_var.reset()
            if abil.conditions[i] and self.coyote_touch[i]:
                meets_condition = True
        


        if abil.amount_var.real > 0 and meets_condition:
            attempt = False
            if abil.press_type == 0:
                attempt = True
            
            if abil.press_type == 1:
                key_pressed = True
                if type(abil.key) == list:
                    for i in abil.key:
                        key_pressed = key_down(i) and key_pressed
                else:
                    key_pressed = key_down(abil.key)

                if key_pressed:
                    attempt = True
            
            if abil.press_type == 2:
                key_pressed = True
                if type(abil.key) == list:
                    for i in abil.key:
                        key_pressed = key_down(i) and key_pressed
                else:
                    key_pressed = key_down(abil.key)

                if key_pressed:
                    if not abil.was_pressed:
                        attempt = True
                    abil.was_pressed = True
                else:
                    abil.was_pressed = False

            
            if attempt:
                self.use_abil(abil)
                abil.amount_var.use()
                if not abil.at_start == None:
                    self.use_abil(abil.at_start)
                    abil.at_start.repeat_num = abil.at_start.repeat
                abil.repeat_num = abil.repeat
    



    def use_abil(self,abil:Ability):
        if abil.operation_type == 0:
            self.vel.x *= abil.x
            self.vel.y *= abil.y
        if abil.operation_type == 1:
            self.vel.x += abil.x
            self.vel.y += abil.y
        if abil.operation_type == 2:
            if abil.affect[0]:
                self.vel.x = abil.x
            if abil.affect[1]:
                self.vel.y = abil.y


    def get_touching(self):
        final = [False,False,False,False]
        self.pos.y += 0.03125
        if self.player_collide():
            final[1] = True
        self.pos.y -= 0.0625
        if self.player_collide():
            final[3] = True
        self.pos.y += 0.03125
        self.pos.x += 0.03125
        if self.player_collide():
            final[2] = True
        self.pos.x -= 0.0625
        if self.player_collide():
            final[2] = True
        self.pos.x += 0.03125
        if not(final[1] or final[2] or final[3]):
            final[0] = True
        return final


    def move(self):
        for _ in range(mini_steps):
            self.pos.x += self.vel.x/mini_steps
            if self.player_collide():
                if self.vel.x < 0:
                    self.pos.x += 1-((self.pos.x-self.pw/2) - floor(self.pos.x-self.pw/2))
                    self.pos.x += 0.001
                else:
                    self.pos.x -= (self.pos.x+self.pw/2) - floor(self.pos.x+self.pw/2)
                    self.pos.x -= 0.001
                self.vel.x = 0
            
            self.pos.y += self.vel.y/mini_steps
            if self.player_collide():
                if self.vel.y< 0:
                    self.pos.y += 1-((self.pos.y-self.ph/2) - floor(self.pos.y-self.ph/2))
                    self.pos.y += 0.001
                else:
                    self.pos.y -= (self.pos.y+self.ph/2) - floor(self.pos.y+self.ph/2)
                    self.pos.y -= 0.001
                self.vel.y = 0

    def collide(self,pos:Vector2):
        if pos.x >= self.gw:
            return True
        if pos.x < 0:
            return True
        if pos.y >= self.gh:
            return True
        if pos.y < 0:
            return True
        if self.grid[floor(pos.x)][floor(pos.y)] == 1:
            return True
        
        return False
    

    def player_collide(self):
        for i in self.p_hit:
            if self.collide(self.pos+i):
                return True
        return False
