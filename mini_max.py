
import random
from functools import reduce


class MiniMax:

    # MAX_DEPTH = 6
    CHECKER_POINTS = 1
    KING_POINTS = 2

    def __init__(self, board, meta_info, depth):
        self._board = board
        self._meta_info = meta_info
        self._depth = depth

    def find_best_move(self):
        best_move = None
        best_score = None
        possible_moves = self._board.get_possible_moves()
        if len(possible_moves) == 1:
            return possible_moves[0]

        random.shuffle(possible_moves)

        for move in possible_moves:
            # print(f'MAYBEEEEEEEEEEEEEEEEEE {move}')
            # start = datetime.datetime.now()
            # was_captured = self._board.do_move(move)
            # self._board.do_reverse_move(move, was_captured)
            # end = datetime.datetime.now()
            # print(end - start)
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
        # self._board.print()
        # print(move)
        # self._apply_heuristic()
        score = self._alpha_beta(new_depth, alpha, beta)
        self._board.do_reverse_move(move, was_captured)
        return score

    def _alpha_beta(self, depth: int, alpha: float, beta: float):
        if depth <= 0:  # or self._is_terminal(board):
            # print('TERMINAL TERMINAL TERMINAL TERMINAL TERMINAL ')
            return self._apply_heuristic()

        if self._meta_info.self_number == self._board.player_turn:
            value = float("-inf")
            possible_moves = self._board.get_possible_moves()
            random.shuffle(possible_moves)

            for move in possible_moves:
                value = max(value, self._alpha_beta_call(move, depth, alpha, beta))
                alpha = max(alpha, value)
                if alpha >= beta:
                    # print(f'Cutted on {depth} depth')
                    break
            return value

        else:
            value = float("inf")
            possible_moves = self._board.get_possible_moves()
            random.shuffle(possible_moves)

            for move in possible_moves:
                value = min(value, self._alpha_beta_call(move, depth, alpha, beta))
                # self._alpha_beta(board.create_new_board_from_move(move), depth - 1, alpha, beta))
                beta = min(beta, value)
                if beta <= alpha:
                    # print(f'Cutted on {depth} depth')
                    break
            return value

    def _apply_heuristic(self):  # todo make static?
        self_score = reduce(
            (lambda count, piece: count + (self.KING_POINTS if piece.king else self.CHECKER_POINTS)),
            self._board.searcher.get_pieces_by_player(self._meta_info.self_number), 0)
        opponent_score = reduce(
            (lambda count, piece: count + (self.KING_POINTS if piece.king else self.CHECKER_POINTS)),
            self._board.searcher.get_pieces_by_player(self._meta_info.opponent_number), 0)
        # print(f'HEURISTIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIC {self_score - opponent_score}')
        return self_score - opponent_score

    # def _is_terminal(self, board):  # todo make static?
    #     return not board.count_movable_player_pieces(board.player_turn)