import random
from copy import deepcopy

from heuristics.current_position_statistics import CurrentPositionStatistics
from heuristics.position_statistics import PositionStatistics


class MiniMaxIterative:

    def __init__(self, board, meta_info, depth, heuristic):
        self._board = board
        self._meta_info = meta_info
        self._depth = depth
        self._heuristic = heuristic
        self._queue = None

    def find_best_move(self):
        ways = [[]]
        best = None
        for i in range(0,10):
            print('ways')
            print(ways)
            results = []
            for way in ways:
                captured = []
                for step in way:
                    captured.append(self._board.do_move(step))
                result = self._find_best_move_from(way)
                for i in range(len(captured) - 1, -1, -1):
                    self._board.do_reverse_move(way[i], captured[i])
                results += result
            results.sort(key=lambda x:x[0], reverse=False)
            results = results[:3]
            new_ways = []
            for result in results:
                new_ways.append(result[1])
            ways = new_ways
            if best is None or (len(results) > 0 and best[0] < results[0][0]):
                best = deepcopy(results[0])
        return best[1][0]

    def _find_best_move_from(self, way_here):
        best_move = None
        best_score = None
        possible_moves = self._board.get_possible_moves()

        random.shuffle(possible_moves)

        res = []
        for move in possible_moves:
            score = self._alpha_beta_call(
                move,
                self._depth,
                float('-inf') if best_score is None else best_score,
                float("inf")
            )
            res.append((score, deepcopy(way_here) + [move]))
        return res

    def _alpha_beta_call(self, move, depth, alpha, beta):
        was_captured = self._board.do_move(move)
        new_depth = depth if self._board.piece_requiring_further_capture_moves is not None else depth - 1
        score = self._alpha_beta(new_depth, alpha, beta)
        self._board.do_reverse_move(move, was_captured)
        return score

    def _alpha_beta(self, depth: int, alpha: float, beta: float):
        if depth <= 0 and len(self._board.get_possible_capture_moves()) == 0:
            return self._apply_heuristic()

        if self._meta_info.self_number == self._board.player_turn:
            value = float("-inf")
            possible_moves = self._board.get_possible_moves()
            random.shuffle(possible_moves)

            for move in possible_moves:
                value = max(value, self._alpha_beta_call(move, depth, alpha, beta))
                alpha = max(alpha, value)
            return value

        else:
            value = float("inf")
            possible_moves = self._board.get_possible_moves()
            random.shuffle(possible_moves)

            for move in possible_moves:
                value = min(value, self._alpha_beta_call(move, depth, alpha, beta))
                beta = min(beta, value)
            return value

    def _apply_heuristic(self):
        self_statistics = CurrentPositionStatistics(self._board, self._meta_info.self_number)
        opponent_statistics = PositionStatistics(self._board, self._meta_info.opponent_number)

        heuristic = self._heuristic.calculate(
            self_statistics=self_statistics, opponent_statistics=opponent_statistics
        )

        return heuristic
