from utilize.Algorithms.pso import PSO
from utilize.Algorithms.random import Random
from utilize.Execution.execut import Execut
from utilize.Algorithms.DRL.main import Run
import numpy as np
from threading import *
# from utilize.Algorithms.DQN.Env.engine import Engine
def specific_resource(scheduled,resources,edge,job):
    """
    id={"type":x , "id":y}
    """
    
    
    for resource in resources:
        if resource["type"]==scheduled["type"] and resource["id"]==scheduled["id"]:
            return resource
    # current_res=0
    # length=len(resource)
    # if id==length-1:
    #     for i in range(len(edge)):
    #         if edge[i]["id"]==job[0]:
    #             current_res=edge[i]["specif"]
    # else:
    #     current_res=resource[id]
        
    # return current_res                
    

def Det_time_inter(task,job,edge): #this function return maximum end time between parents of task 
        tmax=task["time"]
        workflow=[]
        for numb2 in range(1,len(edge)):#determine devices in UE zone
           if edge[numb2]['id']==job[0][0]:
                workflow=edge[numb2]["workflow"]
        for numb1 in range(len(task["parentid"])):
            for numb2 in range(len(workflow)):
                if task["parentid"][numb1]==workflow[numb2][0]["id"]:
                   if tmax < workflow[numb2][0]["time"]:
                        tmax=workflow[numb2][0]["time"]
                        task["time"]=workflow[numb2][0]["time"]
                  


def provisioned_resources_list(fog=[],cloud=[],ue_zones=[]):
        # print(ue_zones)
        test=[]
        resource_list=[]
        if fog!=[]:
            for numb1 in range(1,len(fog)):
                resource_list.append(fog[numb1])
        if cloud!=[]:
            for numb1 in range(len(cloud)):
                resource_list.append(cloud[numb1])
        resource_list+=[edge["specif"] for edge in ue_zones[1:]]

        # resource_list.append(0)  
        return resource_list          
#this function list tasks in each workflow according to dependency between them 
def organiz_task(job):
    spare_list = []
    execut_queue = []
    for numbjob in range(len(job)+1):
        flag = 1
        counter = 0

        if len(spare_list) != 0:
            while (flag):
                for numbspare in range(len(spare_list)):
                    numbspare -= counter
                    counter = 0
                    if (set(spare_list[numbspare]["parentid"]).issubset(set(execut_queue))):
                        execut_queue.append(
                            spare_list[numbspare]["id"])
                        spare_list.pop(numbspare)
                        counter += 1
                    else:
                        flag = 0

                flag = 0
        if numbjob < len(job):
            if job[numbjob][0]['parentid'] == 0:
                execut_queue.append(job[numbjob][0]['id'])
            else:
                parents = job[numbjob][0]['parentid']
                if (set(parents).issubset(set(execut_queue))):
                    execut_queue.append(job[numbjob][0]['id'])
                else:
                    spare_list.append(
                        {"id": job[numbjob][0]['id'], "parentid": job[numbjob][0]['parentid']})

    return execut_queue                
"""This function creates an execution order of all tasks on all devices"""
def job_list_task(edge,job):
    execute_list=[]
    for numb_E in range(1, len(edge)):
        execute_list.append({"device_id": edge[numb_E]["id"], "task":organiz_task(
            edge[numb_E]["workflow"])})
    counter = per = len(execute_list)
    while 1:
                counter %= per
                #this condition job has 2 item ["device_id","task_id"] and functionality this condition is select a job in order
                if len(execute_list[counter]["task"]) != 0:
                    job.append(([execute_list[counter]["device_id"],execute_list[counter]["task"].pop(0)]))
                else:
                    break
                counter += 1           
          
def temp_job_list_task(edge):
    execute_list=[]
    job_list=[]
    execute_list.append({"device_id": edge["id"], "task":organiz_task(
            edge["workflow"])})
    counter = per = len(execute_list)
    while 1:
        counter %= per
        #this condition job has 2 item ["device_id","task_id"] and functionality this condition is select a job in order
        if len(execute_list[counter]["task"]) != 0:
            job_list.append(([execute_list[counter]["device_id"],execute_list[counter]["task"].pop(0)]))
        else:
            break
        counter += 1 
    return job_list                                          
"""This workflow function lists all devices"""
def task_list(edge,list_task):
    device_id=0
    for i in range(1,(len(edge))):
        device_id=edge[i]["id"]
        for j in range(len(edge[i]["workflow"])):
            list_task.append([device_id,edge[i]["workflow"][j][0]])           

def temp_task_list(edge):
    list_task=[]
    device_id=edge["id"]
    for j in range(len(edge["workflow"])):
        list_task.append([device_id,edge["workflow"][j][0]])
    return list_task

def select_task(task_list,job_list):
    for i in range(len(task_list)):
        if task_list[i][0]==job_list[0][0] and task_list[i][1]["id"]==job_list[0][1]:
            return i
        
def set_task():
    pass           
def scheduling(ue_zone,Job_list,Resource_list):
    scheduled_list=[]
    # Cls=Run(Resource_list,{"jobs":Job_list,"edges":ue_zone})
    # scheduled_list=Cls.scheduling()
    Cls=PSO()
    scheduled_list=Cls.run(Resource_list,Job_list,ue_zone)
    print(scheduled_list)
    del Cls
    return scheduled_list

def exec(index,Job_list,inter_time,list_task,ue_zone,scheduled_list,Resource_list,current_times,flags,obj):
    EX=Execut()
    # print(ue_zone)
    list_task[0][1]["makespan"]=1000
    # print(ue_zone[1]["workflow"][0][0]["makespan"])
    
    while len(Job_list)>0:
        if flags[index]==0:
            break    
        with obj:
            if len(inter_time)>0:
                if current_times[index]>= inter_time[0]:
                    inter_time.pop(0)
                    for i in range(len(flags)): flags[i]=0
                    break
     
        index_task=select_task(list_task,Job_list)
        current_edge=ue_zone[Job_list[0][0]+1]['specif']
        Det_time_inter(list_task[index_task][1],Job_list,ue_zone)
        # print(scheduled_list)
        current_resource=specific_resource(scheduled_list[0],Resource_list,ue_zone,Job_list[0])
        current_times[index]=EX.run(index,list_task[index_task][1],current_edge,current_resource,current_times)
        Job_list.pop(0)
        scheduled_list.pop(0)
        # print(counter)
        # counter-=1
    del EX
            
 
def run(index,zones,ue_zone,clouds,scheduled_list,Job_list,list_task,current_times,inter_time,flags,add_ue,obj,new_device=[]):  
    if add_ue[index]==-1:
        list_task=list_task[index]
        """list of all job of all zone"""
        Job_list=Job_list[index]
        current_fog_zone=zones[index]
        scheduled_list=scheduled_list[index]
        #this function specifies a list of all resource in each fog zone
        Resource_list=provisioned_resources_list(current_fog_zone,clouds,ue_zone)
        #return a list in the form of [[device_id,task_id]]
        task_list(ue_zone,list_task)
        #return a list in the form of [[device_id,task_id]] that selected task in order from each device
        job_list_task(ue_zone,Job_list)
        scheduled_list.extend(scheduling(ue_zone,Job_list,Resource_list))
        exec(index,Job_list,inter_time,list_task,ue_zone,scheduled_list,Resource_list,current_times,flags,obj)    
    elif add_ue[index]==0:
        list_task=list_task[index]
        """list of all job of all zone"""
        Job_list=Job_list[index]
        current_fog_zone=zones[index]
        scheduled_list=scheduled_list[index]
        #this function specifies a list of all resource in each fog zone
        Resource_list=provisioned_resources_list(current_fog_zone,clouds,ue_zone)
        exec(index,Job_list,inter_time,list_task,ue_zone,scheduled_list,Resource_list,current_times,flags,obj)
    elif add_ue[index]==1:
        ue_zone.append(new_device)
        list_task=list_task[index]
        """list of all job of all zone"""
        Job_list=Job_list[index]
        current_fog_zone=zones[index]
        scheduled_list=scheduled_list[index]
        temp_list_task=temp_task_list(new_device)
        temp_joblist=temp_job_list_task(new_device)
        Resource_list=provisioned_resources_list(current_fog_zone,clouds,ue_zone)
        temp_scheduled_list=scheduling(ue_zone,temp_joblist,Resource_list)
        Job_list.extend(temp_joblist)
        list_task.extend(temp_list_task)
        scheduled_list.extend(temp_scheduled_list)
        #this function specifies a list of all resource in each fog zone  
        exec(index,Job_list,inter_time,list_task,ue_zone,scheduled_list,Resource_list,current_times,flags,obj) 