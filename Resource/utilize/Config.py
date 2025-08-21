import configparser
import os

class Config:
    def __init__(self, config_file='config.ini'):
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'+config_file))
        self.config_file = config_path
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Configuration file '{self.config_file}' not found.")
        
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

    def get_config(self,section,name,type=None):  
            value=self.config.get(section,name)
            value = value.split(";")[0].split("#")[0].strip()
            return int(value) if type is None else value

# Initialize the config (to be used in other modules)

