import threading

class Server:
    def __init__(self, capacity):
        self.capacity = capacity
        self.load = 0

class LoadBalancer:
    def __init__(self, capacities):
        self.servers = [Server(cap) for cap in capacities] 
        self._lock = threading.Lock()
    
    def route_request(self):
        with self._lock:
            server_node = None
            min_load = float("inf")
            for i in range(len(self.servers)):
                server = self.servers[i]
                if server.load < min_load and server.load < server.capacity:
                    min_load = server.load
                    server_node = i
            if server_node is None:
                return None 
            self.servers[server_node].load += 1
            return server_node

    def finish_request(self, server_id):
        with self._lock:
            self.servers[server_id].load -= 1

            

