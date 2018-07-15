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


def attempt_push(board, pushed, direction):
    board = copy.deepcopy(board)
    orig_board = copy.deepcopy(board)

    if direction == 'down':
        board_orient = reversed(list(enumerate(board)))
    else:
        board_orient = enumerate(board)

    for y, row in board_orient:
        if direction == 'right':
            row_orient = reversed(list(enumerate(row)))
        else:
            row_orient = enumerate(row)

        for x, elem in row_orient:
            elem_id = ' '.join(elem.split()[0:2])
            if elem_id not in pushed:
                continue

            if direction == 'left':
                t_x, t_y = x-1, y
            if direction == 'right':
                t_x, t_y = x+1, y
            if direction == 'up':
                t_x, t_y = x, y-1
            if direction == 'down':
                t_x, t_y = x, y+1

            target = board[t_y][t_x]
            target_cls = target.split()[0]

            if target_cls == 'space':
                # DO the movement
                spl = elem.split()
                if len(spl) == 5:
                    # We gotta relink a snake as we move it
                    o_y, o_x = [int(s) for s in spl[3:5]]
                    if direction == 'left':
                        n_x, n_y = o_x-1, o_y
                    if direction == 'right':
                        n_x, n_y = o_x+1, o_y
                    if direction == 'up':
                        n_x, n_y = o_x, o_y-1
                    if direction == 'down':
                        n_x, n_y = o_x, o_y+1
                    n_x, n_y = str(n_x), str(n_y)
                    elem = ' '.join(spl[0:3] + [n_y, n_x])

                board[t_y][t_x] = elem
                board[y][x] = 'space'
            elif target_cls in ['solid', 'spike', 'fruit']:
                # Cant push into a solid!
                raise IllegalMove("Cant push into solids")
            elif target_cls in ['snake', 'block']:
                # Recurse with more items
                target_id = ' '.join(target.split()[0:2])
                pushed.append(target_id)
                return attempt_push(orig_board, pushed, direction)
            else:
                raise InvalidMove(f"Cant push into {target}")

    return board


def move_board_state(board, teleports, endpoint, snake, direction):
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

    if blocker_class == 'snake' or blocker_class == 'block':
        # We need to calculate pushing
        # Try to push, will raise an exception if we cannot
        # If we can we set the blocker to space and continue
        blocker_id = ' '.join(blocker.split()[0:2])
        board = attempt_push(board, [blocker_id], direction)
        if board[t_y][t_x] != 'space':
            # Theo nly way our push suceeded yet tere is no space is
            # if we moved (were pushed) ourselves! This is illegal!
            raise IllegalMove()
        blocker = 'space'

    if blocker == 'space':

        # First check if this sapce contains the endpoint, adn do that
        # logic
        if (t_y, t_x) == endpoint:
            fruits_left = 0
            for row in board:
                for elem in row:
                    if elem == 'fruit':
                        fruits_left += 1
            if fruits_left == 0:
                raise MissionComplete()

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
                if int(snake_parts[2]) > 10:
                    exit(1)
                if len(next_seg.split()) < 5:
                    board[y][x] = f'snake {snake} {segment}'
                else:
                    board[y][x] = f'snake {snake} {segment} {next_y} {next_x}'
                x = next_x
                y = next_y
            else:
                board[y][x] = f'space'
                break

    if blocker == 'solid' or blocker == 'spikes':
        # No can do
        raise IllegalMove()

    return board, teleports, endpoint


if __name__ == '__main__':
    import sys
    from board import load_board, draw_board
    from textwrap import dedent
    board = load_board(sys.argv[1])
    while True:
        print(draw_board(*board))
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
                board = move_board_state(*board, color, direction)
            except UnsafeMove:
                print("This kills the snake")
            except IllegalMove:
                print("Cant do that")
            except MissionComplete:
                print("YOU'RE WINNER")
                exit(0)
        elif move == 'q':
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