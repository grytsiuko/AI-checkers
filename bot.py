import asyncio
import random

import aiohttp

from api import Api
from board import Board
from meta_info import MetaInfo
from state import State


class Bot:
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
            move = random.choice(possible_moves)
            await self._api.make_move(self._meta_info.token, move)
            self._board.make_move(move, self._meta_info.self_number)

    def _update_with_last_move(self):
        for move in self._state.last_moves(self._meta_info.opponent_color):
            self._board.make_move(move, self._meta_info.opponent_number)
