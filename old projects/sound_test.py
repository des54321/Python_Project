import numpy as np
import simpleaudio as sa
import pydub as pd
import pygame as pg
import math




frequency = 200
fs = 44100
seconds = 3
detail = 100

wave = np.linspace(0,1,detail)
pg.init()
s_w = 800
s_h = 600
screen = pg.display.set_mode((s_w,s_h))
fps = 120
fps_clock = pg.time.Clock()
running = True
while running:

    if pg.mouse.get_pressed()[0]:
        x = (s_w/detail)*math.floor(pg.mouse.get_pos()[0]/(s_w/detail))
        wave[int(round((x/s_w)*detail))] = (pg.mouse.get_pos()[1]/s_h)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((0,0,0))
    for i in range(len(wave)-1):
        pg.draw.line(screen, (255,255,255), ((i/detail)*s_w, wave[i]*s_h),(((i+1)/detail)*s_w, wave[(i+1)]*s_h), int(s_w/detail/2.2))
    pg.display.update()
    fps_clock.tick(fps)
pg.quit()




t = np.linspace(0, seconds, int(seconds * fs), False)

for i in range(len(t)):
    t[i] = wave[min((math.floor(((t[i]*frequency)%1)*detail),detail-1))]


audio = t * (2**15 - 1)

audio = audio.astype(np.int16)
print(audio)


play_obj = sa.play_buffer(audio, 1, 2, fs)


play_obj.wait_done()