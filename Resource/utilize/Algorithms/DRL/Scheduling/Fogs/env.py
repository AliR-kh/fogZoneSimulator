import numpy as np
from copy import deepcopy
class Engine():
    
    def __init__(self,resources=None,tasks=None):
        self.static_resources=resources
        self.static_tasks=tasks
        self.resources=[]
        self.tasks=[]
        self.reset()
        # self.config=Config() 
        # self._initial_task()
        # self._initial_resources()
        self._initial_state()
        self._initial_static_value()
        self._init_general_norm()
        # self.temp_state=None  
    def get_current_status(self):
        return self.state

    def reset(self):
        self.resources=deepcopy(self.static_resources)
        self.tasks=deepcopy(self.static_tasks)
    
        
    # def _initial_resources(self):
    #     try:
    #         number_of_resource=self.config.get_config(section="Resources",name="number_of_resources")
    #         config_resources=self.config.get_config(section="Resources",name="resource_data",type="dict")
    #         self.resources=Resource(number_of_resource,config_resources,self.A_resources)
    #     except Exception as e:
    #         print(e)
    # def _initial_task(self):
    #     try:
    #         config_tasks=self.config.get_config(section="Tasks",name="tasks_data",type="dict")
    #         self.tasks=Task(config_tasks,self.A_tasks)
    #     except Exception as e:
    #          print(e)
        
     
    def _initial_static_value(self):
        self.min_task_mips = float(min(d["runtime"] for d in self.tasks))
        self.max_task_mips = float(max(d["runtime"] for d in self.tasks))
        self.min_task_size = float(min(d["sizein"] for d in self.tasks))
        self.max_task_size = float(max(d["sizein"] for d in self.tasks))

        # استخراج ویژگی‌های منابع
        self.min_resource_cpu = float(min(d["mips"] for d in self.resources))
        self.max_resource_cpu = float(max(d["mips"] for d in self.resources))
        self.min_bandwidth = float(min(d["down_bw"] for d in self.resources))
        self.max_bandwidth = float(max(d["down_bw"] for d in self.resources))
        self.min_resource_power = float(min(d["con_pow_active"] for d in self.resources))
        self.max_resource_power = float(max(d["con_pow_active"] for d in self.resources))
        self.min_resource_cost = float(min(d["ratepermipscost"] for d in self.resources))
        self.max_resource_cost = float(max(d["ratepermipscost"] for d in self.resources))
        
    def compute_processing_norm(self):
        self.max_processing_time = (self.max_task_mips*1000) / self.min_resource_cpu
        self.total_processing_time_upper_bound = self.get_number_of_task() * self.max_processing_time
        self.max_processing_time_for_norm = self.total_processing_time_upper_bound + self.max_processing_time

    def compute_transfer_norm(self):
        self.max_transfer_time = (self.max_task_size/1000 )/ self.min_bandwidth
        self.total_transfer_time_upper_bound = self.get_number_of_task() * self.max_transfer_time
        self.max_transfer_time_for_norm = self.total_transfer_time_upper_bound + self.max_transfer_time

    def compute_energy_norm(self):
        self.max_energy_per_task = (self.max_processing_time * self.max_resource_power)/1000
        self.total_energy_upper_bound = self.get_number_of_task() * self.max_energy_per_task
        self.max_energy_for_norm = self.total_energy_upper_bound + self.max_energy_per_task

    def compute_load_balancing_norm(self):
        self.max_load_balancing_for_norm =sum(float(d["runtime"]) for d in self.tasks)
        # print(f"self.max_load_balancing_for_norm : {self.max_load_balancing_for_norm}")

    def compute_cost_norm(self):
        self.max_cost_per_task = self.max_processing_time * self.max_resource_cost
        self.total_cost_upper_bound = self.get_number_of_task() * self.max_cost_per_task
        self.max_cost_for_norm = self.total_cost_upper_bound + self.max_cost_per_task

    def _init_general_norm(self):
        self.compute_processing_norm()
        self.compute_transfer_norm()
        self.compute_energy_norm()
        self.compute_cost_norm()
        # self.compute_load_balancing_norm()
        self.w_ex=.2
        self.w_tr=0.2
        self.w_ec=0.33
        self.w_cp=0.33
        self.w_lb=0.2
        self.w_ms=0.33
    
    
    def trancfer_time(self,resource,task):
        return (float(task["sizein"])/1000)/float(resource["down_bw"])
        
    def energy_consumption(self,resource,task):
        task_execution=self.execution_time(resource,task)
        return (task_execution * float(resource["con_pow_active"]))/1000    
        
    def execution_time(self,resource,task):
        return (float(task["runtime"])*1000)/float(resource["mips"])
        
    def execution_cost(self,resource,task):
        task_execution=self.execution_time(resource,task)
        return task_execution * float(resource["ratepermipscost"])   
        
    def execution_load_balancing(self,resource,task):
        return resource["assigned_mips"]+task["runtime"]
          
    
    def summary_changed(self,resource,task):
        return {
            "processing_time":self.execution_time(resource,task),
            "transfer_time": self.trancfer_time(resource,task),
            "energy": self.energy_consumption(resource,task),
            # "load_balancing":self.execution_load_balancing(resource,task),
            "cost": self.execution_cost(resource,task)
        }
              
    def compute_general_norm(self,resource,task):
        summary_changed=self.summary_changed(resource,task)
        execution_time_norm=summary_changed["processing_time"]
        tranfer_time_norm=summary_changed["transfer_time"]
        makespan=(execution_time_norm+tranfer_time_norm+resource["time"])/(self.max_processing_time_for_norm+self.max_transfer_time_for_norm)
        energy_conumption_norm=(summary_changed["energy"]+resource["total_energy"])/self.max_energy_for_norm
        cost_per_second_norm=(summary_changed["cost"]+resource["total_cost"])/self.max_cost_for_norm
        # load_balancing_norm=summary_changed["load_balancing"]/self.max_load_balancing_for_norm
        
        # print(f"norm changed ext {execution_time_norm}   and tt {tranfer_time_norm}   makespan {makespan}")
        # print(f"energy ext {energy_conumption_norm}   and cost {cost_per_second_norm}   load {load_balancing_norm}")
        return (self.w_ms*makespan)+(self.w_ec*energy_conumption_norm)+(self.w_cp*cost_per_second_norm) 
    
    def _reward(self,task_index,resource_index):
        task=self.tasks[task_index]
        resource=self.resources
        reward=[]
        for i in range(len(resource)):
            temp_reward=-(self.execution_time(resource[i],task)+resource[i]["time"])
            reward.append(temp_reward)
        return max(reward)/reward[resource_index]
    

    def _calcultion_state(self,task_index,resource_index):
        task=self.tasks[task_index]
        resource=self.resources[resource_index]
        new_state=self.compute_general_norm(resource,task)
        return new_state

    def temporary_state(self,task_index):
        self.temp_state=self.state.copy()
        for i in range(len(self.resources)):
            self.temp_state[i]=self._calcultion_state(task_index,i)
        if max(self.temp_state)>1:
            print("********************************************")
            print(self.temp_state)
        return self.temp_state
    
    def set_property_to_resource(self,resource_index,summary_changed):
        self.resources[resource_index]["time"]+=summary_changed["processing_time"]+summary_changed["transfer_time"]
        # self.resources[resource_index]["assigned_mips"]+=summary_changed["load_balancing"]
        self.resources[resource_index]["total_energy"]+=summary_changed["energy"]
        self.resources[resource_index]["total_cost"]+=summary_changed["cost"]
        # self.resources[resource_index]["queue_time"]+=summary_changed["processing_time"]
    
     
    def step(self,task_index,action):
        old_state=self.state.copy()
        self.state[action]=self._calcultion_state(task_index,action)
        reward=self._reward(task_index,action)
        self.set_property_to_resource(action,self.summary_changed(self.resources[action],self.tasks[task_index]))
        done= True if task_index==len(self.tasks)-1 else False
        return old_state,self.state,reward,done
    def _initial_state(self):
        self.state=np.zeros(5)
        self.temp_state=None
    

    def get_number_of_task(self):
        return len(self.tasks)