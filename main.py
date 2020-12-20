from dotenv import load_dotenv

from heuristics.amount_heuristic import AmountHeuristic
from heuristics.generic_heuristic import GenericHeuristic

load_dotenv()

import threading
from bot import Bot


if __name__ == '__main__':
    b = threading.Thread(target=Bot("A", 4, GenericHeuristic([(12.424879018719095, 1), (16.263504183839, 1), (-8.663468683373988, 1), (-5.705007490296328, 1), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0)])).start)
    a = threading.Thread(target=Bot("B", 4, GenericHeuristic([(13.047744269718308, 1), (18.012860429655504, 1), (-7.637045805223027, 1), (-6.707325012290806, 1), (10.97800243200367, 1), (14.198338317791185, 1), (-13.126819678658231, 1), (-2.20112071568572, 1), (-5.600701064455507, 1), (0.3064143701525668, 1)])).start)
    a.start()
    b.start()

    a.join()
    b.join()
