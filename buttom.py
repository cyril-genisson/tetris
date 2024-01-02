import pygame as pg


class Button:
    def __init__(self, window, function, pos, image):
        self.image = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] * window.get_rect().w
        self.rect.y = pos[1] * window.get_rect().h

        self.window = window
        self.run = function

    def show(self, events, args=[], kwargs={}):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and self.rect.collidepoint(event.pos):
                    self.run(self, *args, **kwargs)

        self.window.blit(self.image, self.rect)
