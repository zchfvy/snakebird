#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy


class SnakebirdMoveError(Exception):
    pass


class IllegalMove(SnakebirdMoveError):
    """The game won't let you make this move."""


class UnsafeMove(SnakebirdMoveError):
    """This kills the snake."""


class InvalidMove(SnakebirdMoveError):
    """This move doesn't make sense!"""


class MissionComplete(Exception):
    """We are done!"""


def move_board_state(board, snake, direction):
    board = copy.deepcopy(board)
    b_x, b_y = len(board[0]), len(board)

    if snake not in ['red', 'grn', 'blu']:
        raise InvalidMove(f"Unknown snake '{snake}'")
    if direction not in ['up', 'down', 'left', 'right']:
        raise InvalidMove(f"Unknown direction '{direction}'")

    def find_snake():
        for y, row in enumerate(board):
            for x, elem in enumerate(row):
                splitelem = elem.split()
                if len(splitelem) >= 3 and splitelem[2] == '0':
                    if splitelem[1] == snake:
                        return x, y
        raise InvalidMove(f"Cannot find snake '{snake}'")

    x, y = find_snake()

    if direction == 'left' and x == 0:
        raise InvalidMove(f"Moving off of board {direction}")
    if direction == 'right' and x == b_x:
        raise InvalidMove(f"Moving off of board {direction}")
    if direction == 'up' and y == 0:
        raise InvalidMove(f"Moving off of board {direction}")
    if direction == 'down' and y == b_y:
        raise InvalidMove(f"Moving off of board {direction}")

    if direction == 'left':
        t_x, t_y = x-1, y
    if direction == 'right':
        t_x, t_y = x+1, y
    if direction == 'up':
        t_x, t_y = x, y-1
    if direction == 'down':
        t_x, t_y = x, y+1

    blocker = board[t_y][t_x]
    blocker_class = blocker.split()[0]

    if blocker == 'fruit':
        # We advance the snake's head
        segment = 0
        board[t_y][t_x] = f'snake {snake} {segment} {y} {x}'
        # Build out our snake body
        while True:
            segment += 1
            snake_parts = board[y][x].split()
            if len(snake_parts) == 5:
                next_y = int(snake_parts[3])
                next_x = int(snake_parts[4])
                board[y][x] = f'snake {snake} {segment} {next_y} {next_x}'
                x = next_x
                y = next_y
            else:
                board[y][x] = f'snake {snake} {segment}'
                break

    elif blocker == 'space':
        # We advance the snake's head
        segment = 0
        board[t_y][t_x] = f'snake {snake} {segment} {y} {x}'
        # Build out our snake body
        while True:
            segment += 1
            snake_parts = board[y][x].split()
            if len(snake_parts) == 5:
                next_y = int(snake_parts[3])
                next_x = int(snake_parts[4])
                next_seg = board[next_y][next_x]
                if len(next_seg.split()) < 5:
                    board[y][x] = f'snake {snake} {segment}'
                else:
                    board[y][x] = f'snake {snake} {segment} {next_y} {next_x}'
                x = next_x
                y = next_y
            else:
                board[y][x] = f'space'
                break

    elif blocker == 'telep':
        raise NotImplemented()

    elif blocker == 'endpt':
        # We check for fruits, then delete the snake
        raise NotImplemented()

    elif blocker == 'solid' or blocker == 'spikes':
        # No can do
        raise IllegalMove()

    elif blocker_class == 'snake' or blocker_class == 'block':
        # We need to calculate pushing
        raise NotImplemented()

    else:
        raise NotImplemented(f'blocker_class')

    return board


if __name__ == '__main__':
    import sys
    from board import load_board, draw_board
    from textwrap import dedent
    board = load_board(sys.argv[1])
    while True:
        draw_board(board)
        move = input('Choose a move (h for help)')
        if len(move) == 2:
            colors = {
                'r': 'red',
                'g': 'green',
                'b': 'blue'}
            directions = {
                'w': 'up',
                'a': 'left',
                's': 'down',
                'd': 'right'}
            try:
                color = colors[move[0]]
            except KeyError:
                print(f"Invalid color {color}")
                continue
            try:
                direction = directions[move[1]]
            except KeyError:
                print(f"Invalid direction {direction}")
                continue
            try:
                board = move_board_state(board, color, direction)
            except UnsafeMove:
                print("This kills the snake")
            except IllegalMove:
                print("Cant do that")
            except MissionComplete:
                print("YOU'RE WINNER")
                exit(0)
        if move == 'q':
            exit(0)
        else:
            print(dedent("""
            q to quit

            two letters to move, the first is the
            color of the snake and the second is the
            wasd direction to move. Valid snake colors
            are r, g, b. For example if you want to move
            the red snake up print 'rw'.
            """))
            continue
