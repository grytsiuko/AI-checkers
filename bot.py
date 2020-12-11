import asyncio
import aiohttp

from env import SERVER_URL
from game import Game


class Bot:
    def __init__(self, name):
        self._name = name
        self._color = None
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
            await self._refresh_state()
            if self._state['whose_turn'] == self._color:
                break
        print(f'Bot {self._name} is moving')

    async def _connect(self):
        async with self._session.post(
                f'{SERVER_URL}/game',
                params={'team_name': self._name}
        ) as resp:
            res = (await resp.json())['data']
            self._color = res['color']
            self._token = res['token']

    async def _refresh_state(self):
        async with self._session.get(
                f'{SERVER_URL}/game'
        ) as resp:
            res = (await resp.json())['data']
            self._state = res
