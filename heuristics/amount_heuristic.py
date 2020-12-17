from heuristics.current_position_statistics import CurrentPositionStatistics
from heuristics.position_statistics import PositionStatistics


class AmountHeuristic:
    CHECKER_POINTS = 1
    KING_POINTS = 2

    def __init__(self, checker_points=CHECKER_POINTS, king_points=KING_POINTS):
        self._checker_points = checker_points
        self._king_points = king_points

    def calculate(self, self_statistics: CurrentPositionStatistics, opponent_statistics: PositionStatistics):
        return + self._checker_points * self_statistics.simple_amount \
               + self._king_points * self_statistics.king_amount \
               - self._checker_points * opponent_statistics.simple_amount \
               - self._king_points * opponent_statistics.king_amount
