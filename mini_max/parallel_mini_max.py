import multiprocessing
import time
from time import sleep

from mini_max.mini_max_base import MiniMaxBase
import copy


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
        self._manager = multiprocessing.Manager()
        self._depths_list = [depth, depth*2, depth*3]

    def _init_process(self, depth, index):
        return multiprocessing.Process(target=start, args=(
            copy.deepcopy(self._board), self._meta_info, depth, self._heuristic, index, self._process_dict
        ))

    def find_best_move(self):
        depths_amount = len(self._depths_list)

        self._process_dict = self._manager.list([None]*depths_amount)
        best_move = None

        processes = []

        for i in range(0, depths_amount):
            process = self._init_process(self._depths_list[i], i)
            processes.append(process)
            process.start()

        while self._get_millis() + 400 < self._final_time:
            sleep(0.1)

        print(self._process_dict)

        for i in range(0, depths_amount):
            best_move = self._process_dict[i] if self._process_dict[i] else best_move
            processes[i].terminate()

        return best_move

    def _get_millis(self):
        return int(round(time.time() * 1000))
