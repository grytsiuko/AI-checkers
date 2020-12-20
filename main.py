from dotenv import load_dotenv

from heuristics.amount_heuristic import AmountHeuristic
from heuristics.generic_heuristic import GenericHeuristic
from heuristics.legendary_heuristic import LegendaryHeuristic
from mini_max.mini_max_iterative import MiniMaxIterative

load_dotenv()

import threading
from bot import Bot


if __name__ == '__main__':
    a = threading.Thread(target=Bot("A", 4).start)
    b = threading.Thread(target=Bot("B", 2, mini_max_class=MiniMaxIterative).start)

    a.start()
    b.start()

    a.join()
    b.join()
