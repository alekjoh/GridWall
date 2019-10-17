class Board:
    def __init__(self, rows, columns, state, win_state, lose_states, obstacles, x, y, w, h):
        self.start_state = state
        self.current_state = state
        self.win_state = win_state
        self.lose_states = lose_states
        self.obstacles = obstacles
        
        self.hit_goal = False
        
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
        self.row_gap = h / rows
        self.col_gap = w / columns
        
        self.rows = rows
        self.columns = columns
        
        self.board = [[0 for i in range(columns)] for j in range(rows)]
        
        for tup in obstacles:
            if self.is_valid_position(tup):
                row, col = tup
                self.board[row][col] = "obst"
        
        for tup in lose_states:
            if self.is_valid_position(tup):
                row, col = tup
                self.board[row][col] = -1
        
        if self.is_valid_position(win_state):
                row, col = win_state
                self.board[row][col] = 1.0
        
        self.print_board()
        
    #-----------------------------------------------------------------------------------------------------------------------------------------
    
    def check_goal(self):
        if self.current_state == self.win_state or self.current_state in self.lose_states:
            self.hit_goal = True
            

    #-----------------------------------------------------------------------------------------------------------------------------------------
        
    
    def get_reward(self):
        if self.current_state == self.win_state:
            return 1
        elif self.current_state in self.lose_states:
            return -1
        else:
            return 0


    #-----------------------------------------------------------------------------------------------------------------------------------------
    
    
    def is_valid_position(self, pos):
        if not isinstance(pos, tuple) or len(pos) < 2:
            return
        
        row, column = pos
        
        return row >= 0 and row < self.rows and column >= 0 and column < self.columns


    #-----------------------------------------------------------------------------------------------------------------------------------------
    
    
    def next_position(self, action):
        if action == "up":
            next = (self.current_state[0] - 1, self.current_state[1])
        elif action == "down":
            next = (self.current_state[0] + 1, self.current_state[1])
        elif action == "right":
            next = (self.current_state[0], self.current_state[1] + 1)
        else:
            next = (self.current_state[0], self.current_state[1] - 1)
        
        
        if self.is_valid_position(next):
            if next not in self.obstacles:
                return next
        
        # If the move is invalid we return the current state.
        return self.current_state
    
    #-----------------------------------------------------------------------------------------------------------------------------------------
            
    def show(self):
        for row_index, row in enumerate(self.board):
            for cell_index, cell in enumerate(row):
                if cell == "obst":
                    fill(0, 200)
                elif cell == 0:
                    fill(255)
                elif cell == 1:
                    fill(255, 255, 0)
                else:
                    fill(255, 0, 0)
                
                if row_index == self.current_state[0] and cell_index == self.current_state[1]:
                    fill(0, 255, 0)
                
                rect(cell_index * self.col_gap + self.x, row_index * self.row_gap + self.y, self.col_gap, self.row_gap)
    

    #-----------------------------------------------------------------------------------------------------------------------------------------
    
    def show_state_values(self, state_values):
        fill(0)
        textAlign(CENTER)
        for row_index, row in enumerate(self.board):
            for cell_index, cell in enumerate(row):
                if cell == "obst": continue
                text("Score: {}".format(state_values[row_index][cell_index]), cell_index * self.col_gap + self.x + self.col_gap / 2, row_index * self.row_gap + self.y + self.row_gap / 2)
    
    #-----------------------------------------------------------------------------------------------------------------------------------------
    
    def print_board(self):
        print("------------------------------------------------------------")
        for row in self.board:
            string = ""
            for cell in row:
                string += " {:^5}".format(cell)
            print(string)
        print("------------------------------------------------------------")
