class AmountHeuristic:
    CHECKER_POINTS = 1
    KING_POINTS = 2

    def __init__(self, checker_points=CHECKER_POINTS, king_points=KING_POINTS):
        self._checker_points = checker_points
        self._king_points = king_points

    def calculate(
            self,
            self_simple_amount,
            self_king_amount,
            opponent_simple_amount,
            opponent_king_amount,
    ):
        return + self._checker_points * self_simple_amount \
               + self._king_points * self_king_amount \
               - self._checker_points * opponent_simple_amount \
               - self._king_points * opponent_king_amount
