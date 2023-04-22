from pygame import Vector2, key
from math import floor

coyote_time = 10
buffer = 5
mini_steps = 4




class Ability:

    def __init__(self,operation_type:int,conditions:list,press_type:list,amount:int,reset:list,key:str,x:float,y:float,repeat:int):
        '''
        The class that defines a movement ability

        operation_type: 0 (multiply), 1 (add), 2 (set)
        conditions: whether you can use the ability [in air, on ground, on wall, on ceiling]
        press_type: 0 (happens every frame), 1 (every frame when key is held), 2 (once when the key is pressed)
        amount: how many times you can use the ability without it being reset
        reset: when the ability is reset [in air, on ground, on wall, on ceiling]
        key: what key is pressed to use the ability
        x: the vaule of the operation performed of vx
        y: the vaule of the operation performed of vy
        repeat: how many frames the operation will happen for
        '''
        self.operation_type = operation_type
        self.conditions = conditions
        self.press_type = press_type
        self.amount = amount
        self.reset = reset
        self.key = key
        self.x = x
        self.y = y
        self.repeat = repeat
        self.repeat_num = 0
        self.was_pressed = False
        self.amount_num = 0




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
    

    def update_player_hitbox(self):
        self.p_hit = []
        self.p_hit.append(Vector2(self.pw/2,self.ph/2))
        self.p_hit.append(Vector2(-self.pw/2,self.ph/2))
        self.p_hit.append(Vector2(self.pw/2,-self.ph/2))
        self.p_hit.append(Vector2(-self.pw/2,-self.ph/2))

    
    def update(self):
        for i in range(mini_steps):
            self.pos.x += self.vel.x/mini_steps
            if self.collide(self.pos):
                pass



    def collide(self,pos:Vector2):
        if pos.x >= self.gw:
            return True
        if pos.x < 0:
            return True
        if pos.y >= self.gh:
            return True
        if pos.y < 0:
            return True
        if self.grid[floor(pos.x),floor(pos.y)] == 1:
            return True
        
        return False
    

    def player_collide(self):
        for i in self.p_hit:
            if self.collide(self.pos+i):
                return True
        return False
