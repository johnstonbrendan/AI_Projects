from conga import *
import time
import random
import math



def agent_smith (state, time_limit, max_depth):
    time_start = time.time()
    depth_explored = 0
    for i in range (1,max_depth + 1):
        best_move = depth_limited_search(state,i)
        depth_explored = i
        if time.time() - time_start > time_limit:
            break
    print ('Explored depth: ' + str(depth_explored))
    return best_move

def depth_limited_search (state,depth_limit):
    count_of_explored = 0
    depth = 0
    best_move = None
    best_cost = -math.inf
    explored = []
    alpha_0 = -math.inf
    beta_0 = math.inf
    cur_ind = 0
    root_node = Node(True,alpha_0,beta_0,cur_ind,0,state,0,False)
    to_explore = []     
    # now to look at a node
    explored.append(root_node)
    # print(root_node.child_moves)
    # explr_mv = root_node.child_moves.pop()
    # print (explored)
    # print (explr_mv)
    depth = depth + 1
    # current_node = Node (False,alpha,beta,cur_ind,
    #     current_node.cur_index,
    #     current_node.board.move(explr_mv[0][0],explr_mv[0][1],explr_mv[1]),depth,False)
    
    depth_1 = []
    index_1 = 0
    for child_1 in root_node.child_moves:
        if depth_limit == 1:
            count_of_explored = count_of_explored + 1
            node_1 = Node(False,alpha_0,beta_0,index_1,0,
            copy.deepcopy(root_node).board.move(child_1[0][0],child_1[0][1],child_1[1]),1,True)
            depth_1.append(Node(False,alpha_0,beta_0,index_1,0,
            copy.deepcopy(root_node).board.move(child_1[0][0],child_1[0][1],child_1[1]),1,True))
        else:
            alpha_1 = alpha_0
            beta_1 = beta_0
            depth_2 = []
            index_2 = 0
            node_1 = Node(False,alpha_0,beta_0,index_1,0,
            copy.deepcopy(root_node).board.move(child_1[0][0],child_1[0][1],child_1[1]),1,False)
            depth_1.append(node_1)
            for child_2 in node_1.child_moves:
                if node_1.value > beta_1:
                    break
                if depth_limit == 2:
                    count_of_explored = count_of_explored + 1
                    node_2 = Node(True,alpha_1,beta_1,index_2,index_1,
                        copy.deepcopy(node_1).board.move(child_2[0][0],child_2[0][1],child_2[1]),2,True)
                    depth_2.append(Node(True,alpha_1,beta_1,index_2,index_1,
                        copy.deepcopy(node_1).board.move(child_2[0][0],child_2[0][1],child_2[1]),2,True))
                else:
                    alpha_2 = alpha_1
                    beta_2 = beta_1
                    depth_3 = []
                    index_3 = 0
                    node_2 = Node(True,alpha_1,beta_1,index_2,index_1,
                    copy.deepcopy(node_1).board.move(child_2[0][0],child_2[0][1],child_2[1]),2,False)
                    depth_2.append(node_2)
                    for child_3 in node_2.child_moves:
                        if node_2.value < alpha_2:
                            break
                        if depth_limit == 3:
                            count_of_explored = count_of_explored + 1
                            node_3 = Node(False,alpha_2,beta_2,index_3,index_2,
                            copy.deepcopy(node_2).board.move(child_3[0][0],child_3[0][1],child_3[1]),3,True)
                        else:
                            print ("Don't have this many layers")
                            node_3 =  Node(False,alpha_2,beta_2,index_3,index_2,
                            copy.deepcopy(node_2).board.move(child_3[0][0],child_3[0][1],child_3[1]),3,False)
                        index_3 = index_3 + 1
                        if node_2.value > node_3.value:
                            node_2.value = node_3.value
                            beta_2 = node_2.value
                    # # THEN CHANGE THE VALUE EVERYTIME SOMETHING NEW IS ADDED SO YOU ARE CONSTANTLY CHECKING, TRY JUST FOR THIS LEVEL FIRST THEN PROPOGATE
                    # if depth_3.__len__() > 0:
                    #     node_2.value = min(depth_3,key = lambda x:x.value).value
                    # else:
                    #     node_2.value = 0
                index_2 = index_2 + 1
                if node_1.value < node_2.value:
                    node_1.value = node_2.value
                    alpha_1 = node_1.value
            # if depth_2.__len__() > 0:
            #     node_1.value = max(depth_2,key=lambda x:x.value).value
            # else:
            #     node_1.value = 0
        index_1 = index_1 + 1
        if root_node.value > node_1.value:
            root_node.value = node_1.value
            best_1 = node_1
            beta_0 = root_node.value
    # if depth_1.__len__() > 0:
    #     best_1 = min(depth_1,key = lambda x: x.value)
    # else:
    #     best_1 = None # this should never happane as the game should be over by this stage.
    # print (root_node.child_moves[depth_1[0].parent])
    print (count_of_explored)
    return root_node.child_moves[best_1.cur_index]







class Node:
    def __init__(self,is_min,init_alpha,init_beta,current_index,parent_index,board_state,depth,is_leaf):
        self.is_min = is_min
        self.alpha = init_alpha
        self.beta = init_beta
        self.cur_index = current_index
        self.parent = parent_index
        self.is_leaf = is_leaf
        self.board = Board(board_state) # Board(copy.deepcopy(board_state)) 
        # might need to add copy.deepcopy to board state, depends on how function is called
        self.depth = depth
        
        if self.is_leaf:
            self.value = self.board.generate_legal_moves('white').__len__()
        elif self.is_min: # want black to minimise number of moves for white
            self.value = math.inf
            self.child_moves = self.board.generate_legal_moves('black')
        else:
            self.value = -math.inf
            self.child_moves = self.board.generate_legal_moves('white')
        # print (self.value)


def random_agent_white (gameObj):
    avaliable_moves = gameObj._board.generate_legal_moves('white')
    if avaliable_moves.__len__() > 0:
        random_index = random.randint(1,avaliable_moves.__len__()) -1 #make it an index
        gameObj.move(avaliable_moves[random_index])

if __name__ == "__main__":
    cpu_level = 'hard' # options are 'hard' 'med' 'ez'
    game_mode = 'pvc' # options are 'pvp' 'pvc' 'cvc'
    theGame = Conga()
    theGame._agent_fun = agent_smith
    if cpu_level == 'hard':
        theGame._turn_timeout = 1
    elif cpu_level == 'med':
        theGame._turn_timeout = 0.02
    elif cpu_level == 'ez':
        theGame._turn_timeout = 0.001
    while theGame._running:
        theGame.loop()
        if game_mode == 'cvc':
            if theGame._turn == 'white': # this is the random agent
                random_agent_white(theGame)
            if theGame._turn == 'black':
                theGame.move(agent_smith(theGame._board.state,theGame._turn_timeout,3))
        elif game_mode == 'pvc':
            if theGame._turn == 'black':
                theGame.move(agent_smith(theGame._board.state,theGame._turn_timeout,3))


    theGame.on_cleanup() 