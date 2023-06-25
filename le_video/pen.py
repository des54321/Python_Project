import pygame as pg
from pygame import Vector2
lines = []
arrows = []
was_drawing = False
last_dir = 0
last_dir = None
arrow_angle = 40
arrow_length = 40
drawing_arrow = False


def update_lines(del_radius):
    global was_drawing, last_dir, drawing_arrow, lines, arrows

    if pg.key.get_pressed()[pg.K_LALT] or drawing_arrow:
        if pg.mouse.get_pressed()[0]:
            if not was_drawing:
                drawing_arrow = True
                was_drawing = True
                arrows.append([Vector2(pg.mouse.get_pos()),Vector2(pg.mouse.get_pos())])
            else:
                arrows[-1][1] = Vector2(pg.mouse.get_pos())
        else:
            if was_drawing:
                drawing_arrow = False
            was_drawing = False
    else:
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
        
        n = 0
        for _ in range(len(arrows)):
            if pg.Vector2(arrows[n][0]).distance_to(pg.mouse.get_pos())+Vector2(arrows[n][1]).distance_to(pg.mouse.get_pos()) < del_radius+Vector2(arrows[n][1]).distance_to(arrows[n][0]):
                del arrows[n]
                n -= 1
                was_drawing = False
                break
            n += 1
    
    if pg.key.get_pressed()[pg.K_e]:
        lines = []
        arrows = []
        was_drawing = False



def draw_lines(screen,color,width):
    for i in lines:
        for x in range(len(i)-1):
            pg.draw.circle(screen,color,i[x],width//2-1)
            pg.draw.line(screen,color,i[x],i[x+1],width)
        pg.draw.circle(screen,color,i[-1],width//2-1)
    
    for i in arrows:
        if not i[0] == i[1]:
            pg.draw.circle(screen,color,i[0],width//2-1)
            pg.draw.line(screen,color,i[0],i[1],width)
            pg.draw.circle(screen,color,i[1],width//2-1)
            head1 = (i[0]-i[1]).rotate(arrow_angle)
            head2 = (i[0]-i[1]).rotate(-arrow_angle)
            head1.scale_to_length(arrow_length)
            head2.scale_to_length(arrow_length)
            pg.draw.line(screen,color,i[1],i[1]+head1,width)
            pg.draw.circle(screen,color,i[1]+head1,width//2-1)
            pg.draw.line(screen,color,i[1],i[1]+head2,width)
            pg.draw.circle(screen,color,i[1]+head2,width//2-1)