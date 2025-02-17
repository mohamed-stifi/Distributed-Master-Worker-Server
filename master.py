import xmlrpc.server
import threading
import time
from collections import defaultdict

class MasterServer:
    def __init__(self):
        # Task queue and tracking
        self.tasks = []
        self.task_status = {}  # Maps task_id -> (status, start_time, worker)
        self.lock = threading.Lock()  # To ensure thread safety
        self.workers = set()  # Set of worker addresses

    def add_tasks(self, tasks):
        with self.lock:
            self.tasks.extend(tasks)
            for i, task in enumerate(tasks):
                self.task_status[i] = ("PENDING", None, None)  # Initial state

    def register_worker(self, worker_address):
        self.workers.add(worker_address)
        return f"Worker {worker_address} registered."

    def request_task(self, worker_address):
        with self.lock:
            for task_id, (status, _, _) in self.task_status.items():
                if status == "PENDING":
                    self.task_status[task_id] = ("IN_PROGRESS", time.time(), worker_address)
                    return task_id, self.tasks[task_id]
        return None, None  # No tasks available

    def complete_task(self, task_id, worker_address, result):
        with self.lock:
            if task_id in self.task_status:
                self.task_status[task_id] = ("COMPLETED", None, worker_address)
                print(f"Task {task_id} completed by {worker_address} with result: {result}")
                return True
        return False

    def monitor_tasks(self):
        while True:
            with self.lock:
                for task_id, (status, start_time, worker) in self.task_status.items():
                    if status == "IN_PROGRESS" and time.time() - start_time > 10:
                        # Task timed out, mark as PENDING again
                        print(f"Task {task_id} timed out. Reassigning...")
                        self.task_status[task_id] = ("PENDING", None, None)
            time.sleep(5)  # Check every 5 seconds

# Start Master server
# Start Master server
def start_master():
    server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
    master = MasterServer()
    server.register_instance(master)

    # Adding predefined tasks (for example, strings representing file contents)
    tasks = [
        "data file one with some text for word counting",
        "another document with different words and some repeating words",
        "this is a third document with example data for counting",
        "more sample text data to check word frequency in data processing"
    ]*1 #000
    master.add_tasks(tasks)  # Adding tasks to the master

    # Start monitoring thread
    monitor_thread = threading.Thread(target=master.monitor_tasks)
    monitor_thread.daemon = True
    monitor_thread.start()

    print("Master Server started with tasks...")
    server.serve_forever()


if __name__ == "__main__":
    start_master()
