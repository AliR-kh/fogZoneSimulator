from utilize.UE_devices.UE_device import Edge
class UE_broker:
    ue_zone_list = []
    edge = Edge()
    
    def __init__(self) -> None:
        pass
    def creat_ue_zone(self):
        numb =5#input("enter number of UE zone:")
        for count_zon in range(int(numb)):
            self.ue_zone_list.append(self.edge.create_edge_devices_z_z(count_zon,2,0))
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