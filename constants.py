import pygame as pg
from colors import Colors

FPS = 80

pg.init()
title_font = pg.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)

score_rect = pg.Rect(320, 55, 170, 60)
next_rect = pg.Rect(320, 215, 170, 180)

screen = pg.display.set_mode((500, 620))
pg.display.set_caption("Tetris")
favicon = pg.image.load('images/tetris.png')
pg.display.set_icon(favicon)
clock = pg.time.Clock()
