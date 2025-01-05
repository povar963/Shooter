import pygame as pg

pg.init()


class Button:
    f1 = pg.font.Font(None, 36)

    def __init__(self, text: str, color: str, x: int, y: int, lx: int, ly: int, mode):
        self.text = text
        self.color = color
        self.x = x
        self.lx = lx
        self.y = y
        self.ly = ly
        self.mode = mode

    def draw(self):
        btn = pg.draw.rect(screen, self.color, ((self.x, self.y), (self.lx, self.ly)), 2)
        text1 = self.f1.render(self.text, 1, (0, 180, 0))
        x = btn.width / 2 + self.x - text1.get_width() / 2
        y = btn.height / 2 + self.y - text1.get_height() / 2

        screen.blit(text1, (x, y))

    def update(self):
        self.draw()
        mouse_x, mouse_y = pg.mouse.get_pos()
        if self.x <= mouse_x <= self.lx + self.x and self.y <= mouse_y <= self.ly + self.y:
            pass

if __name__ == "__main__":
    run = True
    size = w, h = 900, 900
    screen = pg.display.set_mode(size)
    button1 = Button("Start", "red", 10, h / 2 - 100, 180, 90, 0)
    button2 = Button("Settings", "red", 10, h / 2 + 10, 180, 90, 1)
    while run:
        screen.fill('grey')
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONUP:
                button1.update()
        button1.draw()
        button2.draw()
        pg.display.flip()
pg.quit()
