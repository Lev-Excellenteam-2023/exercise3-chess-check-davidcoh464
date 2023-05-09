import os
import sys
from unittest.mock import Mock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Piece import Knight
from enums import Player


def peaceful_moves(player: Player, point: tuple):
    """
    Generates all possible movements of a knight on a given board, without considering any other pieces.
    Parameters:
        player (Player): The type of players on the rest of the board, used to determine if a square is empty or occupied.
        point (tuple): A tuple of two integers representing the row and column indices of the knight's position on the board.
    Returns:
        A list of tuples representing all possible movements of the knight on the given board that do not involve taking any other pieces.
    """
    game_state_mock = Mock()
    game_state_mock.get_piece.side_effect = lambda x, y: player if x in range(8) and y in range(8) else None
    knight = Knight('n', point[0], point[1], Player.PLAYER_1)
    return knight.get_valid_peaceful_moves(game_state_mock)


def test_get_valid_peaceful_moves_all_empty():
    moves = peaceful_moves(Player.EMPTY,(3, 4))
    expect_moves = {(1, 3), (1, 5), (2, 2), (2, 6), (4, 2), (4, 6), (5, 5), (5, 3)}
    assert set(moves) == expect_moves


def test_get_valid_peaceful_moves_knight_at_edge():
    moves = peaceful_moves(Player.EMPTY, (0, 0))
    expect_moves = {(2, 1), (1, 2)}
    assert set(moves) == expect_moves


def test_get_valid_peaceful_moves_all_occupied():
    moves = peaceful_moves(Player.PLAYER_1, (3, 4))
    assert moves == []


def takes_moves(is_valid_piece: bool, player: Player, point: tuple = (3, 4)):
    """
    Helper function for testing Knight:get_valid_piece_takes()
    Args:
    is_valid_piece (bool): A boolean indicating whether the square containing the knight's potential move is a valid piece.
    player (Player): The player of the piece on the square being evaluated.
    point (tuple, optional): The position of the knight. Defaults to (3, 4).
    Returns:
    A list of tuples, each tuple representing a valid move that the knight can make to take an opponent's piece.
    Each tuple contains the coordinates of the square that the knight can move to. If no valid moves are possible, an empty list is returned.
    Example:
    >> takes_moves(True, Player.PLAYER_2, (2, 5))
    [(0, 4), (0, 6), (1, 3), (1, 7), (3, 3), (3, 7), (4, 4), (4, 6)]
    """
    game_state_mock = Mock()
    game_state_mock.is_valid_piece.return_value = is_valid_piece
    game_state_mock.get_piece.return_value.get_player.return_value = player
    knight = Knight('n', point[0], point[1], Player.PLAYER_1)
    return knight.get_valid_piece_takes(game_state_mock)


def test_get_valid_piece_takes_with_no_valid_moves():
    assert takes_moves(False, Player.EMPTY) == []


def test_get_valid_piece_takes_with_valid_moves():
    moves = takes_moves(True, Player.EMPTY)
    expected_moves = {(1, 3), (1, 5), (2, 2), (2, 6), (4, 2), (4, 6), (5, 5), (5, 3)}
    assert len(moves) == 8
    assert set(moves) == expected_moves


def test_get_valid_piece_takes_with_same_player_piece():
    moves = takes_moves(True, Player.PLAYER_1)
    assert moves == []


def test_get_valid_piece_moves_peace_and_take():
    player1 = Mock()
    player1.get_player.return_value = Player.PLAYER_1

    game_state_mock = Mock()
    game_state_mock.get_piece.side_effect = lambda x, y: Player.EMPTY if x in range(4) and y in range(8) \
        else player1 if x in range(4, 8) and y in range(8) else None
    game_state_mock.is_valid_piece.side_effect = lambda x, y: False if x in range(4) and y in range(8) else True

    knight = Knight('n', 3, 4, Player.PLAYER_2)
    peaceful_moves = {(1, 3), (1, 5), (2, 2), (2, 6)}
    piece_takes = {(4, 2), (4, 6), (5, 3), (5, 5)}
    expected_moves = peaceful_moves.union(piece_takes)
    moves = knight.get_valid_piece_moves(game_state_mock)

    assert len(moves) == 8
    assert set(moves) == expected_moves
    assert set(knight.get_valid_peaceful_moves(game_state_mock)) == peaceful_moves
    assert set(knight.get_valid_piece_takes(game_state_mock)) == piece_takes
