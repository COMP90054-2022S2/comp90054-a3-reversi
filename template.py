import utils
import random


class GameState:

    def __init__(self,num_of_agent,agent_id):
        pass
    
class Action:
    pass


class GameRule:
    def __init__(self, num_of_agent = 2):
        self.current_agent_index = 0
        self.num_of_agent = num_of_agent
        self.current_game_state = self.initialGameState()
        self.action_counter = 0

    def initialGameState(self):
        utils.raiseNotDefined()
        return 0

    def generateSuccessor(self, game_state, action, agent_id):
        utils.raiseNotDefined()
        return 0

    def getNextAgentIndex(self):
        return (self.current_agent_index + 1) % self.num_of_agent

    def getLegalActions(self, game_state, agent_id):
        utils.raiseNotDefined()
        return []

    def calScore(self, game_state,agent_id):
        utils.raiseNotDefined()
        return 0

    def gameEnds(self):
        utils.raiseNotDefined()
        return False

    def update(self, action):
        temp_state = self.current_game_state
        self.current_game_state = self.generateSuccessor(temp_state, action, self.current_agent_index)
        self.current_agent_index = self.getNextAgentIndex()
        self.action_counter += 1

    def getCurrentAgentIndex(self):
        return self.current_agent_index

class Agent(object):
    def __init__(self, _id):
        self.id = _id
        super().__init__()

    # Given a set of available actions for the agent to execute, and
    # a copy of the current game state (including that of the agent),
    # select one of the actions to execute. 
    def SelectAction(self, actions, game_state):
        return random.choice(actions)


class Displayer:
    def __init__(self):
        pass
    
    # show the displayer for the first time
    def InitDisplayer(self,runner):
        pass
            
    def ExcuteAction(self,i,move,game_state):
        utils.raiseNotDefined()
        pass

    def TimeOutWarning(self,runner,id):
        utils.raiseNotDefined()
        pass

    def EndGame(self,game_state,scores):
        utils.raiseNotDefined()
        pass

