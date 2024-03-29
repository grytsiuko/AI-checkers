import random

from heuristics.current_position_statistics import CurrentPositionStatistics
from heuristics.position_statistics import PositionStatistics


class MiniMaxBase:

    def __init__(self, board, meta_info, depth, heuristic):
        self._board = board
        self._meta_info = meta_info
        self._depth = depth
        self._heuristic = heuristic

    def find_best_move(self):
        best_move = None
        best_score = None
        possible_moves = self._board.get_possible_moves()
        if len(possible_moves) == 1:
            return possible_moves[0]

        random.shuffle(possible_moves)

        for move in possible_moves:
            score = self._alpha_beta_call(
                move,
                self._depth,
                float('-inf') if best_score is None else best_score,
                float("inf")
            )
            if best_score is None or best_score < score:
                best_score = score
                best_move = move
        return best_move

    def _alpha_beta_call(self, move, depth, alpha, beta):
        was_captured = self._board.do_move(move)
        new_depth = depth if self._board.piece_requiring_further_capture_moves is not None else depth - 1  # todo if capture_moves more than 1 it can take some time
        score = self._alpha_beta(new_depth, alpha, beta)
        self._board.do_reverse_move(move, was_captured)
        return score

    def _alpha_beta(self, depth: int, alpha: float, beta: float):
        if depth <= 0 and len(self._board.get_possible_capture_moves()) == 0:  # or self._is_terminal(board):
            return self._apply_heuristic()

        if self._meta_info.self_number == self._board.player_turn:
            value = float("-inf")
            possible_moves = self._board.get_possible_moves()
            random.shuffle(possible_moves)

            for move in possible_moves:
                value = max(value, self._alpha_beta_call(move, depth, alpha, beta))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value

        else:
            value = float("inf")
            possible_moves = self._board.get_possible_moves()
            random.shuffle(possible_moves)

            for move in possible_moves:
                value = min(value, self._alpha_beta_call(move, depth, alpha, beta))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value

    def _apply_heuristic(self):
        self_statistics = CurrentPositionStatistics(self._board, self._meta_info.self_number)
        opponent_statistics = PositionStatistics(self._board, self._meta_info.opponent_number)

        heuristic = self._heuristic.calculate(
            self_statistics=self_statistics, opponent_statistics=opponent_statistics
        )

        return heuristic
