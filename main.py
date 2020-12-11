from dotenv import load_dotenv
load_dotenv()

import threading
from bot import Bot


if __name__ == '__main__':
    a = threading.Thread(target=Bot("A").start)
    b = threading.Thread(target=Bot("B").start)

    a.start()
    b.start()

    a.join()
    b.join()
