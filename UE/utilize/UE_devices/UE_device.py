
import numpy as np
from utilize.Task.task_reader import Task_reader

# this class create edge device for each zone with Custom specifications
# output is a list with following itmse
# [[{'id': 0, 'assign_resource': 'noun'}, {'id': 0, 'type': 'Edge', 'mips': '', 'parentid': 0, 'workflow': None, 'con_pow_active': '', 'con_pow_idle': 0, 'down_bw': 0, 'down_cost': 0, 'up_bw': 0, 'up_cost': 0, 'memory_cost': 0, 'exist_flag': 0, 'memory_size': 0,time:0}]]
# out[0:n] contains {} of UE zones, out[x][0] is specification UEzone and out[x][1,n] is specification of device on each zone
# out[x][1:y][item] contains {'id': 0, 'type': 'Edge', 'mips': '', 'parentid': 0, 'workflow': None, 'con_pow_active': '', 'con_pow_idle': 0, 'down_bw': 0, 'down_cost': 0, 'up_bw': 0, 'up_cost': 0, 'memory_cost': 0, 'exist_flag': 0, 'memory_size': 0 ,'time':0}  which has its own workflow


class Edge:
    id = 0
    parentid = 0
    type_dev = "Edge"
    mips = 1000
    ratepermipscost = 0
    con_pow_active = 200
    con_pow_idle = 50
    down_bw = 1000
    down_cost = .08
    down_eng=50
    up_bw = 1000
    up_cost = .08
    up_eng=50
    memory_size = 0
    memory_cost = 0
    exist_flag = 0
    task_exec_cost=0
    cost_transfer=0
    # id is id of the UE broker from a zone
    def create_edge_devices_z_z(self, id,n_dveice,inter_time=0):
        edge=[]
        edge_devic_list = []  # create a list of the devices
        # the first index is id of the broker
        edge_devic_list = [{'id': id, 'assign_resource': 'noun'}]
        # number of the devices in a UE zone
        enter_numb =n_dveice#input("number of devices in UE zone:")
        for count_numb in range(int(enter_numb)):
            edge = self.edge(id, count_numb,inter_time)
            edge_devic_list.append(edge)   
        return edge_devic_list

    def edge(self, id, count_num,inter_time=0):
        self.parentid = id
        self.id =count_num
        # self.mips = input("Enter mips:")
        # self.typeofdev = input("Enter typeofdev:")
        # self.con_pow_active = input("Enter cost active:")
        tem =Task_reader()
        self.workflow =tem.Select_wf(self.id)
        result = {"id": self.id, "parentid": self.parentid,"inter_time":inter_time,\
                  "specif": {"id":-1,"type": self.type_dev, "mips": self.mips,"ratepermipscost":self.ratepermipscost,\
                      "con_pow_active": self.con_pow_active, "con_pow_idle": self.con_pow_idle, "down_bw": self.down_bw,
                  "down_cost": self.down_cost,"down_energy":self.down_eng, "up_bw": self.up_bw, "up_cost": self.up_cost,\
                      "up_energy":self.up_eng, "memory_cost_unit": self.memory_cost, "exist_flag": self.exist_flag,\
                          "exec_cost":self.task_exec_cost, "memory_size": self.memory_size, "time": 0,"idle_energy":0,\
                              "active_energy":0,"total_energy":0,"cost_process":0,"cost_transfer":0,"cost_memory":0,\
                                  "total_cost":0 }, "workflow": self.workflow}
        
        return result


# specification of edge device
"""
"id": device id
"type": type of device
"mips": power of process,
"ratepermipscost":cost for each mips of device
"parentid": self.parentid, 
"con_pow_active": value of energy consumption when device is active mode (unit)
 "con_pow_idle":value of energy consumption when device is idle mode (unit) , 
"down_bw": download bandwidth
"down_cost":Cost per download time
"down_energy":energy per download time, 
"up_bw": upload bandwidth
"up_cost":Cost per upload time
"up_energy":energy per upload time,
"memory_cost_unit": Cost per memory time,
"exist_flag": self.exist_flag,
"exec_cost":self.task_exec_cost, 
"memory_size": self.memory_size, 
"time": time of vm when that is starting
"idle_energy":all idle energy cost
"acive_energy":all active energy cost
"cost_process":all process cost
"cost_transfer":all transfer cost
"cost_memory":all memory cost 
"""