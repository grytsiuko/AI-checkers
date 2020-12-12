import asyncio
import random

import aiohttp

from api import Api
from board import Board
from meta_info import MetaInfo
from state import State
from copy import deepcopy


class Bot:

    MAX_DEPTH = 1

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

            await asyncio.sleep(0.25)
            self._update_with_last_move()
            possible_moves = self._board.get_possible_moves()
            if len(possible_moves) == 0:
                return
            move = self._find_best_move()
            await self._api.make_move(self._meta_info.token, move)
            self._board.make_move(move, self._meta_info.self_number)

    def _find_best_move(self):
        best_move = None
        best_score = float("-inf")
        possible_moves = self._board.get_possible_moves()

        for move in possible_moves:
            score = self._alpha_beta(self._board._game.board.create_new_board_from_move(move),
                                     self.MAX_DEPTH, float("-inf"),
                                     float("inf"), False)
            if best_score < score: # todo (<=) ?
                best_score = score
                best_move = move
        return best_move

    def _alpha_beta(self, board, depth, alpha, beta, is_max_turn):
        if depth <= 0 or self._is_terminal(board):
            return self._evaluate(board)

        if is_max_turn:
            value = float("-inf")
            possible_moves = board.get_possible_moves()
            for move in possible_moves:
                value = max(value,
                            self._alpha_beta(board.create_new_board_from_move(move), depth - 1, alpha, beta, False))
                # alpha = max(alpha, value)
                # if alpha >= beta:
                #     break
            return value

        else:
            value = float("inf")
            possible_moves = board.get_possible_moves()
            for move in possible_moves:
                value = min(value,
                            self._alpha_beta(board.create_new_board_from_move(move), depth - 1, alpha, beta, True))
                # beta = min(beta, value)
                # if beta <= alpha:
                #     break
            return value

    def _evaluate(self, board):  # todo make static?
        return 1

    def _is_terminal(self, board): # todo make static?
        return not board.count_movable_player_pieces(board.player_turn)

    def _update_with_last_move(self):
        for move in self._state.last_moves(self._meta_info.opponent_color):
            self._board.make_move(move, self._meta_info.opponent_number)
