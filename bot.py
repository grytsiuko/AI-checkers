import asyncio

from env import SERVER_URL


class Bot:
    def __init__(self, name):
        self.name = name

    def start(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self._start())
        loop.close()

    async def _start(self):
        print(f'Bot {self.name} init')
        print(SERVER_URL)
        await asyncio.sleep(0.5)
