from tkinter import filedialog as fd
from xml.etree import ElementTree as ET
import os
from utilize.Config import Config
import random
# this class for read workflow from a xml file with specifc structure and create a list of workflow fo execute in resource
# this class specifies the task of each job and dependencies between jobs
# output is a list that its index 0 is {'id': 'ID00010', 'namespace': 'Montage', 'name': 'mDiffFit', 'version': '1.0', 'runtime': '10.58', 'parentid': ['ID00003', 'ID00001'] , size=5048 ,sizeout=x ,time=0 , 'makespan=0} accordignly we can uses this information and creat queu of execution
# job= [{'id': 'ID00014', 'namespace': 'Montage', 'name': 'mBackground', 'version': '1.0',\
#     'runtime': '10.68', 'device_id': 0, 'sizein': 8292710, 'sizeout': 8292498, 'start_time': 0,\
#         'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0,\
#             'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0,\
#                 'parentid': ['ID00002', 'ID00011']}]
# jobs=[job,job2,job3,..........,jobn]
class Task_reader:
    filenameilename = 0

    def Select_wf(self,device_id):
        result = self.creat_dag(device_id)
        return result

    def creat_dag(self,device_id):
        config=Config()
        workflow=config.get_config("UE","workflow","string")
        # workflow_list=["Montage_200","Montage_300","Montage_100"]
        # workflow=random.choice(workflow_list)
        xml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Config/Workflow/'+workflow+'.xml'))
        tree = ET.parse(xml_path)  # open xml
        listjob = []
        for job in tree.iter('job'):  # find tags of job
            temp = 0
            temp = []
            sizein = 0
            sizeout=0
            temp1 = 0
            temp1 = []
            # create one list of job and push its tasks on list
            temp.append(job.attrib)
            for jobus in job:
                temp1.append(jobus.attrib)
            for x in range(len(temp1)):
                if temp1[x]["link"]=="input":
                    sizein += int(temp1[x]["size"])
                if temp1[x]["link"]=="output":
                   sizeout+=int(temp1[x]["size"])
            temp[0]['device_id'] = device_id        
            temp[0]['sizein'] = sizein
            temp[0]["sizeout"]=sizeout
            temp[0]['start_time'] = 0
            temp[0]['time'] = 0
            temp[0]['makespan'] = 0
            temp[0]['time_queue'] = 0
            temp[0]['id_resource'] = 0
            temp[0]['energy'] = 0
            temp[0]['cost'] = 0
            temp[0]["transfer_time_input"]=0
            temp[0]["transfer_time_output"]=0
            temp[0]['execution'] = 0
            temp[0]['type_resource'] = 0
            temp[0]['id_resource'] = 0
            # output is a list consist of [[{job1},{job1's tasks}],....]
            listjob.append(temp)
        for tem in range(len(listjob)):  # in this level find parent of the job
            listjob[tem][0]['parentid'] = []
            listchi = 0
            listchi = []
            find = listjob[tem][0]["id"]
            for chi in tree.iter('child'):
                if find == chi.attrib['ref']:
                    for dep in chi:
                        listchi.append(dep.attrib['ref'])
                        # output is [[{job1, [parents]},{job1's tasks}],....]
                        listjob[tem][0]["parentid"] = listchi
             
        return listjob
