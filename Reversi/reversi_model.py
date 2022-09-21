from template import GameState, GameRule, Agent

import random
import numpy
import copy
import operator
from Reversi.reversi_utils import Cell,filpColor,boardToString,countScore, GRID_SIZE


class ReversiState(GameState):

    def __init__(self, num_of_agents, grid_size,agent_colors):
        self.grid_size = grid_size
        self.agent_colors = agent_colors
        # create the empty board
        self.board = [[Cell.EMPTY for i in range(grid_size)] for i in range(grid_size)]
        self._initialiseBoard()

    # initialise the board with 2 black and 2 white pieces
    def _initialiseBoard(self):
        half = int(self.grid_size/2)
        print(half)
        self.next_player_color = Cell.BLACK
        self.board[half-1][half-1] = Cell.WHITE
        self.board[half][half-1] = Cell.BLACK
        self.board[half-1][half] = Cell.BLACK
        self.board[half][half] = Cell.WHITE

    def getCell(self,cell):
        x,y = cell
        return self.board[x][y]


class ReversiGameRule(GameRule):
    GRIDSIZE = 8

    def __init__(self,num_of_agent):
        super().__init__(num_of_agent)
        self.private_information = None #Reversi is a perfect-information game.


    def initialGameState(self):
        self.agent_colors = {}
        
        self.current_agent_index = random.choice(range(self.num_of_agent))
        self.agent_colors.update({self.current_agent_index:Cell.BLACK,self.getNextAgentIndex():Cell.WHITE})
        self.validPos = self.validPos()
        return ReversiState(self.num_of_agent,GRID_SIZE,self.agent_colors)

    def generateSuccessor(self, state, action, agent_id):
        if action == "Pass":
            return state
        else:
            next_state = copy.deepcopy(state)
            update_color = self.agent_colors[agent_id]
            next_state.board[action[0]][action[1]] = update_color
            # iterate over all 8 directions and check pieces that require updates
            for direction in [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]:
                cur_pos = (action[0] + direction[0], action[1] + direction[1])
                update_list = list()
                flag = False
                # Only searching for updates if the next piece in the direction is from the agent's opponent
                # if next_state.board[cur_pos[0]][cur_pos[1]] == self.agent_colors[(agent_id+1)%2]:
                while cur_pos in self.validPos and next_state.board[cur_pos[0]][cur_pos[1]] != Cell.EMPTY:
                    if next_state.board[cur_pos[0]][cur_pos[1]] == update_color:
                        flag = True
                        break
                    update_list.append(cur_pos)
                    cur_pos = (cur_pos[0] + direction[0], cur_pos[1] + direction[1])
                if flag and len(update_list) != 0:
                    for i,j in update_list:
                        next_state.board[i][j] = update_color
            return next_state


    def getNextAgentIndex(self):
        return (self.current_agent_index + 1) % self.num_of_agent

    def gameEnds(self):
        state = self.current_game_state
        if self.getLegalActions(state,0) == ["Pass"] \
             and self.getLegalActions(state,1) == ["Pass"]:
             return True
        else: return False

    def getLegalActions(self, game_state, agent_id):
        actions = []
        # print(f"Current game state: \n{boardToString(game_state.board,GRID_SIZE)}")
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if game_state.board[x][y] == Cell.EMPTY:
                    pos = (x,y)
                    for direction in [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]:
                        temp_pos = tuple(map(operator.add,pos,direction))
                        if temp_pos in self.validPos and game_state.getCell(temp_pos) != Cell.EMPTY and game_state.getCell(temp_pos) != self.agent_colors[agent_id]:
                            while temp_pos in self.validPos:
                                if game_state.getCell(temp_pos) == Cell.EMPTY:
                                    break
                                if game_state.getCell(temp_pos) == self.agent_colors[agent_id]:
                                    actions.append(pos)
                                    break
                                temp_pos = tuple(map(operator.add,temp_pos,direction))
        if len(actions) == 0:
            actions.append("Pass")
        return actions

    def validPos(self):
        pos_list = []
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                pos_list.append((x,y))
        return pos_list

    def calScore(self, game_state,agent_id):
        return countScore(game_state.board,GRID_SIZE,self.agent_colors[agent_id])
