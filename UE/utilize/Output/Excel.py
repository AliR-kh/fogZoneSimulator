import os
import time
import pandas as pd
class Excel:
    # def workflow(self,zones):
    #     head=["ue_zone_id","device_id","id","start_time","makespan","time","time_queue","transfer_time","execution","type_resource","id_resource","parentid"]
    #     my_data = []

    #     for i in range(len(zones)):
    #         for j in range(1, len(zones[i])):
    #             for k in range(len(zones[i][j]["workflow"])):
    #                 temp = [
    #                     zones[i][0]['id'],
    #                     zones[i][j]["workflow"][k][0]["device_id"],
    #                     zones[i][j]["workflow"][k][0]["id"],
    #                     zones[i][j]["workflow"][k][0]["start_time"],
    #                     zones[i][j]["workflow"][k][0]["makespan"],
    #                     zones[i][j]["workflow"][k][0]["time"],
    #                     zones[i][j]["workflow"][k][0]["time_queue"],
    #                     zones[i][j]["workflow"][k][0]["transfer_time_input"],
    #                     zones[i][j]["workflow"][k][0]["execution"],
    #                     zones[i][j]["workflow"][k][0]["type_resource"],
    #                     zones[i][j]["workflow"][k][0]["id_resource"],
    #                     zones[i][j]["workflow"][k][0]["parentid"]
    #                 ]
    #                 my_data.append(temp)
    #     df = pd.DataFrame(my_data, columns=head)
    #     path=os.getcwd()+'\\UE\\OutputFile\\'
    #     name='output_workflow_'+time.strftime('%Y%B%d_%H_%M_%S')+'.xlsx'
    #     df.to_excel(path+name, index=False)

    def calculation_zone(self,result,total_time):
        head=["zone_id","total_makespan","makespan","energy","cost","run_time"]
        max_makespan=0
        max_energry=0
        max_cost=0
        my_data = []
        for i in range(len(result)): #هر تکرار چندتا زون دارد
            temp=[]
            if max_makespan <result[i][1]:
                max_makespan=result[i][1]
            if max_energry <result[i][3]:
                max_energry=result[i][3]
            if max_cost <result[i][4]:
                max_cost=result[i][4]
            for j in range(len(result[i])):
                
                temp.append(result[i][j])    
            my_data.append(temp)
        my_data.append(["All Zones",max_makespan,max_makespan,max_energry,max_cost,total_time])    
        path=os.getcwd()+'\\UE\\OutputFile\\'
        name='output_calculation_'+time.strftime('%Y%B%d_%H_%M_%S')+'.xlsx'
        df = pd.DataFrame(my_data, columns=head)
        df.to_excel(path+name, index=False)       
        
        
    def workflow(self,zones):
        head=["ue_zone_id","device_id","id","start_time","makespan","time","time_queue","transfer_time","execution","type_resource","id_resource","parentid"]
        my_data = []
        my_data_temp=[]
        my_data_final=[]
        min_time=float('inf')
        min_zone=0
        min_index=0
        for i in range(len(zones)):
            for j in range(1, len(zones[i])):
                for k in range(len(zones[i][j]["workflow"])):
                    my_data_temp.append([zones[i][0]['id'],zones[i][j]["workflow"][k][0]])

        for i in range(len(my_data_temp)):
            for j in range (len(my_data_temp)):
                if my_data_temp[j][1]['time']<min_time:
                    min_time=my_data_temp[j][1]['time']
                    min_zone=my_data_temp[j]
                    min_index=j
            my_data_final.append(min_zone)
            my_data_temp.pop(min_index)
            min_time=min_time=float('inf')
            
        my_data=[]
        for k in range(len(my_data_final)):
            temp = [
                my_data_final[k][0],
                my_data_final[k][1]["device_id"],
                my_data_final[k][1]["id"],
                my_data_final[k][1]["start_time"],
                my_data_final[k][1]["makespan"],
                my_data_final[k][1]["time"],
                my_data_final[k][1]["time_queue"],
                my_data_final[k][1]["transfer_time_input"],
                my_data_final[k][1]["execution"],
                my_data_final[k][1]["type_resource"],
                my_data_final[k][1]["id_resource"],
                my_data_final[k][1]["parentid"]
            ]
            my_data.append(temp)                    
        df = pd.DataFrame(my_data, columns=head)
        path=os.getcwd()+'\\UE\\OutputFile\\'
        name='output_all_workflow_'+time.strftime('%Y%B%d_%H_%M_%S')+'.xlsx'
        df.to_excel(path+name, index=False)