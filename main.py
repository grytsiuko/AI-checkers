from dotenv import load_dotenv

from heuristics.amount_heuristic import AmountHeuristic
from heuristics.generic_heuristic import GenericHeuristic
from heuristics.legendary_heuristic import LegendaryHeuristic

load_dotenv()

import threading
from bot import Bot


if __name__ == '__main__':
    a = threading.Thread(target=Bot("A", 2, LegendaryHeuristic()).start)
    b = threading.Thread(target=Bot("B", 6, LegendaryHeuristic()).start)

    a.start()
    b.start()

    a.join()
    b.join()
