from constants2 import CardType
import effects
from constants import ai_hint
import globe
from frames import persona_frame
from frames import actions
from constants import owners
from constants import trigger
import model


def get_personas():
    return [beast_boy(), blue_beatle(), raven(), red_robin(), starfire(), superboy(), wonder_girl()]


class beast_boy(persona_frame.persona):
    name = "Beast Boy"
    text = "Once during each of your turns, you may discard a card. If you do, put a non-Starter with that card type and cost 6 of less from your discard pile into your hand."
    image = "tt/images/personas/Beast Boy MC.jpg"
    action = None

    def special_action_click(self, player: model.player):
        if len(player.hand.contents) > 0:
            to_discard = effects.may_choose_one_of(self.text, player, player.hand.contents, source=self,
                                                   hint=ai_hint.IFBAD)
            if to_discard is not None:
                cards = []
                player.discard_a_card(to_discard)
                for c in player.discard.contents:
                    print(f"{to_discard.ctype_intersect(c)},  {not c.ctype_eq(CardType.STARTER)}, {c.cost <= 6}")
                    if to_discard.ctype_intersect(c) and not c.ctype_eq(CardType.STARTER) and c.cost <= 6:
                        cards.append(c)
                if len(cards) > 0:
                    to_put_in_hand = effects.choose_one_of(
                        "Put a non-Starter with that card type and cost 6 of less from your discard pile into your hand.",
                        player, cards, source=self, hint=ai_hint.BEST)
                    player.hand.add(to_put_in_hand.pop_self())
                self.player.played.special_options.remove(self.action)

    def ready(self):
        if self.active:
            self.action = actions.special_action("Beast Boy", self.special_action_click, self)
            self.player.played.special_options.append(self.action)

    def ai_is_now_a_good_time(self):
        return False


class blue_beatle(persona_frame.persona):
    name = "Blue Beatle"
    text = "Once during each of your turns, if you control seven or mote cards, draw a card."
    image = "tt/images/personas/Blue Beetle MC.jpg"
    action = None

    def special_action_click(self, player: model.player):
        if len(player.played) + len(player.ongoing) >= 7:
            player.draw_card(1, False, True)
            player.played.special_options.remove(self.action)

    def trigger(self, ttype, data, player: model.player, active, immediate):
        if trigger.test(not immediate, trigger.PLAY, self.trigger, player, ttype,
                        active) and len(player.played.contents) + len(player.ongoing.contents) >= 7:
            self.action = actions.special_action("Blue Beatle", self.special_action_click, self)
            player.played.special_options.append(self.action)
            player.triggers.remove(self.trigger)

    def ready(self):
        self.player.triggers.append(self.trigger)

    def ai_is_now_a_good_time(self):
        if self.action in self.player.played.special_options:
            return self.special_action_click(self.player)

# tested
class raven(persona_frame.persona):
    name = "Raven"
    text = "Once during each of your turns, if you control two or more villains, put a super power from your discard pile into your hand."
    image = "tt/images/personas/Raven MC.jpg"
    action = None

    def special_action_click(self, player: model.player):
        if player.played.get_count(CardType.VILLAIN) + player.ongoing.get_count(CardType.VILLAIN) >= 2:
            cards = []
            for c in player.discard.contents:
                if c.ctype_eq(CardType.SUPERPOWER):
                    cards.append(c)
            if len(cards) > 0:
                into_hand = effects.choose_one_of("Put a super power from your discard pile into your hand.", player,
                                                  cards, source=self, hint=ai_hint.BEST)
                player.hand.add(into_hand.pop_self())
                player.played.special_options.remove(self.action)

    def trigger(self, ttype, data, player: model.player, active, immediate):
        if trigger.test(not immediate, trigger.PLAY, self.trigger, player, ttype,
                        active) and player.played.get_count(CardType.VILLAIN) + player.ongoing.get_count(
            CardType.VILLAIN) >= 2:
            self.action = actions.special_action("Raven", self.special_action_click, self)
            player.played.special_options.append(self.action)
            player.triggers.remove(self.trigger)

    def ready(self):
        self.player.triggers.append(self.trigger)

    def ai_is_now_a_good_time(self):
        if self.action in self.player.played.special_options:
            return self.special_action_click(self.player)


class red_robin(persona_frame.persona):
    name = "Red Robin"
    text = "Once during each of your turns, if you control two or more Heros, +1 power and put an equipment from your discard pile into your hand."
    image = "tt/images/personas/Red Robin MC.jpg"
    action = None

    def special_action_click(self, player: model.player):
        if player.played.get_count(CardType.HERO) + player.ongoing.get_count(CardType.HERO) >= 2:
            player.played.plus_power(1)
            cards = []
            for c in player.discard.contents:
                if c.ctype_eq(CardType.EQUIPMENT):
                    cards.append(c)
            if len(cards) > 0:
                into_hand = effects.choose_one_of("Put an equipment from your discard pile into your hand.", player,
                                                  cards, source=self, hint=ai_hint.BEST)
                player.hand.add(into_hand.pop_self())
            player.played.special_options.remove(self.action)

    def trigger(self, ttype, data, player: model.player, active, immediate):
        if trigger.test(not immediate, trigger.PLAY, self.trigger, player, ttype,
                        active) and player.played.get_count(CardType.HERO) + player.ongoing.get_count(
            CardType.HERO) >= 2:
            self.action = actions.special_action("Red Robin", self.special_action_click, self)
            player.played.special_options.append(self.action)
            player.triggers.remove(self.trigger)

    def ready(self):
        self.player.triggers.append(self.trigger)

    def ai_is_now_a_good_time(self):
        if self.action in self.player.played.special_options:
            return self.special_action_click(self.player)


class starfire(persona_frame.persona):
    name = "Starfire"
    text = "Once during each of your turns, if you control four different card types, you may destroy a card you control."
    image = "tt/images/personas/Starfire TT MC.jpg"
    action = None

    def check_for_types(self, player):
        types = set()
        for c in player.played.contents:
            types.update(c.get_ctype())
        for c in player.ongoing.contents:
            types.update(c.get_ctype())
        if CardType.WEAKNESS in types:
            types.remove(CardType.WEAKNESS)
        if len(types) >= 4:
            return True
        return False

    def special_action_click(self, player: model.player):
        if self.check_for_types(player):
            cards = []
            cards.extend(player.played.contents)
            cards.extend(player.ongoing.contents)
            to_destroy = effects.may_choose_one_of("You may destroy a card in your control.", player, cards,
                                                   source=self, hint=ai_hint.IFBAD)
            if to_destroy is not None:
                to_destroy.destroy(player)
                player.played.special_options.remove(self.action)

    def trigger(self, ttype, data, player: model.player, active, immediate):
        if trigger.test(not immediate, trigger.PLAY, self.trigger, player, ttype,
                        active) and self.check_for_types(player):
            self.action = actions.special_action("Starfire", self.special_action_click, self)
            player.played.special_options.append(self.action)
            player.triggers.remove(self.trigger)

    def ready(self):
        self.player.triggers.append(self.trigger)

    def ai_is_now_a_good_time(self):
        if self.action in self.player.played.special_options:
            return self.special_action_click(self.player)


class superboy(persona_frame.persona):
    name = "Superboy"
    text = "Once during each of your turns, if you control two or more different Super Power, +1 power and draw a card."
    image = "tt/images/personas/Superboy MC.jpg"
    action = None

    def check_for_superpowers(self, player):
        names = set()
        for c in player.played.contents:
            if c.ctype_eq(CardType.SUPERPOWER):
                names.add(c.name)
        for c in player.ongoing.contents:
            if c.ctype_eq(CardType.SUPERPOWER):
                names.add(c.name)
        if len(names) >= 2:
            return True
        return False

    def special_action_click(self, player: model.player):
        if self.check_for_superpowers(player):
            player.played.plus_power(1)
            player.draw_card(1, from_card=False)
            player.played.special_options.remove(self.action)

    def trigger(self, ttype, data, player: model.player, active, immediate):
        if trigger.test(not immediate, trigger.PLAY, self.trigger, player, ttype,
                        active) and self.check_for_superpowers(player):
            self.action = actions.special_action("Superboy", self.special_action_click, self)
            player.played.special_options.append(self.action)
            player.triggers.remove(self.trigger)

    def ready(self):
        self.player.triggers.append(self.trigger)

    def ai_is_now_a_good_time(self):
        if self.action in self.player.played.special_options:
            return self.special_action_click(self.player)

# tested
class wonder_girl(persona_frame.persona):
    name = "Wonder Girl"
    text = "Once during each of your turns, if you control two or more equipment, draw two cards and then discard a card."
    image = "tt/images/personas/Wonder Girl MC.jpg"
    action = None

    def special_action_click(self, player: model.player):
        if player.played.get_count(CardType.EQUIPMENT) + player.ongoing.get_count(CardType.EQUIPMENT) >= 2:
            player.draw_card(2, from_card=False)
            if len(player.hand.contents) > 0:
                to_discard = effects.choose_one_of("Discard a card.",player,player.hand.contents,source=self,hint=ai_hint.WORST)
                player.discard_a_card(to_discard)
            player.played.special_options.remove(self.action)

    def trigger(self, ttype, data, player: model.player, active, immediate):
        print(f"WW: {player.played.get_count(CardType.EQUIPMENT)} {player.ongoing.get_count(CardType.EQUIPMENT)}", flush=True)
        if trigger.test(not immediate, trigger.PLAY, self.trigger, player, ttype,
                        active) and player.played.get_count(CardType.EQUIPMENT) + player.ongoing.get_count(
            CardType.EQUIPMENT) >= 2:
            self.action = actions.special_action("Wonder Girl", self.special_action_click, self)
            player.played.special_options.append(self.action)
            player.triggers.remove(self.trigger)

    def ready(self):
        self.player.triggers.append(self.trigger)

    def ai_is_now_a_good_time(self):
        if self.action in self.player.played.special_options:
            return self.special_action_click(self.player)
