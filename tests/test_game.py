import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chess_engine
from enums import Player


def test_simple_game():
    game_state = chess_engine.game_state()

    #move white pawn
    game_state.move_piece((1, 2), (2, 2), False)
    # move black pawn
    game_state.move_piece((6, 3), (5, 3), False)
    # move white pawn
    game_state.move_piece((1, 1), (3, 1), False)
    # move black queen
    game_state.move_piece((7, 4), (3, 0), False)

    assert game_state.white_turn is True
    assert game_state.get_all_legal_moves(Player.PLAYER_1) == []