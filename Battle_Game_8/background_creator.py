import pickle as pkl
import pygame as pg
import os


os.chdir("C:\\Users\\angela\\Documents\\Python_Project\\Battle_Game_8")
#Creating background sprites
backdrop = (240, 250, 230)

background = pg.image.load("Background/background.png")
fan = pg.image.load("Background/fan.png")
fan_still = pg.image.load("Background/fan_still.png")
fan_speed = 6
fan_rot = 0



bound_max = 2000
bound_min = 500
back_res = 20
for x,i in enumerate(range(900,2000,back_res)):
    print(f'{round((x/len(range(900,2000,back_res)))*100)}% Done!')
    temp_back = pg.transform.scale(background,(i,i))
    temp_fan_still = pg.transform.scale(fan_still,(i,i))
    temp_fan_still.set_alpha(140)
    temp_fan = pg.transform.scale(fan,(i,i))
    temp_fan.set_alpha(140)
    for n in range(90//fan_speed):
        image = pg.Surface((n,n))
        image.fill(backdrop)
        image.blit(temp_back,(0,0))
        rot_fan = pg.transform.rotate(temp_fan,n*fan_speed)
        image.blit(rot_fan,(0,0))
        image.blit(temp_fan_still,(0,0))
        pg.image.save(image,f'back_cache/back-{i}-{n}.bmp')


# with open('back_cache.pkl', 'wb') as save:
#     pkl.dump(backgrounds,save,protocol=5)


print('Done!')
