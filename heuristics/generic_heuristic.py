from heuristics.current_position_statistics import CurrentPositionStatistics
from heuristics.position_statistics import PositionStatistics


class GenericHeuristic:
    PARAMETER_LIST_LENGTH = 4
    MIN_COEF = -20
    MAX_COEF = 20
    MIN_POW = 1
    MAX_POW = 1

    def __init__(self, weights):
        self._weights = weights

    def calculate(self, self_statistics: CurrentPositionStatistics, opponent_statistics: PositionStatistics):
        return + self._calculate_param(0, self_statistics.simple_amount) \
               + self._calculate_param(1, self_statistics.king_amount) \
               + self._calculate_param(2, opponent_statistics.simple_amount) \
               + self._calculate_param(3, opponent_statistics.king_amount) \
               # + self._calculate_param(4, self_statistics.self_side) \
               # + self._calculate_param(5, self_statistics.opponent_side) \
               # + self._calculate_param(6, opponent_statistics.self_side) \
               # + self._calculate_param(7, opponent_statistics.opponent_side) \
               # + self._calculate_param(4, self_statistics.avg_distance) \
               # + self._calculate_param(5, opponent_statistics.avg_distance) \
               # + self._calculate_param(10, self_statistics.capture_possible_moves_amount) \
               # + self._calculate_param(11, self_statistics.capture_open_positions_amount) \
               # + self._calculate_param(12, self_statistics.positional_possible_moves_amount) \
               # + self._calculate_param(13, self_statistics.positional_open_positions_amount) \

    def _calculate_param(self, index, param):
        return self._weights[index][0] * (param ** self._weights[index][1])
