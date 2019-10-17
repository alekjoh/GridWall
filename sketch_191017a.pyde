from board import Board
from agent import Agent

global board
global agent

ROWS = 4
COLUMNS = 4
global FRAME_RATE

text_x_dist = 10

def setup():
    size(800, 600)
    global FRAME_RATE
    FRAME_RATE = 10
    frameRate(FRAME_RATE)
    textSize(15)
    
    w, h = 500, 500
    x, y = (width - w) / 2, (height - h) / 2
    
    state = (3, 0)
    win_state = (0, 3)
    lose_states = [(1, 3)]
    obstacles = [(1, 1), (2, 1)]
    
    global board
    board = Board(rows=ROWS, columns=COLUMNS, state=state, win_state=win_state, lose_states=lose_states, obstacles=obstacles, x=x, y=y, w=w, h=h)
    
    global agent
    agent = Agent(board=board)

def draw():
    background(180, 180, 180)
    textAlign(BASELINE)
    text("Round: {}".format(agent.current_round), text_x_dist, 20)
    text("Rounds won: {}".format(agent.rounds_won), text_x_dist, 40)
    text("Rounds lost: {}".format(agent.rounds_lost), text_x_dist, 60)
    text("Framerate: {}".format(FRAME_RATE), text_x_dist, 80)
    
    board.show()
    board.show_state_values(state_values=agent.state_values)
    agent.play(rounds=100)

def set_framerate():
    frameRate(FRAME_RATE)


def keyPressed():
    global FRAME_RATE
    if key == "+":
        FRAME_RATE += 1
        set_framerate()
    elif key == "-":
        if FRAME_RATE > 1:
            FRAME_RATE -= 1
            set_framerate()
