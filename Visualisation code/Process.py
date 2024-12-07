# Design a default process

class PCB:
    def __init__(self, pid, state= "New", waiting_time=1):
        self.pid = pid
        self.state = state
        self.waiting_time = waiting_time

    def __str__(self):
        return f"Process ID: {self.pid}, State: {self.state}, Waiting Time: {self.waiting_time}"
    
    def set_state(self, state):
        self.state = state

    def set_waiting_time(self, waiting_time):
        self.waiting_time = waiting_time
    
    def get_waiting_time(self):
        return self.waiting_time
    
    def get_state(self):
        return self.state   
    
    def get_pid(self):
        return self.pid
    

class Process_table:
    def __init__(self):
        self.processes = []
        self.total_waiting_time = 0

    def add_process(self, process):
        process.set_state("Ready")
        self.processes.append(process)
        self.total_waiting_time += process.get_waiting_time()

    def remove_process(self, process):
        process.set_state("Terminated")
        self.processes.remove(process)
        self.total_waiting_time -= process.get_waiting_time()

    def get_pprocesses(self, process_id):
        return [process for process in self.processes if process.get_pid() == process_id]

    def __str__(self):
        return "\n".join([str(process) for process in self.processes])
    


if __name__ == "__main__":
    process = PCB(1)
    process_2 = PCB(2)
    process_table = Process_table()
    process_table.add_process(process)
    process_table.add_process(process_2)
    print(process_table)