import time


class State:
    def __init__(self, data=None):
        self._data = data

    def is_finished(self):
        return self._data['is_finished']

    def is_color_move(self, color):
        return self._data['whose_turn'] == color

    def last_moves(self, color):
        if self._last_move_present() and self._is_last_move_color(color):
            return self._data['last_move']['last_moves']
        else:
            return []

    def _last_move_present(self):
        return self._data['last_move'] is not None

    def _is_last_move_color(self, color):
        return self._data['last_move']['player'] == color

    def final_time(self):
        final = int(round(time.time() * 1000)) + self._data["available_time"] * 1000
        return final
