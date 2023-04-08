import math
import pygame as pg
from pygame.math import Vector2
from random import random
import os


pg.init()


backdrop = (240,250,230)
aim_type = 2
cam_x = 0
cam_y = 0
zoom = 2
respawn_immunity = 200
screen_width = 800
screen_height = 600
zoom_radius = 300
grid_spacing = 100
boundary_size = 1500


screen = pg.display.set_mode((screen_width,screen_height))


bullets = []
players = []
specials = []


# Teams = (Name, Deaths, Kills, Players)
teams = [['Bannanas',0,0,[0]],['Apples',0,0,[1,2]]]


#up,right,down,left,fire,aim1,aim2, special
controls = ((pg.K_w,pg.K_d,pg.K_s,pg.K_a,pg.K_SPACE,pg.K_n,pg.K_m,pg.K_f),(pg.K_UP,pg.K_RIGHT,pg.K_DOWN,pg.K_LEFT,pg.K_COMMA,pg.K_v,pg.K_b,pg.K_RSHIFT),(pg.K_i,pg.K_l,pg.K_k,pg.K_j,pg.K_LEFTBRACKET,pg.K_o,pg.K_p,pg.K_u))


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


print(pg.joystick.get_count())
buttons_pressed = []
controllers = []
for i in range(pg.joystick.get_count()):
    controllers.append(pg.joystick.Joystick(i))
    buttons_pressed.append([False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,[0,0],[0,0],[False,False]])

for controller in controllers:
    controller.init()
  

def players_in_radius(pos,radius,not_included = 0):
    in_radius = []
    for i in players:
        if not i.team == not_included:
            if math.dist([i.x,i.y],pos) < radius:
                in_radius.append(i)
    return in_radius



def closest_player(pos,not_included = 0,is_max = False):
    distances = []
    for i in players:
        if i.team == not_included:
            distances.append(10000000)
        else:
            distances.append(math.dist([i.x,i.y],pos))
    if is_max:
        return players[distances.index(max(distances))]
    else:
        return players[distances.index(min(distances))]


def fire_bullet(x,y,type,dir,spread,amount,player,add_vel = True):
    global bullets
    for i in range(amount):
        bullets.append(Bullet(x,y,(dir)+((i-(amount/2)+0.5)*spread),type,player,add_vel))


        #Cool bullet stuff


        if type == rotator:
            bullets[-1].vel = Vector2(0,0)


def draw_bullets():
    for i in bullets:
        i.draw()


def draw_grid():
    for i in range(math.ceil((screen_width)/grid_spacing)):
        x = (grid_spacing-((cam_x/zoom) % grid_spacing))+(i*grid_spacing)
        pg.draw.line(screen,[i * 0.4 for i in backdrop],[x,0],[x,screen_height],5)
    for i in range(math.ceil((screen_height)/grid_spacing)):
        y = ((cam_y/zoom) % grid_spacing)+(i*grid_spacing)
        pg.draw.line(screen,[i * 0.4 for i in backdrop],[0,y],[screen_width,y],5)


def collide_bullets():
    for b in bullets:
        for p in players:
            if not p.immunity > 0:
                if not b.came_from.team == p.team:
                    if math.dist([b.x,b.y],[p.x,p.y]) < (p.type.size+b.bullet_type.size):
                        p.health -= b.bullet_type.damage
                        if b in bullets:
                            del bullets[bullets.index(b)]
    for i in specials:
        if i.type.bullet_collide:
            for b in bullets:
                if not b.came_from.team == i.came_from.team:
                    if math.dist([b.x,b.y],[i.x,i.y]) < (i.type.size+b.bullet_type.size):
                        i.collide_bullet(b)
                    

def bullet_despawn():
    for i in bullets:
        if i.time_left <= 0:
            if i in bullets:


                #Stuff certain bullets do on despawn


                if i.bullet_type == shotgun_bomb:
                    fire_bullet(i.x,i.y,shrapnel,0,5,72,i.came_from)


                del bullets[bullets.index(i)]


def player_respawn():
    for i in players:
        i.respawn()


def adjust_camera():
    global cam_x
    global cam_y
    global zoom
    x = []
    for i in players:
        x.append(i.x)
    cam_x += ((min(x)+max(x))/2-cam_x)*0.05
    y = []
    for i in players:
        y.append(i.y)
    cam_y += ((min(y)+max(y))/2-cam_y)*0.05
    farthest_player = closest_player((cam_x,cam_y),0,True)
    most_dist = math.dist((farthest_player.x,farthest_player.y),(cam_x,cam_y))
    zoom += ((((math.ceil(most_dist/zoom_radius)*zoom_radius)/screen_height)*2)-zoom)*0.05


def move_bullets():
    for i in bullets:
        i.move()


def tick_specials():
    for i in specials:
        i.tick()


def draw_specials():
    for i in specials:
        i.draw()


def draw_players():
    for i in players:
        i.draw()


def move_players():
    for i in players:
        i.move()


def key_down(key):
    return pg.key.get_pressed()[key]


def draw_circle(pos,size,color,outline = 0):
    pg.draw.circle(screen,color,[(pos[0]-cam_x)/zoom+(screen_width/2),screen_height-((pos[1]-cam_y)/zoom+(screen_height/2))],round(size/zoom),outline)


def draw_line(pos1,pos2,size,color):
    pg.draw.line(screen,color,[(pos1[0]-cam_x)/zoom+(screen_width/2),screen_height-((pos1[1]-cam_y)/zoom+(screen_height/2))],[(pos2[0]-cam_x)/zoom+(screen_width/2),screen_height-((pos2[1]-cam_y)/zoom+(screen_height/2))],round(size/zoom))


'''
Stuff in the special class is stuff that does not really fit as a bullet or a player, it can be anything
from a turret to a sheild. If they collide with bullets or players, they need their own function to call
when that should happen. The 'tick' function for the specials will be called every frame.
'''


class SpecialGroup:
    def __init__(self,player_collide,bullet_collide,kind) -> None:
        self.bullet_collide = bullet_collide
        self.player_collide = player_collide

        if kind == 'small_turret':
            self.size = 20
            self.fire_rate = 30
            self.life_time = 1000
            self.color = (50,200,200)
            self.max_health = 40
            self.fires = turret_shot

        if kind == 'damage_orb':
            self.speed = 3
            self.damage = 0.8
            self.life_time = 1000
            self.radius = 170
            self.size = 35
            self.color = (80,10,20)
            self.damage_color = (130,20,80)
        


class Special:
    def __init__(self,type,x,y,extra = None,extra2 = None) -> None:
        self.x =x
        self.y = y
        self.type = type
    
        #Special inits

        if type == small_turret:
            self.health = type.max_health
            self.barrel = Vector2(0,self.type.size*2)
            self.timer = type.fire_rate
            self.came_from = extra
            self.time_left = type.life_time
        if type == damage_orb:
            self.time_left = type.life_time
            self.came_from = extra
            new = Vector2(0,0)
            new.from_polar((self.type.speed,extra2))
            self.vel = new
    
    def tick(self) -> None:
        #Runs once every frame
        global specials

        if self.type == small_turret:

            #Turret aiming
            toward = closest_player([self.x,self.y],self.came_from.team)
            between = Vector2((toward.x-self.x),(toward.y-self.y))
            between.scale_to_length(2)
            new = self.barrel + between
            new.scale_to_length(self.type.size*2)
            self.barrel = new

            #Decreasing timers
            if self.timer > 0:
                self.timer -= 1
            
            if self.time_left > 0:
                self.time_left -= 1
            
            #Firing
            if self.timer <= 0:
                self.timer = self.type.fire_rate
                fire_bullet(self.x+self.barrel.x,self.y+self.barrel.y,self.type.fires,Vector2(0,0).angle_to(self.barrel),0,1,self.came_from,False)
            
            #Running out of time
            if self.time_left <= 0 or self.health <= 0:
                del specials[specials.index(self)]
        
        if self.type == damage_orb:
            #Move
            self.x += self.vel.x
            self.y += self.vel.y

            #Zapping!
            closest = players_in_radius([self.x,self.y],self.type.radius,self.came_from.team)
            for i in closest:
                if not i.immunity > 0:
                    i.health -= self.type.damage
                    draw_line([i.x,i.y],[self.x,self.y],self.type.size//3,self.type.damage_color)

            #Decreasing timers
            if self.time_left > 0:
                self.time_left -= 1
            
            #Running out of time
            if self.time_left <= 0:
                del specials[specials.index(self)]

    def draw(self) -> None:
        #Runs every frame, but only the way that specials are drawn should go here, all the rest goes in 'tick'

        if self.type == small_turret:
            draw_circle([self.x,self.y],self.type.size,[i * (self.health/self.type.max_health) for i in self.type.color])
            draw_line([self.x,self.y],[self.x+self.barrel.x,self.y+self.barrel.y],self.type.size//3,[i * (self.health/self.type.max_health) for i in self.type.color])
            draw_circle([self.x+self.barrel.x,self.y+self.barrel.y],self.type.size//6,[i * (self.health/self.type.max_health) for i in self.type.color])

        if self.type == damage_orb:
            draw_circle([self.x,self.y],self.type.size,self.type.color)
            #draw_circle([self.x,self.y],self.type.radius,self.type.damage_color,self.type.size//2)
    def collide_bullet(self,bullet) -> None:
        #Runs when a bullet collide with the special ( they will only collide if that special type says so)

        if self.type == small_turret:

            self.health -= bullet.bullet_type.damage
            del bullets[bullets.index(bullet)]



            

class BulletGroup:
    def __init__(self,damage,speed,size,color,homing,life_span) -> None:
        self.damage = damage
        self.speed = speed
        self.size = size
        self.color = color
        self.homing = homing
        self.life_span = life_span


class Bullet:
    def __init__(self,x,y,dir,bullet_type,came_from,add_vel = True) -> None:
        self.x = x
        self.y = y
        self.vel = Vector2()
        self.vel.from_polar((bullet_type.speed,dir))
        self.bullet_type = bullet_type
        if not self.bullet_type.speed == 0:
            if add_vel:
                self.vel += came_from.vel*0.5
        self.came_from = came_from
        self.time_left = bullet_type.life_span
        if bullet_type == mini_mine:
            self.vel.scale_to_length((1-(random()**2))*40)
    def move(self) -> None:
        if self.bullet_type == mini_mine:
            self.x += round(self.vel.x)
            self.y += round(self.vel.y)
        else:
            self.x += self.vel.x
            self.y += self.vel.y
        self.time_left -= 1
        if not self.bullet_type.homing == 0:
            if not len(players) == 1:
                toward = closest_player([self.x,self.y],self.came_from.team)
                between = Vector2((toward.x-self.x),(toward.y-self.y))
                between.scale_to_length(self.bullet_type.homing)
                new = self.vel + between
                new.scale_to_length(self.vel.length())
                self.vel = new
        if not self.bullet_type == rotator:
            if math.dist((0,0),(self.x,self.y)) > boundary_size-self.bullet_type.size:
                self.vel *= -1
                new = Vector2(self.x,self.y)
                new.scale_to_length(boundary_size-self.bullet_type.size)
                self.x = new.x
                self.y = new.y


        #Special Bullets Cool Stuff


        if self.bullet_type == mini_mine or self.bullet_type == mine:
            self.vel *= 0.9

        
        if self.bullet_type == rotator:
            self.vel.x = (self.vel.x+5)%360
            old = Vector2()
            old.from_polar((rotator.speed,self.vel.x))
            self.x = self.came_from.x + old.x
            self.y = self.came_from.y + old.y
    def draw(self) -> None:

        if self.bullet_type == mine:
            if self.time_left > 400:
                draw_circle([self.x,self.y],self.bullet_type.size,self.bullet_type.color)
        else:
            draw_circle([self.x,self.y],self.bullet_type.size,self.bullet_type.color)


class Group:
    def __init__(self,size,max_health,move_speed,drift,reload_time,color,bullet_type,special_cooldown,amount,spread) -> None:
        self.size = size
        self.max_health = max_health
        self.move_speed = move_speed
        self.drift = drift
        self.reload_time = reload_time
        self.color = color
        self.fires = bullet_type
        self.special_cooldown = special_cooldown
        self.amount = amount
        self.spread = spread
    def use_special(self,player) -> None:
        if self == shotgun:
            fire_bullet(player.x+player.barrel.x,player.y+player.barrel.y,shotgun_bomb,Vector2(0,0).angle_to(player.barrel),0,1,player)
        if self == mine_layer:
            dir = 0
            for i in range(36):
                fire_bullet(player.x,player.y,mini_mine,dir+(random()*10),0,5,player)
                dir += 10
                game_tick()
        if self == destroyer:
            players.append(Player(destroyer_clone,player.team,player.x + 50,player.y,player.movement))
            players[-1].barrel = Vector2(player.barrel.x,player.barrel.y)
        if self == flash:
            for i in range(12):
                if player.movement[0] == 'controller':
                    player.vel.x += 4 * buttons_pressed[player.movement[1]][15][0]
                    player.vel.y -= 4 * buttons_pressed[player.movement[1]][15][1]
                elif player.movement[0] == 'keyboard':
                    if key_down(controls[player.movement[1]][0]):
                        player.vel.y += 4
                    if key_down(controls[player.movement[1]][1]):
                        player.vel.x += 4
                    if key_down(controls[player.movement[1]][2]):
                        player.vel.y -= 4
                    if key_down(controls[player.movement[1]][3]):
                        player.vel.y -= 4
                fire_bullet(player.x,player.y,big_pellet,Vector2(0,0).angle_to(player.vel),180,2,player)
                game_tick()
        if self == tank:
            for i in range(300):
                player.vel = Vector2(0,0)
                player.timer -=4
                game_tick()
        if self == spinner:
            for i in range(12):
                fire_bullet(player.x+rotator.speed,player.y,rotator,0,0,1,player)
                for x in range(6):
                    game_tick()
        if self == average_char:
            for i in range(3):
                fire_bullet(player.x,player.y,normal_bullet,0,36,10,player)
                for x in range(10):
                    game_tick()
        if self == turret_layer:
            specials.append(Special(small_turret,player.x,player.y,player))
        if self == orbulator:
            specials.append(Special(damage_orb,player.x+player.barrel.x,player.y+player.barrel.y,player,Vector2(0,0).angle_to(player.barrel)))


class Player:
    def __str__(self) -> str:
        return f'{self.x,self.y} pos, {self.vel} vel, {players.index(self)+1} number'
    def __init__(self,group,team,x,y,control_scheme) -> None:
        self.team = team
        self.type = group
        self.x = x
        self.y = y
        self.health = group.max_health
        self.movement = control_scheme
        self.vel = Vector2(0,0)
        self.barrel = Vector2()
        self.barrel.from_polar((self.type.size*2,0))
        self.timer = 0
        #self.cool_down = self.type.special_cooldown
        self.cool_down = 0
        self.immunity = respawn_immunity//3
    def move(self) -> None:
        self.x += self.vel.x
        self.y += self.vel.y
        self.vel.x *= self.type.drift
        self.vel.y *= self.type.drift
        if self.movement[0] == 'keyboard':
            if key_down(controls[self.movement[1]][0]):
                self.vel.y += self.type.move_speed
            if key_down(controls[self.movement[1]][1]):
                self.vel.x += self.type.move_speed
            if key_down(controls[self.movement[1]][2]):
                self.vel.y -= self.type.move_speed
            if key_down(controls[self.movement[1]][3]):
                self.vel.x -= self.type.move_speed
            if self.immunity <= 0:
                if key_down(controls[self.movement[1]][4]):
                    if self.timer <= 0:
                        self.timer = self.type.reload_time
                        fire_bullet(self.x+self.barrel.x,self.y+self.barrel.y,self.type.fires,Vector2(0,0).angle_to(self.barrel),self.type.spread,self.type.amount,self)
                if key_down(controls[self.movement[1]][5]):
                    self.barrel.rotate_ip(5)
                if key_down(controls[self.movement[1]][6]):
                    self.barrel.rotate_ip(-5)
                if key_down(controls[self.movement[1]][7]):
                    if self.cool_down <= 0:
                        self.cool_down = self.type.special_cooldown
                        self.type.use_special(self)
        elif self.movement[0] == 'controller':
            if self.immunity <= 0:
                if buttons_pressed[self.movement[1]][17][1]:
                    if self.timer <= 0:
                        self.timer = self.type.reload_time
                        fire_bullet(self.x+self.barrel.x,self.y+self.barrel.y,self.type.fires,Vector2(0,0).angle_to(self.barrel),self.type.spread,self.type.amount,self)
                if aim_type == 1:
                    if buttons_pressed[self.movement[1]][16][0] == 0 and  buttons_pressed[self.movement[1]][16][1] == 0:
                        self.barrel = Vector2(0,self.type.size*2)
                    else:
                        new = Vector2(buttons_pressed[self.movement[1]][16][0],-buttons_pressed[self.movement[1]][16][1])
                        new.scale_to_length(self.type.size*2)
                        self.barrel  = new
                else:
                    self.barrel.rotate_ip(buttons_pressed[self.movement[1]][16][0]*-8)
                if buttons_pressed[self.movement[1]][17][0]:
                    if self.cool_down <= 0:
                        self.cool_down = self.type.special_cooldown
                        self.type.use_special(self)
            self.vel.x += self.type.move_speed * buttons_pressed[self.movement[1]][15][0]
            self.vel.y -= self.type.move_speed * buttons_pressed[self.movement[1]][15][1]
        if math.dist((0,0),(self.x,self.y)) > boundary_size-self.type.size:
            new = Vector2(self.x,self.y)
            new.scale_to_length(boundary_size-self.type.size)
            self.x = new.x
            self.y = new.y
        if self.timer > 0:
            self.timer -= 1
        if self.cool_down > 0:
            self.cool_down -= 1
        if self.immunity > 0:
            self.immunity -= 1
    def draw(self) -> None:
        if self.health > 0:
            if self.immunity <= 0:
                draw_circle([self.x,self.y],self.type.size,[i * (self.health/self.type.max_health) for i in self.type.color])
                draw_line([self.x,self.y],[self.x+self.barrel.x,self.y+self.barrel.y],self.type.size//3,[i * (self.health/self.type.max_health) for i in self.type.color])
                draw_circle([self.x+self.barrel.x,self.y+self.barrel.y],self.type.size//6,[i * (self.health/self.type.max_health) for i in self.type.color])
            else:
                draw_circle([self.x,self.y],self.type.size,(255,255,255))
                draw_line([self.x,self.y],[self.x+self.barrel.x,self.y+self.barrel.y],self.type.size//3,(255,255,255))
                draw_circle([self.x+self.barrel.x,self.y+self.barrel.y],self.type.size//6,(255,255,255))
            if self.cool_down <= 0:
                draw_circle([self.x,self.y],self.type.size/2,[i * ((self.health/self.type.max_health)*0.5) for i in self.type.color])
    def respawn(self) -> None:
        if self.immunity <= 0:
            if self.health  <= 0:
                self.x = cam_x
                self.y = cam_y
                self.health = self.type.max_health
                self.immunity = respawn_immunity



#Bullet Types
normal_bullet = BulletGroup(10,10,12,(40,200,40),0.4,240)
large_bullet = BulletGroup(30,12,20,(40,60,100),0.1,300)
homing_bullet = BulletGroup(12,20,20,(50,200,50),1.8,100)
bullet_spread = BulletGroup(4,10,8,(150,150,150),0,180)
mine = BulletGroup(100,10,35,(240,50,50),0,500)
mini_mine = BulletGroup(20,30,20,(230,150,150),0,500)
shotgun_bomb = BulletGroup(75,7,50,(210,240,100),0,120)
shrapnel = BulletGroup(10,12,15,(105,120,50),0,50)
pellet = BulletGroup(3,12,6,(200,40,200),0,120)
big_pellet = BulletGroup(10,15,10,(100,20,100),1,25)
rotator = BulletGroup(40,100,20,(120,200,255),0,450)
destroyer_shot = BulletGroup(3,15,6,(20,20,20),0.3,200)
turret_shot = BulletGroup(4,18,10,(20,128,128),0,100)
purple_small_orb = BulletGroup(10,9,20,(80,0,200),1,300)


#Player Characters
shotgun = Group(30,60,6,0.4,50,(240,240,40),bullet_spread,1200,10,4)
average_char = Group(25,50,3,0.7,30,(200,30,30),normal_bullet,1200,1,0)
tank = Group(40,150,4,0.7,80,(60,20,200),large_bullet,1200,1,0)
destroyer = Group(20,10,3,0.8,6,(60,255,30),destroyer_shot,1200,1,0)
destroyer_clone = Group(20,10,3,0.8,6,(60,255,30),destroyer_shot,1200,1,0)
mine_layer = Group(40,100,2,0.6,100,(255,128,20),mine,400,1,0)
flash = Group(20,35,3,0.8,10,(255,100,255),pellet,600,3,160)
spinner = Group(40,55,1,0.95,40,(230,255,50),homing_bullet,1200,1,0)
turret_layer = Group(25,75,2,0.8,50,(100,255,255),turret_shot,600,3,5)
orbulator = Group(40,80,3,0.8,100,(100,10,140),purple_small_orb,150,1,0)


players.append(Player(shotgun,'Bannanas',0,0,['keyboard',0]))
players.append(Player(orbulator,'Apples',0,50,['keyboard',1]))
#players.append(Player(average_char,'Apples',50,50,2))





#Special types
small_turret = SpecialGroup(False,True,'small_turret')
damage_orb = SpecialGroup(False,False,'damage_orb')




def game_tick():
    global running
    for event in pg.event.get():
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
    screen.fill((20,5,13))
    draw_circle((0,0),boundary_size,backdrop)
    #draw_grid()
    adjust_camera()
    move_players()
    move_bullets()
    bullet_despawn()
    collide_bullets()
    tick_specials()
    draw_bullets()
    player_respawn()
    draw_players()
    draw_specials()
    pg.display.update()
    fps_clock.tick(fps)



fps = 60
fps_clock = pg.time.Clock()
running = True
while running:
    game_tick()
pg.quit()