import pygame as pg
from pygame import Vector2
lines = []
was_drawing = False
last_dir = 0
last_dir = None


def update_lines(del_radius):
    global was_drawing, last_dir

    if pg.mouse.get_pressed()[0]:
        if not was_drawing:
            was_drawing = True
            lines.append([])
    else:
        was_drawing = False

    if pg.key.get_pressed()[pg.K_LSHIFT] and pg.mouse.get_pressed()[0]:
            if last_dir == None:
                if len(lines[-1]) == 0:
                    lines[-1].append(pg.mouse.get_pos())
                else:
                    if not pg.mouse.get_pos() == lines[-1][-1]:
                        rel_pos = Vector2(pg.mouse.get_pos())-Vector2(lines[-1][-1])
                        if abs(rel_pos.x) > abs(rel_pos.y):
                            last_dir = 'x'
                            lines[-1].append((pg.mouse.get_pos()[0],lines[-1][-1][1]))
                        else:
                            last_dir = 'y'
                            lines[-1].append((lines[-1][-1][0],pg.mouse.get_pos()[1]))
            else:
                if last_dir == 'x':
                    lines[-1].append((pg.mouse.get_pos()[0],lines[-1][-1][1]))
                else:
                    lines[-1].append((lines[-1][-1][0],pg.mouse.get_pos()[1]))
    else:
        last_dir = None
        if pg.mouse.get_pressed()[0]:
            lines[-1].append(pg.mouse.get_pos())
    

        
    
    
    if pg.mouse.get_pressed()[2]:
        n = 0
        for _ in range(len(lines)):
            for x in range(len(lines[n])-1):
                if pg.Vector2(lines[n][x]).distance_to(pg.mouse.get_pos())+Vector2(lines[n][x+1]).distance_to(pg.mouse.get_pos()) < del_radius+Vector2(lines[n][x+1]).distance_to(lines[n][x]):
                    del lines[n]
                    n -= 1
                    was_drawing = False
                    break
            n += 1



def draw_lines(screen,color,width):
    for i in lines:
        for x in range(len(i)-1):
            pg.draw.circle(screen,color,i[x],width//2-1)
            pg.draw.line(screen,color,i[x],i[x+1],width)
        pg.draw.circle(screen,color,i[-1],width//2-1)