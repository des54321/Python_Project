from colorama import Fore, Style, Back
import ast
import copy
import time
import sys

peice_show = {
    "K": "\u265A",
    "Q": "\u265B",
    "B": "\u265D",
    "R": "\u265C",
    "H": "\u265E",
    "P": "\u2659",
}

coordinates = True

king_moves = [[1, 0], [1, 1], [0, 1], [-1, -1], [0, -1], [-1, 0], [1, -1], [-1, 1]]
thinking_len = 22
b_s = 8


class Board:
    def __init__(self):
        self.peices = "R0H0B0K0Q0B0H0R0P0P0P0P0P0P0P0P00202020202020202020202020202020202020202020202020202020202020202P1P1P1P1P1P1P1P1R1H1B1K1Q1B1H1R1"

    def render(self, highlight=[]):
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
                    if (x + i) % 2 == 0:
                        print(Back.BLACK, end="")
                    else:
                        print(Back.WHITE, end="")
                if self.get([i, x])[1] == "0":
                    print(Fore.BLUE + " " + peice_show[self.get([i, x])[0]], end="  ")
                elif self.get([i, x])[1] == "1":
                    print(Fore.GREEN + " " + peice_show[self.get([i, x])[0]], end="  ")
                else:
                    print(Fore.GREEN, end="    ")
            print(Back.RESET)
            print("", end="    ")
            for x in range(b_s):
                if [i, x] in highlight:
                    print(Back.YELLOW, end="")
                else:
                    if (x + i) % 2 == 0:
                        print(Back.BLACK, end="")
                    else:
                        print(Back.WHITE, end="")
                print(Fore.GREEN, end="    ")
            print(Back.RESET)

    def get(self, pos):
        return (
            self.peices[pos[0] * 16 + pos[1] * 2]
            + self.peices[pos[0] * 16 + pos[1] * 2 + 1]
        )

    def change(self, pos, new):
        self.peices = (
            self.peices[: pos[0] * 16 + pos[1] * 2]
            + new
            + self.peices[pos[0] * 16 + pos[1] * 2 + 2 :]
        )

    def move(self, piece, new_pos):
        store = self.get(piece)
        self.change(piece, "02")
        self.change(new_pos, store)

    def move_new(self, peice, new_pos):
        new = copy.copy(self)
        new.move(peice, new_pos)
        return new

    def all_peices_of(self, color):
        store = []
        for i in range(b_s):
            for x in range(b_s):
                if self.get([i, x])[1] == color:
                    store.append([i, x])
        return store

    def king_of(self, color):
        store = []
        for i in range(b_s):
            for x in range(b_s):
                if self.get([i, x]) == ["K", color]:
                    store = [i, x]
        return store

    def moves_for(self, pos, check=True):
        kind = self.get(pos)
        if kind == "02":
            return []
        else:
            moves = []
            if kind[0] == "R" or kind[0] == "Q":
                store_pos = pos[:]
                for i in range(b_s):
                    store_pos[0] += 1
                    if store_pos[0] == b_s:
                        break
                    if not self.get(store_pos) == "02":
                        if self.get(store_pos)[1] == kind[1]:
                            break
                        else:
                            moves.append(store_pos[:])
                            break
                    moves.append(store_pos[:])
                store_pos = pos[:]
                for i in range(b_s):
                    store_pos[0] -= 1
                    if store_pos[0] == -1:
                        break
                    if not self.get(store_pos) == "02":
                        if self.get(store_pos)[1] == kind[1]:
                            break
                        else:
                            moves.append(store_pos[:])
                            break
                    moves.append(store_pos[:])
                store_pos = pos[:]
                for i in range(b_s):
                    store_pos[1] += 1
                    if store_pos[1] == b_s:
                        break
                    if not self.get(store_pos) == "02":
                        if self.get(store_pos)[1] == kind[1]:
                            break
                        else:
                            moves.append(store_pos[:])
                            break
                    moves.append(store_pos[:])
                store_pos = pos[:]
                for i in range(b_s):
                    store_pos[1] -= 1
                    if store_pos[1] == -1:
                        break
                    if not self.get(store_pos) == "02":
                        if self.get(store_pos)[1] == kind[1]:
                            break
                        else:
                            moves.append(store_pos[:])
                            break
                    moves.append(store_pos[:])

            if kind[0] == "H":
                if (
                    (pos[0] + 1 < b_s)
                    and (pos[1] + 2 < b_s)
                    and (self.get([pos[0] + 1, pos[1] + 2])[1] != kind[1])
                ):
                    moves.append([pos[0] + 1, pos[1] + 2])
                if (
                    (pos[0] + 1 < b_s)
                    and (pos[1] - 2 > -1)
                    and (self.get([pos[0] + 1, pos[1] - 2])[1] != kind[1])
                ):
                    moves.append([pos[0] + 1, pos[1] - 2])
                if (
                    (pos[0] - 1 > -1)
                    and (pos[1] + 2 < b_s)
                    and (self.get([pos[0] - 1, pos[1] + 2])[1] != kind[1])
                ):
                    moves.append([pos[0] - 1, pos[1] + 2])
                if (
                    (pos[0] - 1 > -1)
                    and (pos[1] - 2 > -1)
                    and (self.get([pos[0] - 1, pos[1] - 2])[1] != kind[1])
                ):
                    moves.append([pos[0] - 1, pos[1] - 2])
                if (
                    (pos[0] - 2 > -1)
                    and (pos[1] - 1 > -1)
                    and (self.get([pos[0] - 2, pos[1] - 1])[1] != kind[1])
                ):
                    moves.append([pos[0] - 2, pos[1] - 1])
                if (
                    (pos[0] + 2 < b_s)
                    and (pos[1] + 1 < b_s)
                    and (self.get([pos[0] + 2, pos[1] + 1])[1] != kind[1])
                ):
                    moves.append([pos[0] + 2, pos[1] + 1])
                if (
                    (pos[0] - 2 > -1)
                    and (pos[1] + 1 < b_s)
                    and (self.get([pos[0] - 2, pos[1] + 1])[1] != kind[1])
                ):
                    moves.append([pos[0] - 2, pos[1] + 1])
                if (
                    (pos[0] + 2 < b_s)
                    and (pos[1] - 1 > -1)
                    and (self.get([pos[0] + 2, pos[1] - 1])[1] != kind[1])
                ):
                    moves.append([pos[0] + 2, pos[1] - 1])
                return moves
            if kind[0] == "B" or kind[0] == "Q":
                store_pos = pos[:]
                for i in range(b_s):
                    store_pos[0] += 1
                    store_pos[1] += 1
                    if store_pos[0] == b_s:
                        break
                    if store_pos[1] == b_s:
                        break
                    if not self.get(store_pos) == "02":
                        if self.get(store_pos)[1] == kind[1]:
                            break
                        else:
                            moves.append(store_pos[:])
                            break
                    moves.append(store_pos[:])
                store_pos = pos[:]
                for i in range(b_s):
                    store_pos[0] -= 1
                    store_pos[1] += 1
                    if store_pos[0] == -1:
                        break
                    if store_pos[1] == b_s:
                        break
                    if not self.get(store_pos) == "02":
                        if self.get(store_pos)[1] == kind[1]:
                            break
                        else:
                            moves.append(store_pos[:])
                            break
                    moves.append(store_pos[:])
                store_pos = pos[:]
                for i in range(b_s):
                    store_pos[0] += 1
                    store_pos[1] -= 1
                    if store_pos[0] == b_s:
                        break
                    if store_pos[1] == -1:
                        break
                    if not self.get(store_pos) == "02":
                        if self.get(store_pos)[1] == kind[1]:
                            break
                        else:
                            moves.append(store_pos[:])
                            break
                    moves.append(store_pos[:])
                store_pos = pos[:]
                for i in range(b_s):
                    store_pos[0] -= 1
                    store_pos[1] -= 1
                    if store_pos[0] == -1:
                        break
                    if store_pos[1] == -1:
                        break
                    if not self.get(store_pos) == "02":
                        if self.get(store_pos)[1] == kind[1]:
                            break
                        else:
                            moves.append(store_pos[:])
                            break
                    moves.append(store_pos[:])
            if kind[0] == "P":
                if kind[1] == "0":
                    if not pos[0] == b_s - 1:
                        if self.get([pos[0] + 1, pos[1]]) == "02":
                            moves.append([pos[0] + 1, pos[1]])
                        if not pos[1] == b_s - 1:
                            if self.get([pos[0] + 1, pos[1] + 1])[1] == "1":
                                moves.append([pos[0] + 1, pos[1] + 1])
                        if not pos[1] == 0:
                            if self.get([pos[0] + 1, pos[1] - 1])[1] == "1":
                                moves.append([pos[0] + 1, pos[1] - 1])
                        if pos[0] == 1 and self.get([pos[0] + 2, pos[1]]) == "02":
                            moves.append([pos[0] + 2, pos[1]])
                else:
                    if not pos[0] == 0:
                        if self.get([pos[0] - 1, pos[1]]) == "02":
                            moves.append([pos[0] - 1, pos[1]])
                        if not pos[1] == b_s - 1:
                            if self.get([pos[0] - 1, pos[1] + 1])[1] == "0":
                                moves.append([pos[0] - 1, pos[1] + 1])
                        if not pos[1] == 0:
                            if self.get([pos[0] - 1, pos[1] - 1])[1] == "0":
                                moves.append([pos[0] - 1, pos[1] - 1])
                        if pos[0] == b_s - 2 and self.get([pos[0] - 2, pos[1]]) == "02":
                            moves.append([pos[0] - 2, pos[1]])

            if kind[0] == "K":
                for n in king_moves:
                    if not (
                        pos[0] + n[0] < 0
                        or pos[0] + n[0] > b_s - 1
                        or pos[1] + n[1] < 0
                        or pos[1] + n[1] > b_s - 1
                        or self.get([pos[0] + n[0], pos[1] + n[1]])[1] == kind[1]
                    ):
                        moves.append([pos[0] + n[0], pos[1] + n[1]])

            if check:
              count = 0
              while count < len(moves):
                n = moves[count]
                new = self.move_new(pos,n)
                king = new.king_of(kind[1])
                other_color = new.all_moves_for(str((int(kind[1])+1)%2),False)
                test = True
                for i in other_color:
                  if i[1] == king:
                    test = False
                if test:
                  count += 1
                else:
                  del moves[count]
            return moves

    def all_moves_for(self, color, check=True):
        all_peices = self.all_peices_of(color)
        all_moves = []
        for i in all_peices:
            new = []
            for x in self.moves_for(i, check):
                new.append([i, x])
            all_moves += new
        return all_moves

    def min_max(
        self, depth, color, maxi=True, og=True, alpha=-100, beta=0, animation=False
    ):
        if depth == 0:
            return -len(self.all_moves_for(str(color)))
        if maxi:
            value = -1000
            all_move = self.all_moves_for(str(color))
            if og:
                if depth > 1:
                    best = self.min_max(depth - 2, color)

                    del all_move[all_move.index(best)]
                    all_move = [best] + all_move
                scores = []
            for i in all_move:
                test = self.move_new(i[0], i[1])
                if animation:
                    b = (
                        "Thinking ["
                        + "+"
                        * round((all_move.index(i) / len(all_move)) * thinking_len)
                        + "_"
                        * round(
                            (1 - (all_move.index(i) / len(all_move))) * thinking_len
                        )
                        + "]"
                    )
                    print(b, end="\r")
                if og:
                    score = test.min_max(
                        depth - 1, str((int(color) + 1) % 2), False, False, alpha, beta
                    )
                    scores.append(score)
                    value = max(value, score)
                else:
                    value = max(
                        value,
                        test.min_max(
                            depth - 1,
                            str((int(color) + 1) % 2),
                            False,
                            False,
                            alpha,
                            beta,
                        ),
                    )
                alpha = max(alpha, value)
                if value > beta:
                    return value
            if og:
                return all_move[scores.index(max(scores))]
            return value
        else:
            value = 1000
            all_move = self.all_moves_for(color)
            for i in all_move:
                test = self.move_new(i[0], i[1])
                value = min(
                    value,
                    test.min_max(
                        depth - 1, str((int(color) + 1) % 2), True, False, alpha, beta
                    ),
                )
                beta = min(beta, value)
                if value < alpha:
                    return value
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
    if (
        ast.literal_eval("[" + test + "]")[0] < 0
        or ast.literal_eval("[" + test + "]")[0] > len(boar.peices) - 1
        or ast.literal_eval("[" + test + "]")[1] < 0
        or ast.literal_eval("[" + test + "]")[1] > len(boar.peices) - 1
    ):
        return [False, "Coordinates Given are Invalid"]
    if type == 0:
        if boar.get(ast.literal_eval("[" + test + "]")) == "02":
            return [False, "Square Chosen is not a Peice"]
        if boar.get(ast.literal_eval("[" + test + "]"))[1] == "1":
            return [False, "That's not your Peice!"]
        if len(boar.moves_for(ast.literal_eval("[" + test + "]"))) == 0:
            return [False, "Peice Chosen has no Possible Moves"]
        return [True, ""]
    else:
        if not ast.literal_eval("[" + test + "]") in boar.moves_for(moving):
            return [False, "Move is not Possible by Peice"]
        return [True, ""]


def best_move_LM():
    global boar
    all_moves = boar.all_moves_for("1")
    score = []
    for i in all_moves:
        b = (
            "Thinking ["
            + "+" * round((all_moves.index(i) / len(all_moves)) * thinking_len)
            + "_" * round((1 - (all_moves.index(i) / len(all_moves))) * thinking_len)
            + "]"
        )
        print(b, end="\r")
        test = boar.move_new(i[0], i[1])
        score.append(len(test.all_moves_for("0")))
    best_move = all_moves[score.index(min(score))]
    boar.move(best_move[0], best_move[1])


boar = Board()
while True:
    boar.render()
    print(Style.RESET_ALL)
    move = input("Move >>> ")
    while not invalid_move(move)[0]:
        print(invalid_move(move)[1])
        move = input("Move >>> ")
    move = ast.literal_eval("[" + move + "]")
    pos_move = boar.moves_for(move)
    boar.render(pos_move)
    print(Style.RESET_ALL)
    to = input("To >>> ")
    while not invalid_move(to, 1, move)[0]:
        print(invalid_move(to, 1, move)[1])
        to = input("To >>> ")
    to = ast.literal_eval("[" + to + "]")
    boar.move(move, to)
    boar.render()
    print("")
    start = time.time()
    best_move = boar.min_max(3, "1", animation=True)
    print("")
    print(best_move)
    print(f"It took {time.time()-start}s to finish")
    boar.move(best_move[0],best_move[1])
