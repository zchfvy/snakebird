#!/usr/bin/env python
# -*- coding: utf-8 -*-


class SnakebirdBoardError(Exception):
    """Raised when there's a validaiton error with the board"""


COLOR_RST = '\033[39m'
COLOR_RED = '\033[31m'
COLOR_BLU = '\033[32m'
COLOR_GRN = '\033[33m'
COLOR_YEL = '\033[34m'
COLOR_MAG = '\033[35m'
COLOR_CYA = '\033[36m'


# Board table, contains:
# element_id, symbol, fancy_symbol, color
# Symbols are amtched in order fist to last
# So snake heads have to come before bodies
boardtable = [
    ('space',       ' ', ' ',      None),
    ('solid',       '#', '\u2588', None),
    ('spike',       '+', '\u271A', None),
    ('snake red 0', 'R', '\u263A', COLOR_RED),
    ('snake grn 0', 'G', '\u263A', COLOR_GRN),
    ('snake blu 0', 'B', '\u263A', COLOR_BLU),
    ('snake red',   'r', '\u25CF', COLOR_RED),
    ('snake grn',   'g', '\u25CF', COLOR_GRN),
    ('snake blu',   'b', '\u25CF', COLOR_BLU),
    ('block 1',     '1', '\u25A1', COLOR_CYA),
    ('block 2',     '2', '\u25A1', COLOR_YEL),
    ('block 3',     '3', '\u25A1', COLOR_MAG),
    ('block 4',     '4', '\u25A1', COLOR_BLU),
    ('block 5',     '5', '\u25A1', COLOR_GRN),
    ('fruit',       'F', '\u2764', None),
        ]

# Specials table, teleport and endpoint
specials = [
    ('teleport',     'X', '\u2609', None),
    ('endpoint',     'O', '\u269D', None),
]
specials_lut = {s[0]: s[1:] for s in specials}

# Table of characters to completely ignore
ignore = ['\n']


def load_board(fname):
    board = []
    teleports = []
    endpoint = None
    rowlen = 0
    with open(fname, 'r') as f:
        for y, line in enumerate(f):
            row = []
            board.append(row)
            print('')
            for x, char in enumerate(line):
                for spc in specials:
                    if spc[1] == char:
                        row.append('space')
                        if spc[0] == 'teleport':
                            teleports.append((y,x))
                        if spc[0] == 'endpoint':
                            if endpoint is not None:
                                raise SnakebirdBoardError("Multiple Endpoints")
                            endpoint = (y, x)
                        break
                else:
                    for brd in boardtable:
                        if brd[1] == char:
                            print(brd[0], end=' ')
                            row.append(brd[0])
                            break
                    else:
                        if char not in ignore:
                            raise SnakebirdBoardError(f"Unknown char '{char}'")
            rowlen = len(row)
        numrows = len(board)

    heads = []
    for y, line in enumerate(board):
        for x, elem in enumerate(line):
            if elem in['snake red 0', 'snake grn 0', 'snake blu 0']:
                heads.append((y,x))
    for y, x in heads:
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



def draw_board(board, teleports, endpoint, color=True, fancy=True):
    if fancy:
        idx = 2
    else:
        idx = 1
    for y, row in enumerate(board):
        rowchars = []
        for x, elem in enumerate(row):
            if elem == 'space':
                if endpoint == (y, x):
                    rowchars.append(specials_lut['endpoint'][idx-1])
                    continue
                elif (y,x) in teleports:
                    rowchars.append(specials_lut['teleport'][idx-1])
                    continue
            for brd in boardtable:
                if elem.startswith(brd[0]):
                    if color and brd[3]:
                        rowchars.append(brd[3])
                    rowchars.append(brd[idx])
                    if color and brd[3]:
                        rowchars.append(COLOR_RST)
                    break
        print(''.join(rowchars))


if __name__ == '__main__':
    import sys
    board = load_board(sys.argv[1])
    draw_board(*board)
