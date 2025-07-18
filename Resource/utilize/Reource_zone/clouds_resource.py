from utilize.Config import Config

# this class create cloud device for each zone with Custom specifications
class Cloud:
    id = 0
    type_dev = "Cloud"
    mips = 2000
    ratepermipscost = 0.96
    con_pow_active = 700
    con_pow_idle = 400
    task_exec_cost=0.96
    down_bw = 1000
    down_eng=50
    down_cost = .02
    up_bw = 1000
    up_eng=50
    up_cost = .02
    memory_size = 0
    memory_cost = 0
    exist_flag = 0
    cost_transfer=.02
    inter_time=0
    def create_clouds_device(self):
        config=Config()
        enter_numb=config.get_config("Cloud","number")
        fog_devic_list = []  # create a list of the devices

        for count_numb in range(int(enter_numb)):
            edge = self.clouds(count_numb)
            fog_devic_list.append(edge)
        return fog_devic_list

    def clouds(self, count_num):
        self.id = count_num

        result = {"id": self.id, "type": self.type_dev,"ratepermipscost":self.ratepermipscost ,"mips": self.mips, "con_pow_active": self.con_pow_active, "con_pow_idle": self.con_pow_idle, "down_bw": self.down_bw,
                  "down_cost": self.down_cost, "up_bw": self.up_bw,"down_energy":self.down_eng, "up_cost": self.up_cost,"up_energy":self.up_eng,"exec_cost":self.task_exec_cost ,"memory_cost_unit": self.memory_cost, "exist_flag": self.exist_flag, "memory_size": self.memory_size,"inter_time":self.inter_time, "time": 0,"idle_energy":0,"active_energy":0,"total_energy":0,"cost_process":0,"cost_transfer":0,"cost_memory":0,"total_cost":0,"assigned_mips":0}
        return result



# specification of cloud device
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