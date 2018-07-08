#!/usr/bin/env python
# -*- coding: utf-8 -*-


class SnakebirdBoardError(Exception):
    """Raised when there's a validaiton error with the board"""


def load_board(fname):
    board = []
    rowlen = 0
    with open(fname, 'r') as f:
        for line in f:
            row = []
            board.append(row)
            for char in line:
                if char == ' ':
                    row.append('space')
                elif char == '#':
                    row.append('solid')
                elif char == '+':
                    row.append('spike')
                elif char == 'R':
                    row.append('snake red head')
                elif char == 'G':
                    row.append('snake grn head')
                elif char == 'B':
                    row.append('snake blu head')
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
                    row.append('telep')
                elif char == '\n':
                    continue
                else:
                    raise SnakebirdBoardError(
                            f"Unknown char '{char}'")
            if rowlen != 0 and len(row) != rowlen:
                raise SnakebirdBoardError(
                        "Ragged array for level!")

    return board


COLOR_RST = '\033[39m'
COLOR_RED = '\033[31m'
COLOR_BLU = '\033[32m'
COLOR_GRN = '\033[33m'
COLOR_YEL = '\033[34m'
COLOR_MAG = '\033[35m'
COLOR_CYA = '\033[36m'


def draw_board(board, color=True):
    for row in board:
        rowchars = []
        for elem in row:
            elclass = elem[0:5]
            if elclass == 'space':
                rowchars.append(' ')
            elif elclass == 'solid':
                rowchars.append('\u2588')
            elif elclass == 'spike':
                rowchars.append('\u271A')
            elif elclass == 'telep':
                rowchars.append('\u2609')
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
                if elem[-4:] == 'head':
                    rowchars.append('\u263A')
                else:
                    rowchars.append('\u25A0')
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
    draw_board(board)
