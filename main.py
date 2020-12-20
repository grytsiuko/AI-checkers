from dotenv import load_dotenv

from heuristics.amount_heuristic import AmountHeuristic
from heuristics.generic_heuristic import GenericHeuristic

load_dotenv()

import threading
from bot import Bot


if __name__ == '__main__':
    a = threading.Thread(target=Bot("A", 4, AmountHeuristic()).start)
    b = threading.Thread(target=Bot("B", 4, GenericHeuristic([(8.381027398142448, 1), (14.892423630849386, 1), (-6.113348213713902, 1), (-7.25078953395785, 1)])).start)

    a.start()
    b.start()

    a.join()
    b.join()
