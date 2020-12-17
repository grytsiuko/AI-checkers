from functools import reduce

from heuristics.position_statistics import PositionStatistics


class CurrentPositionStatistics(PositionStatistics):
    def __init__(self, pieces):
        super().__init__(pieces)

    def __str__(self):
        return f'{super().__str__()}\n'
