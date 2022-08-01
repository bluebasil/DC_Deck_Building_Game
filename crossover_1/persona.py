from constants import cardtype
import effects
from constants import ai_hint
import globe
from frames import persona_frame
from frames import actions
from constants import trigger


def get_personas():
    # return [auquaman(),batman(),the_flash()]
    # return [alan_scott(),doctor_fate(),jay_garrick()]
    return [alan_scott(), doctor_fate(), jay_garrick(), mister_terricic(), power_girl(), stargirl(), wildcat()]


class alan_scott(persona_frame.persona):
    name = "Alan Scott"
    text = "Each time you play a different Super Power during your\nturn, reveal the top card of your deck. If the revealed card\ncosts 0, draw it."
    image = "crossover_1/images/personas/Alan Scott MC.jpg"

    def ai_overvalue(self, card):
        if card.ctype_eq(cardtype.SUPERPOWER):
            return persona_frame.overvalue()
        return 0

    def trigger(self, ttype, data, player, active, immediate):
        if globe.DEBUG:
            print("test", self.name, flush=True)
        if trigger.test(not immediate,
                        trigger.PLAY,
                        self.trigger,
                        player, ttype, active) and data[0].ctype_eq(cardtype.SUPERPOWER):
            already_played = False
            for c in self.player.played.played_this_turn:
                if c != data[0] and data[0].name == c.name:
                    already_played = True
            if not already_played:
                top_card = player.reveal_card(public=True)
                if top_card != None and top_card.cost == 0:
                    player.draw_card()

    def ready(self):
        self.player.triggers.append(self.trigger)


class doctor_fate(persona_frame.persona):
    name = "Doctor Fate"
    text = "When you play two cards with consecutive costs during your turn,\n+1 Power.\nWhen you play three cards with consecutive costs during your turn,\ndraw a card."
    image = "crossover_1/images/personas/Doctor Fate MC.jpg"
    cards_registered = []

    def get_costcount(self):
        distribution = {}
        for i in range(25):
            distribution[i] = 1
        assemble = []
        assemble.extend(self.player.deck.contents)
        assemble.extend(self.player.discard.contents)
        for c in assemble:
            distribution[c.cost] += 1
        return distribution

    def ai_overvalue(self, card):
        card_costs = self.get_costcount()
        all_relevant = sum(list(card_costs.values()))
        return 0.25 / (card_costs[card.cost] / all_relevant) - 1

    # print("MAKE SURE NONE OF THESE ARE 0",card.ctype,all_relevant,flush=True)
    # if card.ctype in card_types:
    #	return 0.25/(card_types[card.ctype]/all_relevant) - 1
    # return 0

    # This is a complicated ability.
    # I kind of disagree how its being interpreted on forms, but i am implimenting it thqt way anyways
    # There should be decition mkainging, like what pairs, but i may just base that on order of cards played
    # Idealy, if finds the optimum, but that is hard.  nealy impossible with drawing
    def trigger(self, ttype, data, player, active, immediate):
        if globe.DEBUG:
            print("test", self.name, flush=True)
        if trigger.test(not immediate,
                        trigger.PLAY,
                        self.trigger,
                        player, ttype, active):
            self.cards_registered.append(data[0])
            data[0].df_power = False
            data[0].df_draw = False
            # initialize all cards that have been played, if they have not been inititalized yet
            for c in player.played.played_this_turn:
                if not hasattr(c, 'df_power'):
                    self.cards_registered.append(c)
                    c.df_power = False
                    c.df_draw = False
            for c in player.played.played_this_turn:
                # starts by finding 2 consecutive
                if c != data[0] and abs(c.cost - data[0].cost) == 1:
                    # power portion
                    if c.df_power == False and data[0].df_power == False:
                        c.df_power = True
                        data[0].df_power = True
                        player.played.plus_power(1)
                        if globe.DEBUG:
                            print(f"Doctor Fate got power because of a {data[0].name} and {c.name}")
                    # draw portion
                    if c.df_draw == False and data[0].df_draw == False:
                        # find third match
                        for c2 in player.played.played_this_turn:
                            if c2 != c and c2 != data[0] and c2.df_draw == False and (abs(c.cost - c2.cost) == 1 or abs(
                                    c2.cost - data[0].cost) == 1) and c.df_draw == False and data[0].df_draw == False:
                                data[0].df_draw = True
                                c.df_draw = True
                                c2.df_draw = True
                                player.draw_card()
                                if globe.DEBUG:
                                    print(f"Doctor Fate Drew because of a {data[0].name}, {c.name}, and {c2.name}")

    def ready(self):
        self.cards_registered = []
        self.player.triggers.append(self.trigger)

    # resets all cards that have been touched
    def reset(self):
        for c in self.cards_registered:
            c.df_power = False
            c.df_draw = False


class jay_garrick(persona_frame.persona):
    name = "Jay Garrick"
    text = "When a card tells you to draw one or more cards, before\ndrawing, reveal the top card of your deck and you may\ndiscard it."
    image = "crossover_1/images/personas/Jay Garrick MC.jpg"
    accounted_for = False

    def ai_overvalue(self, card):
        if card.text.lower().count('draw') > 0:
            return persona_frame.overvalue()
        return 0

    def trigger(self, ttype, data, player, active, immediate):
        if globe.DEBUG:
            print("test", self.name, flush=True)
        if trigger.test(immediate,
                        trigger.DRAW,
                        self.trigger,
                        player, ttype, active):
            if globe.DEBUG:
                print("active", self.name, flush=True)
            revealed = player.reveal_card(public=True)
            if revealed != None and effects.ok_or_no(f"Would you like to discard the {revealed.name}?", player,
                                                     revealed, ai_hint.IFBAD):
                player.discard_a_card(revealed)

    def ready(self):
        self.player.triggers.append(self.trigger)


class mister_terricic(persona_frame.persona):
    name = "Mister Terrific"
    text = "Once during each of your turns, you may discard a Punch card.\nIf you do, reveal the top three cards of your deck, draw one\nEquipment revealed this way, and put the rest back in any order."
    image = "crossover_1/images/personas/Mister Terrific MC.jpg"
    action = None

    def ai_overvalue(self, card):
        if card.ctype_eq(cardtype.EQUIPMENT):
            # Really need equipment
            return persona_frame.overvalue() * 2
        return 0

    def special_action_click(self, player):
        # We must ensure that we are doing this on our turn
        if player.pid == globe.boss.whose_turn:
            for c in self.player.hand.contents:
                if c.name == "Punch" and self.action in self.player.played.special_options:
                    self.player.discard_a_card(c)

                    assemble = []
                    for i in range(3):
                        to_add = player.reveal_card(public=False)
                        if to_add != None:
                            assemble.append(to_add)
                            player.deck.contents.pop()

                    equipment_assemble = []
                    for c in assemble:
                        if c.ctype_eq(cardtype.EQUIPMENT):
                            equipment_assemble.append(c)
                    effects.reveal(f"These were the top 3 cards on {player.persona.name}'s deck", player, assemble)
                    if len(equipment_assemble) > 0:
                        result = effects.choose_one_of("Choose one of these to draw.", player, assemble, ai_hint.BEST)
                        # must be there to be drawn
                        player.deck.contents.append(result)
                        player.draw_card(from_card=False)
                        assemble.remove(result)
                    total_times = len(assemble)
                    while len(assemble) > 0:
                        result = effects.choose_one_of(
                            f"Place card back on top of your deck ({total_times - len(assemble) + 1}/{total_times})?",
                            player, assemble, ai_hint.WORST)
                        assemble.remove(result)
                        player.deck.contents.append(result)

                    self.player.played.special_options.remove(self.action)
                    return True
        return False

    def ready(self):
        if self.active:
            self.action = actions.special_action("Mister Terrific", self.special_action_click)
            self.player.played.special_options.append(self.action)

    # If there is more than a 50% chance of getting a card that does anything,
    def ai_is_now_a_good_time(self):
        total_left = 0
        for c in self.player.deck.contents:
            if c.ctype_eq(cardtype.EQUIPMENT):
                total_left += 1
        if total_left / (len(self.player.deck.contents) + 1) > 0.2:
            if self.action in self.player.played.special_options:
                return self.special_action_click(self.player)
        # return self.any_time()
        return False


class power_girl(persona_frame.persona):
    name = "Power Girl"
    text = "Each time you play a different Super Power during your\nturn, put a Punch from your discard pile into your hand."
    image = "crossover_1/images/personas/Power Girl MC.jpg"

    def ai_overvalue(self, card):
        if card.ctype_eq(cardtype.SUPERPOWER):
            return persona_frame.overvalue()
        return 0

    def trigger(self, ttype, data, player, active, immediate):
        if globe.DEBUG:
            print("test", self.name, flush=True)
        if trigger.test(not immediate,
                        trigger.PLAY,
                        self.trigger,
                        player, ttype, active) and data[0].ctype_eq(cardtype.SUPERPOWER):
            already_played = False
            for c in self.player.played.played_this_turn:
                if c != data[0] and data[0].name == c.name:
                    already_played = True
            if not already_played:
                for c in player.discard.contents:
                    if c.name == "Punch":
                        c.pop_self()
                        player.hand.contents.append(c)

    def ready(self):
        self.player.triggers.append(self.trigger)


class stargirl(persona_frame.persona):
    name = "Stargirl"
    text = "When you play a Defense card during your turn or avoid\nan Attack, you may draw a card and then discard a card."
    image = "crossover_1/images/personas/Stargirl MC.jpg"

    def ai_overvalue(self, card):
        if card.defense:
            return persona_frame.overvalue()
        return 0

    def trigger(self, ttype, data, player, active, immediate):
        if globe.DEBUG:
            print("test", self.name, flush=True)
        if (trigger.test(not immediate,
                         trigger.PLAY,
                         self.trigger,
                         player, ttype, active) and data[0].defense) or (trigger.test(not immediate,
                                                                                      trigger.AVOIDED_ATTACK,
                                                                                      self.trigger,
                                                                                      player, ttype, active)):
            if globe.DEBUG:
                print("active", self.name, flush=True)
            player.draw_card(from_card=False)
            result = effects.choose_one_of("Discard a card", player, player.hand.contents, ai_hint.WORST)
            player.discard_a_card(result)

    def reset(self):
        self.player.triggers.append(self.trigger)


class wildcat(persona_frame.persona):
    name = "Wildcat"
    text = "The first time you play a Punch dueing each of your turns:\n-If you have played a Hero this turn, draw a card.\n-If you have played a Villain this turn, draw a card."
    image = "crossover_1/images/personas/Wildcat MC.jpg"

    def ai_overvalue(self, card):
        if card.ctype_eq(cardtype.HERO) or card.ctype_eq(cardtype.VILLAIN):
            return persona_frame.overvalue()
        return 0

    def trigger(self, ttype, data, player, active, immediate):
        if globe.DEBUG:
            print("test", self.name, flush=True)
        if trigger.test(not immediate,
                        trigger.PLAY,
                        self.trigger,
                        player, ttype) and data[0].name == "Punch":
            if active:
                hero_played = False
                villain_played = False
                for c in self.player.played.played_this_turn:
                    if c.ctype_eq(cardtype.HERO):
                        hero_played = True
                    if c.ctype_eq(cardtype.VILLAIN):
                        villain_played = True
                if hero_played:
                    player.draw_card(from_card=False)
                if villain_played:
                    player.draw_card(from_card=False)
            player.triggers.remove(self.trigger)

    def ready(self):
        self.player.triggers.append(self.trigger)
