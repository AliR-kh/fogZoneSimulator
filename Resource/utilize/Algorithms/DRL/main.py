from copy import deepcopy
from utilize.Algorithms.DRL.Allocation.env import Env
import numpy as np
class Run():
    def __init__(self,A_resources=None,A_tasks=None): 
        self.resources=np.array(deepcopy(A_resources))
        self.jobs=np.array(deepcopy(A_tasks["jobs"]))
        self.edges=np.array(deepcopy(A_tasks["edges"]))
        self._prepare_task()
        tt=Env(self.tasks,self.resources)
    def _prepare_task(self):
        tasks=[]
        for jobnumb in range(len(self.jobs)):
            device_id=int(self.jobs[jobnumb][0])
            task_id=self.jobs[jobnumb][1]
            # print("test phase 1")
            for devnumb in range(1,len(self.edges)):
                # print(f" divec id: {type(device_id)}  and edgeid : {type(self.edges[devnumb]["id"])}")
                if device_id==self.edges[devnumb]["id"]:   
                    for tasknumb in range(len(self.edges[devnumb]["workflow"])):
                        if self.edges[devnumb]["workflow"][tasknumb][0]["id"]==task_id:
                            tasks.append(self.edges[devnumb]["workflow"][tasknumb][0])
        self.tasks=np.array(tasks)