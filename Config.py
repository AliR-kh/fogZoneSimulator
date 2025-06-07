import configparser
import os

class Config:
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Configuration file '{self.config_file}' not found.")
        
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

    def get_config(self,section,name,type=""):
        if type=="":
            return self.config.getint(section, name)
        else:
            return self.config.get(section,name)

# Initialize the config (to be used in other modules)

