import asyncio
import aiohttp

from env import SERVER_URL


class Bot:
    def __init__(self, name):
        self._name = name
        self._color = None
        self._token = None
        self._session = None

    def start(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self._start(loop))
        loop.close()

    async def _start(self, loop):
        self._session = aiohttp.ClientSession(loop=loop)
        await self._connect()

        print(f'Bot {self._name} init - {self._color}, {self._token}')

        await self._session.close()

    async def _connect(self):
        async with self._session.post(
                f'{SERVER_URL}/game',
                params={'team_name': self._name}
        ) as resp:
            res = (await resp.json())['data']
            self._color = res['color']
            self._token = res['token']
