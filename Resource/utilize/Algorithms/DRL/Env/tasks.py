from utilize.Algorithms.DRL.Env.env import Env
import random
import numpy as np


class Task(Env):

    def __init__(self, config_of_tasks,A_tasks):
        
        if A_tasks is not None:
            self.jobs=A_tasks["jobs"].copy()
            self.edges=A_tasks["edges"].copy()
            self._prepare_task()
            pass
        else:
            self.config_of_task = config_of_tasks
            self.tasks = self._create_tasks()

    def get_current_status(self):
        return self.tasks

    def _create_tasks(self):
    
        min_mips = self.config_of_task["min_mips"]
        max_mips = self.config_of_task["max_mips"]
        min_data_size = self.config_of_task["min_data_size"]
        max_data_size = self.config_of_task["max_data_size"]
        self.number_of_task = self.config_of_task["number_of_task"]
        tasks = []
        for i in range(self.number_of_task):
            tasks.append(
                {
                    "id": i,
                    "mips": random.randint(min_mips, max_mips),
                    "size": random.randint(min_data_size, max_data_size),
                }
            )
        # print(tasks)    
        return np.array(tasks)

    def _prepare_task(self):
        self.tasks=[]
        for jobnumb in range(len(self.jobs)):
            device_id=self.jobs[jobnumb][0]
            task_id=self.jobs[jobnumb][1]
            for devnumb in range(1,len(self.edges)):
                if device_id==self.edges[devnumb]["id"]:
                    for tasknumb in range(len(self.edges[devnumb]["workflow"])):
                        if self.edges[devnumb]["workflow"][tasknumb][0]["id"]==task_id:
                            self.tasks.append(self.edges[devnumb]["workflow"][tasknumb][0])
        
    def reset(self):
        self.tasks = []


