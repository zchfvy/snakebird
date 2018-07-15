import pytest
from textwrap import dedent
from game import IllegalMove, UnsafeMove, MissionComplete
from game import move_board_state
from board import load_board, draw_board


def brd(board):
    return dedent(board).strip()


def execute(board, moves):
    colors = {
        'r': 'red',
        'g': 'grn',
        'b': 'blu'}
    directions = {
        'w': 'up',
        'a': 'left',
        's': 'down',
        'd': 'right'}
    board, teleports, endpoint = load_board(board, padding=0)
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


def test_finish():
    result = None
    board = brd("""
        _rrrRO_
        #######
    """)
    with pytest.raises(MissionComplete):
        result = execute(board, "rd")
    assert result is None


def test_basic_fall():
    result = None
    board = brd("""
        __rrR__
        ###____
        #######
    """)
    result = execute(board, "rd")
    desired = brd("""
        _______
        ###rrR_
        #######
    """)
    assert result == desired


def test_spikes_fall():
    result = None
    board = brd("""
        __rrR__
        ###____
        +++++++
    """)
    with pytest.raises(UnsafeMove):
        result = execute(board, "rd")
    assert result is None


def test_spikes_partial_fall():
    result = None
    board = brd("""
        __rrR__
        ###____
        ++++___
        #######
    """)
    with pytest.raises(UnsafeMove):
        result = execute(board, "rd")
    assert result is None


def test_spikes_miss_partial_fall():
    result = None
    board = brd("""
        __rrR__
        ###____
        ++++_##
        #######
    """)
    result = execute(board, "rd")
    desired = brd("""
        _______
        ###rrR_
        ++++_##
        #######
    """)
    assert result == desired


def test_finish_fall():
    result = None
    board = brd("""
        __rrR__
        ###__O_
        _______
    """)
    with pytest.raises(MissionComplete):
        result = execute(board, "rd")
    assert result is None


def test_space_snake():
    result = None
    board = brd("""
        _______
        ___R___
        ___r___
        #######
    """)
    result = execute(board, "rw")
    desired = brd("""
        _______
        ___R___
        ___r___
        #######
    """)
    assert result == desired


def test_booster_snake():
    result = None
    board = brd("""
        _______
        ___R___
        ___r___
        __ggG__
        #######
    """)
    result = execute(board, "rw")
    desired = brd("""
        _______
        ___R___
        ___r___
        __ggG__
        #######
    """)
    assert result == desired
