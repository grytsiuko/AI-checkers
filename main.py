from dotenv import load_dotenv

from heuristics.amount_heuristic import AmountHeuristic
from heuristics.generic_heuristic import GenericHeuristic

load_dotenv()

import threading
from bot import Bot


if __name__ == '__main__':
    a = threading.Thread(target=Bot("A", 4, GenericHeuristic([(12.424879018719095, 1), (16.263504183839, 1), (-8.663468683373988, 1), (-5.705007490296328, 1), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0)])).start)
    b = threading.Thread(target=Bot("B", 4, GenericHeuristic([(8.693455660325654, 1), (12.430093947300348, 1), (-4.465470840762692, 1), (-1.5942254940521263, 1), (9.146175702687415, 1), (11.205003175568088, 1), (-7.965155808892185, 1), (-6.182579335317071, 1), (-3.8087539354372475, 1), (3.359151132141541, 1), (0.9666934959878581, 1), (-4.6766698487914145, 1), (-2.5916545659210337, 1), (6.742538287779657, 1)])).start)

    a.start()
    b.start()

    a.join()
    b.join()
