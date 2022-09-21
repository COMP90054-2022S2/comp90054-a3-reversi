from enum import Enum

class Cell(Enum):
    EMPTY = -1
    BLACK = 0
    WHITE = 1

GRID_SIZE = 8

def filpColor(cell):
    if cell == Cell.BLACK:
        return Cell.WHITE
    elif cell == Cell.WHITE:
        return Cell.BLACK
    else:
        return None

def boardToString(board,grid_size):
    output = ""
    for i in range(grid_size):
        for j in range(grid_size):
            if board[i][j] == Cell.EMPTY:
                output = output + "_ "
            elif board[i][j] == Cell.BLACK:
                output = output + "B "
            elif board[i][j] == Cell.WHITE:
                output = output + "W "
            else: output = output + "X "
        output = output + "\n"
    return output

def countScore(board,grid_size,player_color):
    score = 0
    for i in range(grid_size):
        for j in range(grid_size):
            if board[i][j] == player_color:
                score += 1
    return score   


def ActionToString(agent_id, action):
    if valid_move(action):
        x,y = action
        return f"Player {agent_id} places a piece on pos ({y,x})."
    elif action == "Pass":
        return f"Player {agent_id} passes due to no move to play."
    else:
        return f"Unrecognised action {action}."
    
    
def valid_move(action):
    if not len(action) == 2:
        return False 
    elif not type(action[0]) == int:
        return False 
    elif not type(action[1]) == int:
        return False 
    elif int(action[0]) <0 or int(action[0]) >= GRID_SIZE:
        return False 
    elif int(action[1]) <0 or int(action[1]) >= GRID_SIZE:
        return False 
    else: return True