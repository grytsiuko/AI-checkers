from dotenv import load_dotenv

from heuristics.amount_heuristic import AmountHeuristic
from heuristics.generic_heuristic import GenericHeuristic
from heuristics.legendary_heuristic import LegendaryHeuristic
from mini_max.parallel_mini_max import ParallelMiniMax

load_dotenv()

import threading
from bot import Bot


if __name__ == '__main__':
    a = threading.Thread(target=Bot("A", 4).start)
    b = threading.Thread(target=Bot("B", 2, LegendaryHeuristic(), ParallelMiniMax).start)
    # b = threading.Thread(target=Bot("B", 2, mini_max_class=ParallelMiniMax).start)

    a.start()
    b.start()

    a.join()
    b.join()
