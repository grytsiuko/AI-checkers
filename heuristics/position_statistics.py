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

        if self.amount <= 1:
            self.avg_distance = 0
        else:
            distances_sum = 0
            count = 0
            for i in range(0, len(self._pieces) - 1):
                for k in range(i + 1, len(self._pieces)):
                    distances_sum += self._calculate_distance(self._pieces[i], self._pieces[k])
                    count = count + 1
            self.avg_distance = distances_sum / count

    def _calculate_distance(self, piece1, piece2):
        row1, col1 = self._position_to_row_col(piece1.position)
        row2, col2 = self._position_to_row_col(piece2.position)

        return abs(row1 - row2) + abs(col1 - col2)

    def _position_to_row_col(self, pos):
        pos = pos - 1
        col = pos // 4
        row = pos % 4
        row = row * 2
        if col % 2 == 0:
            row = row + 1
        return row, col

    def _is_self_side(self, position):
        if position < 17:  # left
            return self._player_number == 1  # RED - home left
        else:  # right
            return self._player_number == 2  # BLACK - home right

    def __str__(self):
        return f'simple amount  {self.simple_amount}\n' \
               f'king amount    {self.king_amount}\n' \
               f'self side      {self.self_side}\n' \
               f'opponent side  {self.opponent_side}\n' \
               f'avg distance   {self.avg_distance}' \
