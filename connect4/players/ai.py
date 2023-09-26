from os import stat
import random
from tempfile import TemporaryDirectory
import numpy as np
from typing import List, Tuple, Dict
from connect4.utils import get_pts, get_valid_actions, Integer


class AIPlayer:
    def __init__(self, player_number: int, time: int):
        """
        :param player_number: Current player number
        :param time: Time per move (seconds)
        """
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.time = time
        # Do the rest of your implementation here


    def update_board(self,state: Tuple[np.array, Dict[int, Integer]], column: int, player_num: int, is_popout: bool = False):
        board, num_popouts = state
        if not is_popout:
            if 0 in board[:, column]:
                for row in range(1, board.shape[0]):
                    update_row = -1
                    if board[row, column] > 0 and board[row - 1, column] == 0:
                        update_row = row - 1
                    elif row == board.shape[0] - 1 and board[row, column] == 0:
                        update_row = row
                    if update_row >= 0:
                        board[update_row, column] = player_num
                        #self.c.itemconfig(self.gui_board[column][update_row], fill=self.colors[self.current_turn + 1])
                        break
            else:
                err = 'Invalid move by player {}. Column {}'.format(player_num, column, is_popout)
                raise Exception(err)
        else:
            if 1 in board[:, column] or 2 in board[:, column]:
                for r in range(board.shape[0] - 1, 0, -1):
                    board[r, column] = board[r - 1, column]
                    #self.c.itemconfig(self.gui_board[column][r], fill=self.colors[
                       # board[r, column]])  # this needs to be tweaked
                board[0, column] = 0
                #self.c.itemconfig(self.gui_board[column][0], fill=self.colors[0])
            else:
                err = 'Invalid move by player {}. Column {}'.format(player_num, column)
                raise Exception(err)
            num_popouts[player_num].decrement()
        return board,num_popouts
    
    def MiniMax(self,state: Tuple[np.array, Dict[int, Integer]],depth: int ,a,b, max_player : bool):
        
        other_pl=0
        if self.player_number==1:
            other_pl=2
        else:
            other_pl=1
        our_valid_actions = get_valid_actions(self.player_number, state)
        opp_valid_actions=get_valid_actions(other_pl,state)
        
        if depth==0 or len(our_valid_actions)==0 or len(opp_valid_actions)==0:
            if depth==0:
                return None,9999*(get_pts(self.player_number,state[0])-get_pts(other_pl,state[0]))
                
            else:
                if  max_player :
                    return None,get_pts(self.player_number,state[0])
                else:
                    return None,get_pts(other_pl,state[0])

        
                 
            
        if max_player:
            value=-np.inf
            action=None
            for actions in our_valid_actions:
                col,p_out=actions
                new_board=np.copy(state[0])
                temp=state[1].copy()
                if temp[self.player_number].get_int()<=0 and p_out==True:
                    pass
                else:
                    s_copy=new_board,temp
                    s_copy=self.update_board(s_copy,col,self.player_number,p_out)
                    new_points=self.MiniMax(s_copy,depth-1,a,b,False)[1]
                    if new_points>value:
                        value=new_points
                        action=actions
                    a=max(a,value)
                    if a>=b:
                        break
            return action,value
        else:
            value=np.inf
            action=None
            for actions in opp_valid_actions:
                col,p_out=actions
                new_board=np.copy(state[0])
                temp=state[1].copy()
                if temp[other_pl].get_int()<=0 and p_out==True:
                    pass
                else:
                    s_copy=new_board,temp
                    s_copy=self.update_board(s_copy,col,other_pl,p_out)
                    new_points=self.MiniMax(s_copy,depth-1,a,b,True)[1]
                    if new_points<value:
                        value=new_points
                        action=actions
                    b=min(b,value)
                    if b<=a:
                        break
            return action,value
 
    def get_intelligent_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state of the board, return the next move
        This will play against either itself or a human player
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """
        # Do the rest of your implementation here
        #raise NotImplementedError('Whoops I don\'t know what to do')
        depth=int((4*np.log2(self.time*1000))/(3*np.log2(state[0].shape[1])))
        return self.MiniMax(state,depth,-np.inf,np.inf,True)[0]
    
    def Expectimax(self,state: Tuple[np.array, Dict[int, Integer]],depth: int , max_player : bool):
        
        other_pl=0
        if self.player_number==1:
            other_pl=2
        else:
            other_pl=1
        our_valid_actions = get_valid_actions(self.player_number, state)
        opp_valid_actions = get_valid_actions(other_pl, state)
        
        if depth==0 or len(our_valid_actions)==0 or len(opp_valid_actions)==0:
            if depth==0:
                return None,9999*(get_pts(self.player_number,state[0])-get_pts(other_pl,state[0]))
                
            else:
                if  max_player :
                    return None,get_pts(self.player_number,state[0])
                else:
                    return None,get_pts(other_pl,state[0])
        
        if max_player:
            value=-np.inf
            action=None
            for actions in our_valid_actions:
                col,p_out=actions
                new_board=np.copy(state[0])
                temp=state[1].copy()
                if temp[self.player_number].get_int()<=0 and p_out==True:
                    pass
                else:
                    s_copy=new_board,temp
                    s_copy=self.update_board(s_copy,col,self.player_number,p_out)
                    new_points=self.Expectimax(s_copy,depth-1,False)[1]
                    if new_points>value:
                        value=new_points
                        action=actions
            return action,value
        else:
            value=0
            action=None
            for actions in opp_valid_actions:
                col,p_out=actions
                new_board=np.copy(state[0])
                temp=state[1].copy()
                if temp[other_pl].get_int()<=0 and p_out==True:
                    pass
                else:
                    s_copy=new_board,temp
                    s_copy=self.update_board(s_copy,col,other_pl,p_out)
                    new_points=self.Expectimax(s_copy,depth-1,True)[1]
                    value=value+new_points
            value=value//len(opp_valid_actions)
            action=random.choice(opp_valid_actions)
            temp=state[1].copy()
            if temp[other_pl].get_int()<=0:
                while action[1]==True:
                    action=random.choice(opp_valid_actions)

            return action,value

    def get_expectimax_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state of the board, return the next move based on
        the Expecti max algorithm.
        This will play against the random player, who chooses any valid move
        with equal probability
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """
        # Do the rest of your implementation here
        #raise NotImplementedError('Whoops I don\'t know what to do')
        depth=int((np.log2(self.time*1000))/(np.log2(state[0].shape[1])))
        return self.Expectimax(state,depth,True)[0]
