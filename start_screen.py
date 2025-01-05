import pygame as pg

pg.init()


class Button:
    f1 = pg.font.Font(None, 36)
    def __init__(self, text: str, color: str, x: int, y: int, lx: int, ly: int):
        self.text = text
        self.color = color
        self.x = x
        self.lx = lx
        self.y = y
        self.ly = ly

    def draw(self):
        pg.draw.rect(screen, self.color, ((self.x, self.y), (self.lx, self.ly)), 2)
        text1 = self.f1.render(f"sse", 1, (0, 180, 0))
        x = self.lx / 2 - self.x
        y = self.lx / 2 - self.y
        screen.blit(text1, (x, y))


if __name__ == "__main__":
    run = True
    size = w, h = 1920, 1080
    screen = pg.display.set_mode(size)
    button1 = Button("Start", "red", 10, h/2 - 100, 280, 90)
    button2 = Button("Start", "red", 10, h/2 + 10, 280, 90)
    while run:
        screen.fill('grey')
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        button1.draw()
        button2.draw()
        pg.display.flip()
pg.quit()
