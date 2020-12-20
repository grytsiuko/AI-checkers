from dotenv import load_dotenv

from heuristics.amount_heuristic import AmountHeuristic
from heuristics.generic_heuristic import GenericHeuristic

load_dotenv()

import threading
from bot import Bot


if __name__ == '__main__':
    a = threading.Thread(target=Bot("A", 4, GenericHeuristic([(15.847631627141228, 1), (16.844416281435063, 1), (-8.69849000004436, 1), (-7.870489568007705, 1)])).start)
    b = threading.Thread(target=Bot("B", 4, GenericHeuristic([(12.424879018719095, 1), (15.91370955442923, 1), (-8.586177288183745, 1), (-7.246833475445805, 1)])).start)

    a.start()
    b.start()

    a.join()
    b.join()
