from utilize.Algorithms.pso import PSO
from utilize.Algorithms.random import Random
from utilize.Execution.execut import Execut
import numpy as np
from threading import *

def specific_resource(id,resource,edge,job):
    current_res=0
    length=len(resource)
    if id==length-1:
        for i in range(1,len(edge)):
            if edge[i]["id"]==job[0]:
                current_res=edge[i]["specif"]
    else:
        current_res=resource[id]
        
    return current_res                
    

def Det_time_inter(task,job,edge): #this function return maximum end time between parents of task 
        tmax=task["time"]
        workflow=[]
        for numb2 in range(1,len(edge)):#determine devices in UE zone
            #print(edge[numb2]['id'],job[0][0])
            if edge[numb2]['id']==job[0][0]:
                workflow=edge[numb2]["workflow"]
        for numb1 in range(len(task["parentid"])):
            for numb2 in range(len(workflow)):
                if task["parentid"][numb1]==workflow[numb2][0]["id"]:
                    #print("task id:",task["id"], "   parid:",task["parentid"][numb1],"    task time:" ,task["time"],"   parent id id:",workflow[numb2][0]["id"], "end time paren:",workflow[numb2][0]["time"])
                    if tmax < workflow[numb2][0]["time"]:
                        tmax=workflow[numb2][0]["time"]
                        task["time"]=workflow[numb2][0]["time"]
                    #print("parent tassk id: ",workflow[numb2][0]["id"], "parent task time: ",workflow[numb2][0]["time"],"new task time:  ",task["time"],"\n############################################################")                                                                                             



def provisioned_resources_list(fog=[],cloud=[]):
        resource_list=[]
        if fog!=[]:
            for numb1 in range(1,len(fog)):
                resource_list.append(fog[numb1])
        if cloud!=[]:
            for numb1 in range(len(cloud)):
                resource_list.append(cloud[numb1])
        resource_list.append(0)  
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
"""این تابع یک ترتیب اجرا از از تمام تسک های تمام دیوایس ها ایجاد میکند"""
def job_list_task(edge,job):
    execute_list=[]
    for numb_E in range(1, len(edge)):
        execute_list.append({"device_id": edge[numb_E]["id"], "task":organiz_task(
            edge[numb_E]["workflow"])})
    counter = per = len(execute_list)
    while 1:
                #job = []
                counter %= per
                #this condition job has 2 item ["device_id","task_id"] and functionality this condition is select a job in order
                if len(execute_list[counter]["task"]) != 0:
                    job.append(([execute_list[counter]["device_id"],execute_list[counter]["task"].pop(0)]))
                    #np.insert(job,([execute_list[counter]["device_id"],execute_list[counter]["task"].pop(0)]))
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
        #job = []
        counter %= per
        #this condition job has 2 item ["device_id","task_id"] and functionality this condition is select a job in order
        if len(execute_list[counter]["task"]) != 0:
            job_list.append(([execute_list[counter]["device_id"],execute_list[counter]["task"].pop(0)]))
                    #np.insert(job,([execute_list[counter]["device_id"],execute_list[counter]["task"].pop(0)]))
        else:
            break
        counter += 1 
    return job_list                                          
"""این تابع ورک فلو تمام تمام دیوایس ها را لیست میکند"""
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
    Rand=PSO()
    scheduled_list=Rand.initialize_swarm(Resource_list,Job_list,ue_zone)
  
    #scheduled_list=Rand.schedul(Job_list,ue_zone,Resource_list)
    del Rand
    return scheduled_list

def exec(index,Job_list,inter_time,list_task,ue_zone,scheduled_list,Resource_list,current_times,flags,obj):
    EX=Execut()
    while len(Job_list)>0:
        # print(f"inter time: {inter_time}")
        # print(f"current time {current_times}")
        if flags[index]==0:
            break    
        with obj:
            if len(inter_time)>0:
                # print (current_times[index]," ---------------- ", inter_time[0]," ------------ ",index)
                if current_times[index]>= inter_time[0]:
                    inter_time.pop(0)
                    for i in range(len(flags)): flags[i]=0
                    break
     
        index_task=select_task(list_task,Job_list)
        current_edge=ue_zone[Job_list[0][0]+1]['specif']
        
            #print(list_task[index_task][1])
        Det_time_inter(list_task[index_task][1],Job_list,ue_zone)
        current_resource=specific_resource(scheduled_list[0],Resource_list,ue_zone,Job_list[0])
            #print (list_task[index_task][1])
        current_times[index]=EX.run(index,list_task[index_task][1],current_edge,current_resource,current_times)
        Job_list.pop(0)
        scheduled_list.pop(0)
    del EX
            
    """این جا یک شرط تایم بذار که اگه تایم بعد از اجرا از زمان تسک ورودی بیشتر شده یک استاپ بزنه و پروتکل های ورود دستگاه را اجرا کنه
        2.یک بخش برای رکورد مرحله به مرحله دیوایس ها در یک فایل سی اس وی یا هرچیز دیگه ای ذخیره کنه
        3. همین دیگه
        """       
def run(index,zones,ue_zone,clouds,scheduled_list,Job_list,list_task,current_times,inter_time,flags,add_ue,obj,new_device=[]):  
    if add_ue[index]==-1:
        # print(add_ue)
        # print(f"initialize fog zone: {index}       {current_times}")
        list_task=list_task[index]
        """list of all job of all zone"""
        Job_list=Job_list[index]
        current_fog_zone=zones[index]
        #current_times=current_times[index]
        scheduled_list=scheduled_list[index]
        #this function specifies a list of all resource in each fog zone
        Resource_list=provisioned_resources_list(current_fog_zone,clouds)
        #return a list in the form of [[device_id,task_id]]
        task_list(ue_zone,list_task)
        #return a list in the form of [[device_id,task_id]] that selected task in order from each device
        job_list_task(ue_zone,Job_list)
        scheduled_list.extend(scheduling(ue_zone,Job_list,Resource_list))
        exec(index,Job_list,inter_time,list_task,ue_zone,scheduled_list,Resource_list,current_times,flags,obj)    
    elif add_ue[index]==0:
        # print(add_ue)
        # print(f"conitinious fog zone : {index}                {current_times}")
        list_task=list_task[index]
        """list of all job of all zone"""
        Job_list=Job_list[index]
        current_fog_zone=zones[index]
        scheduled_list=scheduled_list[index]
        #this function specifies a list of all resource in each fog zone
        Resource_list=provisioned_resources_list(current_fog_zone,clouds)
        exec(index,Job_list,inter_time,list_task,ue_zone,scheduled_list,Resource_list,current_times,flags,obj)
    elif add_ue[index]==1:
        # print(add_ue)
        # print(f"add decvice to fog zone : {index}                  {current_times}")
        ue_zone.append(new_device)
        list_task=list_task[index]
        """list of all job of all zone"""
        Job_list=Job_list[index]
        current_fog_zone=zones[index]
        scheduled_list=scheduled_list[index]
        temp_list_task=temp_task_list(new_device)
        temp_joblist=temp_job_list_task(new_device)
        Resource_list=provisioned_resources_list(current_fog_zone,clouds)
        temp_scheduled_list=scheduling(ue_zone,temp_joblist,Resource_list)
        Job_list.extend(temp_joblist)
        list_task.extend(temp_list_task)
        scheduled_list.extend(temp_scheduled_list)
        #this function specifies a list of all resource in each fog zone  
        exec(index,Job_list,inter_time,list_task,ue_zone,scheduled_list,Resource_list,current_times,flags,obj) 