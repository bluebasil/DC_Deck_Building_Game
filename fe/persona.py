from constants import cardtype
import effects
from constants import ai_hint
import globe
from frames import persona_frame
from frames import actions
from constants import owners
from constants import trigger


def get_personas():
    return [bane(), bizarro(), black_adam(), black_manta(), deathstroke(), harley_quinn(), lex_luther(), sinestro(),
            the_joker()]


class bane(persona_frame.persona):
    name = "Bane"
    text = "If the first card you play during each of your turns has a cost 1\nor greater, you may destroy it. If you do, +2 Power."
    image = "fe/images/personas/Bane MC.jpg"
    action = None

    def special_action_click(self, player):
        self.player.played.played_this_turn[0].destroy(player)
        self.player.played.plus_power(2)
        self.player.played.special_options.remove(self.action)
        return True

    def trigger(self, ttype, data, player, active, immediate):
        if globe.DEBUG:
            print("test", self.name, flush=True)
        if trigger.test(not immediate, trigger.PLAY, self.trigger, player, ttype, active) and player.played.played_this_turn.index(data[0]) == 0 and data[0].cost >= 1:
            if globe.DEBUG:
                print("active", self.name, flush=True)
            self.action = actions.special_action("Bane", self.special_action_click)
            player.played.special_options.append(self.action)
            player.triggers.remove(self.trigger)

    def ready(self):
        self.player.triggers.append(self.trigger)

    def ai_is_now_a_good_time(self):
        return False


# Once i make harly quin i could not makew the bizzaro button come up until two weakenss cards are in my discard pile?
class bizarro(persona_frame.persona):
    name = "Bizarro"
    text = "When you destroy a card, gain a Weakness.\nDuring your turn, you may put two Weakness cards from your\ndiscard pile on top of the Weakness stack.  If you do, draw a card."
    image = "fe/images/personas/Bizarro MC.jpg"
    action = None

    def special_action_click(self, player):
        to_remove = []
        for c in self.player.discard.contents:
            if c.ctype_eq(cardtype.WEAKNESS):
                to_remove.append(c)
                if len(to_remove) == 2:
                    for w in to_remove:
                        w.pop_self()
                        w.set_owner(owners.WEAKNESS)
                        globe.boss.weakness_stack.add(w)
                    self.player.draw_card(from_card=False)
                    self.player.played.special_options.remove(self.action)
                    return True
        return False

    def ready(self):
        self.player.triggers.append(self.trigger)
        if self.active:
            self.action = actions.special_action("Bizarro", self.special_action_click)
            self.player.played.special_options.append(self.action)

    def ai_is_now_a_good_time(self):
        if self.action in self.player.played.special_options:
            return self.special_action_click(self.player)

    def trigger(self, ttype, data, player, active, immediate):
        if globe.DEBUG:
            print("test", self.name, flush=True)
        if trigger.test(not immediate, trigger.DESTROY, self.trigger, player, ttype, active):
            if globe.DEBUG:
                print("active", self.name, flush=True)
            self.player.gain_a_weakness()


class black_adam(persona_frame.persona):
    name = "Black Adam"
    text = "The first time you play a super power during each of your turns, you may destroy it.  If you do, draw a card and gain 1 VP."
    image = "fe/images/personas/Black Adam MC.jpg"

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
            if globe.DEBUG:
                print("active", self.name, flush=True)
            instruction_text = "Would you like to destory it? If you do, draw a card and gain 1 VP."
            if effects.ok_or_no(instruction_text, player, data[0], ai_hint.IFBAD):
                data[0].destroy(player)
                player.draw_card(from_card=False)
                player.gain_vp(1)
            player.triggers.remove(self.trigger)

    def ready(self):
        self.player.triggers.append(self.trigger)


class black_manta(persona_frame.persona):
    name = "Black Manta"
    text = "You may put any cards you buy or gain from the lineup on the bottom of your deck."
    image = "fe/images/personas/Black Manta MC.jpg"

    def trigger(self, ttype, data, player, active, immediate):
        if trigger.test(immediate,
                        trigger.GAIN_CARD,
                        self.trigger,
                        player, ttype, active) and data[1].owner_type == owners.LINEUP and data[
            0] == False and effects.ok_or_no(f"Would you like to put {data[1].name} on the bottom of your deck?",
                                             player,
                                             data[1], ai_hint.ALWAYS):
            player.deck.contents.insert(0, data[1])
            return True

    def ready(self):
        # if self.active:
        self.player.triggers.append(self.trigger)
    # self.player.gain_redirect.append(self.black_manta_redirect)


class deathstroke(persona_frame.persona):
    name = "Deathstroke"
    text = "+1 Power for each card you destroy during your turn."
    image = "fe/images/personas/Deathstroke MC.jpg"

    def trigger(self, ttype, data, player, active, immediate):
        if trigger.test(not immediate,
                        trigger.DESTROY,
                        self.trigger,
                        player, ttype, active):
            self.player.played.plus_power(1)
            return True

    def ready(self):
        self.player.triggers.append(self.trigger)


# def destory_power(self):
#	if self.active and globe.boss.whose_turn == self.player.pid:
#		self.player.played.plus_power(1)
#	return


class harley_quinn(persona_frame.persona):
    name = "Harley Quinn"
    text = "During each player's turn, the first time you pass\na card or discard a card, draw a card."
    image = "fe/images/personas/Harley Quinn MC.jpg"
    last_seen_turn = -1

    """def discard_power(self):
		if self.active and globe.boss.whose_turn != -1 and self.last_seen_turn != globe.boss.whose_turn:
			self.last_seen_turn = globe.boss.whose_turn
			self.player.draw_card(from_card = False)
		return

	def card_pass_power(self):
		if self.active and globe.boss.whose_turn != -1 and self.last_seen_turn != globe.boss.whose_turn:
			self.last_seen_turn = globe.boss.whose_turn
			self.player.draw_card(from_card = False)
		return"""

    def trigger(self, ttype, data, player, active, immediate):
        # Two trigger events can do this
        # must be during a players turn
        # Only once per players turn
        if (trigger.test(not immediate,
                         trigger.DISCARD,
                         self.trigger,
                         player, ttype, active)
            or trigger.test(not immediate,
                            trigger.PASS,
                            self.trigger,
                            player, ttype,
                            active)) and globe.boss.whose_turn != -1 and self.last_seen_turn != globe.boss.whose_turn:
            self.last_seen_turn = globe.boss.whose_turn
            self.player.draw_card(from_card=False)

    def reset(self):
        self.player.triggers.append(self.trigger)


class lex_luther(persona_frame.persona):
    name = "Lex Luther"
    text = "At the end of your turn, draw an extra card for each Hero you bought or gianed during your turn."
    image = "fe/images/personas/Lex Luthor MC.jpg"

    def ai_overvalue(self, card):
        if card.ctype_eq(cardtype.HERO):
            return persona_frame.overvalue()
        return 0

    # the reset is specifically timed for this to be possible
    def reset(self):
        if self.active:
            for c in self.player.gained_this_turn:
                if c.ctype_eq(cardtype.HERO):
                    self.player.draw_card(from_card=False)


class sinestro(persona_frame.persona):
    name = "Sinestro"
    text = "When one or more foes fails to avoid an Attack you play, gain 1 VP.\nThe first time you gain VPs during each of your turns, draw a card."
    image = "fe/images/personas/Sinestro MC.jpg"
    ability_used = False
    same_attack = False

    def ai_overvalue(self, card):
        if card.attack:
            return persona_frame.overvalue()
        return 0

    def triggerVP(self, ttype, data, player, active, immediate):
        if trigger.test(not immediate,
                        trigger.GAIN_VP,
                        self.triggerVP,
                        player, ttype):
            if active:
                player.draw_card(from_card=False)
            player.triggers.remove(self.triggerVP)

    def triggerReset(self, ttype, data, player, active, immediate):
        if trigger.test(immediate,
                        trigger.PLAY,
                        self.triggerReset,
                        player, ttype):
            self.same_attack = False

    # FA = Failed to Avoid
    def triggerFA(self, ttype, data, player, active, immediate):
        if trigger.test(not immediate,
                        trigger.FAILED_TO_AVOID,
                        self.triggerFA,
                        player, ttype, active) \
                and not self.same_attack:
            self.player.gain_vp(1)
            self.same_attack = True

    def ready(self):
        self.player.triggers.append(self.triggerVP)
        self.player.triggers.append(self.triggerFA)
        self.player.triggers.append(self.triggerReset)


class the_joker(persona_frame.persona):
    name = "The Joker"
    text = "Once during each of your turns, you may destory a Villain you have played this turn.  If you do, draw a card and ATTACK:: Each foe gains a Weakness."
    image = "fe/images/personas/The Joker MC.jpg"
    attack_text = "ATTACK:: Each foe gains a Weakness."
    action = None

    def ai_overvalue(self, card):
        if card.ctype_eq(cardtype.VILLAIN):
            return persona_frame.overvalue()
        return 0

    def special_action_click(self, player):
        instruction_text = "You may destory one of the villains you\nhave played this turn.  If you do, draw a card and Attack::\nEach foes gains a Weakness."
        assemble = []
        for c in player.played.played_this_turn:
            if c.ctype_eq(cardtype.VILLAIN):
                assemble.append(c)
        result = effects.may_choose_one_of(instruction_text, player, assemble, ai_hint.IFBAD)
        if result != None:
            result.destroy(player)
            player.draw_card(from_card=False)
            for p in globe.boss.players:
                if p != player:
                    if effects.attack(p, self, player):
                        p.gain_a_weakness()
            self.player.played.special_options.remove(self.action)
            return True
        return False

    def trigger(self, ttype, data, player, active, immediate):
        if globe.DEBUG:
            print("test", self.name, flush=True)
        if trigger.test(not immediate,
                        trigger.PLAY,
                        self.trigger,
                        player, ttype) and data[0].ctype_eq(cardtype.VILLAIN):
            if globe.DEBUG:
                print("active", self.name, flush=True)
            self.action = actions.special_action("The Joker", self.special_action_click)
            player.played.special_options.append(self.action)
            player.triggers.remove(self.trigger)

    def ready(self):
        self.player.triggers.append(self.trigger)

    def ai_is_now_a_good_time(self):
        if self.action in self.player.played.special_options:
            return self.special_action_click(self.player)
