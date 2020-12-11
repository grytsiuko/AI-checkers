from env import SERVER_URL
from meta_info import MetaInfo
from state import State


class Api:
    def __init__(self, session=None):
        self._session = session

    async def connect(self, name) -> MetaInfo:
        async with self._session.post(
                f'{SERVER_URL}/game',
                params={'team_name': name}
        ) as resp:
            res = (await resp.json())['data']
            return MetaInfo(res)

    async def refresh_state(self) -> State:
        async with self._session.get(
                f'{SERVER_URL}/game'
        ) as resp:
            res = (await resp.json())['data']
            return State(res)

    async def make_move(self, token, move):
        json = {'move': move}
        headers = {'Authorization': f'Token {token}'}
        async with self._session.post(
                f'{SERVER_URL}/move',
                json=json,
                headers=headers
        ):
            pass
