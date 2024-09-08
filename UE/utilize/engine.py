from utilize.UE_devices.UE_zone import UE_broker
from utilize.send_message import send_message
from utilize.distribution import random_time
from utilize.algorithm.Select_zone import Algorithms
from utilize.Task.task_generater import Task_generator
from utilize.Output.Excel import Excel
import pandas as pd
import time
from tabulate import tabulate
class UE_Egine:
    
    run_type="discreate"
    number_zone=0
    dynamic=0
    distribution=None
    N_A_D=0#numbers of devices that will add to environment
    inter_time=[] #times of inter each task to fog environment
    zones=0
    
    def __init__(self,run_type="discreate") -> None:
        self.run_type=run_type
        
        if self.run_type=="discreate":
            self.discreate_time()
        else:
            self.real_time()    
    
    """ this function simulation is ran as real time, thats mean each task n second take long to have be executed
    """
    def real_time(self):
        print("real time simulation")
        

    
    def discreate_time(self):
        #print("discreate time simulation")
        ue_zone=UE_broker() 
        #initializing ue zone and devices
        self.zones=ue_zone.creat_ue_zone()
        self.number_zone=len(self.zones)
        min_t=0
        max_t=10
        #print(self.zones)
        #this loop is for dynamic UE that will join to environment
        for i in range(self.N_A_D):
            self.inter_time.append(random_time(min_t,max_t))
            min_t=max_t
            max_t+=10
        response=send_message('127.0.0.1',1,\
                              {"request":"intial_scheduling","inter_time":self.inter_time,\
                                  "number_zone":self.number_zone,"data":self.zones})    
        self.zones=response
        ue_zone.set_uezone(self.zones)

        response=send_message('127.0.0.1',3,{"request":"scheduling","inter_time":self.inter_time,"number_zone":self.number_zone,"data":self.zones})    
        """in continiouse be received a response that It's time to add the device 
        """
        if response["flags"]:
            i=0
            Algorithm=Algorithms()
            while response["flags"] and self.N_A_D>0:
                    zone_id=Algorithm.random(0,2) #selecting appropirate zone for new ue
                    new_device=ue_zone.add_ue(zone_id,self.inter_time[i]) # add new ue to be selected ue-zone
                    self.zones=ue_zone.get_ue_zone()
                    response=send_message('127.0.0.1',3,{"request":"scheduling_add_ue","id":zone_id,"data":new_device}) # send all ue-zone to broker for scheduling
                    self.N_A_D-=1
                    i+=1
                    #print(f"Add a UE device to zone:{zone_id} and time:{self.inter_time[i]} and response is:{response}")
        else:
            self.zones=response["data"]
            ue_zone.set_uezone(self.zones)
        #print("finally")    
        #print(send_message('127.0.0.1',1,{"request":"get_ue_zons"}) )    
        self.zones=send_message('127.0.0.1',3,{"request":"get_ue_zones","data":self.zones})
        fog_zones,clouds=send_message('127.0.0.1',3,{"request":"fog_zones_stattus","data":self.zones})
        ue_zone.set_uezone(self.zones)  
        total_calculation=send_message('127.0.0.1',3,{"request":"total_calculation",'data':self.zones})
        output=Excel()
        output.calculation_zone(total_calculation)
        output.workflow(self.zones)
        #output.calculation_zone(total_calculation)
        # Print table
        # print(tabulate(my_data, headers=head, tablefmt="grid"))

        # # Store data in an Excel file
        # df = pd.DataFrame(my_data, columns=head)
        # df.to_excel("output_data.xlsx", index=False)

        # print("Data has been stored in 'output_data.xlsx'")
        
        
        
        
        
        
        
        
        
        
        
        
        """   
        for i in range(len(self.zones)):
            print(f"\n-----------------------------------------\n{self.zones[i][0]}")
            for j in range(1,len(self.zones[i])):
                for k in range(len(self.zones[i][j]["workflow"])):
                    temp=[self.zones[i][j]["workflow"][k][0]["device_id"],self.zones[i][j]["workflow"][k][0]["id"],self.zones[i][j]["workflow"][k][0]["start_time"],self.zones[i][j]["workflow"][k][0]["makespan"],self.zones[i][j]["workflow"][k][0]["time"],self.zones[i][j]["workflow"][k][0]["time_queue"],self.zones[i][j]["workflow"][k][0]["transfer_time_input"],self.zones[i][j]["workflow"][k][0]["execution"],self.zones[i][j]["workflow"][k][0]["type_resource"],self.zones[i][j]["workflow"][k][0]["id_resource"],self.zones[i][j]["workflow"][k][0]["parentid"]]
                    my_data.append(temp)
                   
                    #print(f"{self.zones[i][j]["workflow"][k][0]["id"]}       {self.zones[i][j]["workflow"][k][0]["time"]}       {self.zones[i][j]["workflow"][k][0]["makespan"]}      {self.zones[i][j]["workflow"][k][0]["parentid"]}     {self.zones[i][j]["workflow"][k][0]["type_resource"]}-{self.zones[i][j]["workflow"][k][0]["id_resource"]}")     
        fog_zones=send_message('127.0.0.1',3,{"request":"fog_zones_stattus","data":self.zones})
        print(tabulate(my_data, headers=head, tablefmt="grid"))
    " 'workflow': [[{'id': 'ID00000', 'namespace': 'Montage', 'name': 'mProjectPP', 'version': '1.0', 'runtime': '13.45', 'sizein': 4222384, 'sizeout': 8299550, 'start_time': 0.0,'time': 8.40625, 'makespan': 8.40625, 'time_queue': 0, 'id_resource': -1, 'energy': 2.037085908203125, 'cost': 0.40525146484374996, 'transfer_time': 8.40625, 'execution': 8.40625, 'type_resource': 'Edge', 'parentid': []}]"
    """