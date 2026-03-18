from constants2 import CardType
from constants import owners
import effects
from constants import option
import globe
from constants import ai_hint
import random
from frames import actions
from frames import card_frame
from frames import persona_frame
from constants import trigger
import model


class acrobatic_agility(card_frame.card):
    name = "Acrobatic Agility"
    vp = 1
    cost = 1
    ctype = CardType.SUPERPOWER
    defense = True
    text = "+1 Power.  Defense: You may discard this card from your hand to avoid an Attack."
    image = "tt/images/cards/Acrobatic Agility 1.jpg"

    def play_action(self, player: model.player):
        self._plus_power(player, 1)
        return 0

    def defend(self, attacker: model.player = None, defender: model.player = None):
        defender.discard_a_card(self)
        return


class aqualad(card_frame.card):
    name = "Aqualad"
    vp = 1
    cost = 3
    ctype = CardType.HERO
    text = "Ongoing: You may discard this card from play.  If you do, put a card with cost 5 or less from your discard pile on top of your deck."
    image = "tt/images/cards/aqualad 3.jpg"
    ongoing = True

    def special_action_click(self, player: model.player):
        it = "Put a card with cost 5 or less from your discard pile on top of your deck."
        player.discard_a_card(self)
        cards = []
        for c in player.discard.contents:
            if c.cost <= 5:
                cards.append(c)
        if len(cards) > 0:
            to_put_on_deck = effects.choose_one_of(it, player, cards, source=self, hint=ai_hint.BEST)
            player.deck.add(to_put_on_deck.pop_self())
        player.played.special_options.remove(self.action)

    def play_action(self, player):
        if self not in player.ongoing.contents:
            player.ongoing.add(self.pop_self())
        self.action = actions.special_action("Aqualad", self.special_action_click, self)
        player.played.special_options.append(self.action)
        return 0


class arsenal(card_frame.card):
    name = "Arsenal"
    vp = 1
    cost = 1
    ctype = CardType.HERO
    text = "Super-Villains cost you 2 less to defeat this turn."
    image = "tt/images/cards/Arsenal.jpg"

    def trigger(self, ttype, data: list, player: model.player, active, immediate):
        if trigger.test(immediate,
                        trigger.PRICE,
                        self.trigger,
                        player, ttype) and data[1].owner_type == owners.VILLAINDECK:
            if globe.DEBUG:
                print("active", self.name, flush=True)
            return data[0] - 2

    def play_action(self, player):
        player.triggers.append(self.trigger)
        return 0


class azarath(card_frame.card):
    name = "Azarath"
    vp = 1
    cost = 5
    ctype = CardType.LOCATION
    text = "Ongoing: Once during each of your turns, you may discard a card from your hand.  If you do, Attack: Each foe discards a card."
    image = "tt/images/cards/Azarath 5.jpg"
    ongoing = True
    attack = True

    def special_action_click(self, player: model.player):
        it = "You may discard a card from your hand.  If you do, Attack: Each foe discards a card."
        if len(player.hand.contents) > 0:
            to_discard = effects.choose_one_of(it, player, player.hand.contents, source=self, hint=ai_hint.WORST)
            if to_discard:
                player.discard_a_card(to_discard)
                self.attack_action(player)
                player.played.special_options.remove(self.action)

    def attack_action(self, by_player: model.player):
        it = "Discard a card."
        for p in globe.boss.players:
            if p != by_player and effects.attack(p, self):
                if len(p.hand.contents) > 0:
                    to_discard = effects.choose_one_of(it, p, p.hand.contents, ai_hint.WORST)
                    p.discard_a_card(to_discard)

    def play_action(self, player: model.player):
        if self not in player.ongoing.contents:
            player.ongoing.add(self.pop_self())
        self.action = actions.special_action("Azarath", self.special_action_click, self)
        player.played.special_options.append(self.action)
        return 0


class azarath_metrion_zinthos(card_frame.card):
    name = "Azarath Metrion Zinthos"
    vp = 1
    cost = 5
    ctype = CardType.SUPERPOWER
    text = "Ongoing: You may discard this card from play.  If you do, put a card with cost 4 or less from your discard pile into your hand."
    image = "tt/images/cards/Azarath Metrion Zinthos 5.jpg"
    ongoing = True

    def special_action_click(self, player: model.player):
        it = "Put a card with cost 4 or less from your discard pile into your hand."
        player.discard_a_card(self)
        cards = []
        for c in player.discard.contents:
            if c.cost <= 4:
                cards.append(c)
        if len(cards) > 0:
            to_put_in_hand = effects.choose_one_of(it, player, cards, source=self, hint=ai_hint.BEST)
            player.hand.add(to_put_in_hand.pop_self())
        player.played.special_options.remove(self.action)

    def play_action(self, player: model.player):
        if self not in player.ongoing.contents:
            player.ongoing.add(self.pop_self())
        self.action = actions.special_action("Azarath Metrion\nZinthos", self.special_action_click, self)
        player.played.special_options.append(self.action)
        return 0


class birdarang(card_frame.card):
    name = "Birdarang"
    vp = 1
    cost = 1
    ctype = CardType.EQUIPMENT
    text = "If you control a Hero, +2 Power."
    image = "tt/images/cards/Birdarang 1.jpg"

    def play_action(self, player: model.player):
        for c in player.controls():
            if c.ctype_eq(CardType.HERO):
                self._plus_power(player, 2)
                break
        return 0


class bumblebee(card_frame.card):
    name = "Bumblebee"
    vp = 1
    cost = 2
    ctype = CardType.HERO
    text = "Ongoing: You may discard this card from play.  If you do, +1 Power."
    image = "tt/images/cards/Bumblebee 2.jpg"
    ongoing = True

    def special_action_click(self, player: model.player):
        it = "Put a card with cost 4 or less from your discard pile into your hand."
        player.discard_a_card(self)
        self._plus_power(player, 1)
        player.played.special_options.remove(self.action)

    def play_action(self, player: model.player):
        if self not in player.ongoing.contents:
            player.ongoing.add(self.pop_self())
        self.action = actions.special_action("Bumblebee", self.special_action_click, self)
        player.played.special_options.append(self.action)
        return 0


class bunker(card_frame.card):
    name = "Bunker"
    vp = 1
    cost = 4
    ctype = CardType.HERO
    text = "Reveal the top three cards of your deck.  Put one card of each type into your hand, and discard the rest."
    image = "tt/images/cards/Bunker 4.jpg"

    def play_action(self, player: model.player):
        it = "Choose one card of each type to put into your hand."
        cards : list[card_frame.card]= player.reveal_card(True, 3)
        for t in CardType.valid_cardtypes():
            this_type = []
            for c in cards:
                if c.ctype_eq(t):
                    this_type.append(c)
            if len(this_type) == 1:
                player.hand.add(this_type[0].pop_self())
                cards.remove(this_type[0])
            elif len(this_type) > 0:
                to_put_in_hand = effects.choose_one_of(f"Which {t} do you want to put in your hand?", player, this_type,
                                                       source=self, hint=ai_hint.BEST)
                player.hand.add(to_put_in_hand.pop_self())
                cards.remove(to_put_in_hand)
        for c in cards:
            player.discard_a_card(c)
        return 0


class cadmus_labs(card_frame.card):
    name = "Cadmus Labs"
    vp = 2
    cost = 6
    ctype = CardType.LOCATION
    text = "Ongoing: Once during each of your turns, choose a Hero or Villain with cost 3 or less you control. Put it into your hand."
    image = "tt/images/cards/Cadmus Labs 6.jpg"
    ongoing = True

    def special_action_click(self, player: model.player):
        it = "Choose a Hero or Villain with cost 3 or less you control. Put it into your hand."
        cards = []
        for c in player.controls():
            if (c.ctype_eq(CardType.HERO) or c.ctype_eq(CardType.VILLAIN)) and c.cost <= 3:
                cards.append(c)
        if len(cards) > 0:
            to_put_in_hand = effects.choose_one_of(it, player, cards, source=self, hint=ai_hint.BEST)
            player.hand.add(to_put_in_hand.pop_self())
            player.played.special_options.remove(self.action)

    def play_action(self, player):
        if self not in player.ongoing.contents:
            player.ongoing.add(self.pop_self())
        self.action = actions.special_action("Cadmus Labs", self.special_action_click, self)
        player.played.special_options.append(self.action)
        return 0


class cassie_sandsmark(card_frame.card):
    name = "Cassie Sandsmark"
    vp = 1
    cost = 5
    ctype = CardType.HERO
    text = "+2 Power and an additional +1 Power for each different Equipment you control."
    image = "tt/images/cards/Cassie Sandsmark 5.jpg"

    def play_action(self, player: model.player):
        self._plus_power(player, 2)
        card_names = set()
        for c in player.controls():
            if c.ctype_eq(CardType.EQUIPMENT):
                if c.name not in card_names:
                    card_names.add(c.name)
                    self._plus_power(player, 1)
        return 0


class cinderblock(card_frame.card):
    name = "Cinderblock"
    vp = 1
    cost = 3
    ctype = CardType.VILLAIN
    text = "Draw a card.  You may put a Defense card from your discard pile on you of your deck."
    image = "tt/images/cards/Cinderblock 3.jpg"

    def play_action(self, player: model.player):
        it = "You may put a Defense card from your discard pile on you of your deck."
        player.draw_card()
        cards = []
        for c in player.discard.contents:
            if c.defense:
                cards.append(c)
        if len(cards) > 0:
            put_on_top_of_deck = effects.may_choose_one_of(it, player, cards, source=self, hint=ai_hint.BEST)
            if put_on_top_of_deck:
                player.deck.add(put_on_top_of_deck.pop_self())
        return 0


class cloak_of_raven(card_frame.card):
    name = "Cloak Of Raven"
    vp = 1
    cost = 5
    ctype = CardType.HERO
    text = "+2 Power and an additional +1 Power for each different Super Power you control."
    image = "tt/images/cards/Cloak of Raven 5.jpg"

    def play_action(self, player: model.player):
        self._plus_power(player, 2)
        card_names = set()
        for c in player.controls():
            if c.ctype_eq(CardType.SUPERPOWER):
                if c.name not in card_names:
                    card_names.add(c.name)
                    self._plus_power(player, 1)
        return 0


class colony_suit(card_frame.card):
    name = "Colony Suit"
    vp = 1
    cost = 2
    ctype = CardType.EQUIPMENT
    text = "+1 Power. You may discard an Ongoing card you control.  If you do, additional +2 Power."
    image = "tt/images/cards/Colony Suit.jpg"

    def play_action(self, player: model.player):
        it = "You may discard an Ongoing card you control.  If you do, additional +2 Power."
        self._plus_power(player, 1)
        if len(player.ongoing.contents) > 0:
            card_to_discard = effects.may_choose_one_of(it, player, player.ongoing.contents, source=self,
                                                        hint=ai_hint.IFBAD)
            if card_to_discard:
                player.discard_a_card(card_to_discard)
                self._plus_power(player, 2)
        return 0


class conner_kent(card_frame.card):
    name = "Conner Kent"
    vp = 2
    cost = 6
    ctype = CardType.HERO
    text = "+1 Power. You may discard an Ongoing card you control.  If you do, additional +2 Power."
    image = "tt/images/cards/Conner Kent 6.jpg"

    def play_action(self, player: model.player):
        it = "Put up to two Super powers from your discard pile into your hand."
        cards = []
        for c in player.discard.contents:
            if c.ctype_eq(CardType.SUPERPOWER):
                cards.append(c)
        cards_taken = 0
        while len(cards) > 0 and cards_taken < 2:
            card_to_put_in_hand = effects.may_choose_one_of(f"{it} ({cards_taken + 1}/2)", player, cards, source=self, hint=ai_hint.BEST)
            if card_to_put_in_hand is not None:
                player.hand.add(card_to_put_in_hand.pop_self())
            else:
                break
        return 0


class cybernetic_enhancement(card_frame.card):
    name = "Cybernetic Enhancement"
    vp = 1
    cost = 3
    ctype = CardType.EQUIPMENT
    text = "+1 Power for each ongoing card you control."
    image = "tt/images/cards/Cybernetic Enhancement 3.jpg"

    def play_action(self, player: model.player):
        self._plus_power(player, len(player.ongoing.contents))
        return 0


class daughter_of_trigon(card_frame.card):
    name = "Daughter Of Trigon"
    vp = 2
    cost = 7
    ctype = CardType.HERO
    text = "You pay 1 less to defeat Villains and Super-Villains this turn for each different card type you control."
    image = "tt/images/cards/Daughter of Trigon.jpg"

    def trigger(self, ttype, data: list, player: model.player, active, immediate):
        if trigger.test(immediate,
                        trigger.PRICE,
                        self.trigger,
                        player, ttype) and (
                data[1].owner_type == owners.VILLAINDECK or data[1].ctype_eq(CardType.VILLAIN)):
            if globe.DEBUG:
                print("active", self.name, flush=True)
            card_types = set()
            for c in player.controls():
                card_types.update(set(c.get_ctype()))
            return data[0] - len(card_types.intersection(CardType.valid_cardtypes()))

    def play_action(self, player):
        player.triggers.append(self.trigger)
        return 0


class demonic_influence(card_frame.card):
    name = "Demonic Influence"
    vp = 1
    cost = 5
    ctype = CardType.SUPERPOWER
    text = "+2 Power and an additional +1 Power for each different Villain you control."
    image = "tt/images/cards/Demonic Influence 5.jpg"

    def play_action(self, player: model.player):
        villain_names = set()
        for c in player.controls():
            if c.ctype_eq(CardType.VILLAIN):
                villain_names.add(c.name)
        self._plus_power(player, 2 + len(villain_names))
        return 0


class detonator(card_frame.card):
    name = "detonator"
    vp = 1
    cost = 3
    ctype = CardType.EQUIPMENT
    text = "Ongoing: You may discard this card from play.  If you do, destroy a card in your discard pile."
    image = "tt/images/cards/Detonator 3.jpg"
    ongoing = True

    def special_action_click(self, player: model.player):
        it = "You may discard this card from play.  If you do, destroy a card in your discard pile."
        it2 = "Destroy a card in your discard pile."
        if effects.ok_or_no(it, player, self, ai_hint.ALWAYS):
            player.discard_a_card(self)
            if len(player.discard.contents) > 0:
                to_destroy = effects.choose_one_of(it2, player, player.discard.contents, source=self,
                                                   hint=ai_hint.WORST)
                to_destroy.destroy(player)
            player.played.special_options.remove(self.action)

    def play_action(self, player):
        if self not in player.ongoing.contents:
            player.ongoing.add(self.pop_self())
        self.action = actions.special_action("Detonator", self.special_action_click, self)
        player.played.special_options.append(self.action)
        return 0


class dick_greyson(card_frame.card):
    name = "Dick Grayson"
    vp = 0
    cost = 6
    ctype = CardType.HERO
    text = "+2 Power. At the end of the game, this card is worth 1 VP for each different Ongoing card in your deck."
    image = "tt/images/cards/Dick Grayson 6.jpg"

    def play_action(self, player: model.player):
        self._plus_power(player, 2)
        return 0

    def calculate_vp(self, all_cards: list[card_frame.card]):
        card_names = set()
        count = 0
        for card in all_cards:
            if card.ongoing:
                card_names.add(card.name)
        return len(card_names)


class energy_absorption(card_frame.card):
    name = "Energy Absorption"
    vp = 1
    cost = 4
    ctype = CardType.SUPERPOWER
    text = "Draw a card, and then you may destroy a card in your hand."
    image = "tt/images/cards/Energy Absorption 4.jpg"

    def play_action(self, player: model.player):
        it = "You may destroy a card in your hand."
        player.draw_card()
        if len(player.hand.contents):
            print("!! energy absorbtion")
            print(player.hand.contents)
            to_destroy = effects.may_choose_one_of(it, player, player.hand.contents, source=self, hint=ai_hint.IFBAD)
            if to_destroy:
                to_destroy.destroy(player)
        return 0


# tested
class flight_wings(card_frame.card):
    name = "Flight Wings"
    vp = 1
    cost = 4
    ctype = CardType.EQUIPMENT
    text = "+2 Power\nYou may put cards you buy or gain this turn on top of your deck."
    image = "tt/images/cards/Flight Wings 4.jpg"

    def trigger(self, ttype, data, player: model.player, active, immediate):
        if trigger.test(immediate,
                        trigger.GAIN_CARD,
                        self.trigger,
                        player, ttype) and data[0] is False and effects.ok_or_no(
            f"Would you like to put {data[1].name} on top of your deck?", player, data[1],
            ai_hint.ALWAYS):
            if globe.DEBUG:
                print("active", self.name, flush=True)
            player.deck.contents.append(data[1])
            return True  # True means that the card should not go into the discard pile

    def play_action(self, player: model.player):
        self._plus_power(player, 2)
        player.triggers.append(self.trigger)
        return 0


# tested
class garfield_logan(card_frame.card):
    name = "Gardield Logan"
    vp = 1
    cost = 5
    ctype = CardType.HERO
    text = "Ongoing: Once during each of your turns, choose a card type.  The next card you play or discard this turn also has that card type this turn."
    image = "tt/images/cards/Garfield Logan 5.jpg"
    ongoing = True
    affected_cards = []

    def trigger(self, ttype, data: list[card_frame.card], player: model.player, active, immediate):
        if trigger.test(immediate, trigger.BEFORE_PLAY, self.trigger, player, ttype):
            player.triggers.remove(self.trigger)

            local_cardtype = self.next_card_type

            # this prevents infinite loops if for any way this is triggered twise on the same card.
            if data[0].ctype_eq(local_cardtype):
                print("already has this same type" , flush=True)
                return

            def replace_get_ctype(true_self=data[0]):
                print("Using modified get_ctype", flush=True)
                all_type = [local_cardtype]
                all_type.extend(true_self.old_get_ctype())
                return all_type

            # def replace_ctype_eq(card_type: CardType, true_self=data[0]):
            #     print("DHFDKSF")
            #     print(card_type)
            #     print(local_cardtype)
            #     if card_type == local_cardtype:
            #         return True
            #     return true_self.old_ctype_eq(card_type)

            data[0].old_get_ctype = data[0].get_ctype
            data[0].old_ctype_eq = data[0].ctype_eq

            data[0].get_ctype = replace_get_ctype
            # data[0].ctype_eq = replace_ctype_eq

            print("BEFORE PLAY:", flush=True)
            print(data[0].name, flush=True)
            print(data[0].__dict__)
            print(dir(data[0]))
            print(data[0].get_ctype(), flush=True)

            self.affected_cards.append(data[0])
            player.triggers.append(self.cleanup_trigger)

    def cleanup_trigger(self, ttype, data, player: model.player, active, immediate):
        print("testing for cleanup", flush=True)
        if trigger.test(not immediate, trigger.END_TURN, self.cleanup_trigger, player, ttype):
            print("CLEANUP triggered", flush=True)
            player.triggers.remove(self.cleanup_trigger)
            for c in self.affected_cards:
                print("CLEANUP", flush=True)

                c.get_ctype = c.old_get_ctype
                # c.ctype_eq = c.old_ctype_eq
                c.old_get_ctype = None

            self.affected_cards = []
        else:
            print("test rejected", flush=True)

    def special_action_click(self, player: model.player):
        it = "Choose a card type, The next card you play or discard this turn also has that card type this turn."
        self.next_card_type = effects.choose_one_of(it, player, list(CardType.valid_cardtypes()), source=self,
                                                    hint=ai_hint.RANDOM)
        player.triggers.append(self.trigger)
        player.played.special_options.remove(self.action)

    def play_action(self, player: model.player):
        if self not in player.ongoing.contents:
            player.ongoing.add(self.pop_self())
        self.action = actions.special_action("Garfield Logan", self.special_action_click, self)
        player.played.special_options.append(self.action)
        return 0


class geokinesis(card_frame.card):
    name = "GeoKinesis"
    vp = 1
    cost = 4
    ctype = CardType.SUPERPOWER
    text = "+2 Power. Attack: Each for discards an Ongoing card they control."
    attack = True
    attack_text = "Attack: Each for discards an Ongoing card they control."
    image = "tt/images/cards/geokinesisErrata.jpg"

    def play_action(self, player: model.player):
        self._plus_power(player, 2)
        self.attack_action(player)
        return 0

    def attack_action(self, by_player: model.player):
        for p in globe.boss.players:
            if p != by_player and effects.attack(p, self, by_player):
                cards = []
                for c in p.ongoing.contents:
                    if c.ongoing:
                        cards.append(c)
                if len(cards) > 0:
                    to_discard = effects.choose_one_of(self.attack_text, p, cards, source=self,
                                                       hint=ai_hint.WORST)
                    p.discard_a_card(to_discard)
        return


# tested
class gizmo(card_frame.card):
    name = "Gizmo"
    vp = 1
    cost = 2
    ctype = CardType.VILLAIN
    text = "+1 Power. If you control an Equipment, draw a card."
    image = "tt/images/cards/Gizmo.jpg"

    def play_action(self, player: model.player):
        self._plus_power(player, 1)
        print(f"Is in play area: {player.played.contents}", flush=True)
        for c in player.controls():
            print("Is in controls:", flush=True)
            print(c.name, flush=True)
            print(c.__dict__)
            print(dir(c))
            print(c.get_ctype(), flush=True)

            if c.ctype_eq(CardType.EQUIPMENT):
                player.draw_card()
                break
        return 0


class grant_wilson(card_frame.card):
    name = "Grant Wilson"
    vp = 1
    cost = 5
    ctype = CardType.VILLAIN
    text = "+2 Power and an additional +1 Power for each different Hero you control."
    image = "tt/images/cards/Grant Wilson 5.jpg"

    def play_action(self, player: model.player):
        villain_names = set()
        for c in player.controls():
            if c.ctype_eq(CardType.HERO):
                villain_names.add(c.name)
        self._plus_power(player, 2 + len(villain_names))
        return 0


class hive_agent(card_frame.card):
    name = "H.I.V.E. Agent"
    vp = 1
    cost = 1
    ctype = CardType.VILLAIN
    text = "If you control another Villain."
    image = "tt/images/cards/Hive Agent.jpg"

    def play_action(self, player: model.player):
        for c in player.controls():
            if c != self and c.ctype_eq(CardType.VILLAIN):
                self._plus_power(player, 2)
                break
        return 0


class hawk_and_dove(card_frame.card):
    name = "Hawk & Dove"
    vp = 1
    cost = 4
    ctype = CardType.HERO
    text = "+2 Power.  If there are two copies of the same card in play, additional +1 power."
    image = "tt/images/cards/Hawk and Dove 4.jpg"

    def play_action(self, player: model.player):
        self._plus_power(player, 2)
        cards_in_play = set()
        for p in globe.boss.players:
            for c in p.controls():
                if c.name in cards_in_play:
                    self._plus_power(player, 1)
                    return 0
                else:
                    cards_in_play.add(c.name)
        return 0


class inertia(card_frame.card):
    name = "Inertia"
    vp = 2
    cost = 6
    ctype = CardType.VILLAIN
    text = "Ongoing: Once during each of your turns, you may discard a card from your hand. if you do, draw a card."
    image = "tt/images/cards/Inertia 6.jpg"
    ongoing = True

    def special_action_click(self, player: model.player):
        it = "You may discard a card from your hand. if you do, draw a card."
        if len(player.hand.contents) > 0:
            to_dicard = effects.may_choose_one_of(it, player, player.hand.contents, source=self, hint=ai_hint.IFBAD)
            if to_dicard:
                player.discard_a_card(to_dicard)
                player.draw_card()
                player.played.special_options.remove(self.action)

    def play_action(self, player: model.player):
        if self not in player.ongoing.contents:
            player.ongoing.add(self.pop_self())
        self.action = actions.special_action("Inertia", self.special_action_click, self)
        player.played.special_options.append(self.action)
        return 0


class jaime_reyes(card_frame.card):
    name = "Jaime Reyes"
    vp = 1
    cost = 4
    ctype = CardType.HERO
    defense = True
    text = "+2 Power.  Defense: You may put this card in play, if you do, play it during your next turn."
    image = "tt/images/cards/Jaime Reyes.jpg"

    def play_action(self, player: model.player):
        if self.ongoing is False and self in player.ongoing.contents:
            pass  # could optionally add special trigger now
        else:
            self._plus_power(player, 2)
        return 0

    def cleanup_trigger(self, ttype, data, player: model.player, active, immediate):
        if trigger.test(not immediate, trigger.END_TURN, self.cleanup_trigger, player, ttype):
            player.triggers.remove(self.cleanup_trigger)
            player.discard_a_card(self, valid_tigger=False)

    def special_action_click(self, player: model.player):
        print("JR TRIGGERED", flush=True)
        player.played.special_options.remove(self.action)
        self.pop_self()
        player.played.play(self)
        

    def defend(self, attacker: model.player = None, defender: model.player = None):
        if self in defender.hand.contents:
            self.pop_self()
            defender.ongoing.add(self)
            self.action = actions.special_action("Jaime Reyes", self.special_action_click, self)
            defender.played.special_options.append(self.action)
            return True
        return False


class jericho(card_frame.card):
    name = "Jericho"
    vp = 1
    cost = 3
    ctype = CardType.HERO
    text = "+1 Power and choose a foe.  Attack: Gain the game text of one of that foe's Characters this turn."
    image = "tt/images/cards/jerichoErrata.jpg"
    attack = True
    taken_personas = []

    def special_action_click(self, player: model.player):
        it = "You may discard a card from your hand.  If you do, Attack: Each foe discards a card."
        if len(player.hand.contents) > 0:
            to_discard = effects.choose_one_of(it, player, player.hand.contents, source=self, hint=ai_hint.WORST)
            if to_discard:
                player.discard_a_card(to_discard)
                self.attack_action(player)
                player.played.special_options.remove(self.action)

    def attack_action(self, by_player: model.player):
        it = "Choose a foe to attack."
        foe = effects.choose_a_player(it, by_player, includes_self=False, source=self, hint=ai_hint.RANDOM)
        if effects.attack(foe, self, by_player=by_player):
            foe.persona.old_player = foe
            foe.persona.player = by_player
            foe.persona.ready()
            self.taken_personas.append(foe.persona)

    def cleanup_trigger(self, ttype, data, player: model.player, active, immediate):
        if trigger.test(not immediate, trigger.END_TURN, self.cleanup_trigger, player, ttype):
            for p in self.taken_personas:
                p.player = p.old_player

    def play_action(self, player: model.player):
        self._plus_power(player, 1)
        self.attack_action(player)
        return 0


class jinx(card_frame.card):
    name = "Jinx"
    vp = 2
    cost = 6
    ctype = CardType.VILLAIN
    text = "+1 Power and draw a card. Attack: Each foe discards an Ongoing card they control."
    attack = True
    attack_text = "Attack: Each for discards an Ongoing card they control."
    image = "tt/images/cards/Jinx 6.jpg"

    def play_action(self, player: model.player):
        self._plus_power(player, 1)
        player.draw_card()
        self.attack_action(player)
        return 0

    def attack_action(self, by_player: model.player):
        for p in globe.boss.players:
            if p != by_player and effects.attack(p, self, by_player):
                cards = []
                for c in p.ongoing.contents:
                    if c.ongoing:
                        cards.append(c)
                if len(cards) > 0:
                    to_discard = effects.choose_one_of(self.attack_text, p, cards, source=self,
                                                       hint=ai_hint.WORST)
                    p.discard_a_card(to_discard)
        return


class koriandr(card_frame.card):
    name = "Koriand'r"
    vp = 1
    cost = 5
    ctype = CardType.HERO
    text = "Gain a Super Power from the Line-Up and put it into your hand.  If you cannot, draw a card."
    image = "tt/images/cards/Koriandr 5.jpg"

    def play_action(self, player: model.player):
        it = "Gain a Super Power from the Line-Up and put it into your hand."
        cards = []
        for c in globe.boss.lineup.contents:
            if c.ctype_eq(CardType.SUPERPOWER):
                cards.append(c)
        if len(cards) > 0:
            into_hand = effects.choose_one_of(it, player, cards, source=self, hint=ai_hint.BEST)
            player.gain(into_hand)
            player.hand.add(into_hand.pop_self())
        else:
            player.draw_card()
        return 0


class lady_vic(card_frame.card):
    name = "Lady Vic"
    vp = 1
    cost = 4
    ctype = CardType.VILLAIN
    text = "Ongoing: You may discard this card from play.  If you do, +2 Power."
    image = "tt/images/cards/Lady Vic.jpg"
    ongoing = True

    def special_action_click(self, player: model.player):
        it = "You may discard this card from play.  If you do, +2 Power."
        if effects.ok_or_no(it, player, self, ai_hint.ALWAYS):
            player.discard_a_card(self)
            self._plus_power(player, 2)

    def play_action(self, player):
        if self not in player.ongoing.contents:
            player.ongoing.add(self.pop_self())
        self.action = actions.special_action("Lady Vic", self.special_action_click, self)
        player.played.special_options.append(self.action)
        return 0


class lasso_of_lightning(card_frame.card):
    name = "Lasso Of Lightning"
    vp = 1
    cost = 5
    ctype = CardType.EQUIPMENT
    text = "+1 Power.  You may put an Ongoing card from your discard pile into your hand."
    image = "tt/images/cards/Lasso Of Lightning.jpg"

    def play_action(self, player: model.player):
        it = "You may put an Ongoing card from your discard pile into your hand"
        cards = []
        for c in player.discard.contents:
            if c.ongoing:
                cards.append(c)
        if len(cards) > 0:
            into_hand = effects.may_choose_one_of(it, player, cards, source=self, hint=ai_hint.BEST)
            if into_hand:
                player.hand.add(into_hand.pop_self())
        return 0


class mad_mod(card_frame.card):
    name = "Mad Mod"
    vp = 1
    cost = 3
    ctype = CardType.VILLAIN
    text = "+2 Power.  You may discard an Ongoing card you control.  If you do choose a foe and Attack: That foe gains a Weakness."
    attack = True
    attack_text = "Attack: That foe gains a Weakness."
    image = "tt/images/cards/Mad Mod.jpg"

    def play_action(self, player: model.player):
        it = " You may discard an Ongoing card you control.  If you do choose a foe and Attack: That foe gains a Weakness."

        self._plus_power(player, 2)
        cards = []
        for c in player.controls():
            if c.ongoing:
                cards.append(c)
        if len(cards) > 0:
            to_discard = effects.may_choose_one_of(it, player, cards, source=self, hint=ai_hint.BEST)
            if to_discard:
                player.discard_a_card(to_discard)
                self.attack_action(player)
        return 0

    def attack_action(self, by_player: model.player):
        it2 = "Choose a foe and Attack: That foe gains a Weakness."
        p = effects.choose_a_player(it2, by_player, includes_self=False, source=self, hint=ai_hint.RANDOM)
        if effects.attack(p, self, by_player):
            p.gain_a_weakness()
        return


class magic_bracers(card_frame.card):
    name = "Magic Bracers"
    vp = 1
    cost = 2
    ctype = CardType.EQUIPMENT
    defense = True
    text = "+1 Power.  Defense: You may discard this card from your hand to avoid an Attack.  If you do, put an Ongoing card from your discard pile into your hand."
    image = "tt/images/cards/Magic Bracers.jpg"

    def play_action(self, player: model.player):
        self._plus_power(player, 1)
        return 0

    def defend(self, attacker: model.player = None, defender: model.player = None):
        it = "put an Ongoing card from your discard pile into your hand."
        if self not in defender.hand.contents:
            return False
        defender.discard_a_card(self)
        cards = []
        for c in defender.discard.contents:
            if c.ongoing:
                cards.append(c)
        if len(cards) > 0:
            into_hand = effects.choose_one_of(it, defender, cards, source=self, hint=ai_hint.BEST)
            defender.hand.add(into_hand.pop_self())
        return True


# DONE UP TO HERE

# Supervillans

class slade_wilson(card_frame.card):
    name = "Slade Wilson"
    vp = 4
    cost = 8
    ctype = CardType.VILLAIN
    text = "Ongoing: At the start of your turns, you may draw until you have five cards in your hand."
    image = "tt/images/cards/Slade Wilson 8.jpg"
    ongoing = True

    def play_action(self, player: model.player):
        it = "Would you like to draw until you have five cards in your hand?"
        if self not in player.ongoing.contents:
            player.ongoing.add(self.pop_self())
        else:
            if len(player.hand.contents) < 5:
                if effects.ok_or_no(f"{it}", player, self, ai_hint.ALWAYS):
                    player.draw_card(5 - len(player.hand.contents))
        return 0

class blackfire(card_frame.card):
    name = "Blackfire"
    vp = 6
    cost = 11
    ctype = CardType.VILLAIN
    text = "You may gain all Super Powers from the Line-Up and put one in your hand. if you choose not to, +3 Power."
    image = "tt/images/cards/blackfireSvErrata.jpg"

    def play_action(self, player):
        instruction_text_1 = "Would you like to gain all super powers in the line up (and put one in your hand)? if you choose not to, +3 Power."

        if effects.ok_or_no(instruction_text_1, player, self, ai_hint.ALWAYS):
            instruction_text_2 = "Choose a card to put in your hand."
            assemble = []
            for c in globe.boss.lineup.contents:
                if c.ctype_eq(CardType.SUPERPOWER):
                    assemble.append(c)
                    player.gain(c.pop_self())
                    
            if len(assemble) > 0:
                choosen = effects.choose_one_of(instruction_text_1, player, assemble, ai_hint.BEST)
                player.hand.add(choosen.pop_self())
        else:
            self._plus_power(player, 3)
        return 0
    
    def first_apearance(self):
        for p in globe.boss.players:
            if effects.attack(p, self):
                assemble = []
                for c in p.hand.contents:
                    if c.ctype_eq(CardType.SUPERPOWER):
                        assemble.append(c)
                for c in p.ongoing.contents:
                    if c.ctype_eq(CardType.SUPERPOWER):
                        assemble.append(c)
                if len(assemble) > 0:
                    card_to_add = effects.choose_one_of("Choose a card to put in the lineup", p, assemble, ai_hint.WORST)
                    card_to_add.set_owner(owners.LINEUP)
                    globe.boss.lineup.add(card_to_add.pop_self())
                else:
                    p.gain_a_weakness()
        return


class brother_blood(card_frame.card):
    name = "Brother Blood"
    vp = 6
    cost = 11
    ctype = CardType.VILLAIN
    text = "You may gain all Villains from the Line-Up and put one in your hand. if you choose not to, +3 Power."
    image = "tt/images/cards/Brother Blood 11.jpg"
    ongoing = True

    def play_action(self, player):
        instruction_text_1 = "Would you like to gain all villains in the line up (and put one in your hand)? if you choose not to, +3 Power."

        if effects.ok_or_no(instruction_text_1, player, self, ai_hint.ALWAYS):
            instruction_text_2 = "Choose a card to put in your hand."
            assemble = []
            for c in globe.boss.lineup.contents:
                if c.ctype_eq(CardType.VILLAIN):
                    assemble.append(c)
                    player.gain(c.pop_self())
                    
            if len(assemble) > 0:
                choosen = effects.choose_one_of(instruction_text_1, player, assemble, ai_hint.BEST)
                player.hand.add(choosen.pop_self())
        else:
            self._plus_power(player, 3)
        return 0
    
    def first_apearance(self):
        for p in globe.boss.players:
            if effects.attack(p, self):
                assemble = []
                for c in p.hand.contents:
                    if c.ctype_eq(CardType.VILLAIN):
                        assemble.append(c)
                for c in p.ongoing.contents:
                    if c.ctype_eq(CardType.VILLAIN):
                        assemble.append(c)
                for c in p.ongoing.contents:
                    if c.ctype_eq(CardType.VILLAIN):
                        assemble.append(c)
                if len(assemble) > 0:
                    card_to_add = effects.choose_one_of("Choose a card to put in the lineup", p, assemble, ai_hint.WORST)
                    card_to_add.set_owner(owners.LINEUP)
                    globe.boss.lineup.add(card_to_add.pop_self())
        return
    
class cheshire(card_frame.card):
    name = "Cheshire"
    vp = 5
    cost = 10
    ctype = CardType.VILLAIN
    text = "You may gain a 1, 2, and 3 cost card from the Line-Up and put them into your hand.  If you choose not to, +3 Power."
    image = "tt/images/cards/Cheshire 10.jpg"

    def play_action(self, player):
        
        gained_card = False
        for cost in [1,2,3]:
            instruction_text = f"Would you like to gain a {cost} cost card from the lineup?"
            assemble = []
            for c in globe.boss.lineup.contents:
                if c.cost == cost:
                    assemble.append(c)
            result = effects.may_choose_one_of(instruction_text,player,assemble,ai_hint.IFGOOD)
            if result:
                player.gain(result.pop_self())
                gained_card = True
        if not gained_card:
            self._plus_power(player, 3)

    
    def first_apearance(self):
        for p in globe.boss.players:
            if effects.attack(p, self):
                assemble = []
                for c in p.hand.contents:
                    if c.cost in [1,2,3]:
                        assemble.append(c)
                for c in p.ongoing.contents:
                    if c.cost in [1,2,3]:
                        assemble.append(c)
                if len(assemble) > 0:
                    card_to_add = effects.choose_one_of("Choose a card to put in the lineup", p, assemble, ai_hint.WORST)
                    card_to_add.set_owner(owners.LINEUP)
                    globe.boss.lineup.add(card_to_add.pop_self())
                else:
                    p.gain_a_weakness()
        return

class clock_king(card_frame.card):
    name = "Clock King"
    vp = 5
    cost = 9
    ctype = CardType.VILLAIN
    text = "You may gain all Equipment from the Line-Up and put one in your hand. if you choose not to, +2 Power."
    image = "tt/images/cards/Clock King 9.jpg"

    def play_action(self, player):
        instruction_text_1 = "Would you like to gain all equipment in the line up (and put one in your hand)? if you choose not to, +3 Power."

        if effects.ok_or_no(instruction_text_1, player, self, ai_hint.ALWAYS):
            instruction_text_2 = "Choose a card to put in your hand."
            assemble = []
            for c in globe.boss.lineup.contents:
                if c.ctype_eq(CardType.EQUIPMENT):
                    assemble.append(c)
                    player.gain(c.pop_self())
                    
            if len(assemble) > 0:
                choosen = effects.choose_one_of(instruction_text_1, player, assemble, ai_hint.BEST)
                player.hand.add(choosen.pop_self())
        else:
            self._plus_power(player, 2)
        return 0
    
    def first_apearance(self):
        for p in globe.boss.players:
            if effects.attack(p, self):
                assemble = []
                for c in p.hand.contents:
                    if c.ctype_eq(CardType.EQUIPMENT):
                        assemble.append(c)
                for c in p.ongoing.contents:
                    if c.ctype_eq(CardType.EQUIPMENT):
                        assemble.append(c)
                if len(assemble) > 0:
                    card_to_add = effects.choose_one_of("Choose a card to put in the lineup", p, assemble, ai_hint.WORST)
                    card_to_add.set_owner(owners.LINEUP)
                    globe.boss.lineup.add(card_to_add.pop_self())
        return
    
class dr_light(card_frame.card):
    name = "Dr. Light"
    vp = 6
    cost = 12
    ctype = CardType.VILLAIN
    text = "+1 Power for each diferent color among cards in play."
    image = "tt/images/cards/Dr Light 12.jpg"

    def play_action(self, player: model.player):
        colors = set()
        for c in player.played.contents:
            # purposfully not doing get_ctype, as that would include inherited card types, which don't affect color
            colors.add(c.ctype)
        self._plus_power(player, len(colors))
        return 0
    
    def first_apearance(self):
        attack_avoided = False
        for p in globe.boss.players:
            if effects.attack(p, self):
                p.gain_a_weakness()
            else:
                self.attack_avoided = True
        if attack_avoided:
            globe.boss.supervillain_stack.shuffle()
            globe.boss.supervillain_stack.current_sv = globe.boss.supervillain_stack.contents[-1]
            # first apearance attack
            globe.boss.supervillain_stack.current_sv.first_apearance()
        return

class harvest(card_frame.card):
    name = "Harvest"
    vp = 5
    cost = 9
    ctype = CardType.VILLAIN
    text = "You may gain all Heros from the Line-Up and put one in your hand. if you choose not to, +2 Power."
    image = "tt/images/cards/Harvest 9.jpg"

    def play_action(self, player):
        instruction_text_1 = "Would you like to gain all heros in the line up (and put one in your hand)? if you choose not to, +3 Power."

        if effects.ok_or_no(instruction_text_1, player, self, ai_hint.ALWAYS):
            instruction_text_2 = "Choose a card to put in your hand."
            assemble = []
            for c in globe.boss.lineup.contents:
                if c.ctype_eq(CardType.HERO):
                    assemble.append(c)
                    player.gain(c.pop_self())
                    
            if len(assemble) > 0:
                choosen = effects.choose_one_of(instruction_text_1, player, assemble, ai_hint.BEST)
                player.hand.add(choosen.pop_self())
        else:
            self._plus_power(player, 2)
        return 0
    
    def first_apearance(self):
        for p in globe.boss.players:
            if effects.attack(p, self):
                assemble = []
                for c in p.hand.contents:
                    if c.ctype_eq(CardType.HERO):
                        assemble.append(c)
                for c in p.ongoing.contents:
                    if c.ctype_eq(CardType.HERO):
                        assemble.append(c)
                if len(assemble) > 0:
                    card_to_add = effects.choose_one_of("Choose a card to put in the lineup", p, assemble, ai_hint.WORST)
                    card_to_add.set_owner(owners.LINEUP)
                    globe.boss.lineup.add(card_to_add.pop_self())
        return

class psimon(card_frame.card):
    name = "Psimon"
    vp = 5
    cost = 10
    ctype = CardType.VILLAIN
    text = "Look at the top five cards of your deck, draw and play two of them, then put the rest back in any order."
    image = "tt/images/cards/Psimon 10.jpg"

    def play_action(self, player: model.player):
        assemble = []
        for i in range(5):
            to_add = player.reveal_card(public=False)
            if to_add is not None:
                assemble.append(to_add)
                player.deck.contents.pop()
        for i in range(2):
            if len(assemble) > 0:
                result = effects.choose_one_of(f"Play a card ({i+1}/2)", player, assemble, ai_hint.BEST)
                player.played.play(result)
                assemble.remove(result)

        total_times = len(assemble)
        while len(assemble) > 0:
            result = effects.choose_one_of(
                f"Place card back on top of your deck ({total_times - len(assemble) + 1}/{total_times})?", player,
                assemble, ai_hint.WORST)
            assemble.remove(result)
            player.deck.contents.append(result)
        return 0
    
    def first_apearance(self):
        cards_to_pass = []
        contributing_players = []
        for p in globe.boss.players:
            if effects.attack(p, self):
                contributing_players.append(p)

        for p in contributing_players:
            if len(p.hand.contents) <= 2:
                continue

            rejected_cards = []
            for c in p.hand.contents:
                rejected_cards.append(c)
            for i in range(2):
                if len(p.hand.contents) > 0:
                    result = effects.choose_one_of(f"Choose a card to keep ({i+1}/2)",p,rejected_cards,ai_hint.BEST)
                    rejected_cards.remove(result)
            cards_to_pass.append(rejected_cards)

        for i, p in enumerate(contributing_players):
            current = cards_to_pass[i - 1]
            while len(current) > 0:
                c = current.pop()
                c.pop_self()
                c.set_owner(p)
                p.hand.contents.append(c)
                contributing_players[i - 1].card_has_been_passed(c)

class superboy_prime(card_frame.card):
    name = "Superboy Prime"
    vp = 6
    cost = 12
    ctype = CardType.VILLAIN
    text = "+2 Power\nYou may swap your current Super Hero for one outside the game."
    image = "tt/images/cards/Superboy Prime 12.jpg"

    def play_action(self, player: model.player):
        self._plus_power(player, 2)

        result : persona_frame.persona = effects.may_choose_one_of("You may swap your persona with one outside of the game.",player,globe.boss.persona_list, hint=ai_hint.RANDOM, source=self)
        
        if result is None:
            return

        # This behavor intruduces a lot of bugs, since there has been no clean reset patten - personas were not built to cleanup themselevs.
        # The change of persona mid-turn is the issue here.  Any triggers/effects may not be cleaned up. until end-of-turn.
        

        globe.boss.persona_list.remove(result)
        result.active = player.persona.active
        result.set_owner(player)
        globe.boss.persona_list.append(player.persona)

        return 0
    
    def first_apearance(self):
        cards_to_pass = []
        contributing_players : list[model.player] = []
        for p in globe.boss.players:
            if effects.attack(p, self):
                contributing_players.append(p)

        for p in contributing_players:
            cards = p.reveal_card(True, 3)
            instruction_text_1 = "Choose a card to pass the the discard of the player on your left."
            instruction_text_2 = "Choose a card to destroy."

            if len(cards) == 0:
                continue
            card_to_pass = effects.choose_one_of(instruction_text_1, p, cards,ai_hint.WORST)
            cards.remove(card_to_pass)
            cards_to_pass.append(card_to_pass)
            if len(cards) == 0:
                continue
            to_destroy = effects.choose_one_of(instruction_text_2,p,cards,ai_hint.WORST)
            cards.remove(to_destroy)
            to_destroy.destroy(p)
            if len(cards) != 1:
                continue
            p.discard_a_card(cards[0])

        for i, p in enumerate(contributing_players):
            c = cards_to_pass[i - 1]
            c.pop_self()
            c.set_owner(p)
            p.discard.contents.append(c)
            contributing_players[i - 1].card_has_been_passed(c)

class terra(card_frame.card):
    name = "Terra"
    vp = 5
    cost = 10
    ctype = CardType.VILLAIN
    text = "Ongoing: Once during each of your turns, you may destroy a card you played this turn."
    image = "tt/images/cards/Terra 10.jpg"
    ongoing = True

    def special_action_click(self, player: model.player):
        it = "You may destroy a card you played this turn"
        if len(player.hand.contents) > 0:
            to_destroy : card_frame.card = effects.may_choose_one_of(it, player, player.played.contents, source=self, hint=ai_hint.IFBAD)
            if to_destroy:
                to_destroy.destroy(player)
                player.played.special_options.remove(self.action)

    def play_action(self, player: model.player):
        if self not in player.ongoing.contents:
            player.ongoing.add(self.pop_self())
        self.action = actions.special_action("Terra", self.special_action_click, self)
        player.played.special_options.append(self.action)
        return 0
    
    def first_apearance(self):
        for p in globe.boss.players:
            if effects.attack(p, self):
                assemble = []
                for c in p.ongoing.contents:
                    assemble.append(c)
                if len(assemble) > 0:
                    card_to_add = effects.choose_one_of("Destroy a card you control", p, assemble, ai_hint.WORST)
                    card_to_add.destroy(p)
                else:
                    p.gain_a_weakness()
        return

class the_brain_and_monsieur_mallah(card_frame.card):
    name = "The Brian & Monsieur Mallah"
    vp = 5
    cost = 10
    ctype = CardType.VILLAIN
    defense = True
    text = "Draw two card.  Defense: You may reveal this card from your ahnd to avoid an Attack."
    image = "tt/images/cards/The Brain And Monsieur Mallah 10.jpg"

    def play_action(self, player: model.player):
        player.draw_card(2)
        return 0

    def defend(self, attacker: model.player = None, defender: model.player = None):
        return
    
    def first_apearance(self):
        for p in globe.boss.players:
            if effects.attack(p, self):
                p.persona.active = False
        return

    def buy_action(self, player, bought, defeat):
        if defeat:
            for p in globe.boss.players:
                p.persona.active = True
        return True
    

class trigon(card_frame.card):
    name = "Trigon"
    vp = 6
    cost = 13
    ctype = CardType.VILLAIN
    text = "Stack Ongling:: At the start of each player's turn, that player gains a Weakness, and then puts a 0-cost card from their discard pile on top of their deck"
    image = "crossover_1/images/cards/Gog 15.jpg"
    has_stack_ongoing = True

    def stack_ongoing(self, player: model.player):
        player.gain_a_weakness()
        assemble = []
        for c in player.discard.contents:
            c : card_frame.card = c
            if c.cost == 0:
                assemble.append(c)
        
        if assemble > 0:
            result = effects.choose_one_of("Put a 0 cost card from your discard pile on top of your deck",player,assemble,ai_hint.BEST,source=self)
            player.deck.add(result.pop_self())

    def first_apearance(self):
        return
