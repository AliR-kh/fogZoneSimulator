from copy import deepcopy
# from utilize.Algorithms.DRL.Allocation.env import Env
from utilize.Algorithms.DRL.Allocation.test import RunTest
from utilize.Algorithms.DRL.Scheduling.Clouds.pso import PSO

import numpy as np
class Run():
    def __init__(self,A_resources=None,A_tasks=None): 
        self.resources=np.array(deepcopy(A_resources))
        self.jobs=np.array(deepcopy(A_tasks["jobs"]))
        self.edges=np.array(deepcopy(A_tasks["edges"]))
        self._prepare_task()
        # e=Env(self.tasks,self.resources)
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
        
    def allocation_test(self):
        test=RunTest(self.tasks,self.resources)
        self.allocation_list=test.schedule_tasks_with_model()
        self.edges_list =[]
        self.fogs_list=[]
        self.cloud_list=[] 
        for i in range(len(self.allocation_list)):
            if self.allocation_list[i]==0:
                self.edges_list.append({"type":"edge","id":self.tasks[i]["device_id"]})
            elif self.allocation_list[i]==1:
                self.cloud_list.append(self.tasks[i])
            elif self.allocation_list[i]==2:
                self.fogs_list.append(self.tasks[i])   
                    
    def allocation_train(self):
        pass
    
    
    def scheduling(self):
        self.fogs_resources=[]
        self.clouds_resources=[]
        self.edges_resources=[]
        self.fogs_resources+=[resource for resource in self.resources if resource["type"]=="Fog"]
        self.clouds_resources+=[resource for resource in self.resources if resource["type"]=="Cloud"]
        cloud_scheduling=PSO(self.cloud_list,self.clouds_resources)
        cloud_scheduling.run()
    
    