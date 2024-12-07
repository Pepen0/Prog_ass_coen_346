# Design a default process

class PCB:
    def __init__(self, pid, ppid=0, state= "New", runing_time=1):
        self.pid = pid
        self.ppid = ppid
        self.state = state
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

    def __str__(self):
        return "\n".join([str(process) for process in self.processes])

def create_process(process_table, running_time=1):
    pid = len(process_table.get_processes()) + 1
    process = PCB(pid=pid, runing_time=running_time)
    print(process," Action: Created process")
    process_table.add_process(process)

def fork_process(process_table, process_id, running_time=1):
    pid = len(process_table.get_processes()) + 1
    ppid = process_id
    process = PCB(pid=pid, ppid=ppid, runing_time=running_time)
    print(process," Action: Created process ",ppid, " child")
    process_table.add_process(process)

def Algorithm_1(process_table):
    for process in process_table.get_processes():
            process.set_state("Running")

            if process.get_runing_time() > 0:
                print(process," Action: Run process for 1 time unit")
                process.set_runing_time(process.get_runing_time() - 1)
                process.set_state("Waiting")
            elif process.get_runing_time() == 0:
                print(process," Action: Terminate process")
                process_table.remove_process(process)
                process.set_state("Terminated")
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
    fork_process(process_table,process_id=2,running_time=1)
    run_process(process_table, total_runing_time)