from tree import *
from solver import *
import copy
import matplotlib.pyplot as plt
import os
from datetime import datetime

class GP:
    def __init__(self,max_init_depth,population,bitstring_len,sep_percnt,p_m,max_iters,fitness_fun):
        self.max_depth = max_init_depth
        self.population = population
        self.bitstring_len = bitstring_len
        self.trees = self.init_trees()
        self.test_set = []
        self.init_test_set()
        self.sep_percnt = sep_percnt
        self.p_m = p_m
        self.max_iters = max_iters
        self.cur_iter = 0
        self.fitness_fun = fitness_fun
        self.best_tree = self.trees[0]
        self.calculate_fitness() # need to have the calculated fitnesses to get started, this will assign the best tree
        self.best_tree_list = []

    def init_test_set(self):
        binary_array = [None]*self.bitstring_len
        self.generate_binary_strings(binary_array,0)
    
    def generate_binary_strings(self,b_arr,i):
        if self.bitstring_len == i:
            self.test_set.append(copy.copy(b_arr))
            return
        b_arr[i] = 0
        self.generate_binary_strings(b_arr,i+1)
        b_arr[i] = 1
        self.generate_binary_strings(b_arr,i+1)


    def init_trees(self):
        number_of_full = self.population//2
        new_trees = [Tree('full',self.max_depth,self.bitstring_len)]
        for i in range(0,number_of_full - 1):
            ind_tree = Tree('full',self.max_depth,self.bitstring_len)
            new_trees.append(ind_tree)
        for i in range(0,self.population - number_of_full): # these are the number of grow trees
            new_trees.append(Tree('grow',self.max_depth,self.bitstring_len))

        return new_trees

    def crossover(self,tree1,tree2):
        # tree1 = Tree('full',self.max_depth,self.bitstring_len) # this is just for easier coding
        # tree2 = Tree('full',self.max_depth,self.bitstring_len)
        # cross_node_1 = Node('if',None,[])
        # cross_node_2 = Node('if',None,[])
        # copy_node = Node('if',None,[])

        # tree1 = copy.deepcopy(old_tree1)
        # tree2 = copy.deepcopy(old_tree2)
        total_nodes = tree1.num_of_nodes + tree2.num_of_nodes

        cross_node_1 = tree1.random_node()
        cross_node_2 = tree2.random_node()

        # copy_node = Node(cross_node_1.type,cross_node_1.parent,cross_node_1.children,cross_node_1.term_value)
        copy_node = Node(cross_node_1.type,None,cross_node_1.children,cross_node_1.term_value)
        cross_node_1.replace(cross_node_2)
        cross_node_2.replace(copy_node)

        tree2.num_of_nodes = total_nodes - tree1.recalc_num_nodes() # this beats recalculating twice

        return tree1,tree2

        # don't think i need the below code
        # if cross_node_1 != tree1.root and cross_node_2 != tree2.root: #normal replace
        #     copy_node = Node(cross_node_1.type,cross_node_1.parent,cross_node_1.children,cross_node_1.term_value)
        #     cross_node_1.replace(cross_node_2)
        #     cross_node_2.replace(copy_node)

        
        # elif cross_node_1 == tree1.root:
        #     if cross_node_2 != tree2.root: # if it is both the roots then do nothing
        #         tree1.root = cross_node_2
        #         cross_node_1
        # else:
        #     if cross_node_2 == tree2.root:
        #         if cross_node_1 != tree2.root

    def mutate(self,tree1):
        tree2 = Tree('full',self.max_depth,self.bitstring_len)
        # tree1 = copy.deepcopy(oldtree1)
        cross_node_1 = tree1.random_node()
        cross_node_1.replace(tree2.root)
        tree1.recalc_num_nodes()
        return tree1

    def generate_two_parent_trees(self):
        self.trees.sort(key=lambda tree: (tree.fitness,-tree.num_of_nodes),reverse=True)
        percentile_index = int((self.population - 1)*self.sep_percnt)

        if random.random() < 0.8: # this means use the top sep_percnt percentile
            selected_index = random.randint(0,percentile_index)
            parent_1 = self.trees[selected_index]
        else:
            selected_index = random.randint(percentile_index+1,self.population-1)
            parent_1 = self.trees[selected_index]
        parent_1_index = selected_index


        if random.random() < 0.8: # this means use the top sep_percnt percentile
            while(selected_index == parent_1_index):
                selected_index = random.randint(0,percentile_index) # this is so that we don't choose the sameone
            parent_2 = self.trees[selected_index]
        else:
            while (selected_index == parent_1_index):
                selected_index = random.randint(percentile_index+1,self.population-1)
            parent_2 = self.trees[selected_index]

        new_copy_parent_1 = copy.deepcopy(parent_1)
        new_copy_parent_2 = copy.deepcopy(parent_2)
        # new_copy_parent_1  = parent_1.tree_copy()
        # new_copy_parent_2 = parent_2.tree_copy()

        return new_copy_parent_1,new_copy_parent_2
        
    def loop(self):
        while(not(self.terminate())):
            new_trees = []
            while len(new_trees) < self.population:
                parent_1,parent_2 = self.generate_two_parent_trees()
                if random.random() < self.p_m: # This means mutate
                    inter_tree = self.mutate(parent_1) # intermediate tree
                    new_trees.append(inter_tree)
                else: # this means crossover
                    inter_tree1,inter_tree2 = self.crossover(parent_1,parent_2)
                    new_trees.append(inter_tree1)
                    new_trees.append(inter_tree2)
            self.best_tree_list.append(self.best_tree)

            self.trees = new_trees[:self.population] # this is because the new_tress may have 51
            self.calculate_fitness()
            print(f'Current iteration: {self.cur_iter} with fitness: {self.best_tree.fitness} , with number of nodes {self.best_tree.num_of_nodes}')
            self.cur_iter = self.cur_iter + 1
        
        return self.best_tree
        





    def terminate(self):
        if self.cur_iter > self.max_iters:
            return True
        else:
            return False

        

    def calculate_fitness(self): # fitness fun is the function used to assign fitness to a tree such as tree fitness
        for ind_tree in self.trees:
            calc_fitness = self.fitness_fun(ind_tree)
            if calc_fitness > self.best_tree.fitness:
                self.best_tree = copy.deepcopy(ind_tree)
            elif calc_fitness == self.best_tree.fitness and ind_tree.num_of_nodes < self.best_tree.num_of_nodes:
                self.best_tree = copy.deepcopy(ind_tree)
        return self.best_tree
            


class Six_Multi_GP(GP):
    def __init__(self,max_init_depth,population,sep_percnt,p_m,max_iterations):
        self.bitlength = 6
        self.node_limit = 20

        super().__init__(max_init_depth,population,self.bitlength,sep_percnt,p_m,max_iterations,self.tree_fitness)


    def tree_fitness(self,tree): # use full test set this is defined here because we want to change to use partial test for other GPs
        fitness = 0
        for test in self.test_set:
            if tree.evaluate(test) == solver(test):
                fitness = fitness + 1
        
        if tree.num_of_nodes > self.node_limit and fitness != len(self.test_set):
            fitness = fitness - (tree.num_of_nodes - self.node_limit)//100 

        tree.fitness = fitness

        return fitness

class El_Multi_GP(GP):
    def __init__(self,max_init_depth,population,sep_percnt,p_m,max_iterations):
        self.bitlength = 11
        self.node_limit = 500

        super().__init__(max_init_depth,population,self.bitlength,sep_percnt,p_m,max_iterations,self.tree_fitness)


    def tree_fitness(self,tree): # use full test set this is defined here because we want to change to use partial test for other GPs
        fitness = 0
        if self.cur_iter >= self.max_iters: # this means do full evaluation for the last iteration
            proportion = 1.0
        else:
            proportion = 1.0
        index = 0
        for test in self.test_set:
            if random.random() < proportion :
                if tree.evaluate(test) == solver(test):
                    fitness = fitness + 1
            index = index + 1
        
        if tree.num_of_nodes > self.node_limit and fitness != len(self.test_set):
            fitness = fitness - (tree.num_of_nodes - self.node_limit)//100 

        tree.fitness = fitness

        return fitness


class st_md_three_GP(GP):
    def __init__(self,max_init_depth,population,sep_percnt,p_m,max_iterations):
        self.bitlength = 16
        self.node_limit = 5000

        super().__init__(max_init_depth,population,self.bitlength,sep_percnt,p_m,max_iterations,self.tree_fitness)


    def tree_fitness(self,tree): # use full test set this is defined here because we want to change to use partial test for other GPs
        fitness = 0
        if self.cur_iter >= self.max_iters: # this means do full evaluation for the last iterations
            proportion = 1.0 # this means full evaluation at the end
        elif self.cur_iter >= self.max_iters//2:
            proportion = 0.1
        else:
            proportion = 0.05 
        index = 0
        for test in self.test_set:
            if random.random() < proportion :
                if tree.evaluate(test) == solver(test):
                    fitness = fitness + 1
            index = index + 1
        
        if tree.num_of_nodes > self.node_limit and fitness != len(self.test_set):
            fitness = fitness - (tree.num_of_nodes - self.node_limit)//100 

        tree.fitness = fitness

        return fitness
    










if __name__ == '__main__':
    # a = 11
    # print (a//2)
    # b = []
    # b.append('hello')
    # b.append('meme')
    # b[0]
    # print(b)

    # test_tree = Tree('full',10,6)
    # print('hello')
    # Six_Multi_0 = Six_Multi_GP(10,10,0.5,0.02,100)
    # print(Six_Multi_0.test_set)
    # solver_val = solver(Six_Multi_0.test_set[0])
    # print(f'Solver val {solver_val}')
    # tree_val = Six_Multi_0.trees[0].evaluate(Six_Multi_0.test_set[0])
    # print(f"tree val {tree_val}")
    # print('hello')

    # Six_Multi_Prog = Six_Multi_GP(10,10,0.5,0.02,100)
    # Six_Multi_Prog.crossover(Six_Multi_Prog.trees[0],Six_Multi_Prog.trees[1])
    # print('hello')
    
    # test = [1,0,3,5]
    # print(sorted(test,reverse=True))

    # print(test[:2])

    # --------------------- Below is main report code should change iterations though --------- #

    f = open(str(os.path.dirname(os.path.abspath(__file__)))+"\\test_results.txt","a")
    f.write("\n\r"+str(datetime.now())+"\n\r")

    iterations = 300
    six_Multi_Program = Six_Multi_GP(5,100,0.2,0.01,iterations)
    six_best_tree = six_Multi_Program.loop()
    six_fitness_progression = [tree.fitness for tree in six_Multi_Program.best_tree_list]
    six_num_nodes_progression = [tree.num_of_nodes for tree in six_Multi_Program.best_tree_list]
    final_pop_fitness_results = [tree.fitness for tree in six_Multi_Program.trees]
    print('6 Multiplexor Problem Results')
    f.write('6 Multiplexor Problem Results'+'\n\r')
    print('Six_Multi_GP(5,100,0.3,0.01,200)')
    f.write('Six_Multi_GP(5,100,0.3,0.01,200)'+'\n\r')
    print(f'Best tree string: {six_best_tree.stringify()}')
    f.write(f'Best tree string: {six_best_tree.stringify()}'+'\n\r')
    print(f'Best tree fitness: {six_best_tree.fitness}')
    f.write(f'Best tree fitness: {six_best_tree.fitness}'+'\n\r')

    f1 = plt.figure(1)
    plt.plot(six_fitness_progression,label='Fitness')
    # plt.plot(six_num_nodes_progression,label='Number of Nodes')
    # plt.legend()
    plt.title('Six Multiplexor Problem')


    iterations = 400
    el_Multi_Program = El_Multi_GP(9,200,0.3,0.1,iterations)
    el_best_tree = el_Multi_Program.loop()
    el_fitness_progression = [tree.fitness for tree in el_Multi_Program.best_tree_list]
    el_num_nodes_progression = [tree.num_of_nodes for tree in el_Multi_Program.best_tree_list]
    print('11 Multiplexor Problem Results')
    f.write('11 Multiplexor Problem Results'+'\n\r')
    print('El_Multi_GP(9,200,0.3,0.1,400)')
    f.write('El_Multi_GP(9,200,0.3,0.1,400)'+'\n\r')
    print(f'Best tree string: {el_best_tree.stringify()}')
    f.write(f'Best tree string: {el_best_tree.stringify()}'+'\n\r')
    print(f'Best tree fitness: {el_best_tree.fitness}')
    f.write(f'Best tree fitness: {el_best_tree.fitness}'+'\n\r')

    f2 = plt.figure(2)
    plt.plot(el_fitness_progression,label='Fitness')
    # plt.plot(el_num_nodes_progression,label='Number of Nodes')
    # plt.legend()
    plt.title('Eleven Multiplexor Problem')

    iterations = 400
    el_Multi_Program = El_Multi_GP(9,200,0.2,0.05,iterations)
    el_best_tree = el_Multi_Program.loop()
    el_fitness_progression = [tree.fitness for tree in el_Multi_Program.best_tree_list]
    el_num_nodes_progression = [tree.num_of_nodes for tree in el_Multi_Program.best_tree_list]
    print('11 Multiplexor Problem Results')
    f.write('11 Multiplexor Problem Results'+'\n\r')
    print('El_Multi_GP(9,200,0.2,0.05,400)')
    f.write('El_Multi_GP(9,200,0.2,0.05,400)'+'\n\r')
    print(f'Best tree string: {el_best_tree.stringify()}')
    f.write(f'Best tree string: {el_best_tree.stringify()}'+'\n\r')
    print(f'Best tree fitness: {el_best_tree.fitness}')
    f.write(f'Best tree fitness: {el_best_tree.fitness}'+'\n\r')

    f2 = plt.figure(4)
    plt.plot(el_fitness_progression,label='Fitness')
    # plt.plot(el_num_nodes_progression,label='Number of Nodes')
    # plt.legend()
    plt.title('Eleven Multiplexor Problem')
    

    # iterations = 100
    # st_md_three_program = st_md_three_GP(9,100,0.35,0.01,iterations)
    # try:
    #     st_md_best_tree = st_md_three_program.loop()
    # except:
    #     print ("Couldn't FInish st_md_three")
    # st_md_fitness_progression = [tree.fitness for tree in st_md_three_program.best_tree_list]
    # st_md_nodes_progression = [tree.num_of_nodes for tree in st_md_three_program.best_tree_list]
    # print('st_md_three_GP(9,100,0.35,0.01,150)')
    # f.write('st_md_three_GP(9,100,0.35,0.01,150)'+'\n\r')
    # print('16 Middle 3 Problem Results')
    # f.write('16 Middle 3 Problem Results'+'\n\r')
    # print(f'Best tree string: {st_md_best_tree.stringify()}')
    # f.write(f'Best tree string: {st_md_best_tree.stringify()}'+'\n\r')
    # print(f'Best tree fitness: {st_md_best_tree.fitness}')
    # f.write(f'Best tree fitness: {st_md_best_tree.fitness}'+'\n\r')

    # f.close()

    # f3 = plt.figure(3)
    # plt.plot(st_md_fitness_progression,label='Fitness')
    # # plt.plot(st_md_nodes_progression,label='Number of Nodes')
    # # plt.legend()
    # plt.title('Sixteen Middle 3 Problem')

    plt.show()


