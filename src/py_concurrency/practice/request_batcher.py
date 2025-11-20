import threading
from typing import Any, List, Callable

class PendingItem:
    def __init__(self, request) -> None:
        self.request = request
        self.result = None
        self.done = threading.Event()
    
class RequestBatcher:
    def __init__(self, max_batch_size, process_fn) -> None:
        self.max_batch_size = max_batch_size
        self.pending_items = []
        if process_fn is None:
            def default_process_fn(batch: List[Any]) -> List[Any]:
                out = []
                for x in batch:
                    if isinstance(x, (int, float)):
                        out.append(x + 1)
                    elif isinstance(x, str):
                        out.append(x.upper())
                    else:
                        out.append(x)
                return out
            process_fn = default_process_fn

        self._process_fn = process_fn
        
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._stopped = False
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon= True)
        self.worker_thread.start()

    def submit(self, request):
        with self._condition:
            item = PendingItem(request)
            self.pending_items.append(item)
            self._condition.notify()
        item.done.wait()
        return item.result
    
    def _worker_loop(self):
        while True:
            with self._condition:
                while not self.pending_items and not self._stopped:
                    self._condition.wait()
                if self._stopped and not self.pending_items:
                    return
                batch_items = self.pending_items[:self.max_batch_size]
                self.pending_items = self.pending_items[self.max_batch_size:]
            requests = [item.request for item in batch_items]
            results = self._process_fn(requests)
            for i in range(len(results)):
                item = batch_items[i]
                item.result = results[i]
                item.done.set()
    
    def stop(self):
        with self._condition:
            self._stopped = True
            self._condition.notify_all()
        self.worker_thread.join()

