import threading
from collections import deque
import time
import random

class BoundedBlockingQueue:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.queue = deque()
        self.condition = threading.Condition()

    def put(self, item):
        with self.condition:
            while len(self.queue) >= self.capacity:
                self.condition.wait()
            self.queue.append(item)
            self.condition.notify()
    
    def get(self):
        with self.condition:
            while len(self.queue) == 0:
                self.condition.wait()
            item = self.queue.popleft()
            self.condition.notify()
            return item
    
    def size(self):
        with self.condition:
            return len(self.queue)


def producer_thread_fn(bq: BoundedBlockingQueue, producer_id: int, num_items: int):
    for i in range(num_items):
        item = (i, producer_id)
        bq.put(item)
        print(f"[PRODUCER-{producer_id}] put {item}, size={bq.size()}", flush=True)
        # Random short sleep to mix up scheduling
        time.sleep(random.uniform(0.01, 0.1))

def consumer_thread_fn(bq: BoundedBlockingQueue, consumer_id: int, num_items: int):
    for _ in range(num_items):
        item = bq.get()
        print(f"    [CONSUMER-{consumer_id}] got {item}, size={bq.size()}", flush=True)
        time.sleep(random.uniform(0.01, 0.1))

def main():
    capacity = 5
    bq = BoundedBlockingQueue(capacity)
    N_PRODUCERS = 3
    N_CONSUMERS = 2
    ITEMS_PER_PRODUCER = 10
    TOTAL_ITEMS = N_PRODUCERS * ITEMS_PER_PRODUCER
    ITEMS_PER_CONSUMER = TOTAL_ITEMS // N_CONSUMERS  # assumes divisible

    producers = []
    consumers = []

    for pid in range(N_PRODUCERS):
        t = threading.Thread(target = producer_thread_fn, args=(bq, pid, ITEMS_PER_PRODUCER), name=f"producer-{pid}")
        producers.append(t)
        t.start()
    
    for pid in range(N_CONSUMERS):
        t = threading.Thread(target = consumer_thread_fn, args=(bq, pid, ITEMS_PER_CONSUMER), name=f"consumer-{pid}")
        consumers.append(t)
        t.start()
    
    for t in producers:
        t.join()
    
    for t in consumers:
        t.join()

    print("All producers and consumers finished. Final size:", bq.size())

if __name__ == "__main__":
    main()

