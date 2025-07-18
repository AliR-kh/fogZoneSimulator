import math
class Execut:
    def run(self, index,task,current_edge,resource,current_time):
        file_transfer_time_input=0
        file_transfer_time_output=0
        queue_time=0
        idle_energy=0
        active_energy=0
        total_energy=0
        process_cost=0
        transfer_cost=0
        memory_cost=0
        memory=0
        idle_resource_time=0
        # print(f"Type R :{resource["type"]} with id :{resource["id"]} and time is :{resource["time"]}")
        if float(task["time"])< float(resource["time"]): #this condition achievs start time and idle time for calculates id_energy
            start_time =float(resource["time"])
            queue_time=float(resource["time"])-float(task["time"])
        else:
            start_time=float(task["time"])
            idle_resource_time=float(task["time"])-float(resource["time"])
        process_time=self.Time_exec(task["runtime"],resource["mips"])    
        if resource["type"]=="Edge": #transfer time in edge device is ziro
            file_transfer_time_input=0
            file_transfer_time_output=0
        else:    
            file_transfer_time_input=self.Time_trans_f_D_t_R(task["sizein"],resource["down_bw"],current_edge)#the time that task is sent from device to resource
            file_transfer_time_output=self.Time_trans_f_R_t_D(task["sizeout"],resource["up_bw"],current_edge)#the time that result is sent from resource to device
        #
    
        makespan=process_time+file_transfer_time_input#+float(task["time_queue"])
        total_energy,active_energy,idle_energy,device_energy=self.get_energry(process_time,file_transfer_time_input,file_transfer_time_output,idle_resource_time,resource,current_edge)
        active,resource_transfer_cost,device_transfer_cost=self.get_cost(process_time,file_transfer_time_input,file_transfer_time_output,resource,current_edge)
        
        """this section set attributes of execution in resource and task"""
        task["time"]=start_time+process_time+file_transfer_time_output+file_transfer_time_input
        task["start_time"]=start_time
        task["time_queue"]=queue_time 
        task["makespan"]=makespan
        task["transfer_time_input"]=file_transfer_time_input
        task["transfer_time_output"]=file_transfer_time_output
        task["execution"]=process_time
        task["type_resource"]=resource["type"]
        task["id_resource"]=resource["id"]
        current_edge['active_energy']+=device_energy
        current_edge['total_energy']+=device_energy
        current_edge['cost_transfer']+=device_transfer_cost
        current_edge['total_cost']+=device_transfer_cost
        task["energy"]=total_energy
        task["cost"]=active+resource_transfer_cost+device_transfer_cost
        resource["time"]=start_time+process_time
        resource["active_energy"]+=active_energy
        resource["idle_energy"]+=idle_energy
        resource["total_energy"]+=total_energy
        resource["total_cost"]+=active+resource_transfer_cost
        """ End section """
        if (start_time+process_time)>current_time[index]:
            current_time[index]=(start_time+process_time)
        return current_time[index]#end_time,active_energy,idle_energy,process_cost,transfer_cost,memory_cost
        
    def Time_exec(self,task,resource): #calculation time of run a job in cpu
        size_run=float(task) * 1000
        process_time = size_run/float(resource)
        return process_time
    
    
    def Time_trans_f_D_t_R(self,task,resource,current_edge): #calculation time of transfer a job to a vm
        bandwidth=0
        if current_edge['up_bw']<resource:
            bandwidth=current_edge['up_bw']
        else:
            bandwidth=resource
        size_task = float(task)
        file_transfer_time=size_task/1000/float(bandwidth)
        return file_transfer_time
    def Time_trans_f_R_t_D(self,task,resource,current_edge): #calculation time of transfer a result from resource to a device
        bandwidth=0
        if current_edge['down_bw']<resource:
            bandwidth=current_edge['down_bw']
        else:
            bandwidth=resource
        size_task = float(task)
        file_transfer_time=size_task/1000/float(bandwidth)
        return file_transfer_time
    
    def get_energry(self,process_time,file_transfer_time_input,file_transfer_time_output,idle_resource_time,resource,current_edge):
        resource_transfer=0
        device_transfer=0
        active=0
        idle=0
        resource_transfer=(file_transfer_time_input*resource['down_energy'])+(file_transfer_time_output*resource['up_energy'])
        device_transfer=(file_transfer_time_input*current_edge['up_energy'])+(file_transfer_time_output*current_edge['down_energy'])
        active=(resource["con_pow_active"]*process_time/1000)+resource_transfer
        idle=idle_resource_time * float(resource["con_pow_idle"]/1000)
        total_energy=active+idle
        return total_energy,active,idle,device_transfer
                
        
    def get_cost(self,process_time,file_transfer_time_input,file_transfer_time_output,resource,current_edge):
        resource_transfer=0
        device_transfer=0
        active=0
        resource_transfer=(file_transfer_time_input*resource['down_cost'])+(file_transfer_time_output*resource['up_cost'])
        device_transfer=(file_transfer_time_input*current_edge['up_cost'])+(file_transfer_time_output*current_edge['down_cost'])
        active=(resource["ratepermipscost"]*process_time)
       
        return active,resource_transfer,device_transfer
        
    def loadbalancing(self,resources,task,result,res):
        fog=0
        cloud=0
        total_fog=0
        total_cloud=0
        LBF=0
        LBC=0
        for x in range(len(res)):
            if res[x]!=len(res)-1:
                if res[x]["type"]=="Fog":
                    fog+=1
                if  res[x]["type"]=="Cloud":
                    cloud+=1
        temp_fog=[fog]
        temp_cloud=[cloud]
        for Y in range(fog):
            temp_fog.insert(Y,0)
        for Y in range(cloud):
            temp_cloud.insert(Y,0) 
         
        for X in range(len(task)):
            if resources[result[X]]["type"]=="Cloud":
               temp_cloud[resources[result[X]]["id"]]+=self.Time_exec(task[X]["runtime"],resources[result[X]]["mips"])+self.Time_trans(task[X]["sizein"],resources[result[X]]["down_bw"])
               total_cloud+=self.Time_exec(task[X]["runtime"],resources[result[X]]["mips"])+self.Time_trans(task[X]["sizein"],resources[result[X]]["down_bw"])
            if resources[result[X]]["type"]=="Fog":
               temp_fog[resources[result[X]]["id"]]+=self.Time_exec(task[X]["runtime"],resources[result[X]]["mips"])+self.Time_trans(task[X]["sizein"],resources[result[X]]["down_bw"]) 
               total_fog+=self.Time_exec(task[X]["runtime"],resources[result[X]]["mips"])+self.Time_trans(task[X]["sizein"],resources[result[X]]["down_bw"])
        total=0
        total+=total_cloud+total_fog
        total/=(fog+cloud)
        for X in range(len(temp_fog)):
            LBF+=pow(temp_fog[X]-total,2)
        for X in range(len(temp_fog)):
            LBC+=pow(temp_cloud[X]-total,2)    
        LBF=math.sqrt(LBF/fog)
        LBC=math.sqrt(LBC/cloud)  
        return LBC,LBF         
               