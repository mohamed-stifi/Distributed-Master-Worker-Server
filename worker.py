import xmlrpc.client
import time

class WorkerClient:
    def __init__(self, master_address):
        self.master = xmlrpc.client.ServerProxy(master_address)
        self.worker_address = f"Worker-{time.time()}"
        self.master.register_worker(self.worker_address)

    def perform_task(self, task):
        # Simulating task execution (count words in a file)
        file_content = task
        word_count = {}
        for word in file_content.split():
            word_count[word] = word_count.get(word, 0) + 1
        return word_count

    def start(self):
        while True:
            task_id, task = self.master.request_task(self.worker_address)
            if task_id is not None:
                print(f"{self.worker_address} received task {task_id}")
                result = self.perform_task(task)
                self.master.complete_task(task_id, self.worker_address, result)
            else:
                print(f"{self.worker_address} has no tasks, sleeping...")
                time.sleep(2)  # Sleep before checking again

# Start Worker
def start_worker():
    worker = WorkerClient("http://localhost:8000")
    worker.start()

if __name__ == "__main__":
    start_worker()
