class Calculation:
    
    def result(self,fog,edge,cloud):
        total=0
        temp=0
        #self.totalenergy(fog,cloud,edge)
        
        
        for Y in range(len(edge[0][1]["workflow"])):
            if edge[0][1]["workflow"][Y][0]["makespan"]>total:
                total=edge[0][1]["workflow"][Y][0]["makespan"]
        #print(total)
    
    def total_result(self,fog,cloud,edge,zone_id):
        total_energy=0
        total_cost=0
        makespan=0
        total_makespan=0
        for X in range(1,len(fog)):
           total_energy+=fog[X]["active_energy"]
           total_energy+=fog[X]["idle_energy"]
           total_cost+=fog[X]["total_cost"]
           if makespan< fog[X]["time"]:
               makespan=fog[X]["time"]
           if total_makespan <fog[X]["time"]:
               total_makespan=fog[X]["time"]
        for X in cloud:
            total_energy+=X["idle_energy"]
            total_energy+=X["active_energy"]
            total_cost+=X["total_cost"]
            if total_makespan< X["time"]:
               total_makespan=X["time"]
        for Y in range(1,len(edge[0])):
            total_energy+=edge[Y]["specif"]["active_energy"]
            total_energy+=edge[Y]["specif"]["idle_energy"]
            total_cost+=edge[Y]["specif"]["total_cost"]
            if makespan< edge[Y]["specif"]["time"]:
               makespan=edge[Y]["specif"]["time"]
            if total_makespan< edge[Y]["specif"]["time"]:
               total_makespan=edge[Y]["specif"]["time"]
        if total_makespan<makespan:
            total_makespan=makespan       
        return [zone_id,total_makespan,makespan,total_energy,total_cost] 
