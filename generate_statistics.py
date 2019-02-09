import model
import globe
import sys, traceback
import deck_builder
import view



#model.choose_sets()
deck_builder.choosen_sets = [deck_builder.decks[0],deck_builder.decks[1],deck_builder.decks[2],deck_builder.decks[3]]
globe.view = view.view_controler()

while True:
	globe.boss = model.model()
	try:
		globe.boss.start_game()
	except Exception as e:
		print("ERR:", e)
		print("Exception in user code:")
		print('-'*60)
		traceback.print_exc(file=sys.stdout)
		print('-'*60)
		model.output_persona_stats(globe.boss.players,"crash",traceback.format_exc())