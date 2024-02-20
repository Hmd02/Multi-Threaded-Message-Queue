import threading

class CustomPriorityQueue:
    def __init__(self):
        self._queue = []
        self._lock = threading.Lock()
        self._message_available = threading.Condition(self._lock)

    def put(self, message, priority):
        with self._lock:
            self._queue.append((priority, message))
            self._queue.sort(reverse=True)  # Sort in descending order of priority
            self._message_available.notify()  # Notify waiting threads

    def get(self):
        with self._lock:
            while not self._queue:
                self._message_available.wait()  # Wait until a message is available
            curr=self._queue.pop(0)
            return f"{curr[1]} with priority {curr[0]}"# Return the message with the highest priority
            # return self._queue.pop()[1]  # Return the message with the highest priority

    def empty(self):
        with self._lock:
            return len(self._queue) == 0

def task(thread_id, message_queue):
    print(f'Thread {thread_id} started')
    # Sending messages
    message_queue.put(f'Message from thread {thread_id}', thread_id % 3 + 1)

    # Receiving messages
    print(f"Thread {thread_id} received message:", message_queue.get())

if __name__ == "__main__":
    message_queue = CustomPriorityQueue()
    threads = []
    for i in range(10):
        thread = threading.Thread(target=task, args=(i, message_queue))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()



