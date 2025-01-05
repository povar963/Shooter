import pygame as pg
import math
import random
from settings import *

pg.init()
bullets = pg.sprite.Group()
enemies = pg.sprite.Group()
player_group = pg.sprite.Group()


class Enemy(pg.sprite.Sprite):
    img = pg.image.load("./1.png")

    def __init__(self, *groups: list, player):
        super().__init__(*groups)
        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.x = -self.rect.width
        self.rect.y = -self.rect.height
        self.player = player
        self.is_alive = False

    def create(self):
        x = random.randint(70, screen.get_width() - 70)
        y = random.randint(70, screen.get_height() - 70)
        self.rect.x = x
        self.rect.y = y
        self.counter = 100
        self.is_alive = True

        if pg.sprite.collide_mask(self, self.player):
            self.kill()

    def shoot(self):
        x = self.rect.center[0]
        y = self.rect.center[1]
        BulletE([bullets], x=x, y=y, player=self.player)

    def watch(self):
        x = self.rect.center[0]
        y = self.rect.center[1]
        mouse_x, mouse_y = self.player.rect.center
        rel_x, rel_y = mouse_x - x, mouse_y - y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pg.transform.rotate(self.img, int(angle))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        if self.is_alive:
            self.watch()
            if self.player.alive():
                if shoot_enemy:
                    if self.counter <= 0:
                        self.shoot()
                        self.counter = 100
                    elif self.counter > 0:
                        self.counter -= 1
            else:
                self.kill()


class BulletE(pg.sprite.Sprite):
    img = pg.image.load("./Bullet.png")

    def __init__(self, *groups: list, x, y, player):
        super().__init__(*groups)
        mouse_x, mouse_y = player.rect.center
        rel_x, rel_y = mouse_x - x, mouse_y - y
        self.angle = math.atan2(rel_y, rel_x)
        self.speed = 20

        self.xm = self.speed * math.cos(self.angle)
        self.ym = self.speed * math.sin(self.angle)

        self.image = pg.transform.rotate(self.img, -math.degrees(self.angle))
        self.rect = self.image.get_rect(center=(x, y))

        self.player = player

    def update(self):
        self.rect.x += self.xm
        self.rect.y += self.ym
        if not (-2000 < self.rect.x < 2000 and -2000 < self.rect.y < 2000):
            self.kill()
        if pg.sprite.collide_mask(self, self.player):
            if self.player.health == 1:
                self.player.health = 0
                self.player.kill()
            else:
                self.player.health -= 1
            self.kill()


class BulletF(pg.sprite.Sprite):
    img = pg.image.load("./Bullet.png")

    def __init__(self, *groups: list, x, y):
        super().__init__(*groups)
        mouse_x, mouse_y = pg.mouse.get_pos()
        rel_x, rel_y = mouse_x - x, mouse_y - y
        self.angle = math.atan2(rel_y, rel_x)
        self.speed = 20

        self.xm = self.speed * math.cos(self.angle)
        self.ym = self.speed * math.sin(self.angle)

        self.image = pg.transform.rotate(self.img, -math.degrees(self.angle))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.x += self.xm
        self.rect.y += self.ym
        if not (-2000 < self.rect.x < 2000 and -2000 < self.rect.y < 2000):
            self.kill()
        for enemy in enemies:
            if pg.sprite.collide_mask(self, enemy):
                enemy.kill()
                self.kill()


class Player(pg.sprite.Sprite):
    img = pg.image.load("./gg.png")
    f1 = pg.font.Font(None, 36)

    def __init__(self, *groups: list):
        super().__init__(*groups)
        self.health = 3
        self.image = self.img
        self.rect = self.image.get_rect()
        self.speed = 5
        self.counter = 0
        self.def_counter = 100
        self.rect.x = screen.get_width() / 2 - self.rect.width
        self.rect.y = screen.get_height() / 2 - self.rect.height

    def watch(self):
        x = self.rect.center[0]
        y = self.rect.center[1]
        mouse_x, mouse_y = pg.mouse.get_pos()
        rel_x, rel_y = mouse_x - x, mouse_y - y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pg.transform.rotate(self.img, int(angle))
        self.rect = self.image.get_rect(center=(x, y))

    def heath_bar(self):
        fx = self.rect.center[0] - 60
        lx = self.rect.center[0] + 60
        fy = self.rect.center[1] - 100
        pg.draw.line(screen, "DarkRed", (fx, fy), (lx, fy), 10)
        fx = self.rect.center[0] - 58
        lx = fx + (116 * (self.health / 3))
        pg.draw.line(screen, "red", (fx, fy), (lx, fy), 6)
        fx = fx - 20
        lx = fx + 10
        if self.counter == 0:
            pg.draw.line(screen, "green", (fx, fy), (lx, fy), 10)
        else:
            pg.draw.line(screen, "red", (fx, fy), (lx, fy), 10)
        text1 = f1.render(f"hp:{self.health} cd:{self.counter}", 1, (180, 0, 0))
        screen.blit(text1, (10, screen.get_height() - 30))

    def laser(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        x, y = self.rect.center
        pg.draw.line(screen, "red", (x, y), (mouse_x, mouse_y), 10)

    def shoot(self):
        x = self.rect.center[0]
        y = self.rect.center[1]
        if self.counter <= 0:
            BulletF([bullets], x=x, y=y)
            self.counter = self.def_counter

    def control(self, key):
        if key[pg.K_w]:
            if self.rect.center[1] - (self.img.get_height() / 2 + 10) + self.speed >= 0:
                self.rect.y -= self.speed
        if key[pg.K_s]:
            if self.rect.center[1] + (self.img.get_height() / 2) + self.speed <= screen.get_height():
                self.rect.y += self.speed
        if key[pg.K_d]:
            if self.rect.center[0] + (self.img.get_width() / 2) + self.speed <= screen.get_width():
                self.rect.x += self.speed
        if key[pg.K_a]:
            if self.rect.center[0] - (self.img.get_width() / 2 + 10) + self.speed >= 0:
                self.rect.x -= self.speed

    def update(self):
        keys = pg.key.get_pressed()
        mouse = pg.mouse.get_pressed()
        self.control(keys)
        self.watch()
        if keys[pg.K_LALT]:
            self.laser()
        if shoot_player:
            if keys[pg.K_SPACE] or mouse[0]:
                self.shoot()
        if self.counter > 0:
            self.counter -= 1


def spawn(secs, player):
    if secs == 400:
        period = 200
        enms = random.randint(63, 100)
    elif secs == 200:
        period = 200
        enms = random.randint(42, 52)
    elif secs == 100:
        period = 100
        enms = random.randint(32, 42)
    elif secs == 50:
        period = 50
        enms = random.randint(20, 32)
    elif secs == 0:
        period = 50
        enms = random.randint(8, 16)
    else:
        enms = 0
    enemies_spawn = []
    for i in range(enms):
        enemies_spawn.append(Enemy([enemies], player=player))
    return enemies_spawn, period
