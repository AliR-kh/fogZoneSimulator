import os
import configparser
import json
class Config:
    Base_Dire=os.path.dirname(__file__)
    def __init__(self,config_dir="config.ini"):
        self.config_dir=os.path.join(self.Base_Dire,config_dir)
        self._load_config()
    def _load_config(self):
        if not os.path.exists(self.config_dir):
            raise FileNotFoundError(f"Configuration file '{self.config_dir}' not found.")
        
        self.config_file=configparser.ConfigParser()
        self.config_file.read(self.config_dir)
        
    def _get_json_data(self,json_dire):
        json_dire=os.path.join(self.Base_Dire,json_dire)
        if not os.path.exists(json_dire):
            raise FileNotFoundError(f"Configuration file '{json_dire}' not found.") 
        data_dict=None
        with open(json_dire, "r") as f:
            data_dict = json.load(f)
        return data_dict
     
    def get_config(self,section,name,type=""):
        if type=="" or type=="int":
            return self.config_file.getint(section, name)
        if type=="float":
            return self.config_file.getfloat(section, name)
        elif type=="dict":
            return self._get_json_data(self.config_file.get(section,name))
        else:
            return self.config_file.get(section,name)
        
    
        