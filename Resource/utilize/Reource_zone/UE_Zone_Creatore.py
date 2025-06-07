from utilize.Reource_zone.Fog_Resource import Fog
from utilize.Execution.execut import Execut as Ex
from utilize.Algorithms.pso import PSO
from utilize.management.management import Management as MN

# this class for create fog Zones based on number of Ue Zone
#This class creates an object of the Fog class and uses it to place Fog devices into Ue Zones.
class Fog_broker:
    number_zone=0
    def __init__(self,number_zone,fog=[], edge=[], jobs=0) -> None:
        self.number_zone=number_zone
        fog = fog
        edge = edge
        jobs = jobs 
# output is [[{'id': 0}, {'id': 0, 'type': 'Fog', 'mips': '', 'parentid': 0, 'con_pow_active': '', 'con_pow_idle': 0, 'down_bw': 0, 'down_cost': 0, 'up_bw': 0, 'up_cost': 0, 'memory_cost': 0, 'exist_flag': 0, 'memory_size': 0}]]
# out[0:n] is number of zone or sepecification of zon
# out[x][0] is id of zone
# out[x][1:n] specification of fog node
    def createfog(self):
        fog_zone_list = []
        fog = Fog()
        alg = "N"#input("using the algorith: Y or N :")
        if alg == ('Y') or alg == ('y'):
            pass
        else:
            alg = 1
            numzone =1# input("number of fog zone: ")
            for temp in range(int(self.number_zone)):
                fog_zone_list.append(fog.create_fog_device(temp, alg))

            return fog_zone_list