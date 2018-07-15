import pytest
from textwrap import dedent
from game import IllegalMove, InvalidMove, UnsafeMove, MissionComplete
from game import move_board_state
from board import load_board, draw_board

def brd(board):
    return dedent(board).strip()


def execute(board, moves):
    colors = {
        'r': 'red',
        'g': 'green',
        'b': 'blue'}
    directions = {
        'w': 'up',
        'a': 'left',
        's': 'down',
        'd': 'right'}
    board, teleports, endpoint = load_board(board)
    for snake, direction in zip(moves[0::2], moves[1::2]):
        board, teleports, endpoint = move_board_state(
                board, teleports, endpoint,
                colors[snake],
                directions[direction])
    return draw_board(board, teleports, endpoint,
                      color=False, fancy=False).strip()


def test_move_simple():
    result = None
    board = brd("""
        _rrrR__
        #######
    """)
    result = execute(board, "rd")
    desired = brd("""
        __rrrR_
        #######
    """)
    assert result == desired


def test_move_blocked():
    result = None
    board = brd("""
        _rrrR#
        ######
    """)

    with pytest.raises(IllegalMove):
        result = execute(board, "rd")
    assert result is None
