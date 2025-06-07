import random
class Random:
    def schedul(self,joblist,task,resource):
        list_sch=[]
        for i in range(len(joblist)):
            list_sch.append(random.randint(0,len(resource)-1))
        return list_sch