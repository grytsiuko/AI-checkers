from functools import reduce


class PositionStatistics:
    def __init__(self, board, player_number):
        self._board = board
        self._player_number = player_number
        self._pieces = self._board.searcher.get_pieces_by_player(self._player_number)

        self.amount = len(self._pieces)
        self.king_amount = reduce(
            (lambda count, piece: count + (1 if piece.king else 0)), self._pieces, 0
        )
        self.simple_amount = self.amount - self.king_amount

        self.self_side = reduce(
            (lambda count, piece: count + (1 if self._is_self_side(piece.position) else 0)), self._pieces, 0
        )
        self.opponent_side = self.amount - self.self_side

    def _is_self_side(self, position):
        if position < 17:  # left
            return self._player_number == 1  # RED - home left
        else:  # right
            return self._player_number == 2  # BLACK - home right

    def __str__(self):
        return f'simple amount  {self.simple_amount}\n' \
               f'king amount    {self.king_amount}\n' \
               f'self side      {self.self_side}\n' \
               f'opponent side  {self.opponent_side}'
