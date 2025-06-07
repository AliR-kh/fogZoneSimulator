class Management:
    def run(self,cloud=[],fog=[], edge=[],task=[]):
        available_fog = []
        for numb_F in range(1, len(fog)):
            if fog[numb_F]["exist_flag"] == 0 and task["time"]>=fog[numb_F]["time"]:
                available_fog.append(fog[numb_F])
        if edge["exist_flag"] == 0 and task["time"]>=edge["time"]:
            available_fog.append(edge)
          
        return available_fog
    
    def run_spare(self,cloud=[],fog=[], edge=[]):
        tmin=fog[1]
        for numb_F in range(1, len(fog)):
            if fog[numb_F]["exist_flag"] == 0 :
                if fog[numb_F]["time"]<tmin["time"]:
                    tmin=fog[numb_F] 
        if tmin["time"]>edge["time"]:
            tmin=edge 
        return tmin["time"]            
        
        
