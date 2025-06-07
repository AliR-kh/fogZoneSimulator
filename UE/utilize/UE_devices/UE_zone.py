
from utilize.Config import Config
from utilize.UE_devices.UE_device import Edge

# this class for create Ue Zones, delete Ue Zone, show Ue Zone
#This class creates an object of the Edge class and uses it to place Edge devices into Ue Zones.
class UE_broker:
    ue_zone_list = []
    edge = Edge()
    
    def __init__(self) -> None:
        pass
    def creat_ue_zone(self):
        config=Config()
        n_ue_zone=config.get_config("UE","zone")
        n_device_zone=config.get_config("UE","device_e_zone")
        numb =n_ue_zone#input("enter number of UE zone:")
        for count_zon in range(int(numb)):
            self.ue_zone_list.append(self.edge.create_edge_devices_z_z(count_zon,n_device_zone,0))
        return self.ue_zone_list
    def show_zone(self):
        pass
    
    def add_ue(self,zone_id,inter_time=0):
        id_device=len(self.ue_zone_list[zone_id])-1
        edge=self.edge.edge(zone_id,id_device,inter_time)
        self.ue_zone_list[zone_id].append(edge)
        return edge
    
    def show_device(self,zone_id,ue_id):
        pass
    
    def delete_ue(self,zone_id,ue_id):
        pass
    
    def change_ue(self,old_zone_id,new_zone_id,ue_id):
        pass
    
    def get_ue_zone(self):
        return self.ue_zone_list
    
    def set_uezone(self,new_zone):
        self.ue_zone_list=new_zone