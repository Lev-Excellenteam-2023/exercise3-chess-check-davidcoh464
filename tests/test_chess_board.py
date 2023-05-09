import os
import sys
from unittest.mock import Mock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_engine import chess_ai
from enums import Player

chess_ai = chess_ai()


def mocks_player(row, col):
    piece = Mock()
    if row in (0, 1):
        piece.is_player.side_effect = lambda player: player == Player.PLAYER_1
    elif row == 7:
        piece.is_player.side_effect = lambda player: player == Player.PLAYER_2
    else:
        piece.is_player.return_value = False

    if row in (0, 7):
        if col == 0:
            piece.get_name.return_value = "r"
        elif col == 1:
            piece.get_name.return_value = "n"
        elif col == 2:
            piece.get_name.return_value = "b"
        elif col == 3:
            piece.get_name.return_value = "k"
        elif col == 4:
            piece.get_name.return_value = "q"
        elif col == 5:
            piece.get_name.return_value = "b"
        elif col == 6:
            piece.get_name.return_value = "n"
        elif col == 7:
            piece.get_name.return_value = "r"
    elif row == 1:
        piece.get_name.return_value = "p"
    return piece


def test_evaluate_board():
    game_state_mock = Mock()
    game_state_mock.get_piece.side_effect = mocks_player
    game_state_mock.is_valid_piece.side_effect = lambda x, y: True if x in (0, 1, 7) and y in range(8) else False
    evaluation_score = chess_ai.evaluate_board(game_state_mock, Player.PLAYER_1)
    assert evaluation_score == -80
    evaluation_score = chess_ai.evaluate_board(game_state_mock, Player.PLAYER_2)
    assert evaluation_score == 80


