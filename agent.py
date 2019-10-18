from board import Board

class Agent:
    def __init__(self, board):
        self.board = board
        #self.current_state = board.current_state
        self.states = []
        self.actions = ["up", "down", "right", "left"]
        self.state_values = [[0 for i in range(board.columns)] for j in range(board.rows)]
        
        self.rounds_won = 0
        self.rounds_lost = 0
        
        self.learning_rate = 0.3 # For propogating the reward
        self.exp_rate = 0.4 # Prob used when exploring. Basically the chance that the agent will do a random action
        
        
        
        self.current_round = 0
    
    
    #-----------------------------------------------------------------------------------------------------------------------------------------
    
    def choose_action(self):
        # If randomness, then do random move.
        if random(1) < self.exp_rate:
            mutable_action_list = [action for action in self.actions]
            
            rand_index = floor(random(len(mutable_action_list)))
            action = mutable_action_list.pop(rand_index)
            
            while not self.board.is_valid_action(action):
                rand_index = floor(random(len(mutable_action_list)))
                action = mutable_action_list.pop(rand_index)
                
            return action
        else:
            # Find best outcome.
            best_outcome = -1000 # So far it is pretty bad...
            best_action = "rip"
            for a in self.actions:
                row, column = self.board.next_position(action=a)
                state_value = self.state_values[row][column]
                
                if state_value > best_outcome:
                    best_action = a
                    best_outcome = state_value
            
            return best_action
    
    #-----------------------------------------------------------------------------------------------------------------------------------------
    
    def reset(self):
        self.states = []
        self.board.current_state = self.board.start_state
        self.board.hit_goal = False
    
    
    #-----------------------------------------------------------------------------------------------------------------------------------------
    
    def play(self, rounds=10):
        if self.current_round < rounds:
            if self.board.hit_goal:
                # Get reward
                # Set reward and backpropogate
                # Reset board
                
                reward = self.board.get_reward()
                row, column = self.board.current_state
                self.state_values[row][column] = reward
                
                propogated_reward = reward
                for state in reversed(self.states):
                    row, column = state # unpack tuple
                    propogated_reward = self.state_values[row][column] + self.learning_rate * (propogated_reward - self.state_values[row][column])
                    self.state_values[row][column] = round(propogated_reward, 3)
                
                self.reset()
                self.current_round += 1
                
                if reward == 1:
                    self.rounds_won += 1
                elif reward == -1:
                    self.rounds_lost += 1
                
            else:
                # Perform action
                # Add new state to self.states
                # Check for goal
                
                action = self.choose_action()
                next_position = self.board.next_position(action=action)
                self.states.append(next_position)
                self.board.current_state = next_position
                self.board.check_goal()
    
    #-----------------------------------------------------------------------------------------------------------------------------------------
    
    def print_state_values(self):
        print("--------------------------------------------------------------------------------------------------------------------------------------------")
        for row in self.state_values:
            string = ""
            for cell in row:
                string += " {:^6}".format(cell)
            print(string)
        print("--------------------------------------------------------------------------------------------------------------------------------------------")
