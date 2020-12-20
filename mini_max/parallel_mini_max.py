import multiprocessing
import time
from time import sleep

from mini_max.mini_max_base import MiniMaxBase
import copy

manager = multiprocessing.Manager()


def start(board, meta_info, depth, heuristic, index, th_dic):
    base_mini_max = MiniMaxBase(board, meta_info, depth, heuristic)
    index = index
    th_dic[index] = base_mini_max.find_best_move()
    print(f'{index} done {th_dic}')


class ParallelMiniMax:

    def __init__(self, board, meta_info, depth, heuristic):
        self._process_dict = {}
        self._board = board
        self._meta_info = meta_info
        self._depth = depth
        self._heuristic = heuristic
        self._final_time = None

    def _init_process(self, depth, index):
        return multiprocessing.Process(target=start, args=(
            copy.deepcopy(self._board), self._meta_info, depth, self._heuristic, index, self._process_dict
        ))

    def find_best_move(self):
        self._process_dict = manager.list([None, None, None])
        best_move = None

        process6 = self._init_process(6, 2)
        process4 = self._init_process(4, 1)
        process2 = self._init_process(2, 0)

        process6.start()
        process4.start()
        process2.start()

        while self._get_millis() + 400 < self._final_time:
            sleep(0.1)

        print(self._process_dict)
        best_move = self._process_dict[0] if self._process_dict[0] else best_move
        best_move = self._process_dict[1] if self._process_dict[1] else best_move
        best_move = self._process_dict[2] if self._process_dict[2] else best_move

        process2.terminate()
        process4.terminate()
        process6.terminate()

        return best_move

    def _get_millis(self):
        return int(round(time.time() * 1000))
