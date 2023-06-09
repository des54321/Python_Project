import pygame as pg
lines = []
was_drawing = False


def update_lines():
    global was_drawing
    if pg.mouse.get_pressed()[0]:
        if not was_drawing:
            was_drawing = True
            lines.append([])
        lines[-1].append(pg.mouse.get_pos())
    else:
        was_drawing = False


def draw_lines(screen,color,width):
    for i in lines:
        for x in range(len(i)-1):
            pg.draw.circle(screen,color,i[x],width//2-1)
            pg.draw.line(screen,color,i[x],i[x+1],width)