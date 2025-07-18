from utilize.Algorithms.DRL.Env.resources import Resource
from utilize.Algorithms.DRL.Env.tasks import Task
from utilize.Algorithms.DRL.Env.env import Env
from utilize.Algorithms.DRL.Configs.config import Config
import numpy as np
import torch
class Engine(Env):
    
    def __init__(self,A_resources=None,A_tasks=None):
        self.A_resources=A_resources
        self.A_tasks=A_tasks
        self.config=Config() 
        self._initial_task()
        self._initial_resources()
        # self._initial_state()
        # self._initial_static_value()
        # self._init_general_norm()
        # self.temp_state=None  
    def get_current_status(self):
        return self.state

    def reset(self):
        self._initial_resources()
        self._initial_task()
        self._initial_state()
    
        
    def _initial_resources(self):
        try:
            number_of_resource=self.config.get_config(section="Resources",name="number_of_resources")
            config_resources=self.config.get_config(section="Resources",name="resource_data",type="dict")
            self.resources=Resource(number_of_resource,config_resources,self.A_resources)
        except Exception as e:
            print(e)
    def _initial_task(self):
        try:
            config_tasks=self.config.get_config(section="Tasks",name="tasks_data",type="dict")
            self.tasks=Task(config_tasks,self.A_tasks)
        except Exception as e:
             print(e)
        
     
    def _initial_static_value(self):
        self.min_task_mips = min(d["mips"] for d in self.tasks.get_current_status())
        self.max_task_mips = max(d["mips"] for d in self.tasks.get_current_status())
        self.min_task_size = min(d["size"] for d in self.tasks.get_current_status())
        self.max_task_size = max(d["size"] for d in self.tasks.get_current_status())

        # استخراج ویژگی‌های منابع
        self.min_resource_cpu = min(d["cpu"] for d in self.resources.get_current_status())
        self.max_resource_cpu = max(d["cpu"] for d in self.resources.get_current_status())
        self.min_bandwidth = min(d["down_bw"] for d in self.resources.get_current_status())
        self.max_bandwidth = max(d["down_bw"] for d in self.resources.get_current_status())
        self.min_resource_power = min(d["consume_power"] for d in self.resources.get_current_status())
        self.max_resource_power = max(d["consume_power"] for d in self.resources.get_current_status())
        self.min_resource_cost = min(d["cost_per_second"] for d in self.resources.get_current_status())
        self.max_resource_cost = max(d["cost_per_second"] for d in self.resources.get_current_status())
        
    def compute_processing_norm(self):
        self.max_processing_time = self.max_task_mips / self.min_resource_cpu
        self.total_processing_time_upper_bound = self.tasks.number_of_task * self.max_processing_time
        self.max_processing_time_for_norm = self.total_processing_time_upper_bound + self.max_processing_time

    def compute_transfer_norm(self):
        self.max_transfer_time = self.max_task_size / self.min_bandwidth
        self.total_transfer_time_upper_bound = self.tasks.number_of_task * self.max_transfer_time
        self.max_transfer_time_for_norm = self.total_transfer_time_upper_bound + self.max_transfer_time

    def compute_energy_norm(self):
        self.max_energy_per_task = self.max_processing_time * self.max_resource_power
        self.total_energy_upper_bound = self.tasks.number_of_task * self.max_energy_per_task
        self.max_energy_for_norm = self.total_energy_upper_bound + self.max_energy_per_task

    def compute_load_balancing_norm(self):
        self.max_load_balancing_for_norm =sum(d["mips"] for d in self.tasks.get_current_status())
        # print(f"self.max_load_balancing_for_norm : {self.max_load_balancing_for_norm}")

    def compute_cost_norm(self):
        self.max_cost_per_task = self.max_processing_time * self.max_resource_cost
        self.total_cost_upper_bound = self.tasks.number_of_task * self.max_cost_per_task
        self.max_cost_for_norm = self.total_cost_upper_bound + self.max_cost_per_task

    def _init_general_norm(self):
        self.compute_processing_norm()
        self.compute_transfer_norm()
        self.compute_energy_norm()
        self.compute_cost_norm()
        self.compute_load_balancing_norm()
        self.w_ex=self.config.get_config(section="Objective",name="execution_time",type="float")
        self.w_tr=self.config.get_config(section="Objective",name="transfer_time",type="float")
        self.w_ec=self.config.get_config(section="Objective",name="energy_consumption",type="float")
        self.w_cp=self.config.get_config(section="Objective",name="cost_per_seccond",type="float")
        self.w_lb=self.config.get_config(section="Objective",name="load_balancing",type="float")
        self.w_ms=self.config.get_config(section="Objective",name="makespan",type="float")
    
    
    def trancfer_time(self,resource,task):
        return task["size"]/resource["down_bw"]
        
    def energy_consumption(self,resource,task):
        task_execution=self.execution_time(resource,task)
        return task_execution * resource["consume_power"]    
        
    def execution_time(self,resource,task):
        return task["mips"]/resource["cpu"]
        
    def execution_cost(self,resource,task):
        task_execution=self.execution_time(resource,task)
        return task_execution * resource["consume_power"]   
        
    def execution_load_balancing(self,resource,task):
        return resource["assigned_mips"]+task["mips"]
          
    
    def summary_changed(self,resource,task):
        return {
            "processing_time":self.execution_time(resource,task),
            "transfer_time": self.trancfer_time(resource,task),
            "energy": self.energy_consumption(resource,task),
            "load_balancing":self.execution_load_balancing(resource,task),
            "cost": self.execution_cost(resource,task)
        }
              
    def compute_general_norm(self,resource,task):
        summary_changed=self.summary_changed(resource,task)
        execution_time_norm=summary_changed["processing_time"]
        tranfer_time_norm=summary_changed["transfer_time"]
        makespan=(execution_time_norm+tranfer_time_norm+resource["makespan"])/(self.max_processing_time_for_norm+self.max_transfer_time_for_norm)
        energy_conumption_norm=(summary_changed["energy"]+resource["consumed_power"])/self.max_energy_for_norm
        cost_per_second_norm=(summary_changed["cost"]+resource["consumed_cost"])/self.max_cost_for_norm
        load_balancing_norm=summary_changed["load_balancing"]/self.max_load_balancing_for_norm
        
        # print(f"norm changed ext {execution_time_norm}   and tt {tranfer_time_norm}   makespan {makespan}")
        # print(f"energy ext {energy_conumption_norm}   and cost {cost_per_second_norm}   load {load_balancing_norm}")
        return (self.w_ms*makespan)+(self.w_ec*energy_conumption_norm)+(self.w_lb*load_balancing_norm)+(self.w_cp*cost_per_second_norm) 
    
    def _reward(self,task_index,resource_index):
        task=self.tasks.get_current_status()[task_index]
        resource=self.resources.get_current_status()
        reward=[]
        for i in range(len(resource)):
            temp_reward=-(self.execution_time(resource[i],task)+resource[i]["queue_time"])
            reward.append(temp_reward)
        return max(reward)/reward[resource_index]
    

    def _calcultion_state(self,task_index,resource_index):
        task=self.tasks.get_current_status()[task_index]
        resource=self.resources.get_current_status()[resource_index]
        new_state=self.compute_general_norm(resource,task)
        return new_state

    def temporary_state(self,task_index):
        self.temp_state=self.state.copy()
        for i in range(len(self.resources.get_current_status())):
            self.temp_state[i]=self._calcultion_state(task_index,i)
        if max(self.temp_state)>1:
            print("********************************************")
            print(self.temp_state)
        return self.temp_state
    
     
    def step(self,task_index,action):
        old_state=self.state.copy()
        self.state[action]=self._calcultion_state(task_index,action)
        reward=self._reward(task_index,action)
        self.resources.set_property_to_resource(action,self.summary_changed(self.resources.get_current_status()[action],self.tasks.get_current_status()[task_index]))
        done= True if task_index==len(self.tasks.get_current_status())-1 else False
        return old_state,self.state,reward,done
    def _initial_state(self):
        self.state=np.zeros(5)
        self.temp_state=None
    
            