from dotenv import load_dotenv

from heuristics.amount_heuristic import AmountHeuristic
from heuristics.generic_heuristic import GenericHeuristic

load_dotenv()

import threading
from bot import Bot


if __name__ == '__main__':
    a = threading.Thread(target=Bot("A", 4, AmountHeuristic()).start)
    b = threading.Thread(target=Bot("B", 4, GenericHeuristic([(10.305413115612751, 1), (13.44464928240105, 1), (-6.898465436692924, 1), (-3.9897523806930675, 1), (8.634223509855085, 1), (10.549956226868659, 1), (-10.577144271386192, 1), (-1.6370015788510208, 1), (-4.951456651269732, 1), (-0.12184513632545538, 1)])).start)

    a.start()
    b.start()

    a.join()
    b.join()
