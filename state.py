class State:
    def __init__(self, data=None):
        self._data = data

    def is_finished(self):
        return self._data['is_finished']

    def is_color_move(self, color):
        return self._data['whose_turn'] == color

    def last_move_present(self):
        return self._data['last_move'] is not None

    def is_last_move_color(self, color):
        return self._data['last_move']['player'] == color

    def last_moves(self):
        return self._data['last_move']['last_moves']
