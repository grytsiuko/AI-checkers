

if __name__ == '__main__':
    from dotenv import load_dotenv

    from heuristics.legendary_heuristic import LegendaryHeuristic
    from mini_max.parallel_mini_max import ParallelMiniMax

    load_dotenv()

    import threading
    from bot import Bot

    a = threading.Thread(target=Bot("A", 4).start)
    b = threading.Thread(target=Bot("B", 2, LegendaryHeuristic(), ParallelMiniMax).start)
    # b = threading.Thread(target=Bot("B", 2, mini_max_class=ParallelMiniMax).start)

    a.start()
    b.start()

    a.join()
    b.join()
