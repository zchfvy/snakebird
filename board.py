#!/usr/bin/env python
# -*- coding: utf-8 -*-


class SnakebirdBoardError(Exception):
    """Raised when there's a validaiton error with the board"""


def load_board(fname):
    board = []
    teleports = []
    endpoint = None
    rowlen = 0
    heads = []
    with open(fname, 'r') as f:
        for y, line in enumerate(f):
            row = []
            board.append(row)
            for x, char in enumerate(line):
                if char == ' ':
                    row.append('space')
                elif char == '#':
                    row.append('solid')
                elif char == '+':
                    row.append('spike')
                elif char == 'R':
                    row.append('snake red 0')
                    heads.append((x, y))
                elif char == 'G':
                    row.append('snake grn 0')
                    heads.append((x, y))
                elif char == 'B':
                    row.append('snake blu 0')
                    heads.append((x, y))
                elif char == 'r':
                    row.append('snake red')
                elif char == 'g':
                    row.append('snake grn')
                elif char == 'b':
                    row.append('snake blu')
                elif char == '1':
                    row.append('block 1')
                elif char == '2':
                    row.append('block 2')
                elif char == '3':
                    row.append('block 3')
                elif char == '4':
                    row.append('block 4')
                elif char == '5':
                    row.append('block 5')
                elif char == 'F':
                    row.append('fruit')
                elif char == 'X':
                    teleports.append((y,x))
                    row.append('space')
                elif char == 'O':
                    row.append('space')
                    if endpoint is not None:
                        raise SnakebirdBoardError("Multiple Endpoints")
                    endpoint = (y, x)
                elif char == '\n':
                    continue
                else:
                    raise SnakebirdBoardError(f"Unknown char '{char}'")
            if rowlen != 0 and len(row) != rowlen:
                raise SnakebirdBoardError("Ragged array for level!")
            rowlen = len(row)
    numrows = len(board)

    for x, y in heads:
        snake = board[y][x][6:9]
        index = 0
        while True:
            index = index + 1
            # Left
            adjecents = [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]
            for ay, ax in adjecents:
                if not (0 <= ax < rowlen) or not (0 <= ay < numrows):
                    continue
                adj = board[ay][ax]
                if adj[0:5] == 'snake' and adj[6:9] == snake:
                    if len(adj) >= 11:
                        continue  # already visited!
                    board[y][x] = board[y][x] + f" {ay} {ax}"
                    board[ay][ax] = board[ay][ax] + f" {index}"
                    x, y = ax, ay
                    break
            else:
                # No more segents found!
                break

    return board, teleports, endpoint


COLOR_RST = '\033[39m'
COLOR_RED = '\033[31m'
COLOR_BLU = '\033[32m'
COLOR_GRN = '\033[33m'
COLOR_YEL = '\033[34m'
COLOR_MAG = '\033[35m'
COLOR_CYA = '\033[36m'


def draw_board(board, teleports, endpoint, color=True):
    for y, row in enumerate(board):
        rowchars = []
        for x, elem in enumerate(row):
            elclass = elem[0:5]
            if elclass == 'space':
                if endpoint == (y, x):
                    rowchars.append('\u269D')
                elif (y,x) in teleports:
                    rowchars.append('\u2609')
                else:
                    rowchars.append(' ')
            elif elclass == 'solid':
                rowchars.append('\u2588')
            elif elclass == 'spike':
                rowchars.append('\u271A')
            elif elclass == 'fruit':
                rowchars.append('\u2764')
            elif elclass == 'snake':
                clr = elem[6:9]
                if color:
                    if clr == 'red':
                        rowchars.append(COLOR_RED)
                    elif clr == 'grn':
                        rowchars.append(COLOR_BLU)
                    elif clr == 'blu':
                        rowchars.append(COLOR_GRN)
                if elem[10] == '0':
                    rowchars.append('\u263A')
                else:
                    rowchars.append('\u25CF')
                if color:
                    rowchars.append(COLOR_RST)
            elif elclass == 'block':
                num = elem[6]
                if color:
                    if num == '1':
                        rowchars.append(COLOR_CYA)
                    elif num == '2':
                        rowchars.append(COLOR_MAG)
                    elif num == '3':
                        rowchars.append(COLOR_YEL)
                    elif num == '4':
                        rowchars.append(COLOR_GRN)
                    elif num == '5':
                        rowchars.append(COLOR_BLU)
                rowchars.append('\u25A1')
                if color:
                    rowchars.append(COLOR_RST)
        print(''.join(rowchars))


if __name__ == '__main__':
    import sys
    board = load_board(sys.argv[1])
    draw_board(*board)
