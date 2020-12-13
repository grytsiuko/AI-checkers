from checkers import game


class GameWrapper:

    def __init__(self):
        self._game = game.Game()

    def get_possible_moves(self):
        return self._game.get_possible_moves()

    def make_move(self, move, player):
        assert self._game.whose_turn() == player
        self._game = self._game.move(move)
