boss = None
view = None
bus = None

DEBUG = True

#If the cpu's should not output to the terminal, set this to True
#False is usefull for debugging
#If a graphic display is used, this wont affect anything that the user sees
CPU_TERMINAL_INVISIBLE = False

# Set this to 0 so that the cpu's take no time to make their moves
# Set this higher (like 1 or 0.5) to make a more realistic, easy to follow
# (but slower) experiance
TIME_BETWEEN_CPU_MOVES = 2

# 0 is pause, 1 is normal speed, 2 is skip
PAUSED_STATE = 1

# For web server mode: reference to Flask-SocketIO instance for thread-safe emission
socketio_instance = None

# Recent game events list for frontend animation hints (cleared after each emit)
events = []

def add_event(event):
	events.append(event)

def flush_events():
	result = list(events)
	events.clear()
	return result
