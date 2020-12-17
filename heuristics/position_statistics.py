from functools import reduce


class PositionStatistics:
    def __init__(self, board, player_number):
        self._board = board
        self._pieces = self._board.searcher.get_pieces_by_player(player_number)
        self.amount = len(self._pieces)
        self.king_amount = reduce(
            (lambda count, piece: count + (1 if piece.king else 0)), self._pieces, 0
        )
        self.simple_amount = self.amount - self.king_amount

    def __str__(self):
        return f'simple amount  {self.simple_amount}\n' \
               f'king amount    {self.king_amount}'
