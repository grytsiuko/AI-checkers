import asyncio
import random

import aiohttp
# from checkers.board import Board

from api import Api
from game_board import Board
from meta_info import MetaInfo
from state import State
from functools import reduce
import datetime


class Bot:
    MAX_DEPTH = 6
    CHECKER_POINTS = 1
    KING_POINTS = 2

    def __init__(self, name):
        self._name = name
        self._board: Board = Board()
        self._state: State = State()
        self._meta_info: MetaInfo = MetaInfo()
        self._api: Api = Api()

    def start(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self._start(loop))
        loop.close()

    async def _start(self, loop):
        session = aiohttp.ClientSession(loop=loop)
        self._api = Api(session)
        self._meta_info = await self._api.connect(self._name)

        await self._play()
        await session.close()

    async def _play(self):
        while True:
            while True:
                self._state = await self._api.refresh_state()
                if self._state.is_finished():
                    return
                if self._state.is_color_move(self._meta_info.self_color):
                    break

            # await asyncio.sleep(0.25)
            self._update_with_last_move()
            move = self._find_best_move()
            if move is None:
                print("None move!!!")
                return
            await self._api.make_move(self._meta_info.token, move)
            self._board.make_move(move, self._meta_info.self_number)

    def _find_best_move(self):
        best_move = None
        best_score = float("-inf")
        possible_moves = self._board.get_possible_moves()
        random.shuffle(possible_moves)

        for move in possible_moves:
            start = datetime.datetime.now()
            was_captured = self._board.do_move(move)
            self._board.do_reverse_move(move, was_captured)
            end = datetime.datetime.now()
            print(end - start)
            # start = datetime.datetime.now()
            # self._apply_heuristic(self._board._game.board.create_new_board_from_move(move))
            # end = datetime.datetime.now()
            # print(end - start)
            score = self._alpha_beta_call(move, self.MAX_DEPTH, best_score, float("inf"))
            if best_score <= score:
                best_score = score
                best_move = move
        return best_move

    def _alpha_beta_call(self, move, depth, alpha, beta):
        was_captured = self._board.do_move(move)
        score = self._alpha_beta(depth, alpha, beta)
        self._board.do_reverse_move(move, was_captured)
        return score

    def _alpha_beta(self, depth: int, alpha: float, beta: float):
        if depth <= 0:  # or self._is_terminal(board):
            return self._apply_heuristic()

        if self._meta_info.self_number == self._board.player_turn:
            value = float("-inf")
            possible_moves = self._board.get_possible_moves()
            random.shuffle(possible_moves)

            for move in possible_moves:
                value = max(value, self._alpha_beta_call(move, depth - 1, alpha, beta))
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
                value = min(value, self._alpha_beta_call(move, depth - 1, alpha, beta))
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
        return self_score - opponent_score

    # def _is_terminal(self, board):  # todo make static?
    #     return not board.count_movable_player_pieces(board.player_turn)

    def _update_with_last_move(self):
        for move in self._state.last_moves(self._meta_info.opponent_color):
            self._board.make_move(move, self._meta_info.opponent_number)
