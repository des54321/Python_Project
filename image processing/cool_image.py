from PIL import Image
from copy import copy
from math import floor


def convul(img,dirs,values):
    pixels = img.load()
    real_dat = []
    for x in range(img.size[0]):
        real_dat.append([])
        for y in range(img.size[1]):
            real_dat[-1].append(copy(pixels[x,y]))


    for x in range(img.size[0]):
        for y in range(img.size[1]):
            total = [0,0,0]
            for i,dir in enumerate(dirs):
                if (x+dir[0] >= 0) and (x+dir[0] < img.size[0]) and (y+dir[1] >= 0) and (y+dir[1] < img.size[1]):
                    total[0] += real_dat[x+dir[0]][y+dir[1]][0]*values[i]
                    total[1] += real_dat[x+dir[0]][y+dir[1]][1]*values[i]
                    total[2] += real_dat[x+dir[0]][y+dir[1]][2]*values[i]
            final = [floor(min(max(n,0),255)) for n in total]
            pixels[x,y] = tuple(final)
    


vects = [
    (0,1),
    (1,1),
    (1,0),
    (1,-1),
    (0,-1),
    (-1,-1),
    (-1,0),
    (-1,1),
    (0,0)
]

vals = [
    -1,
    0,
    -1,
    0,
    -1,
    0,
    -1,
    0,
    5
]

with Image.open("fam.jpeg") as im:

    convul(im,vects,vals)
    im.save('testing.png')