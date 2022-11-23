import threading
from queue import Queue
import queue

VALUE = True

class DiscordThread(threading.Thread):
    def __init__(self, queue: Queue, args=(), kwargs=None):
        super().__init__(group=None, args=args, daemon=True, kwargs=kwargs)
        self.queue = queue

    def run(self):
        print(threading.current_thread().name)
        while True:
            if(self.queue.qsize() >= 1):
                val = self.queue.get_nowait()
                print(threading.current_thread().name, val)

if __name__ == "__main__":
    q = Queue()
    q.put("hi")
    t = DiscordThread(q)
    t.start()
    flag = True
    while flag:
        s = input()
        q.put(s)

