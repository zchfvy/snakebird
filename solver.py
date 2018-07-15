import game
import board as gameboard
import re
import itertools
import heapq
import hashlib


def score_heuristic(board, teleports, endpoint, cur_move):
    cost_live_snake = 50
    cost_distance = 0  # Distance cost when fruit are on board
    cost_fruit = 20
    cost_fruit_distance = 2  # Cost of being far from fruit
    cost_final_distance = 2  # Distance cost when no fruit left
    cost_move_length = 1  # How many moves we amde to get here

    score = 0

    heads = []
    for y, row in enumerate(board):
        for x, elem in enumerate(row):
            is_head = re.match('^snake ... 0', elem)
            if is_head:
                heads.append((y, x))

    for y, row in enumerate(board):
        for x, elem in enumerate(row):
            is_fruit = elem == 'fruit'
            if is_fruit:
                score += cost_fruit
                fruit = (y, x)
                for head in heads:
                    dist = abs(head[0] - fruit[0]) + abs(head[1] - fruit[1])
                    score += dist * cost_fruit_distance

    for head in heads:
        score += cost_live_snake
        dist = abs(head[0] - endpoint[0]) + abs(head[1] - endpoint[1])
        if game.any_fruit_exists(board):
            score += dist * cost_distance
        else:
            score += dist * cost_final_distance

    score += cost_move_length * len(cur_move) / 2

    return score


def pprint_move(move):
    COLOR_RST = '\033[39m'
    COLOR_RED = '\033[31m'
    COLOR_BLU = '\033[34m'
    COLOR_GRN = '\033[32m'
    
    AR_LEFT = "▲"
    AR_UP = "▼"
    AR_RIGHT = "◀"
    AR_DOWN = "▶"

    lut = {
        'r': COLOR_RED,
        'g': COLOR_GRN,
        'b': COLOR_BLU,
        'w': AR_UP,
        'a': AR_LEFT,
        's': AR_DOWN,
        'd': AR_RIGHT
    }

    res = []
    for char in move:
        res.append(lut[char])
    return ' '.join(res) + COLOR_RST


def hash_board(board):
    h = hashlib.md5()
    for row in board:
        for elem in row:
            h.update(elem.encode('utf-8'))
    return h.digest()


def make_move(board, teleports, endpoint, move):
    colors = {
        'r': 'red',
        'g': 'grn',
        'b': 'blu'}
    directions = {
        'w': 'up',
        'a': 'left',
        's': 'down',
        'd': 'right'}

    color = colors[move[0]]
    direction = directions[move[1]]

    board, teleports, endpoint = game.move_board_state(
            board, teleports, endpoint, color, direction)

    return board, teleports, endpoint


def move_to_board(board, teleports, endpoint, moves):
    for move in zip(moves[0::2], moves[1::2]):
        board, teleports, endpoint = make_move(board, teleports, endpoint, move)

    return board, teleports, endpoint


def solve(board, teleports, endpoint):
    # Set of boards already dealt with (hashes of board states)
    closed_set = set()
    # Set of boards we need to deal with (priorty queue of move strings)
    open_set = []
    counter = itertools.count()
    score = score_heuristic(board, teleports, endpoint, '')
    heapq.heappush(open_set, (score, next(counter), ''))

    while True:
        # Add ourselves to the already seen states
        if len(open_set) == 0:
            raise Exception("No solution!")
        cur_score, _, cur_move = heapq.heappop(open_set)
        cur_board, _, _ = move_to_board(board, teleports, endpoint, cur_move)
        closed_set.add(hash_board(cur_board))
        
        print(gameboard.draw_board(cur_board, teleports, endpoint))
        nmoves = int(len(cur_move) / 2)
        print(f"Move #{nmoves}. Score:{cur_score}")
        print(pprint_move(cur_move))

        # First let's find all snakes and possiblem oves
        colors = []
        for y, row in enumerate(board):
            for x, elem in enumerate(row):
                is_head = re.match('^snake ... 0', elem)
                if is_head:
                    colors.append(elem[6])
        next_moves = []
        for color in colors:
            for direction in ['w', 'a', 's', 'd']:
                next_moves.append(color + direction)

        for mv in next_moves:
            move = cur_move + mv
            try:
                next_board, _, _ = make_move(
                        cur_board, teleports, endpoint, mv)
            except game.MissionComplete:
                return move  # Done! Horray
            except (game.InvalidMove, game.IllegalMove, game.UnsafeMove):
                continue
            else:
                h = hash_board(next_board)
                if h in closed_set:  # Already seen this state (a loop)
                    continue
                score = score_heuristic(next_board, teleports, endpoint, move)
                heapq.heappush(open_set, (score, next(counter), move))


if __name__ == '__main__':
    import sys
    board = gameboard.load_file(sys.argv[1])
    print(gameboard.draw_board(*board))
    sol = solve(*board)
    print(sol)
