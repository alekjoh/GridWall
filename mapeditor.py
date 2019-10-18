from board import Board
from agent import Agent

global MODES
MODES = ["OBSTACLE", "START", "GOAL", "DEMISE", "FLOOR"]

class MapEditor:
    def __init__(self, rows, cols, x, y, w, h):
        self.board = Board(rows=rows, columns=cols, state=None, win_state=None, lose_states=[], obstacles=[], x=x, y=y, w=w, h=h)
        
        self.mode_index = 1
        self.place_mode = MODES[self.mode_index]
        
        self.agent = Agent(self.board)
    
    #-----------------------------------------------------------------------------------------------------------------------------------------
    
    def show(self):
        self.board.show()


    #-----------------------------------------------------------------------------------------------------------------------------------------
    
    def place_object(self):
        x = mouseX - self.board.x
        y = mouseY - self.board.y
        
        
        row = y // self.board.row_gap
        column = x // self.board.col_gap
        
        if row < 0:
            row = 0
        elif row >= self.board.rows:
            row = self.board.rows - 1
        
        if column < 0:
            column = 0
        elif column >= self.board.columns:
            column = self.board.columns - 1
        
        self.add_piece(row, column)
    
    #-----------------------------------------------------------------------------------------------------------------------------------------
    
    def add_piece(self, row, column):
        if self.place_mode == "START":
            self.board.set_current_state(row, column)
            
        elif self.place_mode == "OBSTACLE":
            self.board.add_obstacle(row, column)
            
        elif self.place_mode == "GOAL":
            self.board.set_goal(row, column)
            
        elif self.place_mode == "DEMISE":
            self.board.add_lose_state(row, column)
    
    #-----------------------------------------------------------------------------------------------------------------------------------------
    
    def toggle_mode(self):
        self.mode_index = self.mode_index + 1 if self.mode_index < len(MODES) - 1 else 0
        self.place_mode = MODES[self.mode_index]
    
    #-----------------------------------------------------------------------------------------------------------------------------------------
    
    def remove_object(self):
        x = mouseX - self.board.x
        y = mouseY - self.board.y
        
        
        row = y // self.board.row_gap
        column = x // self.board.col_gap
        
        if row < 0:
            row = 0
        elif row >= self.board.rows:
            row = self.board.rows - 1
        
        if column < 0:
            column = 0
        elif column >= self.board.columns:
            column = self.board.columns - 1
        
        self.remove_piece(row, column)
    
    #-----------------------------------------------------------------------------------------------------------------------------------------
    
    def remove_piece(self, row, column):
        if self.place_mode == "START":
            self.board.remove_current_state()
            
        elif self.place_mode == "OBSTACLE":
            self.board.remove_obstacle(row, column)
            
        elif self.place_mode == "GOAL":
            self.board.remove_goal(row, column)
            
        elif self.place_mode == "DEMISE":
            self.board.remove_lose_state(row, column)
    
    #-----------------------------------------------------------------------------------------------------------------------------------------
    
    def play(self, rounds=10):
        if self.board.current_state == None or self.board.win_state == None or len(self.board.lose_states) == 0:
            print("Wot ze fook!")
            print("current state = {}".format(self.board.current_state))
            print("win_state = {}".format(self.board.win_state))
            print("lose states: {}".format(" ".join([str(bs) for bs in self.board.lose_states])))
            return
        
        self.agent.board = self.board
        self.agent.play(rounds=rounds)
            
            
