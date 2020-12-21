import asyncio

import aiohttp
# from checkers.board import Board

from api import Api
from game_board import Board
from heuristics.legendary_heuristic import LegendaryHeuristic
from heuristics.space_heuristic import SpaceHeuristic
from meta_info import MetaInfo
from mini_max.mini_max_base import MiniMaxBase
from state import State


class Bot:

    def __init__(self, name, depth, heuristic=SpaceHeuristic(), mini_max_class=MiniMaxBase):
        self._name = name
        self._depth = depth
        self._board: Board = Board()
        self._state: State = State()
        self._meta_info: MetaInfo = MetaInfo()
        self._api: Api = Api()
        self._mini_max = None
        self._heuristic = heuristic
        self._mini_max_class = mini_max_class

    def start(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self._start(loop))
        loop.close()

    async def _start(self, loop):
        session = aiohttp.ClientSession(loop=loop)
        self._api = Api(session)
        self._meta_info = await self._api.connect(self._name)
        self._init_mini_max()

        await self._play()
        await session.close()

    def _init_mini_max(self):
        self._mini_max = self._mini_max_class(self._board, self._meta_info, self._depth, self._heuristic)

    async def _play(self):
        while True:
            while True:
                self._state = await self._api.refresh_state()
                self._mini_max._final_time = self._state.final_time()
                if self._state.is_finished():
                    return
                if self._state.is_color_move(self._meta_info.self_color):
                    break

            self._update_with_last_move()
            move = self._mini_max.find_best_move()
            if move is None:
                print("None move!!!")
                return
            await self._api.make_move(self._meta_info.token, move)
            self._board.make_move(move, self._meta_info.self_number)

    def _update_with_last_move(self):
        for move in self._state.last_moves(self._meta_info.opponent_color):
            self._board.make_move(move, self._meta_info.opponent_number)
