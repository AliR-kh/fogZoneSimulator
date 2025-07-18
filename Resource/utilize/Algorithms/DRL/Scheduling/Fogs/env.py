from copy import deepcopy
import numpy as np
class Env():
    def __init__(self,tasks,resources):
        self.tasks=deepcopy(tasks)
        self.resources=deepcopy(resources)
        self.reset()
    def _seperate_resources(self):
        self.fogs_resources+=[resource for resource in self.resources if resource["type"]=="Fog"]
        self.clouds_resources+=[resource for resource in self.resources if resource["type"]=="Cloud"]
        self.edges_resources+=[resource for resource in self.resources if resource["type"]=="Edge"]
        self.fogs_resources=np.array(self.fogs_resources)
        self.clouds_resources=np.array(self.clouds_resources)
        self.edges_resources=np.array(self.edges_resources)
        
    def _calculate_load(self):
        pass
    
    def _compute_load_balancing_norm(self):
        self.max_runtime=sum(float(task["runtime"]) for task in self.tasks)
        self.max_load_Edge={} 
        self.max_edge_mips={} 
        self.max_fogs_mips=sum(float(fog["mips"]) for fog in self.fogs_resources)
        self.max_clouds_mips=sum(float(cloud["mips"]) for cloud in self.clouds_resources)
        if self.max_fogs_mips>0:
            self.max_load_fog=(self.max_runtime*1000)/self.max_fogs_mips
        if self.max_clouds_mips>0:    
            self.max_load_cloud=(self.max_runtime*1000)/self.max_clouds_mips
        for edge in self.edges_resources:
            self.max_load_Edge[str(edge["id"])]=0
            self.max_edge_mips[str(edge["id"])]=edge["mips"]
            self.assigned_to_edges[str(edge["id"])]=0
            for task in self.tasks:
                if str(task["device_id"])==str(edge["id"]):
                    self.max_load_Edge[str(edge["id"])]+=(float(task["runtime"])*1000)/float(edge["mips"])
                    

                    
    def _init_general_norm(self):
        self._compute_load_balancing_norm()
        
    def execution_load_balancing(self,resource,task):
        return resource["assigned_mips"]+task["mips"]
    
    def _summary_changed(self,task):
        self.summary_changed={
            "edge":self.assigned_to_edges[str(task["device_id"])]+(float(task["runtime"])*1000/self.max_edge_mips[str(task["device_id"])]),
            "fog":self.assigned_to_fogs+(float(task["runtime"])*1000/self.max_fogs_mips),
            "cloud":self.assigned_to_clouds+(float(task["runtime"])*1000/self.max_clouds_mips)    
        }
        
    def compute_general_norm(self,resource,task):
        self._summary_changed(task)
        if resource["type"]=="edge":
            return self.summary_changed["edge"]/self.max_load_Edge[str(task["device_id"])]
        elif resource["type"]=="cloud":
            return self.summary_changed["cloud"]/self.max_load_cloud
        elif resource["type"]=="fog":
            return self.summary_changed["fog"]/self.max_load_fog
    
    
    def _temporary_state(self,task_index):
        self.temp_state=self.state.copy()
        task=self.tasks[task_index]
        # print(task)
        self.temp_state[0]=self.compute_general_norm({"type":"edge","device_id":str(task["device_id"])},task)       
        self.temp_state[1]=self.compute_general_norm({"type":"cloud"},task)       
        self.temp_state[2]=self.compute_general_norm({"type":"fog"},task)
    
    
    def _reward(self,task_index,resource):
        reward=[]
        edge=-self.summary_changed["edge"]
        fog=-self.summary_changed["fog"]
        cloud=-self.summary_changed["cloud"]
        reward.append(edge)
        reward.append(fog)
        reward.append(cloud)
        if resource["type"]=="edge":
           return max(reward)/edge
        elif resource["type"]=="fog":
            return max(reward)/fog
        elif resource["type"]=="cloud":
            return max(reward)/cloud
    
    def set_property_to_resource(self,resource,task):
        if resource["type"]=="edge":
            # print(f"before select edge_id{task["device_id"]}  is {self.assigned_to_edges[str(task["device_id"])]}")        
            self.assigned_to_edges[str(task["device_id"])]=self.summary_changed["edge"]
            # print(f"summary_changed is {self.summary_changed["edge"]}")
            # print(f"after select edge_id{task["device_id"]}  is {self.assigned_to_edges[str(task["device_id"])]}")
            # print("***************************************************************************************")
        elif resource["type"]=="fog":
            # print(f"before select fog is {self.assigned_to_fogs}")  
            self.assigned_to_fogs=self.summary_changed["fog"]
            # print(f"summary_changed is {self.summary_changed["fog"]}")
            # print(f"after select fog is {self.assigned_to_fogs}")
            # print("***************************************************************************************")
        elif resource["type"]=="cloud":
            # print(f"before select cloud is {self.assigned_to_clouds}")  
            self.assigned_to_clouds=self.summary_changed["cloud"]
            # print(f"summary_changed is {self.summary_changed["cloud"]}")
            # print(f"after select cloud is {self.assigned_to_clouds}")
            # print("***************************************************************************************")
    def step(self,task_index,action):
        old_state=self.state.copy()
        self.state[action["id"]]=self.compute_general_norm(action["resource"],self.tasks[task_index])
        reward=self._reward(task_index,action["resource"])
        self.set_property_to_resource(action["resource"],self.tasks[task_index])
        done= True if task_index==len(self.tasks)-1 else False
        return old_state,self.state,reward,done
               
    def _initialize_state(self):
        self.state=np.zeros([3])
    
    
    
    def reset(self):
        self.fogs_resources=[]
        self.clouds_resources=[]
        self.edges_resources=[]
        self.assigned_to_fogs=0
        self.assigned_to_clouds=0
        self.assigned_to_edges={}
        self._seperate_resources()
        self._initialize_state()
        self._init_general_norm()