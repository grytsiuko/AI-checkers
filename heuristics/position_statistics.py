from functools import reduce


class PositionStatistics:
    def __init__(self, pieces):
        self._pieces = pieces
        self.amount = len(pieces)
        self.king_amount = reduce(
            (lambda count, piece: count + (1 if piece.king else 0)), self._pieces, 0
        )
        self.simple_amount = self.amount - self.king_amount

    def __str__(self):
        return f'simple amount  {self.simple_amount}\n' \
               f'king amount    {self.king_amount}'
