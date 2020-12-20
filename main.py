from dotenv import load_dotenv

from heuristics.amount_heuristic import AmountHeuristic
from heuristics.generic_heuristic import GenericHeuristic

load_dotenv()

import threading
from bot import Bot


if __name__ == '__main__':
    a = threading.Thread(target=Bot("A", 4, GenericHeuristic([(12.424879018719095, 1), (16.263504183839, 1), (-8.663468683373988, 1), (-5.705007490296328, 1)])).start)
    b = threading.Thread(target=Bot("B", 4, GenericHeuristic([(11.832950298231378, 1), (15.961607139833205, 1), (-8.612233287751327, 1), (-5.705007490296328, 1)])).start)

    a.start()
    b.start()

    a.join()
    b.join()
