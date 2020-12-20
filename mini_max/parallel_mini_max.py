import random
import time
from functools import reduce
from time import sleep

from heuristics.current_position_statistics import CurrentPositionStatistics
from heuristics.position_statistics import PositionStatistics
from mini_max.mini_max_base import MiniMaxBase
import threading
import copy


threads_dict = {}

class Worker:

    def __init__(self, board, meta_info, depth, heuristic, index):
        self._base_mini_max = MiniMaxBase(board, meta_info, depth, heuristic)
        self._index = index

    def start(self):
        global threads_dict
        threads_dict[self._index] = self._base_mini_max.find_best_move()




class ParallelMiniMax:

    def __init__(self, board, meta_info, depth, heuristic):
        self._board = board
        self._meta_info = meta_info
        self._depth = depth
        self._heuristic = heuristic
        self._final_time = None

    def _start_in_thread(self, depth, index):

        thread = threading.Thread(target=Worker(copy.deepcopy(self._board), self._meta_info, depth, self._heuristic, index).start)
        thread.start()
        thread.join()
        return thread


    def find_best_move(self):
        global threads_dict
        threads_dict = {2: None, 4: None, 6: None}
        best_move = None

        thread2 = self._start_in_thread(2, 2) #todo stop
        thread4 = self._start_in_thread(4, 4)
        thread6 = self._start_in_thread(6, 6)

        while self._get_millis() + 400 < self._final_time:
            sleep(0.1)

        best_move = threads_dict[2] if threads_dict[2] else best_move
        best_move = threads_dict[4] if threads_dict[4] else best_move
        best_move = threads_dict[6] if threads_dict[6] else best_move

        return best_move

    def _get_millis(self):
        return int(round(time.time() * 1000))
