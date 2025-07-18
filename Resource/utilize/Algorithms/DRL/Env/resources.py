from utilize.Algorithms.DRL.Env.env import Env
import torch
import numpy as np

class Resource(Env):
    def __init__(self, number_of_resource=5, config_of_resource=None,A_resources=None,):
        if A_resources is not None:
            self.resources=A_resources[:-1].copy()
        else:
            self.number_of_resources = number_of_resource
            self.config_of_resource = config_of_resource
            self.resources = self._create_resources()
    def get_current_status(self):
        return self.resources
    def _create_resources(self):
        resources = []
        for i in range(self.number_of_resources):
            if len(self.config_of_resource) < self.number_of_resources:
                config = self.config_of_resource
                resources.append(
                    {
                        "type": config["type"],
                        "id": i,
                        "cpu": config["cpu"],
                        "cost_per_second":config["cost_per_second"],
                        "consume_power": config["consume_power"],
                        "idle_power": config["idle_power"],
                        "down_bw": config["down_bw"],
                        "up_bw": config["up_bw"],
                        "queue_time": 0,
                        "assigned_mips":0,
                        "consumed_power":0,
                        "consumed_cost":0,
                        "makespan":0,
                    }
                )
            else:
                config = self.config_of_resource[i]
                resources.append(
                    {
                        "type": config["type"],
                        "id": i,
                        "cpu": config["cpu"],
                        "cost_per_second":config["cost_per_second"],
                        "consume_power": config["consume_power"],
                        "idle_power": config["idle_power"],
                        "down_bw": config["down_bw"],
                        "up_bw": config["up_bw"],
                        "queue_time": 0,
                        "assigned_mips":0,
                        "consumed_power":0,
                        "consumed_cost":0,
                        "makespan":0,
                    }
                )
                
        return np.array(resources)

    def reset(self):
        self.resources = []

    def set_property_to_resource(self,resource_index,summary_changed):
        self.resources[resource_index]["makespan"]+=summary_changed["processing_time"]+summary_changed["transfer_time"]
        self.resources[resource_index]["assigned_mips"]+=summary_changed["load_balancing"]
        self.resources[resource_index]["consumed_power"]+=summary_changed["energy"]
        self.resources[resource_index]["consumed_cost"]+=summary_changed["cost"]
        self.resources[resource_index]["queue_time"]+=summary_changed["processing_time"]