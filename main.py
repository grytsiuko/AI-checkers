if __name__ == '__main__':
    from dotenv import load_dotenv

    from mini_max.parallel_mini_max import ParallelMiniMax
    from heuristics.amount_heuristic import AmountHeuristic
    from heuristics.space_heuristic import SpaceHeuristic
    from mini_max.mini_max_base import MiniMaxBase

    load_dotenv()

    import threading
    from bot import Bot

    a = threading.Thread(target=Bot("A", 4, AmountHeuristic(), MiniMaxBase).start)
    b = threading.Thread(target=Bot("B", 2, SpaceHeuristic(), ParallelMiniMax).start)

    a.start()
    b.start()

    a.join()
    b.join()
