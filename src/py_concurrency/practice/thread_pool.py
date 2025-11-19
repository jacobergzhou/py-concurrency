import threading
import queue
from typing import Any, Callable, Optional
import time


class FutureLike:
    def __init__(self):
        self._done = threading.Event()
        self._result : Any = None
        self._exc : Optional[BaseException] = None

    def set_result(self, result: Any):
        self._result = result
        self._done.set()
    
    def set_exception(self, exc: BaseException):
        self._exc = exc
        self._done.set()

    def result(self, timeout: Optional[float] = None):
        finished = self._done.wait(timeout)
        if not finished:
            raise TimeoutError(f"timeout {timeout} seconds exceeds")
        
        if self._exc is not None:
            raise self._exc

        return self._result
    

class ThreadPool:
    def __init__(self, num_workers):
        self._num_workers = num_workers
        self._queue = queue.Queue()
        self._threads = []
        self._sentinal = object()
        self._shutdown = False

        for i in range(num_workers):
            t = threading.Thread(target=self._worker_loop, name=f"worker{i}", daemon=True)
            self._threads.append(t)
            t.start()
        
    def _worker_loop(self):
        while True:
            task = self._queue.get()
            try:
                if task == self._sentinal:
                    break
                fn, arg, kwarg, future = task
                try:
                    res = fn(*arg, **kwarg)
                except BaseException as e:
                    future.set_exception(e)
                else:
                    future.set_result(res)
            finally:
                self._queue.task_done()
        
    def submit(self, fn: Callable[..., Any], *args, **kwargs) -> FutureLike:
        if self._shutdown:
            raise RuntimeError("Pool is shut down")
        future = FutureLike()
        task = (fn, args, kwargs, future)
        self._queue.put(task)
        return future

    def shutdown(self, wait: bool = True):
        self._shutdown = True

        for _ in range(self._num_workers):
            self._queue.put(self._sentinal)

        if wait:
            self._queue.join()
            for t in self._threads:
                t.join()

def square(x):
    time.sleep(1)  # pretend to do work
    return x * x

if __name__ == "__main__":
    pool = ThreadPool(num_workers=3)

    f1 = pool.submit(square, 2)
    f2 = pool.submit(square, 3)
    f3 = pool.submit(square, 4)

    print(f1.result())  # blocks until worker finishes square(2)
    print(f2.result())
    print(f3.result())

    pool.shutdown()

