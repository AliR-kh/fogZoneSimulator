
from utilize.Reource_zone.clouds_resource import Cloud
from utilize.Config import Config
# this class create fog device for each zone with Custom specifications
class Fog:
    id = 0
    parentid = 0
    type_dev = "Fog"
    mips =1500
    ratepermipscost = 0.48
    con_pow_active = 500
    con_pow_idle = 200
    down_bw = 1000
    down_cost = .04
    down_eng=50
    up_bw = 1000
    up_cost = .04
    up_eng=50
    memory_size = 0
    memory_cost = 0
    exist_flag = 0
    task_exec_cost=0
    cost_transfer=0.01
    inter_time=0
    def create_fog_device(self, id, alg):
        config=Config()
        n_fog_zone=config.get_config("Fog","device_e_zone")
        n_clouds=config.get_config("Cloud","number")
        fog_devic_list = []  # create a list of the devices
        if alg == 1:
            # the first index is id of the broker
            fog_devic_list = [{'id': id}]
            # number of the devices in a FOG zone
            enter_numb =n_fog_zone#input("number of fog in fog zone:")
            for count_numb in range(int(enter_numb)):
                fog = self.fog(id, count_numb)
                fog_devic_list.append(fog)
            Clouds=Cloud()
            clouds=Clouds.create_clouds_device()
            fog_devic_list.extend(clouds)
            return fog_devic_list

    def fog(self, id, count_num):
        if id != "Noun":
            self.parentid = id
        else:
            self.parentid = "Noun"
        self.id = count_num
        result = {"id": self.id, "type": self.type_dev, "mips": self.mips,"ratepermipscost":self.ratepermipscost, "parentid": self.parentid, "con_pow_active": self.con_pow_active, "con_pow_idle": self.con_pow_idle, "down_bw": self.down_bw,
                  "down_cost": self.down_cost,"down_energy":self.down_eng, "up_bw": self.up_bw, "up_cost": self.up_cost,"up_energy":self.up_eng, "memory_cost_unit": self.memory_cost, "exist_flag": self.exist_flag,"exec_cost":self.task_exec_cost,"inter_time":self.inter_time, "memory_size": self.memory_size, "time": 0,"idle_energy":0,"active_energy":0,"total_energy":0,"cost_process":0,"cost_transfer":0,"cost_memory":0,"total_cost":0,"assigned_mips":0}
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