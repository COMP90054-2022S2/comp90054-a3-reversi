import tkinter, copy, time, os, time, numpy
from   collections             import defaultdict, Counter
from   Reversi.reversi_utils       import *
from   template                import Displayer


# CLASS DEF ----------------------------------------------------------------------------------------------------------#

#Function to create labels at given pixel coordinates.
def make_label(master, x, y, h, w, *args, **kwargs):
    f = tkinter.Frame(master, height=h, width=w)
    f.pack_propagate(0)
    f.place(x=x, y=y)
    label = tkinter.Label(f, *args, **kwargs)
    label.pack(fill=tkinter.BOTH, expand=1)
    return label

#Class to draw images of pieces on the board.
class BoardArea():
    def __init__(self, root):
        self.root = root
        
    def update(self, state, resources):
        
        # Display the current score
        result = dict(sum(map(Counter, state.board), Counter()))
        for i,c in state.agent_colors.items():
            
            
            tk_string = tkinter.StringVar()
            if c not in result:
                tk_string.set(f"Agent {i} ({c})'s \ncurrent score is: 0")
            else:
                tk_string.set(f"Agent {i} ({c})'s \ncurrent score is: {result[c]}")
            make_label(self.root, textvariable=tk_string, x=SCORE_POS[i][0], 
                                    y=SCORE_POS[i][1], h=60*s, w=400*s, font=('times', int(20*s)), bg='white', fg='black')
        

        # #Update pieces in the gameboard
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                piece = state.getCell((y,x))
                if piece != Cell.EMPTY:
                    # x1, y1 = x, y+x*0.5 #A simple skew transform to convert coordinates to a non-orthogonal board.
                    piece_name = 'white' if piece==Cell.WHITE else 'black' 
                    self.root.create_image(BOARD_POS[0]+x*PIECE_SEP[0], BOARD_POS[1]+y*PIECE_SEP[1], 
                                           image=resources[piece_name], tags='piece')
                
#Class to control GUI.
class GUIDisplayer(Displayer):
    def __init__(self, scale, delay = 0.1):
        self.delay = delay
        # Absolute positions for resources.
        global s,TITL_POS,BOARD_POS,SCORE_POS,SCORE_SEP,PIECE_SEP,C_WIDTH,C_HEIGHT
        s = 0.5 if scale else 1
        TITL_POS  = [1000*s, 50*s]
        # BOARD_POS = [562*s, -140*s]
        BOARD_POS = [75*s, 75*s]
        SCORE_POS = [[1000*s, 300*s],[1000*s, 450*s]]
        # SCORE_SEP = [1186*s, 86*s] #Separation between "won" rings, serving as a visual scoreboard.
        PIECE_SEP = [117*s, 122*s] #Separation between board pieces.
        C_WIDTH   = 1920*s #Canvas dimensions.
        C_HEIGHT  = 1080*s
                
    def InitDisplayer(self, runner):
        #Initialise root frame.
        self.root = tkinter.Tk()
        self.root['bg']='white'
        self.root.title("Reversi ------ COMP90054 AI Planning for Autonomy")
        
        # ImageTk.PhotoImage(Image.open("neon_timer.png"))
        self.root.tk.call('wm', 'iconphoto', self.root._w, tkinter.PhotoImage(file='Reversi/resources/ICON_1.png'))
        # self.root.tk.call('wm', 'iconphoto', self.root._w, tkinter.PhotoImage(file='Reversi/resources/ICON_0.png'))
        self.root.geometry("{}x{}".format(int(C_WIDTH), int(C_HEIGHT)))
        self.maximised = True
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_fullscreen)
        
        #Load resources (i.e. images of tabletop, cards, and player chips).
        self.resources = {'table': tkinter.PhotoImage(file="Reversi/resources/table.png" ).subsample(int(1/s)),
                          'white':tkinter.PhotoImage(file="Reversi/resources/ICON_0.png").subsample(int(1/s)),
                          'black':tkinter.PhotoImage(file="Reversi/resources/ICON_1.png").subsample(int(1/s))}
        
        #Initialise canvas and place elements.
        self.canvas = tkinter.Canvas(self.root, height=C_HEIGHT, width=C_WIDTH, bg='white')
        self.canvas.pack()
        self.table  = self.canvas.create_image(0, 0, image=self.resources['table'], anchor='nw')
        self.board_area = BoardArea(self.canvas)
        self.agent_title_var = tkinter.StringVar()
        self.agent_title_var.set(f'{runner.agents_namelist[0]} (Agent 0) \n vs. \n{runner.agents_namelist[1]} (Agent 1)')
        self.agent_titles = make_label(self.canvas, textvariable=self.agent_title_var, x=TITL_POS[0], 
                                       y=TITL_POS[1], h=120*s, w=400*s, font=('times', int(20*s)), bg='white', fg='black')
        

        #Generate scoreboard in separate window.
        self.sb_window = tkinter.Toplevel(self.root)
        self.sb_window.title("Reversi ------ Activity Log")
        self.sb_window.tk.call('wm', 'iconphoto', self.sb_window._w, tkinter.PhotoImage(file='Reversi/resources/ICON_0.png'))
        self.sb_window.geometry("640x455")
        self.sb_frame = tkinter.Frame(self.sb_window)
        self.sb_frame.pack()
        self.scrollbar = tkinter.Scrollbar(self.sb_frame, orient=tkinter.VERTICAL)
        self.move_box=tkinter.Listbox(self.sb_frame,name="actions:", height=37, width=88, \
                                      selectmode="single", borderwidth=4, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.move_box.yview,troughcolor="white",bg="white")
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.move_box.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)   
        self.game_state_history=[]
        self.round_num = 0
        self.sb_window.attributes("-topmost", True)
        
    def toggle_fullscreen(self, event=None):
        self.maximised = not self.maximised
        self.root.attributes("-fullscreen", self.maximised)

    def end_fullscreen(self, event=None):
        self.maximised = False
        self.root.attributes("-fullscreen", False)
        
    def _InsertState(self, text, game_state):
        text = text.replace("\n ","")
        self.game_state_history.append(copy.deepcopy(game_state))
        self.move_box.insert(tkinter.END,text)
        self.move_box.see(tkinter.END)
        self.move_box.selection_clear(0, last=None) 
    
    #Rebuild canvas images.
    def _DisplayState(self, game_state):
        #Destroy and replace canvas images.
        self.canvas.delete('piece')
        self.board_area.update(game_state, self.resources)
        self.canvas.update()

    def ExcuteAction(self,agent_id, action, game_state):
        self._InsertState(ActionToString(agent_id, action), game_state)
        self._DisplayState(game_state)
        time.sleep(self.delay)

    def TimeOutWarning(self,runner,id):
        self._InsertState("Agent {} time out, {} out of {}. Choosing random action instead."\
                          .format(id, runner.warnings[id],runner.warning_limit),runner.game_rule.current_game_state)
        if id == 0:
            self.move_box.itemconfig(tkinter.END, {'bg':'red','fg':'blue'})
        else:
            self.move_box.itemconfig(tkinter.END, {'bg':'blue','fg':'yellow'})
        pass
        
    def EndGame(self,game_state,scores):
        self._InsertState("--------------End of game-------------",game_state)
        result = dict(sum(map(Counter, game_state.board), Counter()))
        for i,c in game_state.agent_colors.items():
            if c not in result:
                self._InsertState(f"Final score with bonus for Agent {i}: 0",game_state)
            else:
                self._InsertState(f"Final score with bonus for Agent {i}: {result[c]}",game_state)
        
        self.focus = None
        def OnHistorySelect(event):
            w = event.widget
            self.focus = int(w.curselection()[0])
            if self.focus < len(self.game_state_history):
                self._DisplayState(self.game_state_history[self.focus])
        def OnHistoryAction(event):
            if event.keysym == "Up":
                if self.focus>0:
                    self.move_box.select_clear(self.focus)
                    self.focus -=1
                    self.move_box.select_set(self.focus)
                    if self.focus < len(self.game_state_history):
                        self._DisplayState(self.game_state_history[self.focus])
            if event.keysym == "Down":
                if self.focus<len(self.game_state_history)-1:
                    self.move_box.select_clear(self.focus)
                    self.focus +=1
                    self.move_box.select_set(self.focus)
                    self._DisplayState(self.game_state_history[self.focus])

        self.move_box.bind('<<ListboxSelect>>', OnHistorySelect)
        self.move_box.bind('<Up>', OnHistoryAction)
        self.move_box.bind('<Down>', OnHistoryAction)
    
        self.root.mainloop()
        pass  


class TextDisplayer(Displayer):
    def __init__(self):
        print ("--------------------------------------------------------------------")
        return

    def InitDisplayer(self,runner):
        pass

    def StartRound(self,game_state):
        pass

    def _DisplayState(self, game_state):
        pass 

    def ExcuteAction(self,i,move, game_state):
        print(f"\nAgent {i} has chosen the following move: {move}\n")
        
        print(f"The next player color is: {game_state.next_player_color}\n")
        print(f"The current board is: \n{boardToString(game_state.board,game_state.grid_size)}")
        print ("--------------------------------------------------------------------")
        
    def TimeOutWarning(self,runner,id):
        print ( "Agent {} Time Out, {} out of {}.".format(id,runner.warnings[id],runner.warning_limit))

    def EndGame(self,game_state,scores):
        print("The game has ended: ")
        print(f"player 0 scores {scores[0]} and player 1 scores {scores[1]}")
        if scores[0] == scores[1]: print("tie\n")
        elif scores[0] < scores[1]: print("player 1 wins\n")
        elif scores[0] > scores[1]: print("player 0 wins\n")


# class GUIDisplayer(Displayer):
#     def __init__(self, scale, delay = 0.1):
#         print ("--------------------------------------------------------------------")
#         return

#     def InitDisplayer(self,runner):
#         pass

#     def StartRound(self,game_state):
#         pass    

#     def ExcuteAction(self,i,move, game_state):
#         print(f"\nAgent {i} has chosen the following move: {move}\n")
        
#         print(f"The next player color is: {game_state.next_player_color}\n")
#         print(f"The current board is: \n{boardToString(game_state.board,game_state.grid_size)}")
#         print ("--------------------------------------------------------------------")
        
#     def TimeOutWarning(self,runner,id):
#         print ( "Agent {} Time Out, {} out of {}.".format(id,runner.warnings[id],runner.warning_limit))

#     def EndGame(self,game_state,scores):
#         print("The game has ended: ")
#         print(f"player 0 scores {scores[0]} and player 1 scores {scores[1]}")
#         if scores[0] == scores[1]: print("tie\n")
#         elif scores[0] < scores[1]: print("player 1 wins\n")
#         elif scores[0] > scores[1]: print("player 0 wins\n")
