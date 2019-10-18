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
                self.set_obstacle(row, col)
        
        for tup in lose_states:
            if self.is_valid_position(tup):
                row, col = tup
                self.set_lose_state(row, col)
        
        if self.is_valid_position(win_state):
                row, col = win_state
                self.set_goal(row, col)
        
    #-----------------------------------------------------------------------------------------------------------------------------------------
    
    def set_goal(self, row, col):
        self.remove_goal(row, col)
        self.win_state = (row, col)
        self.board[row][col] = 1
    
    def set_obstacle(self, row, col):
        self.board[row][col] = "obst"
    
    def set_lose_state(self, row, col):
        self.board[row][col] = -1
    
    
    def add_obstacle(self, row, col):
        self.obstacles.append((row, col))
        self.board[row][col] = "obst"
    
    def add_lose_state(self, row, col):
        self.lose_states.append((row, col))
        self.board[row][col] = -1
    
    def set_current_state(self, row, col):
        self.current_state = (row, col)
        self.start_state = (row, col)
    
    
    #-----------------------------------------------------------------------------------------------------------------------------------------
    
    def remove_goal(self, row, col):
        if self.win_state != None:
            goal_row, goal_col = self.win_state
            self.board[goal_row][goal_col] = 0
    
    
    def remove_obstacle(self, row, col):
        if self.board[row][col] == "obst":
            self.obstacles.remove((row, col))
            self.board[row][col] = 0
    
    
    def remove_lose_state(self, row, col):
        if self.board[row][col] == -1:
            self.lose_states.remove((row, col))
            self.board[row][col] = 0
    
    def remove_current_state(self):
        print("Hi there!")
        self.current_state = None
    
    
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
    
    def is_valid_action(self, action):
        pos = self.next_position(action)
        
        return self.is_valid_position(pos) and pos not in self.obstacles
    
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
                
                if self.current_state != None:
                    if row_index == self.current_state[0] and cell_index == self.current_state[1]:
                        fill(0, 0, 255)
                
                rect(cell_index * self.col_gap + self.x, row_index * self.row_gap + self.y, self.col_gap, self.row_gap)
    

    #-----------------------------------------------------------------------------------------------------------------------------------------
    
    def show_state_values(self, state_values):
        textSize(120 / self.rows)
        fill(0)
        textAlign(CENTER)
        for row_index, row in enumerate(self.board):
            for cell_index, cell in enumerate(row):
                if cell == "obst": continue
                
                if cell == 0:
                    score = state_values[row_index][cell_index]
                    
                    
                    rgb_threshold = 50
                    if score < 0:
                        rgb_val = 255 * abs(score / 1)
                        rgb_val = rgb_val if rgb_val > rgb_threshold else rgb_threshold
                        fill(rgb_val, 0, 0)
                        
                    elif score > 0:
                        rgb_val = 255 * abs(score / 1)
                        rgb_val = rgb_val if rgb_val > rgb_threshold else rgb_threshold
                        fill(0, rgb_val, 0)
                    
                    else:
                        fill(255)
                        
                    if self.current_state != None:
                        if row_index == self.current_state[0] and cell_index == self.current_state[1]:
                            fill(0, 0, 255)
                        
                    rect(cell_index * self.col_gap + self.x, row_index * self.row_gap + self.y, self.col_gap, self.row_gap)
                
                fill(0)
                text("{}".format(state_values[row_index][cell_index]), cell_index * self.col_gap + self.x + self.col_gap / 2, row_index * self.row_gap + self.y + self.row_gap / 2)
    
    #-----------------------------------------------------------------------------------------------------------------------------------------
    
    def print_board(self):
        print("------------------------------------------------------------")
        for row in self.board:
            string = ""
            for cell in row:
                string += " {:^5}".format(cell)
            print(string)
        print("------------------------------------------------------------")
