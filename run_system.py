import subprocess
import os
import time

# Directory to store worker logs
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Number of workers to launch
NUM_WORKERS = 3

def start_master():
    """Start the Master server."""
    print("Starting Master...")
    log_file = os.path.join(LOG_DIR, f"master.log")
    
    
    # Open log file for writing
    log = open(log_file, "w")  # Keep the log file open
    
    return subprocess.Popen(
        ["python", "-u", "master.py"],  # Use '-u' to unbuffer output
        stdout=log,
        stderr=log
    )

def start_worker(worker_id):
    """Start a Worker client and log its output."""
    log_file = os.path.join(LOG_DIR, f"worker_{worker_id}.log")
    print(f"Starting Worker {worker_id}, logging to {log_file}...")
    
    # Open log file for writing
    log = open(log_file, "w")  # Keep the log file open
    
    # Start the worker process
    return subprocess.Popen(
        ["python", "-u", "worker.py"],  # Use '-u' to unbuffer output
        stdout=log, stderr=log
    )

if __name__ == "__main__":
    # Start the Master server
    master_process = start_master()
    time.sleep(2)  # Wait for the master to start
    
    # Start multiple Worker processes
    worker_processes = []
    for i in range(NUM_WORKERS):
        worker_process = start_worker(i + 1)
        worker_processes.append(worker_process)
    
    try:
        # Keep the script running until interrupted
        print("Master and Workers are running... Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down all processes...")
        # Terminate all processes
        master_process.terminate()
        for wp in worker_processes:
            wp.terminate()

        print("All processes stopped.")
