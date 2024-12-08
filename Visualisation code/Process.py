# Design a default process

class PCB:
    def __init__(self, pid, ppid=0, state= "New", running_time=1,arrival_time=0):
        self.pid = pid
        self.ppid = ppid
        self.state = state
        self.running_time = running_time
        self.arrival_time = arrival_time
        self.cpid = 0
        self.iswaitingforchild = 0
        self.iswaitingforchildpid = 0

    def __str__(self):
        return f"Process ID: {self.pid}, Parent ID: {self.ppid}, State: {self.state}, Waiting Time: {self.running_time}"
    
    def set_state(self, state):
        self.state = state

    def set_running_time(self, running_time):
        self.running_time = running_time
    
    def get_running_time(self):
        return self.running_time
    
    def get_state(self):
        return self.state   
    
    def get_pid(self):
        return self.pid
    
    def get_ppid(self):
        return self.ppid
    
    def set_cpid(self, cpid):
        self.cpid = cpid
    
    def get_waiting_status(self):
        return self.iswaitingforchild, self.iswaitingforchildpid
    
    def set_waiting_status(self, iswaitingforchild, iswaitingforchildpid):
        self.iswaitingforchild = iswaitingforchild
        self.iswaitingforchildpid = iswaitingforchildpid
    

class Process_table:
    def __init__(self):
        self.processes = []
        self.total_running_time = 0

    def add_process(self, process):
        process.set_state("Ready")
        self.processes.append(process)
        self.total_running_time += process.get_running_time()
        
        print(process," Action: Added process to ready queue")

    def remove_process(self, process):
        process.set_state("Terminated")
        self.processes.remove(process)
        self.total_running_time -= process.get_running_time()
        print(process," Action: Removed process from ready queue")

    def get_processes(self):
        return self.processes
    
    def get_process_by_pid(self, pid):
        return [process for process in self.processes if process.get_pid() == pid]

    def __str__(self):
        return "\n".join([str(process) for process in self.processes])
class Scheduler:
    def __init__(self,Algorithm= "FIFO"):
        self.timer = 0
        self.process_table = Process_table()
        self.Algorithm = Algorithm

        total_running_time = 20
        self.create_process(running_time=1)
        self.create_process(running_time=2)
        self.fork_process(parent_id=2)
        self.run_process(total_running_time=total_running_time)

    def create_process(self, running_time=1):
        self.timer += 1
        pid = len(self.process_table.get_processes()) + 1
        process = PCB(pid=pid, running_time=running_time, arrival_time=self.timer)
        print(process, "Action: Created process")
        self.process_table.add_process(process)

    def fork_process(self, parent_id):
        self.timer += 1
        pid = len(self.process_table.get_processes()) + 1
        parent_process = self.process_table.get_process_by_pid(parent_id)[0]
        parent_process.set_cpid(pid)
        process = PCB(pid=pid, ppid=parent_id, running_time=parent_process.get_running_time(), arrival_time=self.timer)
        print(process, "Action: Created process", parent_id, "child")
        self.process_table.add_process(process)

    def exec_process(self, process):
        self.timer += 1
        process.set_running_time(process.get_running_time() - 1)
        # TODO: Add code to read code here
        process.set_state("Waiting")

    def terminate_process(self, process):
        self.timer += 1
        if process.get_ppid() != 0:
            parent_process = self.process_table.get_process_by_pid(process.get_ppid())[0]
            if parent_process.get_waiting_status()[1] == process.get_pid():
                parent_process.set_waiting_status(0, 0)
            elif parent_process.get_waiting_status()[0] == 1 and parent_process.get_waiting_status()[1] == 0:
                parent_process.set_waiting_status(0, 0)

        print(process, "Action: Terminate process")
        self.process_table.remove_process(process)
        process.set_state("Terminated")

    def wait_process(self, process):
        self.timer += 1
        if process.get_cpid() != 0:
            process.set_state("Waiting")
            process.set_waiting_status(1, 0)

    def wait_process_pid(self, parent_process, child_process):
        self.timer += 1
        if parent_process.get_cpid() != 0:
            parent_process.set_state("Waiting")
            parent_process.set_waiting_status(1, child_process.get_pid())

    def FIFO(self):
        for process in self.process_table.get_processes():
            process.set_state("Running")
            Timeout= 100

            while process.get_running_time() >= 0 and Timeout > 0:
                Timeout -= 1
                if process.get_running_time() > 0:
                    print(process, "Action: Run process for 1 time unit")
                    self.exec_process(process)
                elif process.get_running_time() == 0:
                    if process.get_waiting_status()[0] == 0:
                        self.terminate_process(process)
                        Timeout = 0
                    elif process.get_waiting_status()[1] != 0:
                        print(process, "Action: Waiting for child process", process.get_waiting_status()[1])
                    else:
                        print(process, "Action: Waiting for any child process")
                else:
                    print("Error: Process running time is less than 0")
    
    def SJF(self):
        pass


    def RR(self):
        pass

    def Priority(self):
        pass

    def run_process(self, total_running_time):
        for _ in range(total_running_time):
            
            if self.Algorithm == "FIFO":
                self.FIFO()
            elif self.Algorithm == "SJF":
                self.SJF()
            elif self.Algorithm == "RR":
                self.RR()
            elif self.Algorithm == "Priority":
                self.Priority()
            else:
                print("Error: Invalid algorithm")

if __name__ == "__main__":
    scheduler = Scheduler("FIFO")