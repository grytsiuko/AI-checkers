if __name__ == '__main__':
    from dotenv import load_dotenv

    from mini_max.parallel_mini_max import ParallelMiniMax
    from heuristics.space_heuristic import SpaceHeuristic

    load_dotenv()

    from bot import Bot

    Bot("21 Checkers", 2, SpaceHeuristic(), ParallelMiniMax).start()
