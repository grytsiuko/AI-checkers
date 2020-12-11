import asyncio
import random

import aiohttp

from env import SERVER_URL
from board import Board
from meta_info import MetaInfo
from state import State


class Bot:
    def __init__(self, name):
        self._name = name
        self._session = None
        self._board: Board = Board()
        self._state: State = State()
        self._meta_info: MetaInfo = MetaInfo()

    def start(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self._start(loop))
        loop.close()

    async def _start(self, loop):
        self._session = aiohttp.ClientSession(loop=loop)
        await self._connect()

        print(f'Bot {self._name} init - {self._meta_info.self_color}, {self._meta_info.token}')
        await self._play()

        await self._session.close()

    async def _play(self):
        while True:
            while True:
                await self._refresh_state()
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
            await self._make_move(move)
            self._board.make_move(move, self._meta_info.self_number)

    def _update_with_last_move(self):
        if self._state.last_move_present() and self._state.is_last_move_color(self._meta_info.opponent_color):
            for move in self._state.last_moves():
                self._board.make_move(move, self._meta_info.opponent_number)

    async def _connect(self):
        async with self._session.post(
                f'{SERVER_URL}/game',
                params={'team_name': self._name}
        ) as resp:
            res = (await resp.json())['data']
            self._meta_info = MetaInfo(res)

    async def _refresh_state(self):
        async with self._session.get(
                f'{SERVER_URL}/game'
        ) as resp:
            res = (await resp.json())['data']
            self._state = State(res)

    async def _make_move(self, move):
        json = {'move': move}
        headers = {'Authorization': f'Token {self._meta_info.token}'}
        async with self._session.post(
                f'{SERVER_URL}/move',
                json=json,
                headers=headers
        ) as resp:
            resp = (await resp.json())['data']
            print(f'Player {self._name} made move {move}, response: {resp}')
