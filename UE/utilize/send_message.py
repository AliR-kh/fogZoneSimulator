import socket
import pickle
import zlib
import time
def send_message(address,port,message):
    CHUNK_SIZE = 8192
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((address,port))
        data=pickle.dumps(message)
        index=int(len(data)/CHUNK_SIZE)
        min_chunk=0
        max_chunk=CHUNK_SIZE
        if 0:#len(data)%index==0: 
            header={"number_chunk":index,"last_chunk":CHUNK_SIZE}
            header=pickle.dumps(header)
            s.sendall(header)
            for i in range(index):
                s.sendall(data[min_chunk:max_chunk])
                min_chunk=max_chunk
                max_chunk+=CHUNK_SIZE  
        else: 
         
            last_chunk=len(data)-(index*CHUNK_SIZE) 
            index+=1
            header={"number_chunk":index,"last_chunk":last_chunk}
            header=pickle.dumps(header)
            s.sendall(header)
            #response = s.recv(8)
            #print(response)
            i=0
            
            while True:
                s.sendall(data[min_chunk:max_chunk])
                response = s.recv(8).decode()
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
            #response = s.recv(8)  
    
        buffer=bytearray()
        message_header=s.recv(1024)
        message_header=pickle.loads(message_header)
        index=message_header["number_chunk"]
        last_chunk=message_header["last_chunk"]
        i=0
        while True:
            message_data=s.recv(CHUNK_SIZE)
            if i <index-1:
                if len(message_data)==CHUNK_SIZE:
                    buffer.extend(message_data)
                    i+=1
                    s.send(b"1")
                else:
                    s.send(b"0")
            elif i==index -1:
                if len(message_data)==last_chunk:
                    buffer.extend(message_data)
                    i+=1
                    s.send(b"1")
                else:
                    s.send(b"0")
            if i==index:
                break               
        data=pickle.loads(buffer)
        return data
    
        
        
    # buffer=bytearray()
    # message_header=s.recv(1024)
    # message_header=pickle.loads(message_header)
    # index=message_header["number_chunk"]
    # #s.send(b"1")
    # for i in range(index):
    #     #print(len(buffer))
    #     message_data=s.recv(1024)
    #     buffer.extend(message_data)
    #     #s.send(b"1")
    # #print(len(buffer))    
    # data=pickle.loads(buffer)    
    # return data        
            
            
            
                 
        # responce=s.recv(8192)
        # responce=pickle.loads(responce)
    
    
    
    
    
    #    # Serialize and compress the object
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