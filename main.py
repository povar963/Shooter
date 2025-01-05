import random
import pygame as pg
import math
import time
from player import *

pg.init()


def start():
    global spawn_queue
    player = Player([player_group])
    start_time = time.time()
    clock = pg.time.Clock()
    elapsed = 0
    spawn_countdown = 0
    run = True
    while run:
        screen.fill('grey')
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        if pg.mouse.get_focused():
            player_group.draw(screen)
            player_group.update()
            focus = True
        else:
            focus = False
        if focus:
            if spawn_toggle:
                if elapsed in [0, 50, 100, 200, 400]:
                    spawn_queue, period = spawn(elapsed, player)
                    countdown_queue = []
                    for i in range(len(spawn_queue)):
                        count = i + 1
                        countdown_queue.append(period//len(spawn_queue)*count)
                if spawn_queue:
                    if int(elapsed) in countdown_queue:
                        i = countdown_queue.index(int(elapsed))
                        spawn_queue[i].create()
                        countdown_queue.pop(i)
                        spawn_queue.pop(i)

            enemies.update()
            enemies.draw(screen)
            bullets.update()
            bullets.draw(screen)

            player_group.update()
            player_group.draw(screen)
            if player.alive():
                player.heath_bar()
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
            screen.blit(text_seconds, (screen.get_width() / 2 - text_seconds.get_width(), 10))
            pg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    start()

pg.quit()
