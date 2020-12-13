from checkers.board import Board


class BoardWrap:

    def __init__(self):
        self._board: Board = Board()

    def get_possible_moves(self):
        return self._board.get_possible_moves()

    def make_move(self, move, player):
        assert self._board.player_turn == player
        if move in self._board.get_possible_capture_moves():
            self._board.perform_capture_move(move)
        else:
            self._board.perform_positional_move(move)

