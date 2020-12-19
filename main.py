from dotenv import load_dotenv

from heuristics.amount_heuristic import AmountHeuristic
from heuristics.generic_heuristic import GenericHeuristic

load_dotenv()

import threading
from bot import Bot


if __name__ == '__main__':
    a = threading.Thread(target=Bot("A", 4, AmountHeuristic()).start)
    b = threading.Thread(target=Bot("B", 4, GenericHeuristic([(7.914061892508757, 1), (19.551653679861975, 5), (-7.786509878886294, 1), (-8.593531918124507, 1)])).start)

    a.start()
    b.start()

    a.join()
    b.join()
