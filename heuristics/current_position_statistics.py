from heuristics.position_statistics import PositionStatistics


class CurrentPositionStatistics(PositionStatistics):
    def __init__(self, board, player_number):
        super().__init__(board, player_number)

        # capture_moves = self._board.get_possible_capture_moves()
        # self.capture_possible_moves_amount = len(capture_moves)
        # self.capture_open_positions_amount = self._unique_starts(capture_moves)
        #
        # positional_moves = self._board.get_possible_positional_moves()
        # self.positional_possible_moves_amount = len(positional_moves)
        # self.positional_open_positions_amount = self._unique_starts(positional_moves)

    def _unique_starts(self, moves):
        return len(
            set(
                map(
                    (lambda move: move[0]),
                    moves
                )
            )
        )

    def __str__(self):
        return f'{super().__str__()}\n' \
               f'capture possible moves {self.capture_possible_moves_amount}\n' \
               f'capture open positions {self.capture_open_positions_amount}\n' \
               f'positional possible moves {self.positional_possible_moves_amount}\n' \
               f'positional open positions {self.positional_open_positions_amount}'
