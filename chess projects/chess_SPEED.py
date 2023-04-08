from colorama import Fore, Style, Back
import ast
import time
import sys
coordinates = True
b_s = 8
thinking_len = 22
piece_value = {
    'K':0,
    'Q':9,
    'B':3,
    'R':5,
    'P':1,
    'H':3
}


peice_show = {
    "K": "\u265A",
    "Q": "\u265B",
    "B": "\u265D",
    "R": "\u265C",
    "H": "\u265E",
    "P": "\u2659",
}

knight_moves = [
    [1,2],
    [2,1],
    [-1,2],
    [-2,1],
    [1,-2],
    [2,-1],
    [-1,-2],
    [-2,-1]
]

king_moves = [
    [1,0],
    [1,1],
    [0,1],
    [-1,1],
    [-1,0],
    [-1,-1],
    [0,-1],
    [1,-1]
]

bishop_dirs = [
    [1,1],
    [1,-1],
    [-1,-1],
    [-1,1]
]

rook_dirs = [
    [1,0],
    [0,1],
    [-1,0],
    [0,-1]
]



def render_board(board, highlight = []):
    print("")
    if coordinates:
        print(Fore.MAGENTA, end="    ")
        for i in range(b_s):
            print(Fore.MAGENTA + " " + f"{i}", end="  ")
        print("")
        print("")
    for i in range(b_s):
        if coordinates:
            print(Back.RESET + Fore.MAGENTA + f"{i}", end="   ")
        for x in range(b_s):
            if [i, x] in highlight:
                print(Back.YELLOW, end="")
            else:
                if (x + i) % 2 == 1:
                    print(Back.BLACK, end="")
                else:
                    print(Back.WHITE, end="")
            if get_kind(board,[i, x]) == "0":
                print(Fore.BLUE + " " + peice_show[get_s(board,[i, x])[0]], end="  ")
            elif get_kind(board,[i, x]) == "1":
                print(Fore.GREEN + " " + peice_show[get_s(board,[i, x])[0]], end="  ")
            else:
                print(Fore.GREEN, end="    ")
        print(Back.RESET)
        print("", end="    ")
        for x in range(b_s):
            if [i, x] in highlight:
                print(Back.YELLOW, end="")
            else:
                if (x + i) % 2 == 1:
                    print(Back.BLACK, end="")
                else:
                    print(Back.WHITE, end="")
            print(Fore.GREEN, end="    ")
        print(Back.RESET)



def get_s(board, pos):
    return ( board[pos[0] * 16 + pos[1] * 2] + board[pos[0] * 16 + pos[1] * 2 + 1] )

def get_kind(board, pos):
    return board[pos[0] * 16 + pos[1] * 2 + 1]

def change(board, pos, new):
     return (board[: pos[0] * 16 + pos[1] * 2] + new + board[pos[0] * 16 + pos[1] * 2 + 2 :])

def move_piece(board, piece, new_pos):
    if piece == new_pos:
        return board[:]
    new = change(board, new_pos, get_s(board,piece))
    return change(new, piece, '02')

def all_pieces_of(board, color):
        store = []
        for i in range(b_s):
            for x in range(b_s):
                if get_kind(board,[i, x]) == color:
                    store.append([i, x])
        return store

def king_of(board, color):
    ind = board.find('K'+color)
    return ind_to_p(ind)

def ind_to_p(ind):
    return [ind//16, (ind//2)%b_s]

def in_bound(square):
    if square[0] > -1 and square[0] < b_s:
        if square[1] > -1 and square[1] < b_s:
            return True
    return False

def moves_of(board,pos,check = True):
    f_pos = pos[:]
    kind = get_s(board,pos)
    if kind == '02':
        return []
    else:
        moves = []
        if kind[0] == 'H':
            
            for i in knight_moves:
                new_p = [pos[0]+i[0],pos[1]+i[1]]
                if in_bound(new_p):
                    if not get_kind(board, new_p) == kind[1]:
                        moves.append(new_p)
        
        if kind[0] == 'K':
            
            for i in king_moves:
                new_p = [pos[0]+i[0],pos[1]+i[1]]
                if in_bound(new_p):
                    if not get_kind(board, new_p) == kind[1]:
                        moves.append(new_p)
        
        if kind[0] == 'Q' or kind[0] == 'R':

            for x in rook_dirs:

                f_pos = pos[:]

                for i in range(b_s):
                    f_pos  = [f_pos[0]+x[0],f_pos[1]+x[1]]
                    if not in_bound(f_pos):
                        break
                    if get_kind(board, f_pos) != '2':
                        if get_kind(board, f_pos) == kind[1]:
                            break
                        else:
                            moves.append(f_pos)
                            break
                    moves.append(f_pos)

        if kind[0] == 'Q' or kind[0] == 'B':

            for x in bishop_dirs:

                f_pos = pos[:]

                for i in range(b_s):
                    f_pos  = [f_pos[0]+x[0],f_pos[1]+x[1]]
                    if not in_bound(f_pos):
                        break
                    if get_kind(board, f_pos) != '2':
                        if get_kind(board, f_pos) == kind[1]:
                            break
                        else:
                            moves.append(f_pos)
                            break
                    moves.append(f_pos)
        
        if kind[0] == 'P':

            if kind[1] == '0':

                if in_bound([pos[0]+1,pos[1]+1]):
                    if get_kind(board,[pos[0]+1,pos[1]+1]) == str((int(kind[1])+1)%2):
                        moves.append([pos[0]+1,pos[1]+1])
                
                if in_bound([pos[0]+1,pos[1]-1]):
                    if get_kind(board,[pos[0]+1,pos[1]-1]) == str((int(kind[1])+1)%2):
                        moves.append([pos[0]+1,pos[1]-1])
                
                if in_bound([pos[0]+1,pos[1]]):
                    if get_kind(board,[pos[0]+1,pos[1]]) == '2':
                        moves.append([pos[0]+1,pos[1]])
                        if pos[0] == 1:
                            if get_kind(board,[pos[0]+2,pos[1]]) == '2':
                                moves.append([pos[0]+2,pos[1]])

            else:

                if in_bound([pos[0]-1,pos[1]+1]):
                    if get_kind(board,[pos[0]-1,pos[1]+1]) == str((int(kind[1])+1)%2):
                        moves.append([pos[0]-1,pos[1]+1])
                
                if in_bound([pos[0]-1,pos[1]-1]):
                    if get_kind(board,[pos[0]-1,pos[1]-1]) == str((int(kind[1])+1)%2):
                        moves.append([pos[0]-1,pos[1]-1])
                
                if in_bound([pos[0]-1,pos[1]]):
                    if get_kind(board,[pos[0]-1,pos[1]]) == '2':
                        moves.append([pos[0]-1,pos[1]])
                        if pos[0] == b_s-2:
                            if get_kind(board,[pos[0]-2,pos[1]]) == '2':
                                moves.append([pos[0]-2,pos[1]])
        
        if check:
            count = 0
            
            while count < len(moves):
                n = moves[count]
                new = move_piece(board, pos, n)
                king = king_of(new , kind[1])
                opp_moves = all_moves_for(new, str((int(kind[1])+1)%2) , False )
                test = True
                for i in opp_moves:
                    if i[1] == king:
                        test = False
                if test:
                    count += 1
                else:
                    del moves[count]
        
        return moves




def all_moves_for(board, color, check = True):
    all_pieces = all_pieces_of(board, color)
    all_moves = []
    for i in all_pieces:
        all_moves += [[i,x] for x in moves_of(board,i,check)]
    return all_moves


def min_max(board, depth, color, maxi=True, og=True, alpha=-100, beta=100, animation=False, extra_move = True, give_score = False):
    if depth == 0:
        # test = len(all_moves_for(board, str(color)))
        # if test == 0:
        #     return 1000
        return sum([piece_value[get_s(board,i)[0]] for i in all_pieces_of(board, str((int(color) + 1) % 2))])-sum([piece_value[get_s(board,i)[0]] for i in all_pieces_of(board, color)])
    if maxi:
        value = -1000
        all_move = all_moves_for(board, str(color))
        if og:
            if extra_move:
                if depth > 1:
                    best = min_max(board, depth - 2, color)

                    del all_move[all_move.index(best)]
                    all_move = [best] + all_move
            scores = []
        if len(all_move) == 0:
            if og:
                sys.exit()
            else:
                return -1000
        for i in all_move:
            test = move_piece(board, i[0], i[1])
            if animation:
                b = (
                    "Thinking [" + 
                    "+" * round((all_move.index(i) / len(all_move)) * thinking_len) +
                     "_" * round((1 - (all_move.index(i) / len(all_move))) * thinking_len) 
                     + "]"
                )
                print(b, end="\r")
            if og:
                score = min_max(test, depth - 1, str((int(color) + 1) % 2), False, False, alpha, beta)
                scores.append(score)
                value = max(value, score)
            else:
                value = max(
                    value,
                    min_max(
                        test,
                        depth - 1,
                        str((int(color) + 1) % 2),
                        False,
                        False,
                        alpha,
                        beta
                    ),
                )
            alpha = max(alpha, value)
            if value > beta:
                break
        if og:
            if give_score:
                return [all_move[scores.index(max(scores))],max(scores)]
            return all_move[scores.index(max(scores))]
        return value
    else:
        value = 1000
        all_move = all_moves_for(board, color)
        if len(all_move) == 0:
            return 1000
        for i in all_move:
            test = move_piece(board, i[0], i[1])
            value = min(
                value,
                min_max(
                    test,
                    depth - 1, 
                    str((int(color) + 1) % 2), 
                    True, 
                    False, 
                    alpha, 
                    beta
                ),
            )
            beta = min(beta, value)
            if value < alpha:
                break
        return value

def invalid_move(test, type=0, moving=[0, 0]):
    if test == 'quit':
        sys.exit()
    try:
        ast.literal_eval("[" + test + "]")
    except:
        return [False, "Invalid"]
    if not len(ast.literal_eval("[" + test + "]")) == 2:
        return [False, "That is not a Coordinate"]
    if not in_bound(ast.literal_eval("[" + test + "]")):
        return [False, "Coordinates Given are Invalid"]
    if type == 0:
        if get_kind(game_b, ast.literal_eval("[" + test + "]")) == "2":
            return [False, "Square Chosen is not a Peice"]
        if get_kind(game_b, ast.literal_eval("[" + test + "]")) == "1":
            return [False, "That's not your Peice!"]
        if len(moves_of(game_b,ast.literal_eval("[" + test + "]"))) == 0:
            return [False, "Peice Chosen has no Possible Moves"]
        return [True, ""]
    else:
        if not ast.literal_eval("[" + test + "]") in moves_of(game_b, moving):
            return [False, "Move is not Possible by Peice"]
        return [True, ""]




game_b = "R0H0B0K0Q0B0H0R0P0P0P0P0P0P0P0P00202020202020202020202020202020202020202020202020202020202020202P1P1P1P1P1P1P1P1R1H1B1K1Q1B1H1R1"
while True:
    render_board(game_b)
    print(Style.RESET_ALL)
    move_chose = input("Move >>> ")
    while not invalid_move(move_chose)[0]:
        print(invalid_move(move_chose)[1])
        move_chose = input("Move >>> ")
    move_chose = ast.literal_eval("[" + move_chose + "]")
    pos_move = moves_of(game_b, move_chose,True)
    render_board(game_b,pos_move)
    print(Style.RESET_ALL)
    move_to = input("To >>> ")
    while not invalid_move(move_to, 1, move_chose)[0]:
        print(invalid_move(move_to, 1, move_chose)[1])
        move_to = input("To >>> ")
    move_to = ast.literal_eval("[" + move_to + "]")
    game_b = move_piece(game_b, move_chose, move_to)
    render_board(game_b)
    print("")
    start = time.time()
    best_move = min_max(game_b,3, "1", animation=True)
    print('')
    mabye = min_max(game_b,3,'1',alpha=900,beta=1100,extra_move=False,give_score=True)
    print("")
    print(best_move)
    print('')
    print(mabye)
    print('')
    print(f"It took {time.time()-start}s to finish")
    if mabye[1] == 1000:
        game_b = move_piece(game_b, mabye[0][0],mabye[0][1])
    else:
        game_b = move_piece(game_b, best_move[0],best_move[1])