import random
import copy

class Node:
    def __init__(self,node_type,parent_node,child_nodes,term_value = -1):
        self.type = node_type
        # self.parent = parent_node
        self.children = child_nodes
        # If it is a terminal value this will first be initialised to be the index of the bitstream
        self.term_value = term_value 
        self.validate_init()
        self.assign_req_children()


    def validate_init(self):
        if self.type != 'and' and self.type != 'or' and self.type != 'not'\
            and self.type != 'if' and self.type != 'term':
            raise 'Invalid Node Type'

    def assign_req_children(self):
        if self.type == 'if':
            self.req_children = 3
        elif self.type == 'not':
            self.req_children = 1
        elif self.type == 'term':
            self.req_children = 0
        else:
            self.req_children = 2
            

    def evaluate(self,bitstring): # this will be recursive kinda
        if self.type == 'and':
            return self.children[0].evaluate(bitstring) & self.children[1].evaluate(bitstring)

        elif self.type == 'or':
            return self.children[0].evaluate(bitstring) | self.children[1].evaluate(bitstring)


        elif self.type == 'not':
            return self.children[0].evaluate(bitstring) ^ 1


        elif self.type == 'if':
            if self.children[0].evaluate(bitstring):
                return self.children[1].evaluate(bitstring)
            else:
                return self.children[2].evaluate(bitstring)

        else: # means is terminal
            return bitstring[self.term_value]

    def stringify(self): # this will be recursive kinda
        if self.type == 'and':
            return '(' + self.children[0].stringify() +' and '+ self.children[1].stringify() + ')'

        elif self.type == 'or':
            return '('+self.children[0].stringify() +' or '+ self.children[1].stringify()+')'


        elif self.type == 'not':
            return 'not (' + self.children[0].stringify() + ')'


        elif self.type == 'if':
            return 'if (' + self.children[0].stringify() + '): (' + self.children[1].stringify() + ')' + ' else: (' + self.children[2].stringify() + ')'
            if self.children[0].stringify():
                return self.children[1].stringify()
            else:
                return self.children[2].stringify()

        else: # means is terminal
            return 'bitstring[' + str(self.term_value) + ']'

    def replace(self,node_to_replace): # this will replace the current node with another but keep the parents
        self.type = copy.copy(node_to_replace.type)
        self.children = copy.copy(node_to_replace.children)
        self.term_value = copy.copy(node_to_replace.term_value)

    # def copy_node(self):
    #     copy_type = copy.copy(self.type)
    #     copy_children = copy.copy(self.children)
    #     copy_term_value = copy.copy(self.term_value)
    #     copy_parent = copy.copy(self.parent)
    #     copy_node = Node(copy_type,copy_parent,copy_children,copy_term_value)
    #     return copy_node



def generate_random_tree_full(max_depth,bitstring_length):
        options = ['and','or','not','if'] # didn't include 'term as it is the full function'
        depth = 0
        def crt_option(option_values):
            return option_values[random.randint(0,len(option_values)-1)]
        select_option = crt_option(options)
        root = Node(select_option,None,[])
        cur_depth_nodes = [root]
        num_of_nodes = 1
        for i in range (1,max_depth):
            next_depth_nodes = []
            for node in cur_depth_nodes:
                for j in range(0,node.req_children):
                    new_child = Node(crt_option(options),node,[])
                    node.children.append(new_child)
                    next_depth_nodes.append(new_child)
                    num_of_nodes = num_of_nodes + 1
            cur_depth_nodes = next_depth_nodes
            
        for node in cur_depth_nodes:
            for j in range(0,node.req_children):
                    new_child = Node('term',node,[],random.randint(0,bitstring_length-1))
                    node.children.append(new_child)
                    num_of_nodes = num_of_nodes + 1
        
        return root,num_of_nodes
                

def generate_random_tree_grow(max_depth,bitstring_length):
    options = ['and','or','not','if'] # add term later
    depth = 0
    def crt_option(option_values):
        return option_values[random.randint(0,len(option_values)-1)]
    select_option = crt_option(options)
    options.append('term') # did this here so that the root wouldn't be a term
    root = Node(select_option,None,[])
    cur_depth_nodes = [root]
    num_of_nodes = 1
    for i in range (1,max_depth):
        next_depth_nodes = []
        for node in cur_depth_nodes:
            for j in range(0,node.req_children):
                if i == max_depth - 1:
                    new_option = 'term'
                else:
                    new_option = crt_option(options)
                if (new_option == 'term'):
                    new_child = Node(new_option,node,[],random.randint(0,bitstring_length-1))
                else:
                    new_child = Node(new_option,node,[])
                node.children.append(new_child)
                next_depth_nodes.append(new_child)
                num_of_nodes = num_of_nodes + 1
        cur_depth_nodes = next_depth_nodes

    return root,num_of_nodes

class Tree:
    def __init__(self,tree_gen_type,max_depth,bitstring_length):
        self.num_of_nodes = 0 # we need number of nodes as it makes generating a random selection easier
        # make sure when using num_of_nodes probability to subtract by one to not include root
        self.root = Node('if',None,[]) # this is just for now will get replaced below
        self.fitness = 0
        if tree_gen_type == 'full': # this is how the initial tree is generated
            self.root,self.num_of_nodes = generate_random_tree_full(max_depth,bitstring_length)
        elif tree_gen_type == 'grow': # gen type is grow
            self.root,self.num_of_nodes = generate_random_tree_grow(max_depth,bitstring_length)
    
    def evaluate(self,bitstring):
        # self.assign_term_values(bitstring)
        return self.root.evaluate(bitstring)

    def stringify(self):
        return self.root.stringify()

    def random_node(self):
        select = random.randint(0,self.num_of_nodes - 1)
        to_check = copy.copy([self.root])
        selected = self.root
        for i in range(0,select):
            selected = to_check.pop(0)
            to_check.extend(selected.children)
        return selected

    def recalc_num_nodes(self):
        total = 1
        to_check = copy.copy(self.root.children)
        while len(to_check) > 0:
            child = to_check.pop(0)
            to_check.extend(child.children)
            total = total + 1
        self.num_of_nodes = total
        return total

    # def tree_copy(self):
    #     new_tree = Tree('donothing',0,0) # this is a pointless tree
    #     new_tree.root = self.root.copy_node()
    #     # new_node = 
    #     # THEN NEED TO DO THIS COPY NODE THING FOR ALL THE NODES IN THE TREE AS i THINK DEEP COPY IS ALSO COPYTING PARAENTS

    #     new_tree.num_of_nodes = copy.copy(self.num_of_nodes)
    #     new_tree.fitness = copy.copy(self.fitness)

    #     return new_tree


    # def assign_term_values(self,bitstring):
    #     to_check = copy.copy(self.root.children)
    #     while len(to_check) > 0:
    #         child = to_check.pop(0)
    #         if child.type == 'term':
    #             child.term_value = bitstring[child.term_value]
    #         to_check.extend(child.children)


        




if __name__ == '__main__':
    tree1 = Tree('full',2,6)
    for i in range (0,1000):
        tree1.random_node()
    print(tree1.evaluate([0,1,0,1,1,1]))
    print("Hello")
    test = 1
    print(test^1)
    print(tree1.num_of_nodes)
    print(tree1.recalc_num_nodes())
    # print(tree1.stringify())
    bitstring = [0,1,0,1,1,1]
    # string = 'if True: (True and not(1))'
    # print(eval(string))
    print(f'Bitstring: {bitstring}')
    print(f'Stringify: {tree1.stringify()}')
    print(f'Evaluation: {tree1.evaluate(bitstring)}')




