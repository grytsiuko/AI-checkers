from bot import Bot
from game_board import Board
from heuristics.amount_heuristic import AmountHeuristic
from meta_info import MetaInfo

MAX_COUNT_NO_CAPTURE = 100


def test_bots(a, b):
    board = Board()
    a._board = board
    b._board = board

    a._meta_info = MetaInfo({'token': '', 'color': 'RED'})
    a._init_mini_max()

    b._meta_info = MetaInfo({'token': '', 'color': 'BLACK'})
    b._init_mini_max()

    count = 0
    while True:
        if board.get_possible_capture_moves():
            count = 0

        if board.player_turn == 1:
            move = a._mini_max.find_best_move()
        else:
            move = b._mini_max.find_best_move()

        print(f'{board.player_turn} - {move}')

        if move is None:
            winner_number = 3 - board.player_turn
            return winner_number - 1
        if count >= MAX_COUNT_NO_CAPTURE:
            return None

        board.do_move(move)
        count = count + 1


def test_heuristics(a, b):
    b1 = Bot("A", 2, a)
    b2 = Bot("B", 2, b)
    return test_bots(b1, b2)


if __name__ == '__main__':
    a = AmountHeuristic()
    b = AmountHeuristic()
    winner = test_heuristics(a, b)
    print(f'winner (0 - first, 1 - second, None - tie): {winner}')
