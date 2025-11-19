import threading
import time

class TokenBucketRateLimiter:
    def __init__(self, rate, capacity):
        self.capacity = capacity
        self.rate = rate
        self.last_updated_ts = time.monotonic()
        self.bucket_size = float(capacity)
        self.lock = threading.Lock()
    
    def allow(self) -> bool:
        with self.lock:    
            ts = time.monotonic()
            elapsed = ts - self.last_updated_ts
            num_token = min(self.capacity, elapsed * self.rate + self.bucket_size)
            self.last_updated_ts = ts
            self.bucket_size = num_token
            if num_token >= 1.0:
                self.bucket_size -= 1.0
                return True
            else:
                return False
            
limiter = TokenBucketRateLimiter(5, 10)

def worker(id):
    for i in range(10):
        allowed = limiter.allow()
        print(f"thread-{id}: request {i}, allowed = {allowed}")
        time.sleep(0.3)

def main():
    threads = []
    for id in range(3):
        t = threading.Thread(target=worker, args = (id,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()