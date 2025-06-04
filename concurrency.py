import threading
import queue
import random
import time

class GameThreadManager:
    def __init__(self, pcb, log_callback=None):
        self.pcb = pcb
        self.running = False
        self.log_callback = log_callback  # Callback for GUI logging

    def log(self, message):
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)

    def producer(self):
        inputs = ["up", "down", "left", "right"]
        for _ in range(2):
            if not self.running or self.pcb.state == "terminated":
                break
            input_key = random.choice(inputs)
            self.pcb.input_queue.put(input_key)
            self.log(f"{self.pcb.name} Producer: Added '{input_key}'")
            time.sleep(0.5)

    def consumer(self):
        for _ in range(2):
            if not self.running or self.pcb.state == "terminated":
                break
            try:
                input_key = self.pcb.input_queue.get(timeout=0.5)
                with self.pcb.score_lock:
                    self.pcb.score += 1
                    self.log(f"{self.pcb.name} Consumer: Processed '{input_key}', Score: {self.pcb.score}")
                self.pcb.input_queue.task_done()
            except queue.Empty:
                pass

    def start_threads(self):
        self.running = True
        producer_thread = threading.Thread(target=self.producer)
        consumer_thread = threading.Thread(target=self.consumer)
        self.pcb.threads = [producer_thread, consumer_thread]
        for thread in self.pcb.threads:
            thread.daemon = True
            thread.start()

    def stop_threads(self):
        self.running = False
        for thread in self.pcb.threads:
            thread.join(timeout=0.5)