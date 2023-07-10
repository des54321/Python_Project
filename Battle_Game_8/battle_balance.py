import math
from math import floor
import pygame as pg
import os
from pygame.math import Vector2
from random import random
import copy
import menu_engine
from menu_engine import Menu, Button, Slider, Text
import pickle


# os.chdir("C:\\Users\\robin\\Documents\\Python_Project\\Battle_Game_8")
os.chdir("C:\\Users\\angela\\Documents\\Python_Project\\Battle_Game_8")


bot_happy_dist = 50
smart_bot_avoidance = 4



def reset_stats():
    global team_stats
    team_stats = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in players:
        team_stats[team_to_num(i.team)][2] += 1


boundary_size = 1500
keyboard_barrel_rot_speed = 3
bot_target_dist = 400
respawn_immunity = 200
bot_rand = 2

players = []
bullets = []
specials = []

team_stats = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]


# Viva el fuctions, yay




def reset_players():
    global bullets, specials
    teams = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    bullets = []
    specials = []
    for n, i in enumerate(players):
        i: Player
        teams[team_to_num(i.team)][2] += 1
        i.reset()
        pos = Vector2()
        pos.from_polar((boundary_size - 100, 360 * n / len(players)))
        i.x = pos.x
        i.y = pos.y


def players_in_radius(pos, radius: float, not_included=0):
    in_radius = []
    for i in players:
        if not i.team == not_included:
            if math.dist([i.x, i.y], pos) < radius:
                in_radius.append(i)
    return in_radius


def closest_player(pos, not_included=0, is_max=False,is_rand=False,rand=0):
    distances = []
    for i in players:
        if i.team == not_included:
            distances.append(10000000)
        else:
            if is_rand:
                distances.append(math.dist([i.x, i.y], pos)+random()*rand)
            else:
                distances.append(math.dist([i.x, i.y], pos))
    if is_max:
        return players[distances.index(max(distances))]
    else:
        return players[distances.index(min(distances))]


def closest_bullet(pos, not_included=0, is_max=False,is_rand=False,rand=0):
    distances = []
    for i in bullets:
        i:Bullet
        if i.came_from.team == not_included:
            distances.append(10000000)
        else:
            if is_rand:
                distances.append(math.dist([i.x, i.y], pos)+random()*rand)
            else:
                distances.append(math.dist([i.x, i.y], pos))
    if is_max:
        return bullets[distances.index(max(distances))]
    else:
        return bullets[distances.index(min(distances))]


def fire_bullet(
    x: float,
    y: float,
    type: str,
    dir: float,
    spread: float,
    amount: int,
    player: object,
    add_vel: bool = True,
):
    global bullets
    for i in range(amount):
        bullets.append(
            Bullet(
                x, y, (dir) + ((i - (amount / 2) + 0.5) * spread), type, player, add_vel
            )
        )

        # Cool bullet stuff

        if type == rotator:
            bullets[-1].vel = Vector2(0, 0)







def collide_bullets():
    for b in bullets:
        for p in players:
            if not p.immunity > 0:
                if not b.came_from.team == p.team:
                    if math.dist([b.x, b.y], [p.x, p.y]) < (
                        p.type.size + b.bullet_type.size
                    ):
                        p.health -= b.bullet_type.damage

                        # Death message + death counter
                        if p.health <= 0 and not p.dead:
                            team_stats[team_to_num(b.came_from.team)][0] += 1
                            team_stats[team_to_num(p.team)][1] += 1
                            p.dead = True

                        if b in bullets:
                            del bullets[bullets.index(b)]
    for i in specials:
        if i.type.bullet_collide:
            for b in bullets:
                if not b.came_from.team == i.came_from.team:
                    if math.dist([b.x, b.y], [i.x, i.y]) < (
                        i.type.size + b.bullet_type.size
                    ):
                        i.collide_bullet(b)


def team_to_num(team):
    """
    Will give the number of a team given its name
    """
    if team == "red":
        return 0
    if team == "green":
        return 1
    if team == "blue":
        return 2
    if team == "yellow":
        return 3


def player_specials_update():
    for i in players:
        i.type.use_special(i)


def bullet_despawn():
    for i in bullets:
        if i.time_left <= 0:
            if i in bullets:
                # Stuff certain bullets do on despawn

                if i.bullet_type == shotgun_bomb:
                    fire_bullet(i.x, i.y, shrapnel, 0, 5, 72, i.came_from)

                del bullets[bullets.index(i)]


def player_respawn():
    for i in players:
        i.respawn()



def move_bullets():
    for i in bullets:
        i.move()


def tick_specials():
    for i in specials:
        i.tick()





def move_players():
    for i in players:
        i.move()

def damage_player(player,team,damage):
    player.health -= damage

    # Death message + death counter
    if player.health <= 0 and not player.dead:
        team_stats[team_to_num(team)][0] += 1
        team_stats[team_to_num(player.team)][1] += 1
        player.dead = True


"""
Stuff in the special class is stuff that does not really fit as a bullet or a player, it can be anything
from a turret to a sheild. If they collide with bullets or players, they need their own function to call
when that should happen. The 'tick' function for the specials will be called every frame.
"""


class SpecialGroup:
    def __init__(self, player_collide, bullet_collide, kind) -> None:
        self.bullet_collide = bullet_collide
        self.player_collide = player_collide

        if kind == "small_turret":
            self.size = 20
            self.fire_rate = 30
            self.life_time = 1000
            self.color = (50, 200, 200)
            self.max_health = 40
            self.fires = turret_bullet

        if kind == "damage_orb":
            self.speed = 7
            self.damage = 1
            self.life_time = 250
            self.radius = 250
            self.size = 40
            self.color = (80, 10, 20)
            self.damage_color = (130, 20, 80)

        if kind == "large_sheild":
            self.lenth = 150
            self.life_time = 1000
            self.width = 10
            self.color = (80, 10, 20)
            self.size = 100


class Special:
    def __init__(self, type: SpecialGroup, x, y, extra=None, extra2=None) -> None:
        self.x = x
        self.y = y
        self.type = type

        # Special inits

        if type == small_turret:
            self.health = type.max_health
            self.barrel = Vector2(0, self.type.size * 2)
            self.timer = type.fire_rate
            self.came_from = extra
            self.time_left = type.life_time
        if type == damage_orb:
            self.time_left = type.life_time
            self.came_from = extra
            new = Vector2(0, 0)
            new.from_polar((self.type.speed, extra2))
            self.vel = new

    def tick(self) -> None:
        # Runs once every frame
        global specials

        if self.type == small_turret:
            # Turret aiming
            toward = closest_player([self.x, self.y], self.came_from.team)
            toward_pos = (
                Vector2(toward.x, toward.y)
                + (toward.vel / self.type.fires.speed)
                * Vector2((toward.x - self.x), (toward.y - self.y)).length()
            )
            between = toward_pos - Vector2(self.x, self.y)
            between.scale_to_length(8)
            new = self.barrel + between
            new.scale_to_length(self.type.size * 2)
            self.barrel = new

            # Decreasing timers
            if self.timer > 0:
                self.timer -= 1

            if self.time_left > 0:
                self.time_left -= 1

            # Firing
            if self.timer <= 0:
                self.timer = self.type.fire_rate
                fire_bullet(
                    self.x + self.barrel.x,
                    self.y + self.barrel.y,
                    self.type.fires,
                    Vector2(0, 0).angle_to(self.barrel),
                    0,
                    1,
                    self.came_from,
                    False,
                )

            # Running out of time
            if self.time_left <= 0 or self.health <= 0:
                del specials[specials.index(self)]

        if self.type == damage_orb:
            # Move
            self.x += self.vel.x
            self.y += self.vel.y

            # Zapping!
            closest = players_in_radius(
                [self.x, self.y], self.type.radius, self.came_from.team
            )
            for i in closest:
                if not i.immunity > 0:
                    damage_player(i,self.came_from.team,self.type.damage)

            # Decreasing timers
            if self.time_left > 0:
                self.time_left -= 1

            # Running out of time
            if self.time_left <= 0:
                del specials[specials.index(self)]

    def collide_bullet(self, bullet) -> None:
        # Runs when a bullet collide with the special ( they will only collide if that special type says so)

        if self.type == small_turret:
            self.health -= bullet.bullet_type.damage
            del bullets[bullets.index(bullet)]


class BulletGroup:
    def __init__(self, image, damage, speed, size, color, homing, life_span) -> None:
        self.damage = damage
        self.speed = speed
        self.size = size
        self.color = color
        self.homing = homing
        self.life_span = life_span
        self.images = []


class Bullet:
    def __init__(self, x, y, dir, bullet_type, came_from, add_vel=True) -> None:
        self.x = x
        self.y = y
        self.vel = Vector2()
        self.vel.from_polar((bullet_type.speed, dir))
        self.bullet_type = bullet_type
        if not self.bullet_type.speed == 0:
            if add_vel:
                self.vel += came_from.vel * 0.5
        self.came_from = came_from
        self.time_left = bullet_type.life_span
        if bullet_type == mini_mine:
            self.vel.scale_to_length((1 - (random() ** 2)) * 40)

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
                toward = closest_player([self.x, self.y], self.came_from.team)
                between = Vector2((toward.x - self.x), (toward.y - self.y))
                if between.length() < 1:
                    between = Vector2(1,0)
                else:
                    between.scale_to_length(self.bullet_type.homing)
                new = self.vel + between
                new.scale_to_length(self.vel.length())
                self.vel = new
        if not self.bullet_type == rotator:
            if (
                math.dist((0, 0), (self.x, self.y))
                > boundary_size - self.bullet_type.size
            ):
                self.vel *= -1
                new = Vector2(self.x, self.y)
                new.scale_to_length(boundary_size - self.bullet_type.size)
                self.x = new.x
                self.y = new.y

        # Special Bullets Cool Stuff

        if self.bullet_type == mini_mine or self.bullet_type == mine:
            self.vel *= 0.9

        if self.bullet_type == rotator:
            self.vel.x = (self.vel.x + 5) % 360
            old = Vector2()
            old.from_polar((rotator.speed, self.vel.x))
            self.x = self.came_from.x + old.x
            self.y = self.came_from.y + old.y



class PlayerCharacter:
    def __init__(
        self,
        top_image: str,
        size: int,
        max_health: int,
        move_speed: float,
        drift: float,
        reload_time: int,
        color: tuple,
        bullet_type: BulletGroup,
        special_cooldown: int,
        amount: int,
        spread: int,
        name: str,
    ) -> None:
        """
        Top image is the file name of the image that its top is
        """
        self.size = size
        self.name = name
        self.max_health = max_health
        self.move_speed = move_speed
        self.drift = drift
        self.reload_time = reload_time
        self.color = color
        self.fires = bullet_type
        self.special_cooldown = special_cooldown
        self.amount = amount
        self.spread = spread
        self.tops = []
        all_chars.append(self)

    def init_special_use(self, player) -> None:
        player: Player
        if self == shotgun_char:
            fire_bullet(
                player.x + player.barrel.x,
                player.y + player.barrel.y,
                shotgun_bomb,
                Vector2(0, 0).angle_to(player.barrel),
                0,
                1,
                player,
            )
        if self == mine_layer:
            player.left = 18
        if self == cloner_char:
            for i, n in enumerate(players):
                n: Player
                if n.team == player.team:
                    players[i].immunity = 130
                    if not n == player:
                        players[i].cool_down = 0

        if self == speed_char:
            player.left = 12
        if self == tank_char:
            player.left = 300
        if self == spin_char:
            player.left = 12
        if self == blaster_char:
            player.left = 3
        if self == turret_layer:
            specials.append(Special(small_turret, player.x, player.y, player))
        if self == orb_char:
            specials.append(
                Special(
                    damage_orb,
                    player.x + player.barrel.x,
                    player.y + player.barrel.y,
                    player,
                    Vector2(0, 0).angle_to(player.barrel),
                )
            )

    def use_special(self, player) -> None:
        if self == mine_layer:
            if player.left > 0:
                player.left -= 1
                fire_bullet(
                    player.x,
                    player.y,
                    mini_mine,
                    player.left * 20 + (random() * 20),
                    0,
                    4,
                    player,
                )
        if self == speed_char:
            if player.left > 0:
                player.left -= 1
                fire_bullet(
                    player.x,
                    player.y,
                    speed_big_pellet,
                    Vector2(0, 0).angle_to(player.vel),
                    180,
                    2,
                    player,
                )
        if self == tank_char:
            if player.left > 0:
                player.left -= 1
                player.vel = Vector2(0, 0)
                player.timer -= 4
        if self == spin_char:
            if player.left > 0:
                if player.wait <= 0:
                    player.left -= 1
                    player.wait = 6
                    fire_bullet(
                        player.x + rotator.speed, player.y, rotator, 0, 0, 1, player
                    )
        if self == blaster_char:
            if player.left > 0:
                if player.wait <= 0:
                    player.left -= 1
                    player.wait = 10
                    fire_bullet(player.x, player.y, blaster_bolt, 0, 36, 10, player)


class Player:
    def __str__(self) -> str:
        return f"{self.x,self.y} pos, {self.vel} vel, {players.index(self)+1} number"

    def __init__(self, group: PlayerCharacter, team, x, y) -> None:
        self.team = team
        self.type = group
        self.x = x
        self.y = y
        self.health = group.max_health
        self.vel = Vector2(0, 0)
        self.barrel = Vector2(0, self.type.size * 2)
        self.timer = 0
        self.left = 0
        self.wait = 0
        self.cool_down = self.type.special_cooldown
        self.immunity = respawn_immunity // 3
        self.dead = False
        team_stats[team_to_num(team)][2] += 1

    def move(self) -> None:
        self.x += self.vel.x
        self.y += self.vel.y
        self.vel.x *= self.type.drift
        self.vel.y *= self.type.drift
        self.control_mid()

        if math.dist((0, 0), (self.x, self.y)) > boundary_size - self.type.size:
            new = Vector2(self.x, self.y)
            new.scale_to_length(boundary_size - self.type.size)
            self.x = new.x
            self.y = new.y
        if self.timer > 0:
            self.timer -= 1
        if self.cool_down > 0:
            self.cool_down -= 1
        if self.immunity > 0:
            self.immunity -= 1
        if self.wait > 0:
            self.wait -= 1
    

    def control_mid(self):
        target:Player = closest_player(Vector2(self.x, self.y), self.team,is_rand=True,rand=bot_rand)
        dist = Vector2(self.x, self.y).distance_to(Vector2(target.x, target.y))
        if len(bullets) > 0:
            near:Bullet = closest_bullet(Vector2(self.x, self.y), self.team,is_rand=True,rand=bot_rand)
            dist_bul = Vector2(self.x, self.y).distance_to(Vector2(near.x, near.y))
            if dist_bul < (near.bullet_type.size+near.bullet_type.speed) * smart_bot_avoidance and near.came_from.team != self.team:
                if near.y < self.y:
                    self.vel.y += self.type.move_speed
                if near.x < self.x:
                    self.vel.x += self.type.move_speed
                if near.y > self.y:
                    self.vel.y -= self.type.move_speed
                if near.x > self.x:
                    self.vel.x -= self.type.move_speed
            else:
                self.bot_move(dist,target)
        else:
            self.bot_move(dist,target)
        toward_pos = (
            Vector2(target.x, target.y)
            + (target.vel / max(self.type.fires.speed,15))
            * min(Vector2((target.x - self.x), (target.y - self.y)).length(),400)
        )

        dir = toward_pos - Vector2(self.x, self.y)
        self.barrel = dir
        if self.barrel.length() < 1:
            self.barrel = Vector2(self.type.size*2,0)
        self.barrel.scale_to_length(self.type.size*2)
        
        if self.immunity <= 0:
            if self.timer <= 0:
                self.timer = self.type.reload_time
                fire_bullet(
                    self.x + self.barrel.x,
                    self.y + self.barrel.y,
                    self.type.fires,
                    Vector2(0, 0).angle_to(self.barrel),
                    self.type.spread,
                    self.type.amount,
                    self,
                )
            if self.cool_down <= 0:
                self.cool_down = self.type.special_cooldown
                self.type.init_special_use(self)
    

    def bot_move(self,dist,target):
        if abs(dist - bot_target_dist) > bot_happy_dist:
            if dist > bot_target_dist:
                if target.y > self.y:
                    self.vel.y += self.type.move_speed
                if target.x > self.x:
                    self.vel.x += self.type.move_speed
                if target.y < self.y:
                    self.vel.y -= self.type.move_speed
                if target.x < self.x:
                    self.vel.x -= self.type.move_speed
            else:
                if target.y < self.y:
                    self.vel.y += self.type.move_speed
                if target.x < self.x:
                    self.vel.x += self.type.move_speed
                if target.y > self.y:
                    self.vel.y -= self.type.move_speed
                if target.x > self.x:
                    self.vel.x -= self.type.move_speed
    


    def respawn(self) -> None:
        if self.immunity <= 0:
            if self.health <= 0:
                self.dead = False
                self.x = 0
                self.y = 0
                self.health = self.type.max_health
                self.immunity = respawn_immunity

    def reset(self):
        self.health = self.type.max_health
        self.vel = Vector2(0, 0)
        self.barrel = Vector2()
        self.barrel.from_polar((self.type.size * 2, 0))
        self.timer = 0
        self.left = 0
        self.wait = 0
        self.cool_down = self.type.special_cooldown
        self.immunity = respawn_immunity // 3
        self.dead = False


# Bullet Types
blaster_bolt = BulletGroup("blaster_bolt", 7, 12, 12, (40, 200, 40), 0.35, 240)
tank_shell = BulletGroup("tank_shell", 20, 8, 15, (40, 60, 100), 0.05, 200)
spin_char_bullet = BulletGroup("spin_char_bullet", 6, 15, 20, (50, 200, 50), 1.4, 100)
shotgun_pellet = BulletGroup("shotgun_pellet", 2.5, 18, 8, (150, 150, 150), 0, 25)
mine = BulletGroup("mine", 100, 25, 40, (240, 50, 50), 0, 800)
mini_mine = BulletGroup("mini_mine", 20, 30, 25, (230, 150, 150), 0, 500)
shotgun_bomb = BulletGroup("shotgun_bomb", 75, 12, 50, (210, 240, 100), 0, 60)
shrapnel = BulletGroup("shrapnel", 30, 20, 15, (105, 120, 50), 0, 40)
speed_pellet = BulletGroup("speed_pellet", 4, 12, 6, (200, 40, 200), 0, 120)
speed_big_pellet = BulletGroup("speed_big_pellet", 10, 18, 10, (100, 20, 100), 1, 25)
rotator = BulletGroup("rotator", 35, 100, 20, (120, 200, 255), 0, 350)
cloner_bullet = BulletGroup("cloner_bullet", 3, 12, 6, (20, 20, 20), 0.2, 200)
turret_bullet = BulletGroup("turret_bullet", 3, 15, 12, (20, 128, 128), 0, 95)
small_orb = BulletGroup("small_orb", 10, 17, 18, (80, 0, 200), 0.1, 95)


# Player Characters
all_chars = []
shotgun_char = PlayerCharacter(
    "shotgun_char",
    30,
    65,
    5,
    0.4,
    60,
    (240, 240, 40),
    shotgun_pellet,
    1100,
    9,
    4,
    "Shotgun",
)
blaster_char = PlayerCharacter(
    "blaster_char",
    25,
    50,
    3,
    0.7,
    45,
    (200, 30, 30),
    blaster_bolt,
    1200,
    1,
    0,
    "Blaster",
)
tank_char = PlayerCharacter(
    "tank_char", 40, 120, 2.2, 0.65, 90, (60, 20, 200), tank_shell, 1100, 1, 0, "Tank"
)
cloner_char = PlayerCharacter(
    "cloner_char",
    20,
    25,
    2,
    0.8,
    9,
    (60, 255, 30),
    cloner_bullet,
    1300,
    1,
    0,
    "Support"
)
mine_layer = PlayerCharacter(
    "mine_layer", 40, 130, 2, 0.6, 45, (255, 128, 20), mine, 600, 1, 0, "Mines"
)
speed_char = PlayerCharacter(
    "speed_char", 20, 35, 3, 0.8, 10, (255, 100, 255), speed_pellet, 600, 2, 20, "Speed"
)
spin_char = PlayerCharacter(
    "spin_char",
    40,
    60,
    1,
    0.95,
    35,
    (230, 255, 50),
    spin_char_bullet,
    1200,
    1,
    0,
    "Spinner",
)
turret_layer = PlayerCharacter(
    "turret_layer",
    25,
    65,
    2.3,
    0.8,
    50,
    (100, 255, 255),
    turret_bullet,
    500,
    3,
    4,
    "Turrets",
)
orb_char = PlayerCharacter(
    "orb_char", 40, 45, 2.8, 0.82, 65, (100, 10, 140), small_orb, 600, 1, 0, "Orbulator"
)





# Special types
small_turret = SpecialGroup(False, True, "small_turret")
damage_orb = SpecialGroup(False, False, "damage_orb")


def game_tick():
    move_players()
    move_bullets()
    bullet_despawn()
    collide_bullets()
    tick_specials()
    player_specials_update()
    player_respawn()



chars_stats = []


for i in all_chars:
    i:PlayerCharacter
    kills = 0
    deaths = 0
    for x in all_chars:
        x:PlayerCharacter
        players = []
        players.append(Player(i,'red',0,0))
        players.append(Player(x,'green',0,0))
        players.append(Player(i,'red',0,0))
        players.append(Player(x,'green',0,0))
        reset_players()
        reset_stats()
        for n in range(15000):
            game_tick()
        print(f'{i.name} vs {x.name}: {team_stats[0][0]} and {team_stats[1][0]} kills')
        kills += team_stats[0][0]
        deaths += team_stats[1][0]
    chars_stats.append(f'{i.name} killed {kills} times, died {deaths} times, KDR = {round(kills/deaths,2)}')


for i in chars_stats:
    print(i)
    




    

