import random
import datetime as dt
from utilize.Execution.execut import Execut as EX

class PSO:
    def __init__(self,tasks,resources,particle_count=20, iterations=10, c1=2, c2=2):
        self.particle_count = particle_count
        self.iterations = iterations
        self.c1 = c1
        self.c2 = c2
        self.W = 1
        self.MSmax = 1
        self.MSmin = 0
        self.TCmax = 0
        self.TCmin = 0
        self.TEmax = 0
        self.TEmin = 0
        self.LBCmax = 0
        self.LBCmin = 0
        self.LBFmax = 0
        self.LBFmin = 0
        self.tasks=tasks
        self.resources=resources
    def initialize_swarm(self):
        swarm = []
        gbest = None
        gbest_fitness = float('-inf')
        for _ in range(self.particle_count):
            position = [random.randint(0, len(self.resources) - 1) for _ in range(len(self.tasks))]
            velocity = [random.uniform(0.0, 1.0) for _ in range(len(self.tasks))]
            pbest = position.copy()
            pbest_fitness = self.fitness(position)

            if pbest_fitness > gbest_fitness:
                gbest_fitness = pbest_fitness
                gbest = position.copy()

            swarm.append((position, velocity, pbest, pbest_fitness))

        return gbest,swarm

    def update_swarm(self, swarm, gbest, gbest_fitness):
        for x in range(len(swarm)):
            position, velocity, pbest, pbest_fitness = swarm[x]
            new_velocity = [
                self.calculate_new_velocity(velocity[y], pbest[y], position[y], gbest[y])
                for y in range(len(position))
            ]
            new_position = [max(0, min(int(position[y] + new_velocity[y]), len(self.resources) - 1)) for y in range(len(position))]

            new_fitness = self.fitness(new_position)

            if new_fitness > pbest_fitness:
                pbest = new_position
                pbest_fitness = new_fitness

            if new_fitness > gbest_fitness:
                gbest = new_position
                gbest_fitness = new_fitness

            swarm[x] = (new_position, new_velocity, pbest, pbest_fitness)

        return gbest, gbest_fitness

    def run(self):
        gbest, swarm = self.initialize_swarm()

        for _ in range(self.iterations):
            gbest, _ = self.update_swarm(swarm, gbest, self.fitness(gbest))

        print(gbest)
        return gbest
     
    def fitness(self,position):
        result=0
        for jobnumb in range(len(self.tasks)):
            runtime=self.tasks[jobnumb]["runtime"]
            mips=self.resources[position[jobnumb]]["mips"]
            result+=self.calculate_makespan(runtime,mips)

        return result                
    def calculate_makespan(self, task_runtime, resource_mips):
        temp = EX()
        process_time = temp.Time_exec(task_runtime, resource_mips)
        
        self.MSmax = max(self.MSmax, process_time)
        self.MSmin = min(self.MSmin, process_time)
        
        return (process_time - self.MSmin) / (self.MSmax - self.MSmin) if self.MSmax != self.MSmin else 0

    def calculate_new_velocity(self, velocity, pbest, position, gbest):
        inertia = self.W * velocity
        cognitive = self.c1 * random.uniform(0, 1) * (pbest - position)
        social = self.c2 * random.uniform(0, 1) * (gbest - position)
        return inertia + cognitive + social
