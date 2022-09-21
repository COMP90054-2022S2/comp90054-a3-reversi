# Reversi (Othello) : A Competitive Game Environment for COMP90054, Semester 2, 2022
---------------------------------------------------------------------------

### Table of contents

  * [Introduction](#introduction)
     * [Key files to read:](#key-files-to-read)
     * [Other supporting files (do not modify):](#other-supporting-files-do-not-modify)
  * [Rules of YINSH](#rules-of-yinsh)
     * [Layout:](#layout)
     * [Scoring:](#scoring)
     * [Winning:](#winning)
     * [Computation Time:](#computation-time)
  * [Getting Started](#getting-started)
     * [Restrictions:](#restrictions)
     * [Warning:](#warning)
     * [Ranking](#ranking)
  
## Introduction

For COMP90054 this semester, you will be competing against agent teams in Reversi, a strategic board game.
There are many files in this package, most of them implementing the game itself. The **only** file that you should change is `myTeam.py`. You can use additional files in your team folder (agents/t_XXX/), which is the **only** directory that we will copy from your repository. 

### Key files to read:

* `reversi_model.py`: The model file that generates game states and valid actions. Start here to understand how everything is structured, and what is passed to your agent. In particular, ```getLegalActions()``` will provide a concise rundown of what a turn consists of, and how that is encapsulated in an action.
<!-- * `agents/generic/example_bfs.py`: Example code that defines the skeleton of a basic planning agent. You aren't required to use any of the filled in code, but your agent submitted in `myTeam.py` will at least need to be initialised with __init__(self, _id), and implement SelectAction(self, actions, rootstate) to return a valid action when asked. -->

### Other supporting files (do not modify):

* `general_game_runner.py`: Support code to setup and run games. See the loadParameter() function for details on acceptable arguments.

* `reversi_utils.py`: Stores important constants, such as the integer values used to represent each game piece.

Of course, you are welcome to read and use any and all code supplied. For instance, if your agent is trying to simulate future gamestates, it might want to appropriate code from `reversi_model.py` in order to do so.


## Rules of REVERSI (Othello):

### GUI Layout: 

Upon loading REVERSI, both **Game** and **Activity Log** windows will appear. The Activity Log window will remain in front, tracking each agent's move. At the end of the game, you are able to click on actions in this window and watch the state reload in Game window accordingly (close the Game window to proceed forward).

The Game window will display the game board, with each agent's pieces counter to display the current score as the game progresses.

### How to play:

Please read the rules or play a sample game here: https://cardgames.io/reversi/

### Winning:

The game proceeds turn by turn. When both players cannot make a valid move (pass), the game ends. The player who has the most number of pieces on the board wins the game. 

### Computation Time:

Each agent has 1 second to return each action. Each move which does not return within one second will incur a warning. After three warnings, or any single move taking more than 3 seconds, the game is forfeit. 
There will be an initial start-up allowance of 15 seconds. Your agent will need to keep track of turns if it is to make use of this allowance. 


## Getting Started

Make sure the version of Python used is **>= 3.8** (we are going to use python 3.8 run your code, which you can find in [Dockerfile](docker\Dockerfile)), and that you have installed:
* func-timeout: ```pip install func-timeout```
* gitpython: ```pip install gitpython```

By default, you can run a game against two random agents with the following:

```bash
$ python general_game_runner.py
```

The starter of the game is determined randomly. You can specify which agent to run by the following code.
```bash
$ python3 general_game_runner.py -a agents.t_XXX.MyTeam,agents.t_XXX.anotherAgent
```

If the game renders at a resolution that doesn't fit your screen, try using the argument --half-scale. The game runs in windowed mode by default, but can be toggled to fullscreen with F11.

### Debugging

There are many options when running the game, you can view them by:
```bash
$ python general_game_runner.py -h
```
A few options that are commonly used: 
* `-p`: print the sys.out and sys.err in the terminal
* `-s`: save the game replay
* `-l`: save the log

### Testing
We are going to run your code on our server with docker image. So that you are able to test the server environment locally by this command:
```bash
bash docker_runner.sh python general_game_runner.py 
```

### Restrictions: 

You are free to use any techniques you want, but will need to respect the provided APIs to have a valid submission. Agents which compute during the opponent's turn will be disqualified. In particular, any form of multi-threading is disallowed, because we have found it very hard to ensure that no computation takes place on the opponent's turn.

### Warning (the output of your code is public): 

If one of your agents produces any stdout/stderr output during its games in the any tournament (preliminary or final), that output will be included in the contest results posted on the website. Additionally, in some cases a stack trace may be shown among this output in the event that one of your agents throws an exception. You should design your code in such a way that this does not expose any information that you wish to keep confidential.

### Ranking: 

Rankings are determined according to ELO score received in tournaments, where a win is worth 3 points, a tie is worth 1 point, and losses are worth 0 (Ties are not worth very much to discourage stalemates). Extra credit will be awarded according to the final competition, but participating early in the pre-competitions will increase your learning and feedback. In addition, staff members have entered the tournament with their own devious agents, seeking fame and glory. These agents have team names beginning with `Staff-`.
