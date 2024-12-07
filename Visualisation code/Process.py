# Design a default process

class PCB:
    def __init__(self, pid, ppid=0, state= "New", runing_time=1):
        self.pid = pid
        self.ppid = ppid
        self.cpid = 0
        self.state = state
        self.iswaitingforchild = 0
        self.iswaitingforchildpid = 0
        self.runing_time = runing_time

    def __str__(self):
        return f"Process ID: {self.pid}, Parent ID: {self.ppid}, State: {self.state}, Waiting Time: {self.runing_time}"
    
    def set_state(self, state):
        self.state = state

    def set_runing_time(self, runing_time):
        self.runing_time = runing_time
    
    def get_runing_time(self):
        return self.runing_time
    
    def get_state(self):
        return self.state   
    
    def get_pid(self):
        return self.pid
    
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
        self.total_runing_time = 0

    def add_process(self, process):
        process.set_state("Ready")
        self.processes.append(process)
        self.total_runing_time += process.get_runing_time()
        
        print(process," Action: Added process to ready queue")

    def remove_process(self, process):
        process.set_state("Terminated")
        self.processes.remove(process)
        self.total_runing_time -= process.get_runing_time()
        print(process," Action: Removed process from ready queue")

    def get_processes(self):
        return self.processes
    
    def get_process_by_pid(self, pid):
        return [process for process in self.processes if process.get_pid() == pid]

    def __str__(self):
        return "\n".join([str(process) for process in self.processes])

def create_process(process_table, running_time=1):
    pid = len(process_table.get_processes()) + 1
    process = PCB(pid=pid, runing_time=running_time)
    print(process," Action: Created process")
    process_table.add_process(process)

def fork_process(process_table, parent_id):
    pid = len(process_table.get_processes()) + 1
    ppid = parent_id
    parent_process = process_table.get_process_by_pid(parent_id)[0]
    parent_process.set_cpid(pid)
    process = PCB(pid=pid, ppid=ppid, runing_time=parent_process.get_runing_time())
    print(process," Action: Created process ",ppid, " child")
    process_table.add_process(process)

def exec_process(process):
    process.set_runing_time(process.get_runing_time() - 1)
    #TODO: Add code to read code here
    process.set_state("Waiting")

def terminate_process(process_table, process):
    process_parent = process_table.get_process_by_pid(process.get_pid())[0]

    if process_parent.get_waiting_status()[1] == process.get_pid():
        process_parent.set_waiting_status(0,0)
    elif process_parent.get_waiting_status()[0] == 1 and process_parent.get_waiting_status()[1] == 0:
        process_parent.set_waiting_status(0,0)

    print(process," Action: Terminate process")
    process_table.remove_process(process)
    process.set_state("Terminated")

def wait_process(process):
    if process.cpid != 0:
        process.set_state("Waiting")
        process.set_waiting_status(1, 0)

def wait_process_pid(parent_process, child_process):
    if parent_process.cpid != 0:
        parent_process.set_state("Waiting")
        parent_process.set_waiting_status(1, child_process.get_pid())

def Algorithm_1(process_table):
    for process in process_table.get_processes():
            process.set_state("Running")

            if process.get_runing_time() > 0:
                print(process," Action: Run process for 1 time unit")
                exec_process(process)
            elif process.get_runing_time() == 0:
                if process.get_waiting_status()[0] == 0:
                    terminate_process(process_table, process)
                elif process.get_waiting_status()[1] != 0:
                    print(process," Action: waiting for child process", process.get_waiting_status()[1])
                else:
                    print(process," Action: waiting for any child process")

            else:
                print("Error: Process runing time is less than 0")

def run_process(process_table, total_runing_time):
    
    for i in range(total_runing_time):
        Algorithm_1(process_table)

def switch_process(process_table, process_1_id, process_2_id):
    process_1 = process_table.get_processes(process_1_id)[0]
    process_2 = process_table.get_processes(process_2_id)[0]
    process_1.set_state("Running")
    process_2.set_state("Waiting")
    process_table.remove_process(process_1)
    process_table.add_process(process_1)
    process_table.remove_process(process_2)
    process_table.add_process(process_2)

if __name__ == "__main__":
    process_table = Process_table()
    total_runing_time = 20
    create_process(process_table)
    create_process(process_table,2)
    fork_process(process_table=process_table,parent_id=2)
    run_process(process_table, total_runing_time)