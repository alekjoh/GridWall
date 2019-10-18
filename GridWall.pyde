from board import Board
from agent import Agent
from mapeditor import MapEditor

global board
global agent

paused = True

ROWS = 5
COLUMNS = 5
global FRAME_RATE

global editor

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
    
    global editor
    editor = MapEditor(rows=ROWS, cols=COLUMNS, x=x, y=y, w=w, h=h)

def draw():
    background(180, 180, 180)
    map_editor()


def play_normal():
    textAlign(BASELINE)
    text("Round: {}".format(agent.current_round), text_x_dist, 20)
    text("Rounds won: {}".format(agent.rounds_won), text_x_dist, 40)
    text("Rounds lost: {}".format(agent.rounds_lost), text_x_dist, 60)
    text("Framerate: {}".format(FRAME_RATE), text_x_dist, 80)
    
    board.show()
    board.show_state_values(state_values=agent.state_values)
    agent.play(rounds=100)


def map_editor():
    editor.show()
    editor.board.show_state_values(state_values=editor.agent.state_values)
    fill(0)
    
    textAlign(BASELINE)
    if paused:
        text("Mode: {}".format(editor.place_mode), 20, 20)
    
    if paused: return
    
    textSize(70 / ROWS)
    
    text("Round: {}".format(editor.agent.current_round), text_x_dist, 20)
    text("Rounds won: {}".format(editor.agent.rounds_won), text_x_dist, 40)
    text("Rounds lost: {}".format(editor.agent.rounds_lost), text_x_dist, 60)
    text("Framerate: {}".format(FRAME_RATE), text_x_dist, 80)
    
    editor.play(rounds=1000)

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
    
    elif key == "f":
        editor.toggle_mode()
    
    elif key == ENTER:
        global paused
        paused = not paused
    
    elif keyCode == 37:
        FRAME_RATE = FRAME_RATE - 10 if FRAME_RATE >= 11 else FRAME_RATE
        set_framerate()
    
    elif keyCode == 38:
        FRAME_RATE = 300
        set_framerate()
    
    elif keyCode == 39:
        FRAME_RATE = FRAME_RATE + 10
        set_framerate()
    
    elif keyCode == 40:
        FRAME_RATE = 10
        set_framerate()

def mousePressed():
    if mouseButton == LEFT:
        editor.place_object()
    elif mouseButton == RIGHT:
        editor.remove_object()
