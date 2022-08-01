boss = None
view = None
bus = None

DEBUG = False

#If the cpu's should not output to the terminal, set this to True
#False is usefull for debugging
#If a graphic display is used, this wont affect anything that the user sees
CPU_TERMINAL_INVISIBLE = False

# Set this to 0 so that the cpu's take no time to make their moves
# Set this higher (like 1 or 0.5) to make a more realistic, easy to follow 
# (but slower) experiance
TIME_BETWEEN_CPU_MOVES = 0.5

# 0 is pause, 1 is normal speed, 2 is skip
PAUSED_STATE = 1