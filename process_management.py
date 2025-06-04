import time
import queue
import threading
from concurrency import GameThreadManager

class PCB:
    def __init__(self, pid, name, burst_time, pages_needed=4):
        self.pid = pid
        self.name = name
        self.state = "ready"
        self.burst_time = burst_time
        self.total_runtime = 0
        self.pages = []
        self.pages_needed = pages_needed
        self.input_queue = queue.Queue()
        self.score = 0
        self.score_lock = threading.Lock()
        self.threads = []

    def __str__(self):
        return f"{self.name} (PID: {self.pid}, State: {self.state}, Score: {self.score})"

class Scheduler:
    def __init__(self, time_quantum, memory_manager, file_system, log_callback=None):
        self.ready_queue = []
        self.time_quantum = time_quantum
        self.memory_manager = memory_manager
        self.file_system = file_system
        self.thread_managers = {}
        self.next_pid = 1
        self.log_callback = log_callback

    def log(self, message):
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)

    def add_process(self, name, burst_time=6, pages_needed=4):
        pcb = PCB(self.next_pid, name, burst_time, pages_needed)
        self.next_pid += 1
        if self.memory_manager.allocate_memory(pcb):
            self.ready_queue.append(pcb)
            self.thread_managers[pcb.pid] = GameThreadManager(pcb, self.log_callback)
            self.log(f"Added {pcb.name} to ready queue")
            self.file_system.create_file(f"{pcb.name.lower()}.txt", f"Initial score: {pcb.score}")
        else:
            self.log(f"Failed to add {pcb.name} due to insufficient memory")

    def clear_queue(self):
        for pcb in self.ready_queue[:]:  # Copy to avoid modifying list during iteration
            self.thread_managers[pcb.pid].stop_threads()
            self.file_system.delete_file(f"{pcb.name.lower()}.txt")
            self.memory_manager.deallocate_memory(pcb)
            del self.thread_managers[pcb.pid]
        self.ready_queue.clear()
        self.log("Queue cleared")

    def remove_last_process(self):
        if not self.ready_queue:
            return False
        pcb = max(self.ready_queue, key=lambda x: x.pid)  # Highest PID is last added
        self.ready_queue.remove(pcb)
        self.thread_managers[pcb.pid].stop_threads()
        self.file_system.delete_file(f"{pcb.name.lower()}.txt")
        self.memory_manager.deallocate_memory(pcb)
        del self.thread_managers[pcb.pid]
        self.log(f"Removed last process: {pcb.name}")
        return True

    def remove_process_by_name(self, name):
        for pcb in self.ready_queue:
            if pcb.name == name:
                self.ready_queue.remove(pcb)
                self.thread_managers[pcb.pid].stop_threads()
                self.file_system.delete_file(f"{pcb.name.lower()}.txt")
                self.memory_manager.deallocate_memory(pcb)
                del self.thread_managers[pcb.pid]
                self.log(f"Removed process: {pcb.name}")
                return True
        return False

    def show_queue(self):
        if not self.ready_queue:
            self.log("Ready Queue: Empty")
            return
        queue_str = "Ready Queue: ["
        for pcb in self.ready_queue:
            queue_str += f" {pcb.name} "
            if pcb == self.ready_queue[-1]:
                queue_str += "]"
            else:
                queue_str += "|"
        self.log(queue_str)

    def run(self):
        while self.ready_queue:
            pcb = min(self.ready_queue, key=lambda x: x.total_runtime)
            self.ready_queue.remove(pcb)
            pcb.state = "running"
            self.log(f"\nRunning: {pcb}")
            _, msg = self.memory_manager.translate_address(pcb.pid, 1500)
            self.log(f"Address Translation: {msg}")
            self.thread_managers[pcb.pid].start_threads()
            time.sleep(self.time_quantum)
            self.thread_managers[pcb.pid].stop_threads()
            pcb.burst_time -= self.time_quantum
            pcb.total_runtime += self.time_quantum
            with pcb.score_lock:
                self.file_system.write_file(f"{pcb.name.lower()}.txt", f"Score: {pcb.score}")
            if pcb.burst_time > 0:
                pcb.state = "ready"
                self.ready_queue.append(pcb)
                self.log(f"{pcb.name} moved back to ready queue")
            else:
                pcb.state = "terminated"
                self.log(f"{pcb.name} terminated")
                with pcb.score_lock:
                    self.file_system.save_high_score(pcb.name, pcb.score)
                self.memory_manager.deallocate_memory(pcb)
                del self.thread_managers[pcb.pid]
                self.file_system.delete_file(f"{pcb.name.lower()}.txt")
            self.show_queue()