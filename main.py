import threading

from bot import Bot

if __name__ == '__main__':
    threading.Thread(target=Bot().start).start()
    threading.Thread(target=Bot().start).start()
