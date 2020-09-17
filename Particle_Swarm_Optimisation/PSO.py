from particle import *
import math
import matplotlib.pyplot as plt
import turtle
from time import sleep
import os
from datetime import datetime


class PSO:
    def __init__(self,swarm_size,init_params,max_iterations,velocity_fun,show_animation):
        self.size = swarm_size
        self.init_params = init_params
        self.show_animation = show_animation
        self.position_range = self.init_params[6] # this is mainly for animation
        if self.show_animation:
            self.animate_init()
        self.swarm = self.init_swarm()
        self.max_iterations = max_iterations
        self.iteration = 1
        self.velocity_fun = velocity_fun # options are, "default","inertia_weight","constrict","guarenteed"
        self.best_solution = Solution(100,100) # This will be overwritten as the init cost is inf
        self.avg_fitness = []
        self.best_particle_fitness = []

    def init_swarm(self):
        pos = self.init_params[0]
        vel = self.init_params[1]
        weight = self.init_params[2]
        c1 = self.init_params[3]
        c2 = self.init_params[4]
        v_max = self.init_params[5]
        self.position_range = self.init_params[6]
        new_swarm = [Particle(pos[i],vel,weight,c1,c2,v_max,position_range,self.show_animation) for i in range(0,self.size)]

        return new_swarm

    def terminate(self):
        if self.iteration > self.max_iterations:
            return True
        return False
    
    def run(self): # implement with async update
        for i in range(0,self.size):
            self.update_gbest(self.swarm[i].pbest) # need to do this first to find which is the best
        
        if self.show_animation:
            gbest_point = turtle.Turtle()
            gbest_point.turtlesize(0.5,0.5)
            gbest_point.speed(5)
            gbest_point.shape("circle")
            gbest_point.color('red','green')
            
        while (not(self.terminate())):
            iter_particle_fitness = []
            for i in range(0,self.size):
                if self.velocity_fun == "default":
                    self.swarm[i].weight = 1 # this is just without weight
                    self.swarm[i].update_velocity_weight()
                elif self.velocity_fun == 'weight':
                    self.swarm[i].update_velocity_weight()
                elif self.velocity_fun == 'constriction':
                    self.swarm[i].update_velocity_constr()
                elif self.velocity_fun == 'convergence':
                    self.swarm[i].update_velocity_guaren()
                else:
                    raise ('velocity function not selected')
                self.swarm[i].update_position()
                self.swarm[i].update_pbest()
                self.update_gbest(self.swarm[i].pbest)
                iter_particle_fitness.append(self.swarm[i].cur_cost)
                if self.show_animation:
                    self.swarm[i].animate()
            if self.show_animation:
                gbest_point.clear()
                gbest_point.goto(self.best_solution.position.x,self.best_solution.position.y)


                turtle.update()
                # sleep(1)

            print("iteration: " + str(self.iteration) + " z: " \
                + str(self.best_solution.cost) + " (x,y): ("+str(self.best_solution.position.x) + "," \
                + str(self.best_solution.position.y) + ")")
            self.iteration = self.iteration + 1
            self.avg_fitness.append(sum(iter_particle_fitness)/self.size)
            self.best_particle_fitness.append(self.best_solution.cost)
        return self.best_solution

    def update_gbest(self,cur_pbest):
        if cur_pbest.cost < self.best_solution.cost:
            new_sol = Solution(cur_pbest.position.x,cur_pbest.position.y) # this and below means it will copy
            new_sol.cost = cur_pbest.cost
            self.best_solution = new_sol
            for i in range(0,self.size):
                self.swarm[i].gbest = new_sol
                if (self.swarm[i].pbest.position.x == new_sol.position.x and self.swarm[i].pbest.position.y == new_sol.position.y):
                    self.swarm[i].is_gbest = True
                else:
                    self.swarm[i].is_gbest = False

    def animate_init(self):
        turtle.setworldcoordinates(self.position_range[0],self.position_range[0],self.position_range[1],self.position_range[1])
        # turtle.tracer(100000,100) # Made this large as we will be manually callin update


            


if __name__ == "__main__":
    show_animation = False
    size = 100 
    range_min = -5
    range_max = 5
    starting_positions = [Position((random.random()-0.5)*2*range_max,(random.random()-0.5)*2*range_max)\
                             for i in range(0,size)]
    start_vel = Velocity(0,0)
    weight = 0.5
    c1 = 1.5
    c2 = c1
    original_c1 = c1
    v_max = 1000
    position_range = [range_min,range_max]
    start_params = [starting_positions,start_vel,weight,c1,c2,v_max,position_range]
    max_iterations = 100
    velocity_function = 'default' # options are 'weight' , 'constriction' , 'convergence'
    
    

    f = open(str(os.path.dirname(os.path.abspath(__file__)))+"\\test_results.txt","a")
    f.write("\n\r"+str(datetime.now())+"\n\r")

    velocity_options = ['default','weight','constriction','convergence']
    for iter_val in range(0,len(velocity_options)):
        velocity_function = velocity_options[iter_val]
        if velocity_function == 'constriction':
            c1 = 2.05
            c2 = c1
        else:
            c1 = original_c1
            c2 = c1
        swarm_0 = PSO(size,start_params,max_iterations,velocity_function,show_animation)
        best_solution_0 = swarm_0.run()
        f.write(f'Parameters:\n\rVelocity_Fun:{velocity_function}\n\rMax_Iterations{max_iterations}\n\rSize:{size}\n\rRange: {range_min},{range_max}\n\rStart_vel:{start_vel}\n\rWeight:{weight}\n\rc1:{c1}\n\rc2{c2}\n\rv_max:{v_max}\n\r')
        f.write("Best solution was at (" + str(best_solution_0.position.x) \
                + "," + str(best_solution_0.position.y) + ") where z = " + \
                    str(best_solution_0.cost)+"\n\r")
        print ("Best solution was at (" + str(best_solution_0.position.x) \
                + "," + str(best_solution_0.position.y) + ") where z = " + \
                    str(best_solution_0.cost))

        f1 = plt.figure(iter_val)
        x1 = [i for i in range(1,max_iterations+1)]

        plt.plot(x1,copy.copy(swarm_0.avg_fitness),label = "Average Fitness")
        plt.plot(x1,copy.copy(swarm_0.best_particle_fitness),label = "Best Particle Fitness")
        plt.legend()
        plt.xlabel("Iteration")
        plt.ylabel("Fitness")
        plt.title("Fitness vs Iteration ("+str(velocity_function)+")")

    plt.show()

    

                