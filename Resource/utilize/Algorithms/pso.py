# import random
# import datetime as dt
# import time
# from utilize.Execution.execut import Execut as EX
# class PSO:
#     partcle=20
#     iteration=10
#     c1=2      
#     c2=2
#     W=1
#     w1=0
#     w2=0
#     w3=0
#     w4=0
#     MSmax=1
#     MSmin=0
#     TCmax=0
#     TCmin=0
#     TEmax=0
#     TEmin=0
#     LBCmax=0
#     LBCmin=0
#     LBFmax=0
#     LBFmin=0
#     def initializing(self,resources,job,edge):
#         new_fitness=0
#         new_best=[]
#         gbest_fitness=0
#         pbest_fitness=0
#         tasknumber=len(job)
#         vmnumber=len(resources)
#         gbest=[]
#         pbest=[]
#         position=[]
#         velocity=[]
#         swarm=[]
#         #print(resources)
#         for NP in range(self.partcle):
#             #random.seed(str(dt.datetime.now()))
#             position=[]
#             velocity=[]
#             pbest_fitness=0
#             for NT in range(tasknumber):
#                 #print(NT)
#                 #random.seed(str(dt.datetime.now()))
#                 #time.sleep(.01)
#                 position.append(random.randint(0,vmnumber-1))
#                 velocity.append(random.uniform(0.0,1.0))
#                 #print("position {}".format(NT),position[NT]," velocity= ",velocity[NT])
#             pbest=position
#             pbest_fitness=self.fitness(position,job,edge,resources)
#             if NP==0:
#                 gbest_fitness=pbest_fitness
#                 gbest=position
#             elif gbest_fitness< pbest_fitness:
#                 gbest=pbest
#                 gbest_fitness=pbest_fitness    
#                 #print(pbest,"\n ",position,"\n ",gbest,"\n ",pbest_fitness)
#             #print("particle:",NP, " pbest:",pbest_fitness,"\n")
#             swarm.append((position,velocity,pbest,pbest_fitness))
#             new_best,new_fitness=self.Updatepso(swarm,gbest,gbest_fitness,vmnumber,job,edge,resources)
#             #print(gbest)
#         return gbest
#     def Updatepso(self,swarm,gbest,gbest_fitness,vm,job,edge,resources):
#         new_fitness=0
#         new_velocity=[]
#         new_position=[]
#         tasknum=len(job)
#         particle=len(swarm)
#         for x in range(particle):
#             position,velocity,pbest,pbest_fitness=swarm[x]
#             #print("position",position, "velocity",velocity," pbest",pbest,"pbest_fitness",pbest_fitness)
#             for y in range(tasknum):
#                 new_velocity.append(self.newvelocity(velocity[y],pbest[y],position[y],gbest[y]))
#                 new_position.append(((position[y]+new_velocity[y])))
#                 new_position[y]=max(0,min(int(new_position[y]),vm-1))   
#             new_fitness=self.fitness(new_position,job,edge,resources)
#             if new_fitness > pbest_fitness:
#                 pbest = new_position
#                 pbest_fitness = new_fitness
#             if new_fitness > gbest_fitness: # type: ignore
#                 gbest = new_position
#                 gbest_fitness = new_fitness
#         return gbest,gbest_fitness    
                    
#     def fitness(self,position,job,edge,resources):
#         result=0
#         vm=[]
#         vmnumb=len(resources)-1
#         task=[]
#         flag=1
#         for jobnumb in range(len(job)):
#             device_id=job[jobnumb][0]
#             task_id=job[jobnumb][1]
#             for devnumb in range(1,len(edge)):
#                 if device_id==edge[devnumb]["id"]:
#                     if position[jobnumb]==vmnumb:
#                         vm=edge[devnumb]["specif"]
#                         mips=float(vm["mips"])
#                         #print(vm)
#                     else:  #print("device_id: ",edge[devnumb]["id"]," task_id:",edge[devnumb]["workflow"][tasknumb][0]["id"],"\n\n\n\n")
#                         vm=resources[position[jobnumb]]
#                         mips=float(vm["mips"])
#                     for tasknumb in range(len(edge[devnumb]["workflow"])):
#                         if edge[devnumb]["workflow"][tasknumb][0]["id"]==task_id:
#                             task=edge[devnumb]["workflow"][tasknumb]
#                            #print("device_id: ",edge[devnumb]["id"]," task_id:",edge[devnumb]["workflow"][tasknumb][0]["id"],"\n\n\n\n")
#             #print("vm number: ",vmnumb," vm:: ",vm["id"])
#             runtime=task[0]["runtime"]
#             temp1=self.calculationMS(runtime,mips)
#             result+=temp1
#             #print("result: ",result,"\n position: ",position)
#             return result                
                            
        
#     def calculationMS(self,task,resource):
#         temp=EX()
#         process_time=temp.Time_exec(task,resource)
#         MSNORM=(process_time-self.MSmin)/(self.MSmax-self.MSmin)
#         if self.MSmax==1:
#             self.MSmax=process_time  
#         else:
#             process_time=temp.Time_exec(task,resource)
#             if process_time >self.MSmax:
#                 self.MSmax=process_time
#             if process_time < self.MSmin:
#                 self.MSmin=process_time 
#         return MSNORM          
#     def calculationTC(self,task,resource):
#         temp=EX()
#         process_time=temp.Time_exec(task["runtim"],resource["mips"])
#         timetrans=temp.Time_trans(task("sizein"),resource["down_bw"])
#         TC=temp.get_cost(resource,process_time,task,timetrans)
#         TCNORM=(TC-self.TCmin)/(self.TCmax-self.TCmin)
#         if self.TCmax==1:
#             self.TCmax=TC  
#         else:
#             if TC >self.TCmax:
#                 self.TCmax=process_time
#             if TC < self.TCmin:
#                 self.TCmin=process_time 
#         return TCNORM
    
#     def calculationTE(self,task,resource):
            
#         temp=EX()
#         process_time=temp.Time_exec(task["runtim"],resource["mips"])
#         timetrans=temp.Time_trans(task("sizein"),resource["down_bw"])
#         TE=temp.get_energry(resource,process_time,timetrans,task)
#         TENORM=(TE-self.TEmin)/(self.TEmax-self.TEmin)
#         if self.TEmax==1:
#             self.TEmax=TE 
#         else:
#             if TE >self.TCmax:
#                 self.TEmax=process_time
#             if TE < self.TCmin:
#                 self.TEmin=process_time 
#         return TENORM 
    
    
#     def calculationLB(self,task,resource):
            
#         size_run=float(task) * 1000
#         process_time = size_run/float(resource)
#         return process_time
    
    
#     def calculationLF(self,task,resource):
            
#         size_run=float(task) * 1000
#         process_time = size_run/float(resource)
#         return process_time  
        
#     def newvelocity(self,velocity,pbest,position,gbest):
#         temp1=self.W*velocity
#         temp2=self.c1*random.uniform(0,1)*(pbest-position)
#         temp3=self.c2*random.uniform(0,1)*(gbest-position)
#         temp4=temp1+temp2+temp3
#         #print(temp1," ",pbest," ",position," ",gbest," ",temp4)
#         return temp4    


import random
import datetime as dt
from utilize.Execution.execut import Execut as EX

class PSO:
    def __init__(self, particle_count=20, iterations=10, c1=2, c2=2):
        self.particle_count = particle_count
        self.iterations = iterations
        self.c1 = c1
        self.c2 = c2
        self.W = 1
        self.MSmax = 1
        self.MSmin = 0
        self.TCmax = 0
        self.TCmin = 0
        self.TEmax = 0
        self.TEmin = 0
        self.LBCmax = 0
        self.LBCmin = 0
        self.LBFmax = 0
        self.LBFmin = 0

    def initialize_swarm(self, resources, jobs, edges):
        swarm = []
        gbest = None
        gbest_fitness = float('-inf')

        for _ in range(self.particle_count):
            position = [random.randint(0, len(resources) - 1) for _ in range(len(jobs))]
            velocity = [random.uniform(0.0, 1.0) for _ in range(len(jobs))]
            pbest = position.copy()
            pbest_fitness = self.fitness(position, jobs, edges, resources)

            if pbest_fitness > gbest_fitness:
                gbest_fitness = pbest_fitness
                gbest = position.copy()

            swarm.append((position, velocity, pbest, pbest_fitness))

        return gbest, swarm

    def update_swarm(self, swarm, gbest, gbest_fitness, resources, jobs, edges):
        for x in range(len(swarm)):
            position, velocity, pbest, pbest_fitness = swarm[x]
            new_velocity = [
                self.calculate_new_velocity(velocity[y], pbest[y], position[y], gbest[y])
                for y in range(len(position))
            ]
            new_position = [max(0, min(int(position[y] + new_velocity[y]), len(resources) - 1)) for y in range(len(position))]

            new_fitness = self.fitness(new_position, jobs, edges, resources)

            if new_fitness > pbest_fitness:
                pbest = new_position
                pbest_fitness = new_fitness

            if new_fitness > gbest_fitness:
                gbest = new_position
                gbest_fitness = new_fitness

            swarm[x] = (new_position, new_velocity, pbest, pbest_fitness)

        return gbest, gbest_fitness

    def run(self, resources, jobs, edges):
        gbest, swarm = self.initialize_swarm(resources, jobs, edges)

        for _ in range(self.iterations):
            gbest, _ = self.update_swarm(swarm, gbest, self.fitness(gbest, jobs, edges, resources), resources, jobs, edges)

        return gbest

    def fitness(self, position, jobs, edges, resources):
        total_result = 0

        for job in jobs:
            device_id, task_id = job
            vm = resources[position[jobs.index(job)]]
            mips = float(vm["mips"])
            
            for edge in edges[1:]:
                if device_id == edge["id"]:
                    for task in edge["workflow"]:
                        if task[0]["id"] == task_id:
                            runtime = task[0]["runtime"]
                            total_result += self.calculate_makespan(runtime, mips)

        return total_result

    def calculate_makespan(self, task_runtime, resource_mips):
        temp = EX()
        process_time = temp.Time_exec(task_runtime, resource_mips)
        
        self.MSmax = max(self.MSmax, process_time)
        self.MSmin = min(self.MSmin, process_time)
        
        return (process_time - self.MSmin) / (self.MSmax - self.MSmin) if self.MSmax != self.MSmin else 0

    def calculate_new_velocity(self, velocity, pbest, position, gbest):
        inertia = self.W * velocity
        cognitive = self.c1 * random.uniform(0, 1) * (pbest - position)
        social = self.c2 * random.uniform(0, 1) * (gbest - position)
        return inertia + cognitive + social
