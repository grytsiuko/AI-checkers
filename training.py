from bot import Bot
from game_board import Board
from heuristics.amount_heuristic import AmountHeuristic
from meta_info import MetaInfo


def test(a, b):
    board = Board()
    a._board = board
    b._board = board

    a._meta_info = MetaInfo({'token': '', 'color': 'RED'})
    a._init_mini_max()

    b._meta_info = MetaInfo({'token': '', 'color': 'BLACK'})
    b._init_mini_max()

    while True:
        if board.player_turn == 1:
            move = a._mini_max.find_best_move()
        else:
            move = b._mini_max.find_best_move()

        print(f'{board.player_turn} - {move}')
        if move is None:
            winner_number = 3 - board.player_turn
            return winner_number - 1
        board.do_move(move)


if __name__ == '__main__':
    a = Bot("A", 2, AmountHeuristic())
    b = Bot("B", 4, AmountHeuristic())
    winner = test(a, b)
    print(f'winner (0 - first, 1 - second) {winner}')
