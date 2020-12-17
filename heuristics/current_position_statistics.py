from heuristics.position_statistics import PositionStatistics


class CurrentPositionStatistics(PositionStatistics):
    def __init__(self, board, player_number):
        super().__init__(board, player_number)

    def __str__(self):
        return f'{super().__str__()}\n'
