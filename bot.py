import asyncio
import random

import aiohttp

from env import SERVER_URL
from game import Game


class Bot:
    def __init__(self, name):
        self._name = name
        self._color = None
        self._number = None
        self._opponent_number = None
        self._token = None
        self._session = None
        self._game = Game()
        self._state = None

    def start(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self._start(loop))
        loop.close()

    async def _start(self, loop):
        self._session = aiohttp.ClientSession(loop=loop)
        await self._connect()

        print(f'Bot {self._name} init - {self._color}, {self._token}')
        await self._play()

        await self._session.close()

    async def _play(self):
        while True:
            while True:
                await self._refresh_state()
                if self._state['is_finished']:
                    return
                if self._state['whose_turn'] == self._color:
                    break

            await asyncio.sleep(0.25)
            self._update_with_last_move()
            possible_moves = self._game.get_possible_moves()
            if len(possible_moves) == 0:
                return
            move = random.choice(possible_moves)
            await self._make_move(move)
            assert self._game.whose_turn() == self._number
            self._game = self._game.move(move)

    def _update_with_last_move(self):
        if self._state['last_move'] is not None and self._state['last_move']['player'] != self._color:
            for move in self._state['last_move']['last_moves']:
                assert self._game.whose_turn() == self._opponent_number
                self._game = self._game.move(move)

    async def _connect(self):
        async with self._session.post(
                f'{SERVER_URL}/game',
                params={'team_name': self._name}
        ) as resp:
            res = (await resp.json())['data']
            self._color = res['color']
            self._token = res['token']
            self._number = 1 if self._color == 'RED' else 2
            self._opponent_number = 3 - self._number

    async def _refresh_state(self):
        async with self._session.get(
                f'{SERVER_URL}/game'
        ) as resp:
            res = (await resp.json())['data']
            self._state = res

    async def _make_move(self, move):
        json = {'move': move}
        headers = {'Authorization': f'Token {self._token}'}
        async with self._session.post(
                f'{SERVER_URL}/move',
                json=json,
                headers=headers
        ) as resp:
            resp = (await resp.json())['data']
            print(f'Player {self._name} made move {move}, response: {resp}')
