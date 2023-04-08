import fly_game_classes as fg
import time


for i in range(1000):
    test = fg.Match()
    while test.update() == None:
        test.blue.left_input()
        test.blue.up_input()
        test.red.up_input()
        test.red.right_input()
    del test

print(time.process_time())




