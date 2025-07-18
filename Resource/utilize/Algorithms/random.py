import random
class Random:
    def schedul(self,joblist,resource):
        list_sch=[]
        for i in range(len(joblist)):
            temp_resources=[]
            temp_resources+=[res for res in resource if res["type"]!="Edge" or (res["type"]=="Edge") and joblist[i][0]==res["id"]]
            print(f"\n++++++++++++++++++\n joblist :{joblist[i]} \n resource: {temp_resources} \n ++++++++++++++++++++++++")
            id=random.randint(0,len(resource)-1)
            list_sch.append({"type":resource[id]["type"],"id":resource[id]["id"]})
        return list_sch