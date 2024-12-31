import socket
import threading
from threading import *
import time
import pickle
import numpy as np
from utilize.Reource_zone.UE_Zone_Creatore import Fog_broker
from utilize.send_message import send_message
from utilize.Scheduling.discreate_scheduling import run as RUN
from utilize.Reource_zone.clouds_resource import Cloud
from utilize.Calcuation_model.Caculation.calculation import Calculation
current_times=[]
flags=[]
inter_time=[]
number_zone=0
zones=[]
clouds=[]
Fog_b=0
scheduled_list=[]
task_list=[]
ue_zone=[]
job_list=[]
add_ue=[]
obj=0
flag_srver=1

# this program is resource Server that reiceve request from client, and detect requset and pass request to a function



# this function for once call when broker request from server fo initial
def connection(Data):
    global current_times,flags,inter_time,number_zone,Fog_b,zones,scheduled_list,task_list,clouds,job_list,add_ue,obj
    number_zone=Data["numbers_zone"]
   
    for i in range(number_zone):
        job_list.append([])
        task_list.append([])
        scheduled_list.append([])
        add_ue.append(-1)
        current_times.append(0)
    flags=Data["flags"]
    inter_time=Data["inter_time"]
    # create fog zone and cloud based on number of Ue zone
    Fog_b=Fog_broker(number_zone)
    Clouds=Cloud()
    clouds=[]#Clouds.create_clouds_device()
    zones=Fog_b.createfog()
    obj=threading.Lock()
    response=zones#f"fog-zones is intialized.\n there are {number_zone} zone in environment"
    return  response

    
# For the first time that Ue environment send request for execut task, call this function
def scheduling(Data):
    global current_times,flags,inter_time,number_zone,Fog_b,zones,scheduled_list,task_list,ue_zone,clouds,job_list,task_list,add_ue,obj
    index=0
    ue_zone=Data["data"]
    threads=[]
    for i in range(number_zone):
        for j in range(number_zone):
            if ue_zone[j][0]["assign_resource"]==i:
                index=j
                break
        select_ue_zone=Data["data"][index]    
        threads.append(threading.Thread(target=RUN,args=(i,zones,select_ue_zone,clouds,scheduled_list,job_list,task_list,current_times,inter_time,flags,add_ue,obj)))
        threads[i].start()
    for i in range(number_zone):
        threads[i].join()   
    if flags[0]==0:
        response={"data":0,"flags":1} 
        return response
    response={"data":ue_zone,"flags":0}   
    return response

# when a new edge joined to ue environment for execut task, call this function
def scheduling_add_ue(Data):
    global current_times,flags,inter_time,number_zone,Fog_b,zones,scheduled_list,task_list,ue_zone,clouds,job_list,task_list,add_ue,obj
    zone_id=Data["zone_id"]
    index=0
    threads=[]
    new_device=[]
    for k in range(len(flags)): flags[k]=1
    for i in range(number_zone):
        for j in range(number_zone):
            if ue_zone[j][0]["assign_resource"]==i:
                index=j
                
        if zone_id==i:
            add_ue[i]=1
            new_device=Data["data"]
        else:
            add_ue[i]=0 
            new_device=[]   
        select_ue_zone=ue_zone[index]    
        threads.append(threading.Thread(target=RUN,args=(i,zones,select_ue_zone,clouds,scheduled_list,job_list,task_list,current_times,inter_time,flags,add_ue,obj,new_device)))
        threads[i].start()
    for i in range(number_zone):
        threads[i].join()
    if flags[0]==0:
        response={"data":0,"flags":1} 
        return response
    response={"data":ue_zone,"flags":0}     
    return response
    

def get_ue_zone():
    global ue_zone
    return ue_zone

def fog_zones_status():
    global ue_zone,zones,clouds
    return zones,clouds


def total_calculation():
    rtx=Calculation()
    total_result=[]
    for i in range(len(ue_zone)):
        edge=ue_zone[i]
        fog_index=edge[0]['assign_resource']
        fog=zones[fog_index]
        total_result.append(rtx.total_result(fog,clouds,edge,fog_index))
        
    
    return total_result

def close_program():
    global flag_srver
    flag_srver=0
    return 1

# after give request and decode this, this function detect request
def detect_message(Data):
    if Data['request']=="connection":
        return connection(Data)
    elif Data['request']=="scheduling":
       return scheduling(Data)
    elif Data['request']=="scheduling_add_ue":
        return scheduling_add_ue(Data)
    elif Data['request']=="get_ue_zones":
        return get_ue_zone()
    elif Data['request']=="fog_zones_stattus":
        return fog_zones_status()
    elif Data['request']=="total_calculation":
        return total_calculation()
    elif Data['request']=="close_program":
        return close_program()    
    

def handle_client(client_socket, address):
    CHUNK_SIZE=8192
    print(f"Accepted connection from {address}")
    buffer=bytearray()
    message_header=client_socket.recv(1024)
    message_header=pickle.loads(message_header)
    index=message_header["number_chunk"]
    last_chunk=message_header["last_chunk"]
    i=0
    while True:
        message_data=client_socket.recv(CHUNK_SIZE)
        if i <index-1:
            if len(message_data)==CHUNK_SIZE:
                buffer.extend(message_data)
                i+=1
                client_socket.send(b"1")
            else:  
                client_socket.send(b"0")
        elif i==index -1:
            if len(message_data)==last_chunk:
              
                buffer.extend(message_data)
                i+=1
                client_socket.send(b"1")
            else:
               
                client_socket.send(b"0")
        if i==index:
            break               
   
    data=pickle.loads(buffer)     
    responce=detect_message(data)
    #Handle client request here
    responce=pickle.dumps(responce)
    index=int(len(responce)/CHUNK_SIZE)
    min_chunk=0
    max_chunk=CHUNK_SIZE
    if 0:#len(responce)%index==0: 
        header={"number_chunk":index,"last_chunk":CHUNK_SIZE}
        header=pickle.dumps(header)
        client_socket.sendall(header)
        for i in range(index):
            client_socket.sendall(responce[min_chunk:max_chunk])
            min_chunk=max_chunk
            max_chunk+=CHUNK_SIZE  
    else: 
        last_chunk=len(responce)-(index*CHUNK_SIZE) 
        index+=1
        header={"number_chunk":index,"last_chunk":last_chunk}
        header=pickle.dumps(header)
        client_socket.sendall(header)
        i=0
        while True:
            client_socket.sendall(responce[min_chunk:max_chunk])
            response = client_socket.recv(8).decode()
            if response=="1":
                if i < index-1: 
                    min_chunk=max_chunk
                    max_chunk+=CHUNK_SIZE
                    i+=1
                elif i==index-1:        
                    min_chunk=max_chunk
                    max_chunk+=last_chunk
                    i+=1
                if i==index:
                    break 
    client_socket.close()
    print(f"Connection with {address} closed")
    
# this is server and is running all time and give request
def server():
    global flag_srver
    host = '127.0.0.1'
    port = 3
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    
    print(f"Server  \"Resource\" listening on {host}:{port}")
    
    while flag_srver:
        client_socket, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()
    server_socket.close()

server()  


       
      