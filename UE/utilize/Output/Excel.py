import os
import time
import pandas as pd
class Excel:
    def workflow(self,zones):
        head=["ue_zone_id","device_id","id","start_time","makespan","time","time_queue","transfer_time","execution","type_resource","id_resource","parentid"]
        my_data = []

        for i in range(len(zones)):
            for j in range(1, len(zones[i])):
                for k in range(len(zones[i][j]["workflow"])):
                    temp = [
                        zones[i][0]['id'],
                        zones[i][j]["workflow"][k][0]["device_id"],
                        zones[i][j]["workflow"][k][0]["id"],
                        zones[i][j]["workflow"][k][0]["start_time"],
                        zones[i][j]["workflow"][k][0]["makespan"],
                        zones[i][j]["workflow"][k][0]["time"],
                        zones[i][j]["workflow"][k][0]["time_queue"],
                        zones[i][j]["workflow"][k][0]["transfer_time_input"],
                        zones[i][j]["workflow"][k][0]["execution"],
                        zones[i][j]["workflow"][k][0]["type_resource"],
                        zones[i][j]["workflow"][k][0]["id_resource"],
                        zones[i][j]["workflow"][k][0]["parentid"]
                    ]
                    my_data.append(temp)
        df = pd.DataFrame(my_data, columns=head)
        path=os.getcwd()+'\\UE\\OutputFile\\'
        name='output_workflow_'+time.strftime('%Y%B%d_%H_%M_%S')+'.xlsx'
        df.to_excel(path+name, index=False)

    def calculation_zone(self,result,total_time):
        head=["zone_id","total_makespan","makespan","energy","cost","run_time"]
        my_data = []
        for i in range(len(result)):
            temp=[]
            for j in range(len(result[i])):
                temp.append(result[i][j])    
            my_data.append(temp)
        my_data.append([-1,1,1,1,1,total_time])    
        path=os.getcwd()+'\\UE\\OutputFile\\'
        name='output_calculation_'+time.strftime('%Y%B%d_%H_%M_%S')+'.xlsx'
        df = pd.DataFrame(my_data, columns=head)
        df.to_excel(path+name, index=False)       