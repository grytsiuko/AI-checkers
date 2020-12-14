from dotenv import load_dotenv
load_dotenv()

import threading
from bot import Bot


if __name__ == '__main__':
    a = threading.Thread(target=Bot("A", 2).start)
    b = threading.Thread(target=Bot("B", 2).start)

    a.start()
    b.start()

    a.join()
    b.join()
