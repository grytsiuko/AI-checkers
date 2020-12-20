import random

from bot import Bot
from game_board import Board
from heuristics.amount_heuristic import AmountHeuristic
from heuristics.generic_heuristic import GenericHeuristic
from meta_info import MetaInfo

MAX_COUNT_NO_CAPTURE = 100
WINNER_POINTS = 40


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
            return WINNER_POINTS if winner_index == 0 else -WINNER_POINTS
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
    # weights1 = [(12.424879018719095, 1), (16.263504183839, 1), (-8.663468683373988, 1), (-5.705007490296328, 1), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0)]
    weights1 = [(17.41116823035462, 1), (10.435190890097182, 1), (-7.965428824206731, 1), (-3.915778483892097, 1), (0.4564055792717028, 1), (2.004584341448993, 1)]
    weights2 = [(9.641645271262528, 1), (7.937580998873643, 1), (-10.91580903389827, 1), (-8.305769224686562, 1), (-1.4816960386162217, 1), (1.78721893193003, 1)]

    a = GenericHeuristic(weights1)
    # b = GenericHeuristic(weights2)
    # a = AmountHeuristic()
    b = GenericHeuristic(weights2)

    a_wins = 0
    b_wins = 0

    for i in range(0, 50):
        result = test_heuristics(a, b)
        if result == WINNER_POINTS:
            a_wins += 1
        if result == -WINNER_POINTS:
            b_wins += 1

    print()
    print(f'First wins   {a_wins}')
    print(f'Second wins  {b_wins}')
