import random

from bot import Bot
from game_board import Board
from heuristics.generic_heuristic import GenericHeuristic
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

        # print(f'{board.player_turn} - {move}')

        if move is None:
            winner_number = 3 - board.player_turn
            winner_index = winner_number - 1
            return 1 if winner_index == 0 else -1
        if count >= MAX_COUNT_NO_CAPTURE:
            return len(board.searcher.get_pieces_by_player(1)) - len(board.searcher.get_pieces_by_player(2))

        board.do_move(move)
        count = count + 1


def test_heuristics(a, b):
    b1 = Bot("A", 2, a)
    b2 = Bot("B", 2, b)
    return test_bots(b1, b2)


def random_pair():
    return (
        random.uniform(GenericHeuristic.MIN_COEF, GenericHeuristic.MAX_COEF),
        random.randint(GenericHeuristic.MIN_POW, GenericHeuristic.MAX_POW)
    )


def random_generic_heuristic_weights():
    ans = []
    while len(ans) < GenericHeuristic.PARAMETER_LIST_LENGTH:
        ans.append(random_pair())
    return ans


if __name__ == '__main__':
    weights1 = random_generic_heuristic_weights()
    weights2 = random_generic_heuristic_weights()

    print(weights1)
    print(weights2)

    a = GenericHeuristic(weights1)
    b = GenericHeuristic(weights2)

    winner = test_heuristics(a, b)
    print(f'winner (0 - first, 1 - second, None - tie): {winner}')
