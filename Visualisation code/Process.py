# Design a default process

class PCB:
    def __init__(self, pid, state, priority, waiting_time):
        self.pid = pid
        self.state = state
        self.priority = priority
        self.waiting_time = waiting_time

    def __str__(self):
        return f"Process ID: {self.pid}, State: {self.state}, Priority: {self.priority}, Waiting Time: {self.waiting_time}"
if __name__ == "__main__":
    process = PCB(1, "Running", 5, 10)
    print(process)