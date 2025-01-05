import pygame as pg
import math
import random

pg.init()

spawn_toggle = True
shoot_enemy = True
shoot_player = True
screen = pg.display.set_mode((900, 900))
f1 = pg.font.Font(None, 36)
# Создание группы пуль
bullets = pg.sprite.Group()
# Создание вржеской группы
enemies = pg.sprite.Group()
# Создание персонажа
player_group = pg.sprite.Group()



