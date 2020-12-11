class MetaInfo:
    def __init__(self, data=None):
        if data is not None:
            self.token = data['token']
            self.self_color = data['color']
            self.self_number = 1 if self.self_color == 'RED' else 2
            self.opponent_color = 'BLACK' if self.self_color == 'RED' else 'RED'
            self.opponent_number = 3 - self.self_number
