from abc import ABC,abstractmethod


class Env(ABC):
   
   @abstractmethod
   def __init__(self):
      pass
   
   @abstractmethod
   def get_current_status(self):
      pass
   
   @abstractmethod
   def reset(self):
      pass
   
   