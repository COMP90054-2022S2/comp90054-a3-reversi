from template import Agent
import time

class myAgent(Agent):
    def __init__(self,_id):
        super().__init__(_id)
    
    def SelectAction(self,actions,game_state):
        time.sleep(2)
        return actions[0]
