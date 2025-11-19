import threading

class UnsafeCounter:
    def __init__(self):
        self.value = 0
    
    def increment(self):
        self.value += 1

class SafeCounter:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self.value += 1

INCREMENTS_PER_THREAD = 100_000
NUM_THREADS = 10

def worker(counter):
    for _ in range(INCREMENTS_PER_THREAD):
        counter.increment()

def run_test(counter_cls, label):
    counter = counter_cls()
    threads = []

    for _ in range(NUM_THREADS):
        t = threading.Thread(target=worker, args=(counter,))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print(f"{label} final value: {counter.value}")


if __name__ == "__main__":
    print("Running unsafe counter")
    for _ in range(5):
        run_test(UnsafeCounter, "unsafe")
    
    for _ in range(5):
        run_test(SafeCounter, "safe")