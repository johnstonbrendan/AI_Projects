from pygame.locals import *
import pygame
import sys
import os
import copy

class Board:
    state = [[(0) for i in range(4)] for j in range(4)] # 0 is neutral
    boardSize = 625
    tileSize = boardSize//4
    lineColor = (0,0,128)
    lineSize = 9

    def __init__(self,board_state):
        self.state = board_state

    def reset(self):
        self.state = [[(0) for i in range(4)] for j in range(4)] # 0 is neutral
        self.state[0][0] = (10) # positive is black
        self.state[3][3] = (-10) # negative is white

    def draw(self,display_surf,font):
        bx = 0
        by = 0
        for column in self.state:
            bx = 0
            for tile in column:
                black_number_surface = font.render(str(tile),False,(255,255,255))
                white_number_surface = font.render(str(-tile),False,(0,0,0))
                yellow_number_surface = font.render(str(tile),False,(0,0,128))
               # print ("Index: %d,%d Value: %d",bx,by,tile)
                if tile > 0: # black
                    display_surf.fill((0,0,0),
                    (by*self.tileSize,bx*self.tileSize,
                    (by+1)*self.tileSize,(bx+1)*self.tileSize))
                    display_surf.blit(black_number_surface,(by*self.tileSize,bx*self.tileSize))
                elif tile < 0: # white
                    display_surf.fill((255,255,255),
                    (by*self.tileSize,bx*self.tileSize,
                    (by+1)*self.tileSize,(bx+1)*self.tileSize))
                    display_surf.blit(white_number_surface,(by*self.tileSize,bx*self.tileSize))
                else: # neutral
                    display_surf.fill((255,255,0),
                    (by*self.tileSize,bx*self.tileSize,
                    (by+1)*self.tileSize,(bx+1)*self.tileSize))
                    # display_surf.blit(yellow_number_surface,(by*self.tileSize,bx*self.tileSize))
                bx = bx + 1
            by = by + 1
        
        for i in range(1,4):
            # Vertical line
            pygame.draw.line(display_surf, self.lineColor, 
            (i*self.tileSize,0),(i*self.tileSize,self.boardSize),self.lineSize)
            # Horizontal line
            pygame.draw.line(display_surf, self.lineColor, 
         (0,i*self.tileSize),(self.boardSize,i*self.tileSize),self.lineSize)
    
    
    def generate_legal_moves(self,color):
        positions = []
        legal_moves = []
        ind_x = 0
        ind_y = 0
        # Find the current black positions
        for column in self.state:
            ind_y = 0
            for stones in column:
                if color == 'black':
                    if stones > 0: # meaning black stones
                        positions.append((ind_x,ind_y))
                elif color == 'white':
                    if stones < 0: # meaning white sones
                        positions.append((ind_x,ind_y))
                ind_y = ind_y + 1
            ind_x = ind_x + 1

        # Find possible moves for each position
        for position in positions:
            # Check left
            if self.is_legal(self.state,position[0]-1,position[1],color):
                legal_moves.append((position,'left'))
                # legal_moves.append((position[0]-1,position[1]))
            # Check up-left
            if self.is_legal(self.state,position[0]-1,position[1]-1,color):
                legal_moves.append((position,'up-left'))
                # legal_moves.append((position[0]-1,position[1]-1))
            # Check up
            if self.is_legal(self.state,position[0],position[1]-1,color):
                legal_moves.append((position,'up'))
                # legal_moves.append((position[0],position[1]-1))
            # Check up-right
            if self.is_legal(self.state,position[0]+1,position[1]-1,color):
                legal_moves.append((position,'up-right'))
                # legal_moves.append((position[0]+1,position[1]-1))
            # Check right
            if self.is_legal(self.state,position[0]+1,position[1],color):
                legal_moves.append((position,'right'))
                # legal_moves.append((position[0]+1,position[1]))
            # Check down-right
            if self.is_legal(self.state,position[0]+1,position[1]+1,color):
                legal_moves.append((position,'down-right'))
                # legal_moves.append((position[0]+1,position[1]+1))
            # Check down
            if self.is_legal(self.state,position[0],position[1]+1,color):
                legal_moves.append((position,'down'))
                # legal_moves.append((position[0],position[1]+1))
            # Check down-left
            if self.is_legal(self.state,position[0]-1,position[1]+1,color):
                legal_moves.append((position,'down-left'))
                # legal_moves.append((position[0]-1,position[1]+1))

                
        return legal_moves

    def is_legal(self,board_state,ind_x,ind_y,color):
        # may need to change this later to not have board_state as a parameter
        if ind_x > 3 or ind_x < 0:
            return False
        if ind_y >3 or ind_y < 0:
            return False
        if color == 'black':
            if board_state[ind_x][ind_y] >= 0:
                return True
            else:
                return False
        elif color == 'white':
            if board_state[ind_x][ind_y] <= 0:
                return True
            else:
                return False
        else:
            for i in range(0,10):
                print ("Didn't give correct color to is legel function")
                pygame.quit()

    def move(self,ind_x,ind_y,direction):
        color = ''
        drop_amount = 0
        if self.state[ind_x][ind_y] > 0:
            color = 'black'
            drop_amount = 1

        elif self.state[ind_x][ind_y] < 0:
            color = 'white'
            drop_amount = -1
        else:
            return False # you can't move this square
        if direction == 'up':
            handful = self.state[ind_x][ind_y]
            self.state[ind_x][ind_y] = 0
            drop_x = ind_x
            drop_y = ind_y - 1 #for the up position
            while handful != 0:
                if self.is_legal(self.state,drop_x,drop_y,color):
                    if abs(handful) - abs(drop_amount) >= 0:
                        self.state[drop_x][drop_y] = self.state[drop_x][drop_y] + drop_amount
                        handful = handful - drop_amount
                        drop_amount = drop_amount + (1 * drop_amount//abs(drop_amount))
                        drop_y = drop_y - 1 # check the next spot
                    else: # when the drop amount will empty the handful
                        self.state[drop_x][drop_y] = self.state[drop_x][drop_y] + handful
                        handful = 0
                else: # drop_y + 1 is the previous spot
                    self.state[drop_x][drop_y + 1] = self.state[drop_x][drop_y + 1] + handful
                    handful = 0
        elif direction == 'up-left':
            handful = self.state[ind_x][ind_y]
            self.state[ind_x][ind_y] = 0
            drop_x = ind_x - 1 #for the up-left position
            drop_y = ind_y - 1
            while handful != 0:
                if self.is_legal(self.state,drop_x,drop_y,color):
                    if abs(handful) - abs(drop_amount) >= 0:
                        self.state[drop_x][drop_y] = self.state[drop_x][drop_y] + drop_amount
                        handful = handful - drop_amount
                        drop_amount = drop_amount + (1 * drop_amount//abs(drop_amount))
                        drop_x = drop_x - 1 # check the next spot
                        drop_y = drop_y - 1
                    else: # when the drop amount will empty the handful
                        self.state[drop_x][drop_y] = self.state[drop_x][drop_y] + handful
                        handful = 0
                else: # drop_x + 1 and drop_y + 1 is the previous spot
                    self.state[drop_x + 1][drop_y + 1] = self.state[drop_x + 1][drop_y + 1] + handful
                    handful = 0
        elif direction == 'left':
            handful = self.state[ind_x][ind_y]
            self.state[ind_x][ind_y] = 0
            drop_x = ind_x - 1 #for the left position
            drop_y = ind_y 
            while handful != 0:
                if self.is_legal(self.state,drop_x,drop_y,color):
                    if abs(handful) - abs(drop_amount) >= 0:
                        self.state[drop_x][drop_y] = self.state[drop_x][drop_y] + drop_amount
                        handful = handful - drop_amount
                        drop_amount = drop_amount + (1 * drop_amount//abs(drop_amount))
                        drop_x = drop_x - 1 # check the next spot
                    else: # when the drop amount will empty the handful
                        self.state[drop_x][drop_y] = self.state[drop_x][drop_y] + handful
                        handful = 0
                else: # drop_x + 1 is the previous spot
                    self.state[drop_x + 1][drop_y] = self.state[drop_x + 1][drop_y] + handful
                    handful = 0
        elif direction == 'down-left':
            handful = self.state[ind_x][ind_y]
            self.state[ind_x][ind_y] = 0
            drop_x = ind_x - 1 # for the down-left position
            drop_y = ind_y + 1
            while handful != 0:
                if self.is_legal(self.state,drop_x,drop_y,color):
                    if abs(handful) - abs(drop_amount) >= 0:
                        self.state[drop_x][drop_y] = self.state[drop_x][drop_y] + drop_amount
                        handful = handful - drop_amount
                        drop_amount = drop_amount + (1 * drop_amount//abs(drop_amount))
                        drop_x = drop_x - 1 # check the next spot
                        drop_y = drop_y + 1
                    else: # when the drop amount will empty the handful
                        self.state[drop_x][drop_y] = self.state[drop_x][drop_y] + handful
                        handful = 0
                else: # drop_x + 1 and drop_y -1 is the previous spot
                    self.state[drop_x + 1][drop_y - 1] = self.state[drop_x + 1][drop_y - 1] + handful
                    handful = 0
        elif direction == 'down':
            handful = self.state[ind_x][ind_y]
            self.state[ind_x][ind_y] = 0
            drop_x = ind_x
            drop_y = ind_y + 1 # for the down position
            while handful != 0:
                if self.is_legal(self.state,drop_x,drop_y,color):
                    if abs(handful) - abs(drop_amount) >= 0:
                        self.state[drop_x][drop_y] = self.state[drop_x][drop_y] + drop_amount
                        handful = handful - drop_amount
                        drop_amount = drop_amount + (1 * drop_amount//abs(drop_amount))
                        drop_x = drop_x
                        drop_y = drop_y + 1 # check the next spot
                    else: # when the drop amount will empty the handful
                        self.state[drop_x][drop_y] = self.state[drop_x][drop_y] + handful
                        handful = 0
                else: #  drop_y -1 is the previous spot
                    self.state[drop_x][drop_y - 1] = self.state[drop_x][drop_y - 1] + handful
                    handful = 0
        elif direction == 'down-right':
            handful = self.state[ind_x][ind_y]
            self.state[ind_x][ind_y] = 0
            drop_x = ind_x + 1 #for the down-right position
            drop_y = ind_y + 1
            while handful != 0:
                if self.is_legal(self.state,drop_x,drop_y,color):
                    if abs(handful) - abs(drop_amount) >= 0:
                        self.state[drop_x][drop_y] = self.state[drop_x][drop_y] + drop_amount
                        handful = handful - drop_amount
                        drop_amount = drop_amount + (1 * drop_amount//abs(drop_amount))
                        drop_x = drop_x + 1 # check the next spot
                        drop_y = drop_y + 1
                    else: # when the drop amount will empty the handful
                        self.state[drop_x][drop_y] = self.state[drop_x][drop_y] + handful
                        handful = 0
                else: # drop_x - 1 and drop_y -1 is the previous spot
                    self.state[drop_x - 1][drop_y - 1] = self.state[drop_x - 1][drop_y - 1] + handful
                    handful = 0
        elif direction == 'right':
            handful = self.state[ind_x][ind_y]
            self.state[ind_x][ind_y] = 0
            drop_x = ind_x + 1 #for the right position
            drop_y = ind_y
            while handful != 0:
                if self.is_legal(self.state,drop_x,drop_y,color):
                    if abs(handful) - abs(drop_amount) >= 0:
                        self.state[drop_x][drop_y] = self.state[drop_x][drop_y] + drop_amount
                        handful = handful - drop_amount
                        drop_amount = drop_amount + (1 * drop_amount//abs(drop_amount))
                        drop_x = drop_x + 1 # check the next spot
                        drop_y = drop_y
                    else: # when the drop amount will empty the handful
                        self.state[drop_x][drop_y] = self.state[drop_x][drop_y] + handful
                        handful = 0
                else: # drop_x - 1 is the previous spot
                    self.state[drop_x - 1][drop_y] = self.state[drop_x - 1][drop_y] + handful
                    handful = 0
        elif direction == 'up-right':
            handful = self.state[ind_x][ind_y]
            self.state[ind_x][ind_y] = 0
            drop_x = ind_x + 1 #for the up-right position
            drop_y = ind_y - 1
            while handful != 0:
                if self.is_legal(self.state,drop_x,drop_y,color):
                    if abs(handful) - abs(drop_amount) >= 0:
                        self.state[drop_x][drop_y] = self.state[drop_x][drop_y] + drop_amount
                        handful = handful - drop_amount
                        drop_amount = drop_amount + (1 * drop_amount//abs(drop_amount))
                        drop_x = drop_x + 1 # check the next spot
                        drop_y = drop_y - 1
                    else: # when the drop amount will empty the handful
                        self.state[drop_x][drop_y] = self.state[drop_x][drop_y] + handful
                        handful = 0
                else: # drop_x - 1 and drop_y + 1 is the previous spot
                    self.state[drop_x - 1][drop_y + 1] = self.state[drop_x - 1][drop_y + 1] + handful
                    handful = 0
        return self.state

    def valid_board(self):
        sum = 0
        for columns in self.state:
            for j in columns:
                sum = sum + j
        if sum == 0:
            return True
        else:
            return False

    def game_over(self):
        if self.generate_legal_moves('black').__len__() == 0:
            # print ('white won')
            return 2
        elif self.generate_legal_moves('white').__len__() == 0:
            # print ('black won')
            return 1
        else:
            return 0

            



class Conga:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._mode = None
        self._board_state = [[(0) for i in range(4)] for j in range(4)] # 0 is neutral        
        self._board_state[0][0] = 10 # positive is black
        self._board_state[3][3] = -10 # negative is white
        self._prev_state = copy.deepcopy(self._board_state)
        self._undo_state = copy.deepcopy(self._board_state)
        self._dundo_state = copy.deepcopy(self._board_state)
        self._turn = 'black'
        self._selected = (0,0)
        self._turn_timeout = 1
        self._turn_count = 0
        # # below is for testing
        # self._board_state[0][0] = 0 
        # self._board_state[3][3] = 33
        # self._board_state[0][1] = 1
        # self._board_state[0][2] = 2
        # self._board_state[0][3] = 3
        # self._board_state[1][0] = 10
        # self._board_state[1][1] = 11
        # self._board_state[1][2] = 12
        # self._board_state[1][3] = 13
        # self._board_state[2][0] = 20
        # self._board_state[2][1] = 21
        # self._board_state[2][2] = 22
        # self._board_state[2][3] = 23
        # self._board_state[3][0] = 30
        # self._board_state[3][1] = 31
        # self._board_state[3][2] = 32
        # self._board_state[3][3] = 33

        self._board = Board(self._board_state)
        self._previous_board = Board(self._prev_state)
        self._undo_board = Board(self._undo_state)
        self._dundo_board = Board(self._dundo_state) # this is the double undo board for playing against computer


        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Tahoma', self._board.boardSize // 4 - self._board.boardSize// 16)

        self._display_surf = pygame.display.set_mode(
            (self._board.boardSize,self._board.boardSize),pygame.HWSURFACE)
        pygame.display.set_caption('Conga Game')

    def on_cleanup(self):
        pygame.quit()
        
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self._board.draw(self._display_surf,self.font)
        pygame.display.flip()     

    def mouse_to_board(self,x,y):
        board_x = -1
        board_y = -1
        board_x = x*4 // self._board.boardSize
        board_y = y*4 // self._board.boardSize
        return (board_x,board_y)
        # print ("Mouse x,y: " + str(x) + "," + str(y))
        # print("Board x,y: " + str(board_x) + "," + str(board_y) + "\n")

    def save_previous_change_turn(self):
        if (self._board.state != self._previous_board.state):
            self._dundo_board.state = copy.deepcopy(self._undo_board.state)
            self._undo_board.state = copy.deepcopy(self._previous_board.state)
            self._previous_board.state = copy.deepcopy(self._board.state)
            self.toggle_turn()
            return True # show that a change was made
        else:
            return False # show that no change was made

    def toggle_turn(self):
        if self._turn == 'black':
            self._turn = 'white'
        else:
            self._turn = 'black'
        self._turn_count = self._turn_count + 1


    def move (self,decision): # decision [0][0] is x pos decision[0][1] is y pos decision [1] is direction
        end_state = None
        if self._turn == 'black' and self._board.state[decision[0][0]][decision[0][1]] > 0:
            end_state = self._board.move(decision[0][0],decision[0][1],decision[1])
        elif self._turn == 'white' and self._board.state[decision[0][0]][decision[0][1]] < 0:
            end_state = self._board.move(decision[0][0],decision[0][1],decision[1])
        self.save_previous_change_turn()
        return end_state

    def loop(self):
        # pygame.event.pump()
        # keys = pygame.key.get_pressed()
        # keys = [(0) for i in range(1000)]
        # print (self._selected) # for testing
        for event in pygame.event.get():
            if event.type is pygame.MOUSEBUTTONDOWN:
                (mouse_x, mouse_y) = pygame.mouse.get_pos()
                self._selected = self.mouse_to_board(mouse_x,mouse_y)
                print (self._selected) # for testing
                print (self._turn)
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._running = False
                if event.key == pygame.K_w:
                    self.move((self._selected,'up'))
                if event.key == pygame.K_e:
                    self.move((self._selected,'up-right'))
                if event.key == pygame.K_d:
                    self.move((self._selected,'right'))
                if event.key == pygame.K_c:
                    self.move((self._selected,'down-right'))
                if event.key == pygame.K_x:
                    self.move((self._selected,'down'))
                if event.key == pygame.K_z:
                    self.move((self._selected,'down-left'))
                if event.key == pygame.K_a:
                    self.move((self._selected,'left'))
                if event.key == pygame.K_q:
                    self.move((self._selected,'up-left'))
                if event.key == pygame.K_u:
                    self._board.state = copy.deepcopy(self._undo_board.state)
                    self.save_previous_change_turn()
                if event.key == pygame.K_i:
                    self._board.state = copy.deepcopy(self._dundo_board.state)
                    if self.save_previous_change_turn():
                        self.toggle_turn() # need to add an extra toggle as this is double undo
                        # if you are running double undo after just one move the board will reset with the starting player now swapped
                        # this feature isn't that stable right now
                if event.key == pygame.K_SPACE:
                    avaliable = self._board.generate_legal_moves('black')
                    message =  "Black Count: " + str(avaliable.__len__()) + ", Moves: " + str(avaliable)
                    print (message)
                    avaliable = self._board.generate_legal_moves('white')
                    message =  "White Count: " + str(avaliable.__len__()) + ", Moves: " + str(avaliable)
                    print (message)

                if event.key == pygame.K_b:
                    self._agent_fun(self._board.state,self._turn_timeout)

                # if event.key == pygame.K_f:
                #     if self._turn.__contains__('freeze'):
                #         self._turn = self._turn.replace('freeze','')
                #     else:
                #         self._turn = self._turn + 'freeze'
        
        if self._board.valid_board() == False:
            self._turn = 'freeze'
            print ('error in board')
        
        if self._board.game_over() != 0:
            if self._turn != 'game over':
                if self._board.game_over() == 1:
                    print ('Black won in ' + str(self._turn_count) + ' moves') #check why this isn't working
                    self._turn = 'game over'
                elif self._board.game_over() == 2:
                    print ('White won in ' + str(self._turn_count) + ' moves') #check why this isn't working
                    self._turn = 'game over'
                
        self.on_render()    






        # if (keys[K_ESCAPE]):
        #     self._running = False
        
        # if (keys[K_SPACE]):
        #     avaliable = self._board.generate_legal_moves(self._board.state)
        #     message =  "Count: " + str(avaliable.__len__()) + ", Moves: " + str(avaliable)
        #     print (message)

        # if (keys[K_1]): # test case 1
        #     test_board =[[(0) for i in range(4)] for j in range(4)] # 0 is neutral
        #     test_board[0][0] = 10
        #     test_board[0][1] = -5
        #     test_board[1][1] = -5
        #     self._board = Board(test_board)

        # if (keys[K_2]): # test case 2
        #     test_board =[[(0) for i in range(4)] for j in range(4)] # 0 is neutral
        #     test_board[0][1] = 5
        #     test_board[1][1] = 5
        #     test_board[1][0] = -1
        #     test_board[2][0] = -2
        #     test_board[3][0] = -7

        #     self._board = Board(test_board)

        # if (keys[K_3]): # test case 3
        #     test_board =[[(0) for i in range(4)] for j in range(4)] # 0 is neutral
        #     test_board[1][1] = 10

        #     self._board = Board(test_board)

        # if (keys[K_4]): # test case 4
        #     test_board =[[(0) for i in range(4)] for j in range(4)] # 0 is neutral
        #     test_board[1][1] = -10

        #     self._board = Board(test_board)
            
            

        # if (keys[K_0]):
        #     self._board.reset()

        # if (keys[K_w]):
        #     self._board.move(1,1,'up')
        # if (keys[K_e]):
        #     self._board.move(1,1,'up-right')
        # if (keys[K_d]):
        #     self._board.move(1,1,'right')
        # if (keys[K_c]):
        #     self._board.move(1,1,'down-right')
        # if (keys[K_x]):
        #     self._board.move(1,1,'down')
        # if (keys[K_z]):
        #     self._board.move(1,1,'down-left')
        # if (keys[K_a]):
        #     self._board.move(1,1,'left')
        # if (keys[K_q]):
        #     self._board.move(1,1,'up-left')


        # if (keys[K_p]):
        #     self._board.state[3][3] = self._board.state[3][3] + 10

    def _agent_fun(self,state,timelimit):
        print ("normal function which needs to be overwritten")







if __name__ == "__main__":
    theGame = Conga()
    while theGame._running:
        theGame.loop()
    
    theGame.on_cleanup() 