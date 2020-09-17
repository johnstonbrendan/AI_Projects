from coordinates import distances
import random
from math import inf
import copy
import matplotlib.pyplot as plt
from datetime import datetime
import os

class edge:
    def __init__(self,distance,pheromone,tabu,start,end):
        self.distance = distance
        self.pheromone = pheromone 
        self.probability = 0
        self.tabu = tabu
        self.start = start
        self.end = end

class ant:
    def __init__(self,alpha,beta,starting_pheromone,starting_node,is_online,cities,pheromone_list,control,Q_phero,persistance):
        self.cities = cities
        self.paths = self.init_paths(pheromone_list)
        self.alpha = alpha
        self.beta = beta
        self.cur_node = starting_node
        self.home_node = starting_node
        self.solution = Solution()
        self.is_online = is_online
        self.sum_of_prob = inf
        self.control_parameter = control
        self.Q_phero = Q_phero
        self.starting_pheromone = starting_pheromone
        self.persistance = persistance
        self.best_edge = edge(inf,0,True,0,0) # These are just initial parameters and should be changed before being used


    def init_paths(self,global_pheromone):
        new_paths = []
        for i in range(0,self.cities):
            new = []
            for j in range(0,self.cities):
                if i != j:
                    new.append(edge(distances[i][j],global_pheromone[i][j],False,i,j))
                else:
                    new.append(edge(distances[i][j],global_pheromone[i][j],True,i,j))
            new_paths.append(new)
        return new_paths


    # def update_probabilities(self): # i don't think this is used
    #     i = 0
    #     row_sums = []
    #     for row in self.paths:
    #         j = 0
    #         row_sum = 0
    #         for cur_edge in row:
    #             if i != j:
    #                 row_sum = row_sum + pow(cur_edge.pheromone,self.alpha)/pow(cur_edge.distance,self.beta)
    #             j = j + 1
    #         row_sums.append(row_sum)
    #         i = i + 1

    #     i = 0
    #     for row in self.paths:
    #         j = 0
    #         for cur_edge in row:
    #             if i!=j:
    #                 if cur_edge.tabu == False:
    #                     cur_edge.pheromone = self.pheromone[i][j]
    #                     cur_edge.probability = (pow(cur_edge.pheromone,self.alpha)/
    #                                                 pow(cur_edge.distance,self.beta))/row_sums[i]
    #                 else:
    #                     self.paths[i][j].probability = 0 # Need to change tabu before you change the probability
    #                 #print ("From: " + str(i) + " to: " + str(j) + " prob: " + str(paths[i][j].probability))
    #             j = j + 1
    #         i = i + 1

    def find_sol(self):
        # make this a do while and have it go until therere are no more options.
        options = self.find_path_options_and_set_sum() # This will also update the best path
        self.solution.cost = 0
        while options.__len__() != 0:
            if self.control_parameter > random.random():
                # This means take the best path
                self.solution.cost = self.solution.cost + self.best_edge.distance
                self.update_edge_pher_step_by_step(self.best_edge.start,self.best_edge.end)
                self.solution.trip.append(self.best_edge)
                self.solution.visited.append(self.cur_node)
                self.update_tabu()
                self.cur_node = self.best_edge.end
            else:
                select_option = random.random()
                for edge_option in options:
                    edge_option.probability = (pow(edge_option.pheromone,self.alpha)/pow(edge_option.distance,self.beta))/self.sum_of_prob
                    if edge_option.probability > select_option: # this means select this option
                        self.solution.cost = self.solution.cost + edge_option.distance
                        self.update_edge_pher_step_by_step(edge_option.start,edge_option.end)
                        self.solution.trip.append(edge_option) # This adds the selected edge_option to the solution set
                        self.solution.visited.append(self.cur_node) # This then adds the current node to visited
                        self.update_tabu() # This then makes all edges that contain any visited nodes in start or end tabu, 
                                            # although this will include the path taken this will be okay as it would have already been taken
                        self.cur_node = edge_option.end
                        
                        break
                        #do updtaing so that you select this path, if it's online leave phero and change current node also set tabu
                    else:
                        select_option = select_option - edge_option.probability
                        #do select_option minus edge_option.probability, and go to choose the next one
            options = self.find_path_options_and_set_sum() # This will also update the best path
        self.solution.cost = self.solution.cost + self.paths[self.cur_node][self.home_node].distance
        self.update_edge_pher_step_by_step(self.cur_node,self.home_node)
        self.solution.trip.append(self.paths[self.cur_node][self.home_node])
        self.solution.visited.append(self.cur_node)
        self.cur_node = self.home_node
        return self.solution

    def update_edge_pher_step_by_step(self,start,end):
        if self.is_online: # update using ant quantity model
            # need to update both as it is the same path and some ants might take it going the other way
            self.paths[start][end].pheromone = self.paths[start][end].pheromone + self.Q_phero/self.paths[start][end].distance
            self.paths[end][start].pheromone = self.paths[start][end].pheromone
        else: # update using offline rule
            self.paths[start][end].pheromone = (1-self.persistance[2])*self.paths[start][end].pheromone + self.persistance[2]*self.starting_pheromone
            self.paths[end][start].pheromone = self.paths[start][end].pheromone


    def update_tabu(self):
        # Assuming the last added to the tabu list was the most recent node and that everytime something is added this is called
        to_add = self.solution.visited[-1]

        for cur_edge in self.paths[to_add]:
            cur_edge.tabu = True
        for row in self.paths:
            row[to_add].tabu = True

    def find_path_options_and_set_sum(self):
        options = []
        best_option_prob = -inf
        i = 0
        self.sum_of_prob = 0
        for row in self.paths:
            j = 0
            for cur_edge in row:
                if i == self.cur_node and not(cur_edge.tabu):
                    options.append(cur_edge)
                    cur_probability = pow(cur_edge.pheromone,self.alpha)/pow(cur_edge.distance,self.beta)
                    self.sum_of_prob = self.sum_of_prob + cur_probability
                    if cur_probability > best_option_prob:
                        best_option_prob = cur_probability
                        self.best_edge = cur_edge

                j = j + 1
            i = i + 1
        return options

    def copy_global_phermone_to_local(self,global_pheromone):
        i = 0
        for rows in global_pheromone:
            j = 0
            for val in rows:
                self.paths[i][j].pheromone = val
                j = j + 1
            i = i + 1


class Solution:
    def __init__(self):
        self.cost = inf
        self.trip = [] # This will contain a list of edges taken
        self.visited = [] # This contains a list of the visited nodes


class ACO:
    def __init__(self,population,is_online,initial_pheromone,max_iter,alpha,beta, num_of_cities,control,Q_phero,persistance):
        self.iteration = 0
        self.population = population
        self.is_online = is_online
        self.colony = []
        self.max_iterations = max_iter
        self.alpha = alpha
        self.beta = beta
        self.initial_pheromone = initial_pheromone
        self.num_of_cities = num_of_cities
        self.global_pheromone = self.init_pheromone()
        self.control_parameter = control
        self.Q_phero = Q_phero
        self.persistance = persistance
        self.best_global_solution = Solution()
        self.best_iter_solution = Solution()
        self.colony = []
        self.iter_found_best = self.iteration
        self.costs_found_per_iteration = []
        

        
    def new_colony(self):
        new_colony = []
        for i in range(0,self.population):
            new_colony.append(ant(self.alpha,self.beta,self.initial_pheromone,random.randint(0,self.num_of_cities-1),
                                    self.is_online,self.num_of_cities,self.global_pheromone,self.control_parameter,self.Q_phero,self.persistance))
        return new_colony

    def update_pheromone(self):
        # First do evaporation
        if is_online:
            i = 0
            for row in self.global_pheromone:
                j = 0
                for val in row:
                    self.global_pheromone[i][j] = (1-self.persistance[0])*val
                    j = j + 1
                i = i + 1

        else: # means offline and need to update using the best solution ant only
            for sol_edge in self.best_iter_solution.trip:
                # self.global_pheromone[sol_edge.start][sol_edge.end] = (1-self.persistance[1])*self.global_pheromone[sol_edge.start][sol_edge.end] + \
                #                                                         self.persistance[1]*(self.Q_phero/sol_edge.distance)
                self.global_pheromone[sol_edge.start][sol_edge.end] = self.global_pheromone[sol_edge.start][sol_edge.end] + \
                                                                        self.persistance[1]*(self.Q_phero/sol_edge.distance)
                self.global_pheromone[sol_edge.end][sol_edge.start] = self.global_pheromone[sol_edge.start][sol_edge.end]
                                        


    def loop(self):
        while not(self.check_terminate()):
            self.colony = self.new_colony()
            self.best_iter_solution = Solution()
            # need to wipe the ant memory here
            for ant_sol in self.colony:
                ant_sol.copy_global_phermone_to_local(self.global_pheromone)
                ant_solution = ant_sol.find_sol()
                if ant_solution.cost < self.best_iter_solution.cost:
                    self.best_iter_solution = ant_solution
                self.copy_local_pheromone_to_global(ant_sol.paths) # the ant_sol will have updated pheromone values based off path taken
            if self.best_iter_solution.cost < self.best_global_solution.cost:
                self.best_global_solution = self.best_iter_solution
                self.iter_found_best = self.iteration
            self.costs_found_per_iteration.append(self.best_global_solution.cost)
            self.update_pheromone()
            self.iteration = self.iteration + 1

    def copy_local_pheromone_to_global(self,local_paths):
        i = 0
        for rows in local_paths:
            j = 0
            for cur_edge in rows:
                self.global_pheromone[i][j] = cur_edge.pheromone
                j = j + 1
            i = i + 1


    def check_terminate(self):
        if self.iteration > self.max_iterations:
            return True
        return False

    def init_pheromone(self):
        new_paths = []
        for i in range(0,self.num_of_cities):
            new = []
            for j in range(0,self.num_of_cities):
                new.append(self.initial_pheromone)
            new_paths.append(new)
        return new_paths

    def generate_solution(self):
        self.loop()
        return self.best_global_solution



        

        




if __name__ == "__main__":
    starting_pheromone = 20
    cities = 29
    num_of_ants = 50
    alpha = 1
    beta = 1
    is_online = True
    max_iterations = 200
    control_parameter = 0.5 # was 0.5 for all the tests that don't state the value
    Q_phero = 10000
    evaporation_rate = 0.2
    p_1 = evaporation_rate # p_1 and p_2 used for offline updating
    p_2 = 0.5
    persistance = [evaporation_rate,p_1,p_2]
    
    pheromone_persistance_list = [0.2,0.4,0.5,0.6,0.8]
    control_parameter_list = [0.2,0.4,0.5,0.6,0.8]
    population_list = [25,50,100]
    


    # x1 = [i for i in range(1,max_iterations+1)]
    # y1 = [2*i + 1 for i in x1]

    # y2 = [3*i + 2 for i in x1]

    # f1 = plt.figure(1)
    # plt.plot(x1,y1,label = "1")
    # plt.plot(x1,y2,label = "2")
    # plt.legend()
    # print("blocked")
    # plt.show()
    # print("unblocked")


    best_cost = inf

    is_online = False
    f1 = plt.figure(1)
    x1 = [i for i in range(1,max_iterations + 2)]
    original_evaporation_rate = evaporation_rate
    for evaporation_rate_val in pheromone_persistance_list:
        evaporation_rate = evaporation_rate_val
        persistance = [evaporation_rate,p_1,p_2]
        Colony_0 = ACO(num_of_ants,is_online,starting_pheromone,max_iterations,alpha,beta,cities,control_parameter,Q_phero,persistance)
        # iterations.append(max_iterations)
        iter_solution = Colony_0.generate_solution()
        label_str = "Evaporation = " + str(evaporation_rate)
        plt.plot(x1,Colony_0.costs_found_per_iteration,label = label_str)
        print("one done")
        if iter_solution.cost < best_cost:
            best_cost = iter_solution.cost
            output = "Number of Iterations: " + str(max_iterations) + " With Cost: " + str(iter_solution.cost) + \
                                                        " Starting pheromone: " + str(starting_pheromone) + " population: " + str(num_of_ants) +\
                                                            " alpha: " + str(alpha) + " beta: " + str(beta) + " is_online: " + str(is_online) + \
                                                                " evaporation rate: " + str(evaporation_rate) + " p_1: " + str(p_1) + " p_2: " + str(p_2) + \
                                                                    " Q: " + str(Q_phero) + " Control parameter: " + str(control_parameter) +\
                                                                        " Path: " + str(iter_solution.visited)+ " Found at iteration: " + str(Colony_0.iter_found_best)+" Best Cost so far: " + str(best_cost) + "\n\r"
            print (output)
    plt.title("Changing Evaporation Rate (Offline)")
    plt.legend()
    filePath = str(os.path.dirname(os.path.abspath(__file__))) + "\\"
    fileName = "Change evap offline " + str(datetime.now().strftime("%H%M %S"))
    fileExt = ".png"
    plt.savefig(filePath + fileName + fileExt)
    evaporation_rate = original_evaporation_rate

    f2 = plt.figure(2)
    original_control_parameter = control_parameter
    for control_parameter_val in control_parameter_list:
        control_parameter = control_parameter_val
        Colony_0 = ACO(num_of_ants,is_online,starting_pheromone,max_iterations,alpha,beta,cities,control_parameter,Q_phero,persistance)
        # iterations.append(max_iterations)
        iter_solution = Colony_0.generate_solution()
        label_str = "Control Param = " + str(control_parameter)
        plt.plot(x1,Colony_0.costs_found_per_iteration,label = label_str)
        print("one done")
        if iter_solution.cost < best_cost:
            best_cost = iter_solution.cost
            output = "Number of Iterations: " + str(max_iterations) + " With Cost: " + str(iter_solution.cost) + \
                                                        " Starting pheromone: " + str(starting_pheromone) + " population: " + str(num_of_ants) +\
                                                            " alpha: " + str(alpha) + " beta: " + str(beta) + " is_online: " + str(is_online) + \
                                                                " evaporation rate: " + str(evaporation_rate) + " p_1: " + str(p_1) + " p_2: " + str(p_2) + \
                                                                    " Q: " + str(Q_phero) + " Control parameter: " + str(control_parameter) +\
                                                                        " Path: " + str(iter_solution.visited)+ " Found at iteration: " + str(Colony_0.iter_found_best)+" Best Cost so far: " + str(best_cost) + "\n\r"
            print (output)
    plt.title("Changing Control Parameter (Offline)")
    plt.legend()
    filePath = str(os.path.dirname(os.path.abspath(__file__))) + "\\"
    fileName = "Change control offline " + str(datetime.now().strftime("%H%M %S"))
    fileExt = ".png"
    plt.savefig(filePath + fileName + fileExt)
    control_parameter = original_control_parameter


    f3 = plt.figure(3)
    original_population = num_of_ants
    for population_val in population_list:
        num_of_ants = population_val
        Colony_0 = ACO(num_of_ants,is_online,starting_pheromone,max_iterations,alpha,beta,cities,control_parameter,Q_phero,persistance)
        # iterations.append(max_iterations)
        iter_solution = Colony_0.generate_solution()
        label_str = "Population = " + str(num_of_ants)
        plt.plot(x1,Colony_0.costs_found_per_iteration,label = label_str)
        print("one done")
        if iter_solution.cost < best_cost:
            best_cost = iter_solution.cost
            output = "Number of Iterations: " + str(max_iterations) + " With Cost: " + str(iter_solution.cost) + \
                                                        " Starting pheromone: " + str(starting_pheromone) + " population: " + str(num_of_ants) +\
                                                            " alpha: " + str(alpha) + " beta: " + str(beta) + " is_online: " + str(is_online) + \
                                                                " evaporation rate: " + str(evaporation_rate) + " p_1: " + str(p_1) + " p_2: " + str(p_2) + \
                                                                    " Q: " + str(Q_phero) + " Control parameter: " + str(control_parameter) +\
                                                                        " Path: " + str(iter_solution.visited)+ " Found at iteration: " + str(Colony_0.iter_found_best)+" Best Cost so far: " + str(best_cost) + "\n\r"
            print (output)
    plt.title("Changing Population (Offline)")
    plt.legend()
    filePath = str(os.path.dirname(os.path.abspath(__file__))) + "\\"
    fileName = "Change pop offline " + str(datetime.now().strftime("%H%M %S"))
    fileExt = ".png"
    plt.savefig(filePath + fileName + fileExt)
    num_of_ants = original_population

    is_online = True
    f4 = plt.figure(4)
    original_evaporation_rate = evaporation_rate
    for evaporation_rate_val in pheromone_persistance_list:
        evaporation_rate = evaporation_rate_val
        persistance = [evaporation_rate,p_1,p_2]
        Colony_0 = ACO(num_of_ants,is_online,starting_pheromone,max_iterations,alpha,beta,cities,control_parameter,Q_phero,persistance)
        # iterations.append(max_iterations)
        iter_solution = Colony_0.generate_solution()
        label_str = "Evaporation = " + str(evaporation_rate)
        plt.plot(x1,Colony_0.costs_found_per_iteration,label = label_str)
        print("one done")
        if iter_solution.cost < best_cost:
            best_cost = iter_solution.cost
            output = "Number of Iterations: " + str(max_iterations) + " With Cost: " + str(iter_solution.cost) + \
                                                        " Starting pheromone: " + str(starting_pheromone) + " population: " + str(num_of_ants) +\
                                                            " alpha: " + str(alpha) + " beta: " + str(beta) + " is_online: " + str(is_online) + \
                                                                " evaporation rate: " + str(evaporation_rate) + " p_1: " + str(p_1) + " p_2: " + str(p_2) + \
                                                                    " Q: " + str(Q_phero) + " Control parameter: " + str(control_parameter) +\
                                                                        " Path: " + str(iter_solution.visited)+ " Found at iteration: " + str(Colony_0.iter_found_best)+" Best Cost so far: " + str(best_cost) + "\n\r"
            print (output)
    plt.title("Changing Evaporation Rate (Online)")
    plt.legend()
    filePath = str(os.path.dirname(os.path.abspath(__file__))) + "\\"
    fileName = "Change evap online " + str(datetime.now().strftime("%H%M %S"))
    fileExt = ".png"
    plt.savefig(filePath + fileName + fileExt)
    evaporation_rate = original_evaporation_rate

    f5 = plt.figure(5)
    original_control_parameter = control_parameter
    for control_parameter_val in control_parameter_list:
        control_parameter = control_parameter_val
        Colony_0 = ACO(num_of_ants,is_online,starting_pheromone,max_iterations,alpha,beta,cities,control_parameter,Q_phero,persistance)
        # iterations.append(max_iterations)
        iter_solution = Colony_0.generate_solution()
        label_str = "Control Param = " + str(control_parameter)
        plt.plot(x1,Colony_0.costs_found_per_iteration,label = label_str)
        print("one done")
        if iter_solution.cost < best_cost:
            best_cost = iter_solution.cost
            output = "Number of Iterations: " + str(max_iterations) + " With Cost: " + str(iter_solution.cost) + \
                                                        " Starting pheromone: " + str(starting_pheromone) + " population: " + str(num_of_ants) +\
                                                            " alpha: " + str(alpha) + " beta: " + str(beta) + " is_online: " + str(is_online) + \
                                                                " evaporation rate: " + str(evaporation_rate) + " p_1: " + str(p_1) + " p_2: " + str(p_2) + \
                                                                    " Q: " + str(Q_phero) + " Control parameter: " + str(control_parameter) +\
                                                                        " Path: " + str(iter_solution.visited)+ " Found at iteration: " + str(Colony_0.iter_found_best)+" Best Cost so far: " + str(best_cost) + "\n\r"
            print (output)
    plt.title("Changing Control Parameter (Online)")
    plt.legend()
    filePath = str(os.path.dirname(os.path.abspath(__file__))) + "\\"
    fileName = "Change control online " + str(datetime.now().strftime("%H%M %S"))
    fileExt = ".png"
    plt.savefig(filePath + fileName + fileExt)
    control_parameter = original_control_parameter


    f6 = plt.figure(6)
    original_population = num_of_ants
    for population_val in population_list:
        num_of_ants = population_val
        Colony_0 = ACO(num_of_ants,is_online,starting_pheromone,max_iterations,alpha,beta,cities,control_parameter,Q_phero,persistance)
        # iterations.append(max_iterations)
        iter_solution = Colony_0.generate_solution()
        label_str = "Population = " + str(num_of_ants)
        plt.plot(x1,Colony_0.costs_found_per_iteration,label = label_str)
        print("one done")
        if iter_solution.cost < best_cost:
            best_cost = iter_solution.cost
            output = "Number of Iterations: " + str(max_iterations) + " With Cost: " + str(iter_solution.cost) + \
                                                        " Starting pheromone: " + str(starting_pheromone) + " population: " + str(num_of_ants) +\
                                                            " alpha: " + str(alpha) + " beta: " + str(beta) + " is_online: " + str(is_online) + \
                                                                " evaporation rate: " + str(evaporation_rate) + " p_1: " + str(p_1) + " p_2: " + str(p_2) + \
                                                                    " Q: " + str(Q_phero) + " Control parameter: " + str(control_parameter) +\
                                                                        " Path: " + str(iter_solution.visited)+ " Found at iteration: " + str(Colony_0.iter_found_best)+" Best Cost so far: " + str(best_cost) + "\n\r"
            print (output)
    plt.title("Changing Population (Online)")
    plt.legend()
    filePath = str(os.path.dirname(os.path.abspath(__file__))) + "\\"
    fileName = "Change pop online " + str(datetime.now().strftime("%H%M %S"))
    fileExt = ".png"
    plt.savefig(filePath + fileName + fileExt)
    num_of_ants = original_population

    print("done")
    plt.show()
    







    # # Below was code used to attempt to find the best solution
    # starting_pheromone_to_test = [2]
    # control_parameter_to_test = [0.3,0.4,0.5,0.7]
    # num_of_ants_to_test = [20]
    # alpha_to_test = [3]
    # beta_to_test = [3]
    # is_online_to_test = [True,False]
    # evaporation_rate_to_test = [0.2]
    # p_1_to_test = [0.1,0.2,0.5,0.8]
    # p_2_to_test = [0.1,0.2,0.5,0.8]
    # p_1_to_test = [0.1,0.2]
    # p_2_to_test = [0.1,0.2]
    # Q_phero_to_test = [20]
    # iterations_to_test = [2000]

    # solutions = [] # for plotting
    # iterations = []

    # # Colony_0 = ACO(num_of_ants,is_online,starting_pheromone,max_iterations,alpha,beta,cities,control_parameter,Q_phero,persistance)
    # # iterations.append(max_iterations)


    # # solutions.append(Colony_0.generate_solution())
    # # print ("Best solution was this path: " + str(solution.visited) + " with the cost of: " + str(solution.cost) + " with iterations:: " + str(max_iterations))
    # # distance = 0

    # f = open(str(os.path.dirname(os.path.abspath(__file__)))+"\\test_results.txt","a")
    # f.write(str(datetime.now())+"\n\r")
    # best_cost = inf

    # # Below was an attempt to find the very best solution
    # for control_parameter_val in control_parameter_to_test:
    #     control_parameter = control_parameter_val
    #     for iter_val in iterations_to_test:
    #         max_iterations = iter_val
    #         for Q_phero_val in Q_phero_to_test:
    #             Q_phero = Q_phero_val
    #             for online_val in is_online_to_test:
    #                 is_online = online_val
    #                 for p_2_val in p_2_to_test:
    #                     p_2 = p_2_val
    #                     for p_1_val in p_1_to_test:
    #                         p_1 = p_1_val
    #                         for evap_val in evaporation_rate_to_test:
    #                             evaporation_rate = evap_val
    #                             for beta_val in beta_to_test:
    #                                 beta = beta_val
    #                                 for alpha_val in alpha_to_test:
    #                                     alpha = alpha_val
    #                                     for pops in num_of_ants_to_test:
    #                                         num_of_ants = pops
    #                                         for start_phero in starting_pheromone_to_test:
    #                                             starting_pheromone = start_phero
    #                                             Colony_0 = ACO(num_of_ants,is_online,starting_pheromone,max_iterations,alpha,beta,cities,control_parameter,Q_phero,persistance)
    #                                             # iterations.append(max_iterations)
    #                                             iter_solution = Colony_0.generate_solution()
    #                                             solutions.append(iter_solution.cost)
    #                                             output = "Number of Iterations: " + str(max_iterations) + " With Cost: " + str(iter_solution.cost) + \
    #                                                 " Starting pheromone: " + str(starting_pheromone) + " population: " + str(num_of_ants) +\
    #                                                     " alpha: " + str(alpha) + " beta: " + str(beta) + " is_online: " + str(is_online) + \
    #                                                         " evaporation rate: " + str(evaporation_rate) + " p_1: " + str(p_1) + " p_2: " + str(p_2) + \
    #                                                             " Q: " + str(Q_phero) + " Control parameter: " + str(control_parameter) +\
    #                                                                 " Path: " + str(iter_solution.visited)+ " Found at iteration: " + str(Colony_0.iter_found_best)+" Best Cost so far: " + str(best_cost) + "\n\r"
    #                                             print (output)
    #                                             f.write(output)
    #                                             if iter_solution.cost < best_cost:
    #                                                 best_cost = iter_solution.cost

    # f.close()

    # print (solutions)


    # plt.plot(iterations,solutions)
    
    # # for xy in zip(A, B):                                       # <--
    # #     ax.annotate('(%s, %s)' % xy, xy=xy, textcoords='data') # <--
    # plt.show()
    
    