from functools import reduce
from checkers.board_searcher import BoardSearcher
from checkers.board_initializer import BoardInitializer
import collections


class Board:

    def __init__(self):
        self.player_turn = 1
        self.width = 4
        self.height = 8
        self.position_count = self.width * self.height
        self.rows_per_user_with_pieces = 3
        self.position_layout = {}
        self.piece_requiring_further_capture_moves = None
        # self.previous_move_was_capture = False
        self.searcher = BoardSearcher()
        BoardInitializer(self).initialize()
        self.add_piece_props()

    def add_piece_props(self):
        for piece in self.pieces:
            piece.captured_info = collections.deque()
            piece.king_trace = collections.deque()

    def make_move(self, move, player):  # true move(not minimax)
        assert self.player_turn == player
        piece = self.searcher.get_piece_by_position(move[0])
        self.do_move(move)
        piece.captured_info = collections.deque()
        piece.king_trace = collections.deque()

    def do_move(self, move):
        if move in self.get_possible_capture_moves():
            self.perform_capture_move(move)
            return True
        else:
            self.perform_positional_move(move)
            return False

    def do_reverse_move(self, move, was_captured):
        move.reverse()  # todo new list?

        piece = self.searcher.get_piece_by_position(move[0])
        piece.king = piece.king_trace.popleft()
        piece.possible_capture_moves = None  # todo optimize build?
        piece.possible_positional_moves = None

        if was_captured:
            info = piece.captured_info.popleft()
            enemy_piece = info["piece"]
            enemy_piece.position = info["position"]
            enemy_piece.captured = False

            piece.capture_move_enemies[move[0]] = enemy_piece

            if self.piece_requiring_further_capture_moves is None:
                self.switch_turn()

            self.piece_requiring_further_capture_moves = info["req_moves"]

        else:
            self.switch_turn()

        piece.move(move[1])
        self.pieces = sorted(self.pieces, key=lambda piece: piece.position if piece.position else 0)
        move.reverse()

    def count_movable_player_pieces(self, player_number=1):
        return reduce((lambda count, piece: count + (1 if piece.is_movable() else 0)),
                      self.searcher.get_pieces_by_player(player_number), 0)

    def get_possible_moves(self):
        capture_moves = self.get_possible_capture_moves()

        return capture_moves if capture_moves else self.get_possible_positional_moves()

    def get_possible_capture_moves(self):
        return reduce((lambda moves, piece: moves + piece.get_possible_capture_moves()),
                      self.searcher.get_pieces_in_play(), [])

    def get_possible_positional_moves(self):
        return reduce((lambda moves, piece: moves + piece.get_possible_positional_moves()),
                      self.searcher.get_pieces_in_play(), [])

    def position_is_open(self, position):
        return not self.searcher.get_piece_by_position(position)

    def perform_capture_move(self, move):
        # self.previous_move_was_capture = True
        piece = self.searcher.get_piece_by_position(move[0])
        originally_was_king = piece.king
        enemy_piece = piece.capture_move_enemies[move[1]]
        piece.captured_info.appendleft({"piece": enemy_piece,
                                        "position": enemy_piece.position,
                                        "req_moves": self.piece_requiring_further_capture_moves})
        enemy_piece.capture()
        self.move_piece(move)
        further_capture_moves_for_piece = [capture_move for capture_move in self.get_possible_capture_moves() if
                                           move[1] == capture_move[0]]

        if further_capture_moves_for_piece and (originally_was_king == piece.king):
            self.piece_requiring_further_capture_moves = self.searcher.get_piece_by_position(move[1])
        else:
            self.piece_requiring_further_capture_moves = None
            self.switch_turn()

    def perform_positional_move(self, move):
        # self.previous_move_was_capture = False
        self.move_piece(move)
        self.switch_turn()

    def switch_turn(self):
        self.player_turn = 1 if self.player_turn == 2 else 2

    def move_piece(self, move):
        piece = self.searcher.get_piece_by_position(move[0])
        piece.king_trace.appendleft(piece.king)
        piece.move(move[1])
        self.pieces = sorted(self.pieces, key=lambda piece: piece.position if piece.position else 0)

    def is_valid_row_and_column(self, row, column):
        if row < 0 or row >= self.height:
            return False

        if column < 0 or column >= self.width:
            return False

        return True

    def print(self):
        print("########################")
        for i in range(0, 8):
            for k in range(0, 8):
                flag = False
                for piece in self.pieces:
                    if piece.captured:
                        continue
                    pos = piece.position - 1
                    if k % 2 == 0:
                        row = (i - 1 ) / 2
                    else:
                        row = i / 2
                    col = k
                    if col * 4 + row == pos:
                        king_char = '|' if piece.king else ' '
                        print(king_char + str(piece.player) + king_char, end='')
                        flag = True
                        break
                if not flag:
                    print(' - ', end='')
            print()

        print("########################")

    def __setattr__(self, name, value):
        super(Board, self).__setattr__(name, value)

        if name == 'pieces':
            [piece.reset_for_new_board() for piece in self.pieces]

            self.searcher.build(self)
