
main_view = view_controler()


globe.boss = model.model()

globe.boss.start_game()

for i, p in enumerate(globe.boss.player_score):
	print(f"{i} got a score of {p}")

#print_deck(deck)