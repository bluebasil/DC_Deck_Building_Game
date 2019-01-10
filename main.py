import model
import globe
import view
import window


globe.view = view.view_controler()
globe.boss = model.model()

globe.boss.start_game()

for i, p in enumerate(globe.boss.player_score):
	print(f"{i}-{globe.boss.players[i].persona.name} got a score of {p}")
print(f"Completed in {globe.boss.turn_number} turns")

#print_deck(deck)