class Chopsticks:

    def __init__(self,hands,mod) -> None:
        self.p1 = [1 for i in range(hands)]
        self.p2 = [1 for i in range(hands)]
        self.mod = mod
        self.move_done = None
    

    def min_max(self,maxi,depth,do_move = True):
        score = self.get_score()

        if score == 'p2 win':
            return -128-depth
        if score == 'p1 win':
            return 128+depth
        
        if depth == 0:
            return score

        if maxi:
            if do_move:
                moves = self.all_moves_p1()
                scores = [i.min_max(False,depth-1,False) for i in moves]
                best = moves[scores.index(max(scores))]
                print(scores)
                return best.move_done
                  
            return max([i.min_max(False,depth-1,False) for i in self.all_moves_p1()])
        else:
            if do_move:
                moves = self.all_moves_p2()
                scores = [i.min_max(True,depth-1,False) for i in moves]
                best = moves[scores.index(min(scores))]
                print(scores)
                return best.move_done

            return min([i.min_max(True,depth-1,False) for i in self.all_moves_p2()])




    def find_moves(self):
        moves = []
        p1_done = []
        for i in range(len(self.p1)):
            if self.p1[i] != 0:
                if not self.p1[i] in p1_done:
                    p1_done.append(self.p1[i])
                    p2_done = []
                    for n in range(len(self.p2)):
                        if self.p2[n] != 0:
                            if not self.p2[n] in p2_done:
                                p2_done.append(self.p2[n])
                                moves.append([i,n])
        
        if sum(self.p1)%len(self.p1) == 0:
            if not all([i==sum(self.p1)//len(self.p1) for i in self.p1]):
                moves.append(['s1',sum(self.p1)//len(self.p1)])
        if sum(self.p2)%len(self.p2) == 0:
            if not all([i==sum(self.p2)//len(self.p2) for i in self.p2]):
                moves.append(['s2',sum(self.p2)//len(self.p2)])
        return moves


    def all_moves_p1(self):
        new = []
        for i in self.find_moves():
            if not i[0] == 's2':
                new.append(self.do_move(i,1))
        return new
    

    def all_moves_p2(self):
        new = []
        for i in self.find_moves():
            if not i[0] == 's1':
                new.append(self.do_move(i,2))
        return new
    
    
    def do_move(self,move,p):
        new = Chopsticks(1,self.mod)
        new.move_done = move
        new.p1 = self.p1.copy()
        new.p2 = self.p2.copy()
        if move[0] == 's1':
            new.p1 = [move[1] for i in new.p1]
            return new
        if move[0] == 's2':
            new.p2 = [move[1] for i in new.p2]
            return new
        if p == 1:
            new.p2[move[1]] += new.p1[move[0]]
            new.p2[move[1]] %= self.mod
        else:
            new.p1[move[0]] += new.p2[move[1]]
            new.p1[move[0]] %= self.mod
        return new
    

    def get_score(self):
        if all([i == 0 for i in self.p1]):
            return 'p2 win'
        if all([i == 0 for i in self.p2]):
            return 'p1 win'
        return sum([i == 0 for i in self.p2]) - sum([i == 0 for i in self.p1])


    def __repr__(self) -> str:
        return f'{self.p1} {self.p2}'

    
    def __str__(self):
        return self.__repr__()


game = Chopsticks(2,5)

running = True
turn = 'player'

while running:
    if turn == 'player':
        valid = False
        while not valid:
            move = input('Your Move:')
            if move == 'switch':
                if sum(game.p1)%len(game.p1) == 0 and not (all([i==sum(game.p1)//len(game.p1) for i in game.p1])):
                    vaild = True
                    break
                else:
                    valid = False
                    print('Invalid Move!')
                    continue
            try:
                move = eval('['+move+']')
            except:
                valid = False
                print('Invalid Move!')
                continue
            if not type(move) == list:
                valid = False
                print('Invalid Move!')
                continue
            if not len(move) == 2:
                vaild = False
                print('Invalid Move!')
                continue
            if game.p1[move[0]] == 0 or game.p2[move[1]] == 0:
                vaild = False
                print('Invalid Move!')
            else:
                valid = True
        if move == 'switch':
            game.p1 = [sum(game.p1)//len(game.p1) for i in game.p1]
        else:
            game.p2[move[1]] += game.p1[move[0]]
            game.p2[move[1]] %= game.mod
        turn = 'robot'
    else:
        print("Robot's turn")
        robot_move = game.min_max(False,5)
        print(f'Robot moved: {robot_move}')
        game = game.do_move(robot_move,2)
        turn = 'player'
    print('')
    print('Current Board:')
    print(game)
    print('')
    if game.get_score() == 'p1 win':
        print('Game Won, you win')
        running = False
    if game.get_score() == 'p2 win':
        print('Game Lost, you lose!!')
        running = False