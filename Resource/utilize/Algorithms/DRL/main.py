from copy import deepcopy
# from utilize.Algorithms.DRL.Allocation.env import Env
from utilize.Algorithms.DRL.Allocation.allocation import RunTaskAllocation_DQN 
from utilize.Algorithms.DRL.Scheduling.Clouds.pso import PSO
from utilize.Algorithms.DRL.Scheduling.Fogs.dqn_scheduing import RunFogScheduling_DQN
from utilize.Algorithms.DRL.Scheduling.Fogs.ppo_scheduing import RunFogScheduling_PPO
from utilize.Config import Config
import random
# from utilize.Algorithms.DRL.Scheduling.Fogs.test import RunTest as FogRunTest
import numpy as np
class Run():
    def __init__(self,A_resources=None,A_tasks=None): 
        self.resources=np.array(deepcopy(A_resources))
        self.jobs=np.array(deepcopy(A_tasks["jobs"]))
        self.edges=np.array(deepcopy(A_tasks["edges"]))
        self.fogs_resources=[]
        self.clouds_resources=[]
        self.fogs_resources+=[resource for resource in self.resources if resource["type"]=="Fog"]
        self.clouds_resources+=[resource for resource in self.resources if resource["type"]=="Cloud"]
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
        print(f"**********************\n {len(self.tasks)}\n****************************")
    def _allocation_test(self):
        config=Config()
        offloading=config.get_config("Global","offloading")
        
        if offloading==0:
            Cls=RunTaskAllocation_DQN(self.resources,self.tasks)
            result=self.allocation_list=Cls.test()
            
            # print(result)
            self.edges_list =[]
            self.fogs_list=[]
            self.cloud_list=[] 
            for i in range(len(self.allocation_list)):
                if self.allocation_list[i]==0:
                    self.edges_list.append({"type":"Edge","id":self.tasks[i]["device_id"]})
                elif self.allocation_list[i]==1:
                    self.cloud_list.append(self.tasks[i])
                elif self.allocation_list[i]==2:
                    self.fogs_list.append(self.tasks[i])   
        elif offloading==1:
            for i in range(len(self.tasks)):
                if random.randint(0,1)==0:
                    self.edges_list.append({"type":"Edge","id":self.tasks[i]["device_id"]})
                else:
                    self.fogs_list.append(self.tasks[i])
        elif offloading==2:
            for i in range(len(self.tasks)):
                if random.randint(0,1)==0:
                    self.edges_list.append({"type":"Edge","id":self.tasks[i]["device_id"]})
                else:
                    self.cloud_list.append(self.tasks[i])
        
        elif offloading==3:
            for i in range(len(self.tasks)):
                self.edges_list.append({"type":"Edge","id":self.tasks[i]["device_id"]})
        
        elif offloading==4:
            self.cloud_list=self.tasks                
        elif offloading==5:
            self.fogs_list=self.tasks                
    def allocation_train(self):
        Cls=RunTaskAllocation_DQN(self.resources,self.tasks)
        Cls.train()
    def _fog_schduling_train(self):
        # self._allocation_test()
        rtx=RunFogScheduling_PPO(resources=self.fogs_resources,tasks=self.fogs_list)
        # rtx=RunFogScheduling_DQN(resources=self.fogs_resources,tasks=self.fogs_list)
        rtx.run()
    def _cloud_scheduling_test(self):
        cloud_scheduling=PSO(self.cloud_list,self.clouds_resources)
        self.cloud_scheduling_list=cloud_scheduling.run()
    
    def _fog_schduling_test(self):
        rtx=RunFogScheduling_PPO(resources=self.fogs_resources,tasks=self.fogs_list)
        # rtx=RunFogScheduling_DQN(resources=self.fogs_resources,tasks=self.fogs_list)
        # test=self.rtx.FogRunTest(self.fogs_list,self.fogs_resources)
        result=self.fog_scheduling_list=rtx._test()
        # print(result)clas
        return result
    def scheduling(self):
        # self.allocation_train()
        self._allocation_test()
        # print(self.fogs_list)
        # self._allocation_test()
        # self._cloud_scheduling_test()
        self._fog_schduling_train()
        self._fog_schduling_test()
        print(self.fog_scheduling_list)
        # finall_result = []
        # for i in range(len(self.allocation_list)):
        #     if self.allocation_list[i] == 0:
        #         finall_result.append(self.edges_list.pop(0))
        #     elif self.allocation_list[i] == 1:
        #         finall_result.append({"type": "Cloud", "id": self.cloud_scheduling_list.pop(0)})
        #     elif self.allocation_list[i] == 2:
        #         finall_result.append({"type": "Fog", "id": self.fog_scheduling_list.pop(0)})

        # return finall_result
                    
    
        
        
     