from utilize.Reource_zone.Fog_Resource import Fog
from utilize.Execution.execut import Execut as Ex
from utilize.Algorithms.pso import PSO
from utilize.management.management import Management as MN
import threading
import concurrent.futures
import random
class Fog_broker:
    number_zone=0
    def __init__(self,number_zone,fog=[], edge=[], jobs=0) -> None:
        self.number_zone=number_zone
        fog = fog
        edge = edge
        jobs = jobs
        
    def Det_time_inter(self,task,job,edge,res): #this function return maximum end time between parents of task 
        #print(task,res)
        tmax=task["time"]
        workflow=[]
        for numb1 in range(len(edge)):#determine UE zone
            for numb2 in range(1,len(edge[numb1])):#determine devices in UE zone
                if edge[numb1][numb2]['id']==job[0]:
                    workflow=edge[numb1][numb2]["workflow"]
        for numb1 in range(len(task["parentid"])):
            for numb2 in range(len(workflow)):
                if task["parentid"][numb1]==workflow[numb2][0]["id"]:
                    #print("task id:",task["id"], "   parid:",task["parentid"][numb1],"    task time:" ,task["time"],"   parent id id:",workflow[numb2][0]["id"], "end time paren:",workflow[numb2][0]["time"], "     vm:",res["type"],res["id"])
                    if tmax < workflow[numb2][0]["time"]:
                        tmax=workflow[numb2][0]["time"]
                        task["time"]=workflow[numb2][0]["time"]
                    #print("parent tassk id: ",workflow[numb2][0]["id"], "parent task time: ",workflow[numb2][0]["time"],"new task time:  ",task["time"],"\n############################################################")                                                                                             

    def set_time_job(self,Time,edge,task,job):
        for numb1 in range(len(edge)):
                if edge[numb1][0]["id"]==job[0]:
                    for numb2 in range(1,len(edge[numb1])):
                        if edge[numb1][numb2]["id"]==job[1]:
                            for numb3 in range(len(edge[numb1][numb2]["workflow"])):
                                if edge[numb1][numb2]["workflow"][numb3]["id"]==task[0]:
                                    edge[numb1][numb2]["workflow"][numb3]["time"]=Time     
    def set_attribute_resource(self,resource,IE,AE,CP,CT,CM):
        resource["idle_energy"]+=IE
        resource["acive_energy"]+=AE
        resource["cost_process"]+=CP
        resource["cost_transfer"]+=CT
        resource["cost_memory"]+=CM
        
    def select_resource(self,task,job,task_list,resource_list,result):
        
        for numb in range(len(job)):
            x=result[numb]
            if resource_list[result[numb]]==len(resource_list)-1:
                temp1=self.select_edge_res(job[numb],task)
                task_list.append(temp1)
            else:    
                task_list.append(resource_list[x])        
        """ Finaly_Resource=[]
        #task["time"]=self.Det_time_inter(task,job,task_list)
        for res in resource_list:
            if res["type"] == result["type"]:
                if result["type"] == "Edge":
                    Finaly_Resource = res
                if result["type"] == "Fog":
                    Finaly_Resource = res
                    for numb_f in range(len(fog)):
                        if fog[numb_f]["id"] == result["id"]:
                            fog[numb_f]["exist_flag"] = 1
                if result["type"] == "Cloud":
                    Finaly_Resource = res
                    for numb_f in range(len(fog)):
                        if fog[numb_f]["id"] == result["id"]:
                            fog[numb_f]["exist_flag"] = 1
        return Finaly_Resource """
    
    def provisioned_resources_list(self,resource_list,fog=[],cloud=[]):
        if fog!=[]:
            for numb1 in range(1,len(fog)):
                resource_list.append(fog[numb1])
        if cloud!=[]:
            for numb1 in range(len(cloud)):
                resource_list.append(cloud[numb1])
                    
                
                
                                        
    
# output is [[{'id': 0}, {'id': 0, 'type': 'Fog', 'mips': '', 'parentid': 0, 'con_pow_active': '', 'con_pow_idle': 0, 'down_bw': 0, 'down_cost': 0, 'up_bw': 0, 'up_cost': 0, 'memory_cost': 0, 'exist_flag': 0, 'memory_size': 0}]]
# out[0:n] is number of zone or sepecification of zon
# out[x][0] is id of zone
# out[x][1:n] specification of fog node
    def createfog(self):
        fog_zone_list = []
        fog = Fog()
        alg = "N"#input("using the algorith: Y or N :")
        if alg == ('Y') or alg == ('y'):
            pass
        else:
            alg = 1
            numzone =1# input("number of fog zone: ")
            for temp in range(int(self.number_zone)):
                fog_zone_list.append(fog.create_fog_device(temp, alg))

            return fog_zone_list


    def select_edge_res(self,job,edge):
        for numb_EZ in range(len(edge)):
                for numb_E in range(1,len(edge[numb_EZ])):
                    if edge[numb_EZ][numb_E]["id"] == job[0]:
                        for workflow in edge[numb_EZ][numb_E]["workflow"]:
                            if workflow[0]['id'] == job[1]:
                                
                                Edge_Resource = edge[numb_EZ][numb_E]["specif"]
                                #print(edge[numb_EZ][numb_E]["specif"])
                                return Edge_Resource                            
        
    
    def select_task(self,job,edge,task_list):
        for numbJ in range(len(job)):
            for numb_EZ in range(len(edge)):
                    for numb_E in range(1,len(edge[numb_EZ])):
                        if edge[numb_EZ][numb_E]["id"] == job[numbJ][0]:
                            for workflow in edge[numb_EZ][numb_E]["workflow"]:
                                if workflow[0]['id'] == job[numbJ][1]:
                                    task_list.append(workflow[0])                     
    
    def run_execut_task(self, fog, edge,cloud):
        
        Finaly_Resource =[]
        task_list=[]
        resource_list = []
        execute_list = []
        selectj =0# ST()
        # first should create execute list of workflows of each devices
        # this command is for several uezone in a fog zone
        # if there are several uezone in a fogzon processing oredering is fifo between ue zones
        for numb_EZ in range(len(edge)):
            for numb_E in range(1, len(edge[numb_EZ])):
                execute_list.append({"device_id": edge[numb_EZ][numb_E]["id"], "task": selectj.organiz_task(
                    edge[numb_EZ][numb_E]["workflow"])})
        flag = 1
        job = []
        counter = per = len(execute_list)
        task ={}
        x = 0
        #joblist=execute_list.copy()
        
        while flag:  # in this loop is picked a job from list accordingly dependency between their and this is based on round robin + fifo
            result = []
            while 1:
                #job = []
                counter %= per
                #this condition job has 2 item ["device_id","task_id"] and functionality this condition is select a job in order
                if len(execute_list[counter]["task"]) != 0:
                    job.append([execute_list[counter]["device_id"],execute_list[counter]["task"].pop(0)])
                else:
                    break
                counter += 1
            #this loop selects the workflow of the selected job
            """ 
            for numb_EZ in range(len(edge)):
                for numb_E in range(1,len(edge[numb_EZ])):
                    if edge[numb_EZ][numb_E]["id"] == job[0]:
                        for workflow in edge[numb_EZ][numb_E]["workflow"]:
                            if workflow[0]['id'] == job[1]:
                                task = workflow[0]
                                Edge_Resource = edge[numb_EZ][numb_E]["specif"] """                   
            Man = MN()
            Mpso = PSO()
            Exe = Ex()
            #this function performs the checking the free resource
            """
            t=1 
            while t:
                resource_list = Man.run(fog=fog, edge=Edge_Resource,task=task)
                if resource_list==[]:
                    result=Man.run_spare(fog=fog, edge=Edge_Resource) #if resource is full at the moment, job is waiting to getting empty
                    queue=result-task["time"]
                    task["time"]=result
                    task["time_queue"]=queue
                else:
                    t=0   """  
                    
            #this function give the finaly resource list
            self.provisioned_resources_list(resource_list,fog,cloud) 
            #this function performs the scheduling of the job
            result = Mpso.initializing(resource_list,job,edge[0])
            #print (resource_list)
            #print(result)
            self.select_resource(edge,job,Finaly_Resource,resource_list,result)
            self.select_task(job,edge,task_list)
            #this condition selects the selected resource by type and id of resource
            if result != 0:
                counter1=0
                while counter1<len(job):
                    self.Det_time_inter(task_list[counter1],job[counter1],edge,Finaly_Resource[counter1])                                              
                    executor=concurrent.futures.ThreadPoolExecutor()
                    future=executor.submit(Exe.run,task_list[counter1],Finaly_Resource[counter1])
                    result=future.result()
                    Time,AE,IE,PC,TC,MC=result  #end_time,active_energy,idle_energy,process_cost,transfer_cost,memory_cost
                    #self.set_time_job(Time,edge,task,job)
                    counter1+=1
                if counter1>=len(job):
                    flag=0
                    del Man, Mpso, Exe
                    #cal=Calculation()
                    #cal.result(fog,edge,cloud)
                    break   