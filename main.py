import random
import pygame as pg
import math
import time

pg.init()


class Enemy(pg.sprite.Sprite):
    img = pg.image.load("./1.png")

    def __init__(self, *groups: list):
        super().__init__(*groups)
        x = random.randint(70, screen.get_width() - 70)
        y = random.randint(70, screen.get_height() - 70)
        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 100

        if pg.sprite.collide_mask(self, player):
            self.kill()

    def shoot(self):
        pass
        x = self.rect.center[0]
        y = self.rect.center[1]
        bullet = BulletE([bullets], x=x, y=y)

    def watch(self):
        x = self.rect.center[0]
        y = self.rect.center[1]
        mouse_x, mouse_y = player.rect.center
        rel_x, rel_y = mouse_x - x, mouse_y - y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pg.transform.rotate(self.img, int(angle))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.watch()
        if player.alive():
            if self.counter <= 0:
                self.shoot()
                self.counter = 100
            elif self.counter > 0:
                self.counter -= 1
        else:
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
        self.counter = 100
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

    def laser(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        x, y = self.rect.center
        pg.draw.line(screen, "red", (x, y), (mouse_x, mouse_y), 10)

    def shoot(self):
        x = self.rect.center[0]
        y = self.rect.center[1]
        bullet = BulletF([bullets], x=x, y=y)

    def control(self, keys):
        if keys[pg.K_w]:
            self.rect.y -= self.speed
        if keys[pg.K_s]:
            self.rect.y += self.speed
        if keys[pg.K_d]:
            self.rect.x += self.speed
        if keys[pg.K_a]:
            self.rect.x -= self.speed

    def update(self):
        keys = pg.key.get_pressed()
        self.control(keys)
        self.watch()
        if keys[pg.K_LALT]:
            self.laser()
        if keys[pg.K_SPACE]:
            if self.counter <= 0:
                self.shoot()
                self.counter = 100
        if self.counter > 0:
            self.counter -= 1
        self.heath_bar()


class BulletE(pg.sprite.Sprite):
    img = pg.image.load("./Bullet.png")

    def __init__(self, *groups: list, x, y):
        super().__init__(*groups)
        mouse_x, mouse_y = player.rect.center
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
        if pg.sprite.collide_mask(self, player):
            if player.health == 1:
                player.health = 0
                player.kill()
            else:
                player.health -= 1
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


if __name__ == "__main__":
    screen = pg.display.set_mode((1920, 1080))
    # Создание группы пуль
    bullets = pg.sprite.Group()
    # Создание вржеской группы
    enemies = pg.sprite.Group()
    # Создание персонажа
    player_group = pg.sprite.Group()
    player = Player([player_group])
    # Задача шрифта
    f1 = pg.font.Font(None, 36)

    # Задача времени запуска программы
    start_time = time.time()
    # Включение спавна
    spawn_toggle = True
    elapsed = 0
    run = True
    while run:
        screen.fill('grey')
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        clock = pg.time.Clock()
        if pg.mouse.get_focused():
            player_group.draw(screen)
            player_group.update()
        if spawn_toggle:
            spawn = random.randint(0, 1000)
            if 0 < spawn < 10:
                enemy = Enemy([enemies])
        enemies.update()
        enemies.draw(screen)

        bullets.update()
        bullets.draw(screen)

        player_group.update()
        player_group.draw(screen)
        if player.alive():
            elapsed = time.time() - start_time
        else:
            w = int(screen.get_height() / 3)
            fy = int(screen.get_height() / 3) + w / 2
            f2 = pg.font.Font(None, int(w / 2))
            pg.draw.line(screen, "black", (0, fy), (screen.get_width(), fy), w)
            text_end = f2.render(f"Lose", 1, (180, 0, 0))
            screen.blit(text_end,
                        (int(screen.get_width() / 2 - text_end.get_width() / 2), fy - text_end.get_height() / 2))
            keys = pg.key.get_pressed()
            if keys[pg.K_SPACE]:
                player = Player([player_group])
                start_time = time.time()
        text_seconds = f1.render(f"{int(elapsed)}", 1, (180, 0, 0))

        text1 = f1.render(f"hp:{player.health} cd:{player.counter}", 1, (180, 0, 0))
        screen.blit(text1, (10, screen.get_height() - 30))
        screen.blit(text_seconds, (screen.get_width() / 2 - text_seconds.get_width(), 10))
        pg.display.flip()
        clock.tick(60)
pg.quit()
