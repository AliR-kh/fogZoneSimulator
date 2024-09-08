def algorithm(UE_zone,Fog_zone):
    """
    this section there are algorithm that assign appropriate fog_zone to Ue_zone

    """
    for i in range(len(Fog_zone)):
        UE_zone[i][0]["assign_resource"]=Fog_zone[i][0]["id"]    
    return UE_zone