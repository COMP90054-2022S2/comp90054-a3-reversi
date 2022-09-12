# INFORMATION ------------------------------------------------------------------------------------------------------- #

# Author:  Steven Spratley, extending code by Guang Ho and Michelle Blom
# Date:    07/03/22
# Purpose: Implements "Yinsh" for the COMP90054 competitive game environment

# IMPORTS ------------------------------------------------------------------------------------------------------------#

from re import L
import sys
import os
import importlib
import traceback
import datetime
import time
import pickle
import random
import git
import shutil
import logging
import pytz
import json
from template import Agent as DummyAgent
from game import Game, GameReplayer
from optparse import OptionParser


# CONSTANTS ----------------------------------------------------------------------------------------------------------#

# team_indexs   = ["red_team","blue_team"]
DEFAULT_AGENT = "agents.generic.random"
DEFAULT_AGENT_NAME = "default"
# NUM_AGENTS    = 2
GIT_TOKEN_PATH = "configs/token.txt"
TIMEZONE = pytz.timezone('Australia/Melbourne')
DATE_FORMAT = '%d/%m/%Y %H:%M:%S'  # RMIT Uni (Australia)

# CLASS DEF ----------------------------------------------------------------------------------------------------------#

def is_git_repo(path):
    try:
        _ = git.Repo(path).git_dir
        return True
    except git.InvalidGitRepositoryError:
        return False

# Extract the timestamp for a given tag in a repo
def get_commit_time(repo:git.Repo):
    """
    Returns the commit time based on the TIMEZONE

    :param repo: the repository 
    :return: the commit time
    """
    commit = repo.commit()
    commit_date = datetime.datetime.fromtimestamp(commit.committed_date, tz=TIMEZONE)
    return commit_date.strftime(DATE_FORMAT)



def gitCloneTeam(team_info, output_path):
    
    token = None
    with open(GIT_TOKEN_PATH, "r") as f:
        token = f.read()
    

    if not os.path.exists(output_path):
        os.makedirs(output_path)    
    print(team_info)
    clone_url = f"https://{token}@{team_info['url'].replace('https://','')}"
    team_name = str(team_info['team_name'])
    repo_path = f"{output_path}/{str(team_info['team_name'])}"
    commit_id = team_info['commit_id']
    branch = "main"

    logging.info(f'Checking {repo_path} contains git repo or not.')
    submission_time='N/A'
    if not os.path.exists(repo_path):
        os.makedirs(repo_path)

    if not is_git_repo(repo_path):
        logging.info(f'Trying to clone NEW team repo from URL {clone_url}.')
        try:
            repo = git.Repo.clone_from(clone_url, repo_path, branch=branch, no_checkout=True)
            repo.git.checkout(commit_id)
            # repo = git.Repo.clone_from(clone_url, repo_path)
            submission_time = get_commit_time(repo)
            logging.info(f'Team {team_name} cloned successfully with tag date {submission_time}.')
            team_info.update({'git':'succ'})
            team_info.update({'comments':'N/A'})
            team_info.update({'submitted_time': submission_time})
            repo.close()
            # teams_new.append(team_name)
        except git.GitCommandError as e:
            # teams_missing.append(team_name)
            logging.warning(f'Repo for team {team_name} with tag/branch "{branch}" cannot be cloned: {e.stderr.replace(token,"")}')

            team_info.update({'git':'failed'})
            team_info.update({'comments':f'Repo for team {team_name} with tag/branch {branch} cannot be cloned: {e.stderr.replace(token,"")}'})
            # repo.close()
        except KeyboardInterrupt:
            logging.warning('Script terminated via Keyboard Interrupt; finishing...')
            sys.exit("keyboard interrupted!")
            # repo.close()
        except TypeError as e:
            logging.warning(f'Repo for team {team_name} was cloned but has no tag {branch}, removing it...: {e}')
            shutil.rmtree(repo_path)
            # teams_notag.append(team_name)
            team_info.update({'git':'failed'})
            team_info.update({'comments':f'Repo for team {team_name} was cloned but has no tag {branch}, removing it...: {e}'})
            # repo.close()
        except Exception as e:
            logging.error(
                f'Repo for team {team_name} cloned but unknown error when getting tag {branch}; should not happen. Stopping... {e}')
            team_info.update({'git':'failed'})
            team_info.update({'comments':f'Repo for team {team_name} cloned but unknown error when getting tag {branch}; should not happen. Stopping... {e}'})
            # repo.close()  
    else:
        team_info.update({'git':'succ'})

    if team_info['git'] == 'succ':
        try:
            if not os.path.exists(f"agents/{team_name}"):
                shutil.copytree(f"{repo_path}/agents/{team_name}", f"agents/{team_name}")
        except:
            traceback.print_exc()
        shutil.rmtree(f"{repo_path}")
    team_info.update({'copy_files':os.path.exists(f"agents/{team_name}/player.py")})
    return team_info


def loadAgent(matches,superQuiet = True):
    teams = matches['teams']
    num_of_agents = len(teams)
    agents = [None]*num_of_agents
    valid_game = True
    for i in range(num_of_agents):
        agent_temp = None
        try:
            mymodule = importlib.import_module(teams[i]['agent'])
            agent_temp = mymodule.myAgent(i)
        except (NameError, ImportError, IOError):
            print('Error: Agent at "' + teams[i]['agent'] + '" could not be loaded!', file=sys.stderr)
            traceback.print_exc()
            pass
        except:
            pass

        # if student's agent does not exist, use random agent.
        if agent_temp != None:
            agents[i] = agent_temp
            matches['teams'][i].update({'load_agent': True})
            if not superQuiet:
                print ('Agent {} team {} agent {} loaded'.format(i,matches['teams'][i]["team_name"],teams[i]['agent']))
        else:
            valid_game = False
            agents[i] = DummyAgent(i)
            matches['teams'][i].update({'load_agent': False})
        
    return agents,valid_game


class HidePrint:
    # setting output stream
    def __init__(self,flag,file_path,f_name):
        self.flag = flag
        self.file_path = file_path
        self.f_name = f_name
        self._original_stdout = sys.stdout

    def __enter__(self):
        if self.flag:
            if not os.path.exists(self.file_path):
                os.makedirs(self.file_path)
            sys.stdout = open(f"{self.file_path}/log-{self.f_name}.log", 'w')
            sys.stderr = sys.stdout
        else:
            sys.stdout = open(os.devnull, 'w')
            sys.stderr = sys.stdout

    # Restore
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
        sys.stderr = sys.stdout


def run(options,msg):
    num_of_agents = options.num_of_agents

    # fill in the defaults
    agent_names = options.agent_names.split(",")
    agents = options.agents.split(",")
    agent_urls = options.agent_urls.split(",")
    agent_commit_ids = options.agent_commit_ids.split(",")


    missing  = num_of_agents-len(agent_names)
    for i in range(missing):
        agent_names.append(DEFAULT_AGENT_NAME)
    missing  = num_of_agents-len(agents)
    for i in range(missing):
        agents.append(DEFAULT_AGENT)

    # from Yinsh.yinsh_model import YinshGameRule as GameRule
    # from Yinsh.yinsh_displayer import TextDisplayer,GUIDisplayer
    matches = {}
    matches['games'] = []
    matches.update({'teams':{}})
    matches.update({'num_of_games': options.multipleGames})
    # load agents info
    for i in range(num_of_agents):
        team_info = {}
        team_info['team_name'] = agent_names[i]
        team_info['agent'] = agents[i]
        if options.cloud:
            team_info['url'] = agent_urls[i]
            team_info['commit_id'] = agent_commit_ids[i]
            clone_result = gitCloneTeam(team_info, "temp")
            team_info.update(clone_result)
        matches['teams'].update({i:team_info})
    # Load game based on name
    game_name = options.game 
    # matches.update({'game_name':game_name})
    GameRule = None
    TextDisplayer = None
    GUIDisplayer = None

    # import GameRule
    try:
        model = importlib.import_module(f"{game_name}.{game_name.lower()}_model")
        GameRule = getattr(model, f'{game_name}GameRule')
        displayer = importlib.import_module(f"{game_name}.{game_name.lower()}_displayer")
        TextDisplayer = getattr(displayer, 'TextDisplayer')
        GUIDisplayer = getattr(displayer, 'GUIDisplayer')
    except (NameError, ImportError, IOError):
        traceback.print_exc()
        pass
    except:
        pass

    displayer = GUIDisplayer(options.half_scale, options.delay)
    if options.textgraphics:
        displayer = TextDisplayer()
    elif options.quiet or options.superQuiet:
        displayer = None

    # if random seed is not provide, using timestamp
    if options.setRandomSeed == 90054:
        random_seed = int(str(time.time()).replace('.', ''))
    else:
        random_seed = options.setRandomSeed
    
    # make sure random seed is traceable
    random.seed(random_seed)
    seed_list = [random.randint(0,1e10) for _ in range(1000)]
    seed_idx = 0

    num_of_warning = options.numOfWarnings
    file_path = options.output

    if options.replay != None:
        if not options.superQuiet:
            print('Replaying recorded game %s.' % options.replay)
        replay_dir = options.replay
        replay = pickle.load(open(replay_dir,'rb'),encoding="bytes")
        GameReplayer(GameRule,replay,displayer).Run()
    else: 
        games_results = [tuple([0]*num_of_agents for i in range(5))]
        # results = {"succ":valid_game}
        for game_num in range(options.multipleGames):
            game = {}
            loaded_agents, valid_game = loadAgent(matches, superQuiet=options.superQuiet)

            game.update({'valid_game':valid_game})
            random_seed=seed_list[seed_idx]
            seed_idx += 1
            game.update({'random_seed':random_seed})
            f_name = agent_names[0]
            for name in agent_names[-1:]:
                f_name += '-vs-'+name
            f_name += "-"+datetime.datetime.now().strftime("%d-%b-%Y-%H-%M-%S-%f")
            f_name += "-"+str(random_seed) #Add seed to replay filename for reproducibility.
            game.update({'file_name':f_name})
            if options.saveLog: game.update({'log_path':f"{file_path}/log-{f_name}.log"})
            gr = Game(GameRule,
                        loaded_agents,
                        num_of_agent = num_of_agents,
                        seed=random_seed,
                        time_limit=options.warningTimeLimit,
                        warning_limit=num_of_warning,
                        displayer=displayer,
                        agents_namelist=agent_names,
                        interactive=options.interactive)
            if not options.print:
                with HidePrint(options.saveLog,file_path,f_name):
                    print("Following are the print info for loading:\n{}\n".format(msg))
                    print("\n-------------------------------------\n")
                    print("Following are the print info from the game:\n")
                    if valid_game:          
                        replay = gr.Run()
                    else:
                        print("Invalid game. No game played.\n")
            else:
                print("Following are the print info for loading:\n{}\n".format(msg))
                print("\n-------------------------------------\n")
                print("Following are the print info from the game:\n")
                if valid_game:      
                    replay = gr.Run()
                else:
                    print("Invalid game. No game played.\n")
                    
            if valid_game:
                # loading the current total
                scores,totals,wins,ties,loses = games_results[len(games_results)-1]
                # print(games_results)
                new_scores = []
                new_totals = []
                new_wins = []
                new_ties  = []
                new_loses = []
                game.update({f"scores":replay["scores"]})
                
                #Record scores.
                for i in range(num_of_agents):
                    new_scores.append(replay["scores"][i])
                    
                max_score = max(new_scores)


                        

                #Order agent IDs and scores by their ranks this game. Ranks is a list of ranks (int) in player order.
                #Ranks record ties, so if 2 or more agents achieve the same score, they also achieve the same rank.
                ids,scores = list(zip(*sorted(replay["scores"].items(), key=lambda x : x[1], reverse=True)))
                ranks = []
                for agent_id,score in zip(ids,scores):
                    ranks.append((agent_id, scores.index(score) + 1))
                ranks = [i[1] for i in sorted(ranks, key=lambda x : x[0])]
                
                #Update totals and wins (cumulative).
                # num_first = 0
                for i in range(num_of_agents):
                    new_totals.append(totals[i]+new_scores[i])
                    if new_scores[i]==max_score:
                        if new_scores.count(max_score)>1:
                            new_wins.append(wins[i])
                            new_ties.append(ties[i]+1)
                            new_loses.append(loses[i])
                        else:
                            new_wins.append(wins[i]+1)
                            new_ties.append(ties[i])
                            new_loses.append(loses[i])
                    else:
                        new_wins.append(wins[i])
                        new_ties.append(ties[i])
                        new_loses.append(loses[i]+1)

                if not options.superQuiet:
                    print("Result of game ({}/{}):".format(game_num+1, options.multipleGames))
                    for i in range(num_of_agents):
                        print("    {} earned {} points.".format(agent_names[i],new_scores[i]))
    
                games_results.append((new_scores,new_totals,new_wins, new_ties,new_loses))

                if options.saveGameRecord:
                    if not os.path.exists(file_path):
                        os.makedirs(file_path)
                    if not options.superQuiet:
                        print("Game ({}/{}) has been recorded!".format(game_num+1,options.multipleGames))
                    record = pickle.dumps(replay)
                    game.update({'replay_path': f"{file_path}/replay-{f_name}.replay"})
                    with open(f"{file_path}/replay-{f_name}.replay",'wb') as f:
                        f.write(record)

                matches['games'].append(game)
        print(matches)
        if valid_game:
            scores,totals,wins,ties,loses = games_results[len(games_results)-1]
            
            avgs = []
            win_rates = []
            for i in range(num_of_agents):
                avgs.append(totals[i]/options.multipleGames)
                win_rates.append(wins[i]/options.multipleGames*100)

            if not options.superQuiet:
                print("Over {} games:".format(options.multipleGames))
                for i in range(num_of_agents):
                    print("    {} earned {:.2f} on average and won {} games ({:.2f})%."\
                          .format(agent_names[i],avgs[i],wins[i],win_rates[i]))

            # return results as statistics
            matches["total_scores"] = totals

            matches["wins"] = wins
            matches["ties"] = ties
            matches["loses"] = loses
            matches["win_rates"] = win_rates
            matches["succ"] = True

        return matches


def loadParameter():

    """
    Processes the command used to run Yinsh from the command line.
    """
    usageStr = """
    USAGE:      python runner.py <options>
    EXAMPLES:   (1) python runner.py
                    - starts a game with four random agents.
                (2) python runner.py -c MyAgent
                    - starts a fully automated game where Citrine team is a custom agent and the rest are random.
    """
    parser = OptionParser(usageStr)
    # parser.add_option('-r','--red', help='Red team agent file', default=DEFAULT_AGENT)
    # parser.add_option('-b','--blue', help='Blue team agent file', default=DEFAULT_AGENT) 
    parser.add_option('-a','--agents', help='A list of the agents, etc, agents.myteam.player', default="agents.generic.random,agents.generic.random") 

    # parser.add_option('--redName', help='Red agent name', default='Red')
    # parser.add_option('--blueName', help='Blue agent name', default='Blue') 
    parser.add_option('--agent_names', help='A list of agent names', default="random0,random1") 

    # whether load team from cloud
    parser.add_option('--cloud', action='store_true', help='Display output as text only (default: False)', default=False)

    # parser.add_option('--redURL', help='Red team repo URL', default=None) 
    # parser.add_option('--redCommit', help='Red team commit id', default=None) 
    # parser.add_option('--blueURL', help='Blue team repo URL', default=None) 
    # parser.add_option('--blueCommit', help='Blue team commit id', default=None) 

    parser.add_option('--agent_urls', help='A list of urls', default="")
    parser.add_option('--agent_commit_ids', help='A list of commit ids', default="") 

    parser.add_option('-n', '--num_of_agents', type='int',help='The number of agents in this game', default=2)

    parser.add_option('-t','--textgraphics', action='store_true', help='Display output as text only (default: False)', default=False)
    parser.add_option('-g','--game', help='The name of the game, starting with a uppercase character (default: Reversi)', default="Reversi")
    parser.add_option('-q','--quiet', action='store_true', help='No text nor graphics output, only show game info', default=False)
    parser.add_option('-Q', '--superQuiet', action='store_true', help='No output at all', default=False)
    parser.add_option('-w', '--warningTimeLimit', type='float',help='Time limit for a warning of one move in seconds (default: 1)', default=1.0)
    parser.add_option('--startRoundWarningTimeLimit', type='float',help='Time limit for a warning of initialization for each round in seconds (default: 5)', default=5.0)
    parser.add_option('--numOfWarnings', type='int',help='Num of warnings a team can get before fail (default: 3)', default=3)
    parser.add_option('-m', '--multipleGames', type='int',help='Run multiple games in a roll', default=1)
    parser.add_option('--setRandomSeed', type='int',help='Set the random seed, otherwise it will be completely random (default: 90054)', default=90054)
    parser.add_option('-s','--saveGameRecord', action='store_true', help='Writes game histories to a file (named by teams\' names and the time they were played) (default: False)', default=False)
    parser.add_option('-o','--output', help='output directory for replay and log (default: output)',default='output')
    parser.add_option('-l','--saveLog', action='store_true',help='Writes agent printed information into a log file(named by the time they were played)', default=False)
    parser.add_option('--replay', default=None, help='Replays a recorded game file by a relative path')
    parser.add_option('--delay', type='float', help='Delay action in a play or replay by input (float) seconds (default 0.1)', default=0.1)
    parser.add_option('-p','--print', action='store_true', help='Print all the output in terminal when playing games, will diable \'-l\' automatically. (default: False)', default=False)
    parser.add_option('--half-scale', action='store_true', help='Display game at half-scale (default is 1920x1080)', default=False)
    parser.add_option('--interactive', action='store_true', help="Gives the user control over the Citrine agent's actions", default=False)   

    options, otherjunk = parser.parse_args(sys.argv[1:] )
    assert len(otherjunk) == 0, "Unrecognized options: " + str(otherjunk)
    if options.interactive:
        options.citrineName = 'Human'
    return options

# MAIN ---------------------------------------------------------------------------------------------------------------#

if __name__ == '__main__':

    """
    The main function called when advance_model.py is run
    from the command line:

    > python runner.py

    See the usage string for more details.

    > python runner.py --help
    """
    msg = ""
    options = loadParameter()
    matches = run(options,msg)
    # with open("output/matches.json",'w') as f:
    #     json.dump(matches,f)  

# END FILE -----------------------------------------------------------------------------------------------------------#

# python3 general_game_runner.py -t --cloud -a agents.group6.player,agents.group6.player --agent_urls 'https://github.com/COMP90054-2022S1/comp90054-yinsh-project-group6','https://github.com/COMP90054-2022S1/comp90054-yinsh-project-group6' --agent_commit_ids "c2dfa5a2cc4aa4672ed5b6c4979fdb451265f9b8","c2dfa5a2cc4aa4672ed5b6c4979fdb451265f9b8" --agent_names group6,group6 -s -l