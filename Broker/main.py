    
import socket
import numpy as np
import threading
import time
import pickle
from utilize.send_message import send_message
from utilize.algorithm.UE_FOG_assign import algorithm as A_alorithm
from utilize.algorithm.Assign_new_device import Algorithm as new_device_algorithm
number_zone=0
flag_zone=[] #this flag be used for each resource zone and specific interupt
threads_zone=[]
current_time=0
inter_time=[]
flag_sever=1
def intial_scheduling(Data):
    global threads_zone,number_zone, flag_zone, current_time,inter_time
    number_zone=Data["number_zone"]
    flag_zone=np.ones(number_zone)
    inter_time=Data["inter_time"]
    #this function is for intialazing fog-zones and inter time.
    response=send_message('127.0.0.1',3,{"request":"connection","numbers_zone":number_zone,"flags":flag_zone,"inter_time":inter_time,"data":Data["data"]})
    response=A_alorithm(Data["data"],response)
    #response=send_message('127.0.0.1',3,{"request":"scheduling","time":current_time,"data":Data["data"]})
    return response   
 
def interrupt(Data):
    pass
                
    
def scheduling(Data):

    response=send_message('127.0.0.1',3,{"request":"scheduling","inter_time":inter_time,"data":Data["data"]})
    return response    
    
    
    
    
    
def scheduling_add_ue(Data):
    response=send_message('127.0.0.1',3,{"request":"scheduling_add_ue","zone_id":Data["id"],"data":Data["data"]})
    return response
    
def get_ue_zone(Data):
    response=send_message('127.0.0.1',3,{"request":"get_ue_zones","data":Data})
    return response

def close_program():
    global flag_sever
    flag_sever=0
    return 1


def assign_new_device(data):
    fog_zones,clouds=send_message('127.0.0.1',3,{"request":"fog_zones_stattus","data":data})
    Algorithm=new_device_algorithm()
    zone_id=Algorithm.random_time(0,data["number_zone"]-1)
    return zone_id
    


def detect_message(Data):
    
    if Data['request']=="intial_scheduling":
        return intial_scheduling(Data)
    elif Data['request']=="scheduling":
        return scheduling(Data)
    elif Data['request']=="scheduling_add_ue":
        return scheduling_add_ue(Data)
    elif Data['request']=="zone_status":
        pass
    elif Data['request']=="get_ue_zones":
        return get_ue_zone(Data)
    elif Data['request']=="none":
        pass
    elif Data['request']=="assign_new_device":
        return assign_new_device(Data)
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
            #response = s.recv(8)
            #print(response)
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

    #        # Serialize and compress the object
    # data = pickle.dumps(message, protocol=pickle.HIGHEST_PROTOCOL)
    # compressed_data = zlib.compress(data)
    # CHUNK_SIZE = 4096

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.connect((address, port))
        
    #     # Send the compressed data in chunks
    #     for i in tqdm(range(0, len(compressed_data), CHUNK_SIZE)):
    #         s.sendall(compressed_data[i:i+CHUNK_SIZE])
        
    #     # Receive the response in chunks
    #     response_buffer = bytearray()
    #     while True:
    #         chunk = s.recv(CHUNK_SIZE)
    #         if not chunk:
    #             break
    #         response_buffer.extend(chunk)
        
    #     # Decompress and deserialize the response
    #     decompressed_response = zlib.decompress(response_buffer)
    #     response_obj = pickle.loads(decompressed_response)
    #     return response_obj    


def server():
    global flag_sever
    host = '127.0.0.1'
    port = 1
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    
    print(f"Server  \"Broker\" listening on {host}:{port}")
    
    while flag_sever:
        client_socket, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()
    server_socket.close()



server()
      