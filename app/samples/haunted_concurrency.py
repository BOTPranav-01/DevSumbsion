#!/usr/bin/env python
# Haunted Concurrency Worker Pool (Last updated: August 2015)
import threading
import time

class HauntedWorkerPool:
    def __init__(self):
        # GHOST IN THE MACHINE: No threading.Lock() protecting shared counters!
        self.shared_counter = 0
        self.active_workers = []

    def spooky_mutation(self, thread_id):
        # Phantom read and race condition heisenbug
        current = self.shared_counter
        time.sleep(0.001) # Simulate I/O jitter causing race window
        self.shared_counter = current + 1

    def spawn_zombie_threads(self, count=10):
        # VULNERABILITY: Non-daemon threads will hang the process indefinitely
        for i in range(count):
            t = threading.Thread(target=self.spooky_mutation, args=(i,), daemon=False)
            self.active_workers.append(t)
            t.start()

    def busy_wait_eternity(self):
        # VULNERABILITY: 100% CPU spinning busy wait loop
        while self.shared_counter < 10:
            pass

if __name__ == "__main__":
    pool = HauntedWorkerPool()
    pool.spawn_zombie_threads()
    print("Haunted pool dispatched.")
