#in model
DRAW = 0
	#data[0] is the number of cards attempted to draw
	#data[1] is the boolean 'from_card'
	#data[2] is the list of cards drawn
DISCARD = 1
	#data[0] is the card discarded
PASS = 2
	#data[0] is the card passed
GAIN_CARD = 3
	#pay_forward = True
	#data[0] is a boolean representing if the card has been redirected
	#data[1] is the card gained
	#data[2] is a boolean repesenting if the card waas bought
	#data[3] is a boolean representing if the card was defeated
GAIN_VP = 4
	#data[0] is the amount of vp gained
END_TURN = 5
	#data is an empty list
#in card frame
DESTROY = 6
#in effects
ATTACKING = 7
	#first_result = True
	#This is where prioratization would be usefull, if the attack is 
	#canceled or chanegd, that should happen before anything else
	#data[0] is the player that is being attacked
	#data[1] is the attacking card

#Trigger function heder:
"""
def trigger(self,ttype,data,player):
"""
#Triggers should return None if they do not affect where they are called from

#If pay_forward = True, then data[0] is set to the result of previous valid triggers
#This is especially usefull if a card can only be redirected once, for instance
def all(trigger_id,data,player,pay_forward = False,first_result = False):
	results = []
	#I could do some sort of sorting triggers by priority
	#Right now it will be sorted by order played, which is probably best
	for t in player.triggers.copy():
		result = t(trigger_id,data,player)
		if result != None:
			if pay_forward:
				data[0] = result
			if first_result:
				return result
			else:
				results.append(result)
	if first_result:
		return None
	else:
		return results
