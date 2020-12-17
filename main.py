from dotenv import load_dotenv

from heuristics.amount_heuristic import AmountHeuristic

load_dotenv()

import threading
from bot import Bot


if __name__ == '__main__':
    a = threading.Thread(target=Bot("A", 4, AmountHeuristic()).start)
    b = threading.Thread(target=Bot("B", 4, AmountHeuristic()).start)

    a.start()
    b.start()

    a.join()
    b.join()
