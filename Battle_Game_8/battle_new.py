import math
from math import floor
import pygame as pg
import os
from pygame import Vector2
import menu_engine
from menu_engine import Menu, Button, Slider, Text


pg.init()
# os.chdir("C:\\Users\\robin\\Documents\\Python_Project\\Battle_Game_8")
os.chdir("C:\\Users\\angela\\Documents\\Python_Project\\Battle_Game_8")
menu_engine.default_font = "Fonts/Orbitron-Medium.ttf"
game_icon = pg.image.load("play.png")
pg.display.set_icon(game_icon)
pg.display.set_caption("Battle Game!")