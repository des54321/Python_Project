import fly_game_classes as fg
import neural
import pickle
import time
from math import floor, ceil
from random import random, randint
import threading
from multiprocessing.dummy import Pool as ThreadPool

agent_num = 4
agent_brain = [9,4,3]
match_len = 100
fg.move_speed *= 3
fg.thrust *= 3
fg.time = match_len
start_bias_range = 1
start_weight_range = 1

bias_mutate_rate = 0.15
weight_mutate_rate = 0.3



def find_winner(brain1:neural.NeuralNet,brain2:neural.NeuralNet):
    global polarity
    polarity += 1
    polarity %= 2
    if brain1 == brain2:
        return 0
    game = fg.Match()
    blue = polarity
    while game.update() == None:
        if blue == 1:
            blue_chose = brain1.big_brain([float(game.it == fg.BLUE),game.blue.pos_x,game.blue.pos_y,game.blue.pos_x-game.red.pos_x,game.blue.pos_y-game.red.pos_y,game.blue.vel_x,game.blue.vel_y,game.red.vel_x,game.red.vel_y])
            red_chose = brain2.big_brain([float(game.it  == fg.RED),game.red.pos_x,game.red.pos_y,game.red.pos_x-game.blue.pos_x,game.red.pos_y-game.blue.pos_y,game.red.vel_x,game.red.vel_y,game.blue.vel_x,game.blue.vel_y])
        else:
            blue_chose = brain2.big_brain([float(game.it == fg.BLUE),game.blue.pos_x,game.blue.pos_y,game.blue.pos_x-game.red.pos_x,game.blue.pos_y-game.red.pos_y,game.blue.vel_x,game.blue.vel_y,game.red.vel_x,game.red.vel_y])
            red_chose = brain1.big_brain([float(game.it  == fg.RED),game.red.pos_x,game.red.pos_y,game.red.pos_x-game.blue.pos_x,game.red.pos_y-game.blue.pos_y,game.red.vel_x,game.red.vel_y,game.blue.vel_x,game.blue.vel_y])
        
        if blue_chose[0] > 0:
            game.blue.up_input()
        if blue_chose[1] > 0:
            game.blue.right_input()
        if blue_chose[2] > 0:
            game.blue.left_input()
        

        if red_chose[0] > 0:
            game.red.up_input()
        if red_chose[1] > 0:
            game.red.right_input()
        if red_chose[2] > 0:
            game.red.left_input()
    winner = game.winner
    del game
    if blue == 1:
        if winner == fg.BLUE:
            return 1
        else:
            return 0
    else:
        if winner == fg.RED:
            return 1
        else:
            return 0


def get_score(agent):
    global polarity
    polarity = randint(0,1)
    return sum([find_winner(population[agent], i) for i in population])


def face_every_agent():
    global population
    
    win_num = [get_score(n) for n in range(len(population))]
    return win_num



def sort_key(num):
    return num[0]



population = [neural.NeuralNet(start_bias_range,start_bias_range,agent_brain) for _ in range(agent_num)]


gen = 0
polarity = 0
thread_num = 5
start = time.time()


while gen < 1000:
    current_time = time.time()
    winners = list(zip(face_every_agent(),population))
    winners.sort(key=sort_key,reverse=True)
    pop_sort = [i[1] for i in winners]

    with open('best.pkl', 'wb') as save:
        pickle.dump(pop_sort[0],save,protocol=5)
    
    population = pop_sort

    for i in range(floor(agent_num/2)):
        del population[-1]

    for i in range(floor(agent_num/2)):
        population.append(population[i].mutate(bias_mutate_rate,weight_mutate_rate))






    print(f'Total Time: {time.time() - start}')
    print(f'Generation Time: {time.time() - current_time}')
    print(f'Generation: {gen}')
    gen += 1
    
