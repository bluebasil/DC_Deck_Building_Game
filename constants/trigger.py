import globe

# The infomation transfered should maybe probbaly be an custome objerct
# or maybe just a dictionary

# in model
DRAW = 0
# data[0] is the number of cards attempted to draw
# data[1] is the boolean 'from_card'
# data[2] is the list of cards drawn
DISCARD = 1
# data[0] is the card discarded
PASS = 2
# data[0] is the card passed
GAIN_CARD = 3
# pay_forward = True
# data[0] is a boolean representing if the card has been redirected
# data[1] is the card gained
# data[2] is a boolean repesenting if the card waas bought
# data[3] is a boolean representing if the card was defeated
GAIN_VP = 4
# data[0] is the amount of vp gained
END_TURN = 5
# data is an empty list
PLAY = 6
# data[0] is the card played
# If there is ever a need for ongoing triggers, that could be added
PRICE = 11
# pay_forward = True
# data[0] cost
# data[1] card
# in card frame
DESTROY = 7
# in effects
ATTACKING = 8
# first_result = True
# This is where prioratization would be usefull, if the attack is
# canceled or chanegd, that should happen before anything else
# data[0] is the player that is being attacked
# data[1] is the attacking card
AVOIDED_ATTACK = 9
# data[0] the attacking player
# data[1] the attacking card
# data[2] defending card
FAILED_TO_AVOID = 10
# data[0] is the player that is being attacked
# data[1] is the attacking card
ROTATE = 11
# Not Yet Designed

# Trigger function heder:
"""
def trigger(self,ttype,data,player):
"""


# Triggers should return None if they do not affect where they are called from
# That includes if the trigger type dosnt match

# active refers to if the player's persona was filled right side up when the affect was triggered
# not relevant unless used by personas

# If pay_forward = True, then data[0] is set to the result of previous valid triggers
# This is especially usefull if a card can only be redirected once, for instance

# first result means that as soon as a non-None responce is heard, it is returns, not triggering further
# I don't know if it is, or will be used

# each trigger is called twise.  Once right away, and again, after
def check_triggers(trigger_id, data, player, active, pay_forward=False, first_result=False, immediate=False):
    results = []
    # I could do some sort of sorting triggers by priority
    # Right now it will be sorted by order played, which is probably best
    for t in player.triggers.copy():
        result = t(trigger_id, data, player, active, immediate)
        if result is not None:
            if pay_forward:
                data[0] = result
            if first_result:
                # print("frist result with resutls",result,results,flush = True)
                return result
            else:
                results.append(result)
    if first_result:
        # print("first result without resutls",results,flush = True)
        return None
    else:
        # print("regular",results,flush = True)
        return results


# saves the state of the trigger until later
# unfortunately, a better way would be to ask each card if they are triggered immediately
# and then later execute what they do if they are triggered
# An easy way with the current functionality would be to have 2 tests
# in the trigger, one for immediate (which makes a local self.triggered = True)
# at which point the second non-immediate test is used
class delayed_trigger:
    trigger_id = -1
    data = []
    player = None
    pay_forward = False
    first_result = False
    active = True

    def __init__(self, trigger_id, data, player, pay_forward=False, first_result=False):
        self.trigger_id = trigger_id
        self.data = data
        self.player = player
        self.pay_forward = pay_forward
        self.first_result = first_result
        self.active = player.persona.active

    def run(self):
        return check_triggers(self.trigger_id, self.data, self.player, self.active, self.pay_forward, self.first_result,
                              immediate=False)


def all(trigger_id, data, player, pay_forward=False, first_result=False, immediate=False):
    active = False
    if player is not None:
        active = player.persona.active
    result = check_triggers(trigger_id, data, player, active, pay_forward, first_result, immediate=True)
    if not immediate:
        globe.boss.trigger_queue.append(delayed_trigger(trigger_id, data, player, pay_forward, first_result))
    return result


# These tests are done on every trigger, so I though i could automate them,
# But allowing this to be called or not, means taht triggers dont ahve to, if they are special
# Active dosnt have to be called by cards (only personas, and even then, if it's not suposed
# to be relevent, like if whiel not active it still delets the trigger, then its not nessesary)
def test(immediate, trigger_on, trigger_function, player, ttype, active=True):
    if immediate \
            and ttype == trigger_on \
            and trigger_function in player.triggers \
            and active:
        return True
    else:
        return False
