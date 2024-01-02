from game import Game
import pygame as pg
from buttom import Button
import cv2


def start_game(*args, **kwargs):
    game = Game()
    game.play_game()


def passed(*args, **kwargs):
    pass


if __name__ == "__main__":
    video = cv2.VideoCapture("images/tetris.mp4")
    success, video_image = video.read()
    fps = video.get(cv2.CAP_PROP_FPS)

    window = pg.display.set_mode(video_image.shape[1::-1])
    clock = pg.time.Clock()
    pg.mixer.music.load("Sounds/Tetris_main.mid")
    pg.mixer.music.play(start=0.0, fade_ms=3500,)

    button_start = Button(window, start_game, (0.28, 0.35), 'images/start.png')

    run = success
    while run:
        clock.tick(fps)
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                run = False

        success, video_image = video.read()
        if success:
            video_surf = pg.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
            window.blit(video_surf, (0, 0))

        button_start.show(events)
        pg.display.flip()

pg.quit()
exit()
