import random

import effects
import globe
from constants import ai_hint
from constants import cardtype
from constants import owners
from constants import trigger
from frames import card_frame
from frames import actions
# import model

image_path = "hu/images/cards/"


### Equipment ###
class batarang(card_frame.card):
    name = "Batarang"
    vp = 1
    cost = 2
    ctype = cardtype.EQUIPMENT
    text = "+2 power"
    image = image_path + "Batarang.jpg"

    def play_action(self, player):
        self._plus_power(player, 2)
        return 0


class blue_lantern_power_ring(card_frame.card):
    name = "Blue Lantern Power Ring"
    vp = 0
    cost = 5
    ctype = cardtype.EQUIPMENT
    text = (
        "+1 Power and an additional +1 Power for each Hero in your discard "
        "pile and that you play or have played this turn. At end of game, "
        "this card is worth 1 VP for each Power Ring in your deck.")
    image = image_path + "Blue Lantern Power Ring.jpg"

    def trigger(self, ttype, data, player, active, immediate):
        if globe.DEBUG:
            print("test", self.name, flush=True)
        if trigger.test(not immediate, trigger.PLAY, self.trigger, player,
                        ttype) and data[0].ctype_eq(cardtype.HERO):
            if globe.DEBUG:
                print("active", self.name, flush=True)
            self._plus_power(player, 1)

    def play_action(self, player):
        power = 1
        for discarded_card in player.discard.contents:
            if discarded_card.ctype_eq(cardtype.HERO):
                power += 1
        for played_card in player.played.played_this_turn:
            if played_card.ctype_eq(cardtype.HERO):
                power += 1
        self._plus_power(player, power)
        player.triggers.append(self.trigger)
        return 0

    def calculate_vp(self, all_cards):
        count = 0
        for card in all_cards:
            if card.ctype_eq(
                    cardtype.EQUIPMENT) and "power ring" in card.name.lower():
                count += 1
        return count


class green_lantern_power_ring(card_frame.card):
    name = "Green Lantern Power Ring"
    vp = 0
    cost = 5
    ctype = cardtype.EQUIPMENT
    defense = True
    text = ("+2 Power. Defense: You may discard this card to avoid an Attack. "
            "If you do, draw two cards. At end of game, "
            "this card is worth 1 VP for each Power Ring in your deck.")
    image = image_path + "Green Lantern Power Ring.jpg"

    def play_action(self, player):
        self._plus_power(player, 2)
        return 0

    def defend(self, attacker=None, defender=None):
        self.owner.discard_a_card(self)
        self.owner.draw_card(2)
        return

    def calculate_vp(self, all_cards):
        count = 0
        for card in all_cards:
            if card.ctype_eq(
                    cardtype.EQUIPMENT) and "power ring" in card.name.lower():
                count += 1
        return count


class helmet_of_fate(card_frame.card):
    name = "Helmet of Fate"
    vp = 1
    cost = 3
    ctype = cardtype.EQUIPMENT
    defense = True
    text = ("+2 Power Defense: You may discard this card and any number of "
            "other cards to avoid an Attack. If you do, draw cards equal to "
            "the number of other cards discarded.")
    image = image_path + "Helmet of Fate.jpg"

    def play_action(self, player):
        self._plus_power(player, 2)
        return 0

    def defend(self, attacker=None, defender=None):
        instruction_text = ("You may discard this card and any number of "
                            "other cards to avoid an Attack. If you do, draw cards equal to "
                            "the number of other cards discarded")
        assemble = defender.hand.contents.copy()
        defender.discard_a_card(self)
        # cards_to_discard = effects.may_choose_one_of(
        #     instruction_text, player, collection, ai_hint.IFBAD
        # )
        assemble.remove(self)
        result = effects.choose_however_many(
            "Choose any number to discard", defender, assemble,
            ai_hint.IFBAD)
        if result is None:
            result = []
        for c in result:
            defender.discard_a_card(c)

        redraw = len(result)

        defender.draw_card(redraw)
        return


class indigo_tribe_power_ring(card_frame.card):
    name = "Indigo Tribe Power Ring"
    vp = 0
    cost = 5
    ctype = cardtype.EQUIPMENT
    text = ("+Power equal to the Power of a card you already played this "
            "turn. At end of game, this card is worth 1 VP for each Power "
            "Ring in your deck.")
    image = image_path + "Indigo Tribe Power Ring.jpg"

    def play_action(self, player):
        instruction_text = ("Power equal to the Power of a card you already "
                            "played this turn")
        assemble = []
        if len(player.played.played_this_turn) > 0:
            choosen = effects.choose_one_of(instruction_text, player, player.played.played_this_turn,
                                            source=self, hint=ai_hint.BEST)
            self._plus_power(player, choosen.power)
        return 0

    def calculate_vp(self, all_cards):
        count = 0
        for card in all_cards:
            if card.ctype_eq(
                    cardtype.EQUIPMENT) and "power ring" in card.name.lower():
                count += 1
        return count


class legion_flight_ring(card_frame.card):
    name = "Legion Flight Ring"
    vp = 1
    cost = 2
    ctype = cardtype.EQUIPMENT
    text = "Draw a Card"
    image = image_path + "Legion Flight Ring.jpg"

    def play_action(self, player):
        player.draw_card(1)
        return 0


class mind_control_hat(card_frame.card):
    name = "Mind Control Hat"
    vp = 2
    cost = 7
    attack = True
    attack_text = "Each foe discards a random card."
    ctype = cardtype.EQUIPMENT
    text = ("Draw two cards. Attack: Each foe discards a random card. "
            "If you play or have played Jervis Tetch this turn, you may play "
            "each Hero and Villain in the Line-Up, then return them to the "
            "Line-Up.")
    image = image_path + "Mind Control Hat.jpg"

    def jervis_played(self, player):
        assemble = []
        for c in globe.boss.lineup.contents:
            if c.ctype_eq(cardtype.HERO) or c.ctype_eq(cardtype.VILLAIN):
                assemble.append(c)
        played = []
        while len(assemble) > 0:
            to_play = effects.may_choose_one_of("Would you like to play each Hero and Villain in the Line-Up",
                                                player, assemble, source=self, hint=ai_hint.RANDOM)
            if to_play is None:
                break
            played.append(to_play)
            assemble.remove(to_play)
            to_play.pop_self()
            player.played.play(to_play)

        for c in played:
            globe.boss.lineup.add(c.pop_self())

    def trigger(self, ttype, data, player, active, immediate):
        if globe.DEBUG:
            print("test", self.name, flush=True)
        if trigger.test(not immediate,
                        trigger.PLAY,
                        self.trigger,
                        player, ttype) and (data[0].name == "Jervis Tetch"):
            if globe.DEBUG:
                print("Jervis Tetch played, triggering effect", self.name, flush=True)
            player.triggers.remove(self.trigger)
            self.jervis_played(player)

    def play_action(self, player):
        player.draw_card(2)
        self.attack_action(player)
        jervis_played = False
        instruction_text = ("If you play or have played Jervis Tetch "
                            "this turn, you may play "
                            "each Hero and Villain in the Line-Up, "
                            "then return them to the Line-Up.")
        assemble = []
        for card in player.played.played_this_turn:
            if card.name == "Jervis Tetch":
                jervis_played = True
                self.jervis_played(player)
                return 0
        player.triggers.append(self.trigger)
        return 0

    def attack_action(self, by_player):
        instruction_text = "Each foe discards a random card."
        for p in globe.boss.players:
            if p != by_player and effects.attack(p, self, by_player) and len(p.hand.contents) > 0:
                p.discard_a_card(random.choice(p.hand.contents))
        return


class orange_lantern_power_ring(card_frame.card):
    name = "Orange Lantern Power Ring"
    vp = 0
    cost = 5
    ctype = cardtype.EQUIPMENT
    text = ("You may gain an Equipment with cost 5 or less from the Line-Up "
            "and put it into your hand. If you choose not to, +2 Power. At end "
            "of game, this card is worth 1 VP for each Power Ring in your deck.")
    image = image_path + "Orange Lantern Power Ring.jpg"

    def play_action(self, player):
        instruction_text = "Choose a one of these to gain from the Line-Up"
        assemble = []
        for c in globe.boss.lineup.contents:
            if c.cost <= 5 and len(c.frozen) == 0 and c.ctype_eq(cardtype.EQUIPMENT):
                assemble.append(c)
        if len(assemble) > 0:
            choosen = effects.may_choose_one_of(instruction_text, player,
                                                assemble,
                                                source=self, hint=ai_hint.BEST)
            if choosen is not None:
                player.gain(choosen)
                player.hand.contents.append(choosen.pop_self())
            else:
                self._plus_power(player, 2)
        return 0

    def calculate_vp(self, all_cards):
        count = 0
        for card in all_cards:
            if card.ctype_eq(
                    cardtype.EQUIPMENT) and "power ring" in card.name.lower():
                count += 1
        return count


class red_lantern_power_ring(card_frame.card):
    name = "Red Lantern Power Ring"
    vp = 0
    cost = 5
    ctype = cardtype.EQUIPMENT
    text = ("Look at the top two cards of your deck. Leave one on top and "
            "destroy the other one. +Power equal to the destroyed card's cost. "
            "At end of game, this card is worth 1 VP for each Power Ring in "
            "your deck.")
    image = image_path + "Red Lantern Power Ring.jpg"

    def play_action(self, player):
        assemble = []
        for i in range(2):
            to_add = player.reveal_card(public=False, number=1)
            if to_add is not None:
                assemble.append(to_add)
                to_add.pop_self()
                # player.deck.contents.pop()
        if len(assemble) > 0:
            result = effects.choose_one_of(
                "Choose one to destroy", player, assemble,
                source=self, hint=ai_hint.IFBAD)
            # if result is not None:
            self._plus_power(player, result.cost)
            player.deck.contents.append(result)
            result.destroy(player)
            assemble.remove(result)

        while len(assemble) > 0:
            player.deck.contents.append(assemble.pop())
        return 0

    def calculate_vp(self, all_cards):
        count = 0
        for card in all_cards:
            if card.ctype_eq(
                    cardtype.EQUIPMENT) and "power ring" in card.name.lower():
                count += 1
        return count


class sciencell(card_frame.card):
    name = "Sciencell"
    vp = 0
    cost = 6
    ctype = cardtype.EQUIPMENT
    text = ("+2 Power. At end of game, this card is worth 1 VP for each "
            "different Villain in your deck.")
    image = image_path + "Sciencell.jpg"

    def play_action(self, player):
        self._plus_power(player, 2)

    def calculate_vp(self, all_cards):
        villians = set()
        for card in all_cards:
            if card.ctype_eq(cardtype.VILLAIN):
                villians.add(card.name)
        return len(villians)


class skeets(card_frame.card):
    name = "Skeets"
    vp = 1
    cost = 4
    ctype = cardtype.EQUIPMENT
    defense = True
    text = ("You may put a Hero from your discard pile on top of your deck. "
            "If you choose not to, draw a card. Defense: You may discard this "
            "card to avoid an attack. If you do, you may put a Hero from your "
            "discard pile into your hand or draw a card.")
    image = image_path + "Skeets.jpg"

    def play_action(self, player):
        instruction_text = "Choose a Hero from your discard pile to put onto your deck, if not draw a card."
        assemble = []
        for c in player.discard.contents:
            if c.ctype_eq(cardtype.HERO):
                assemble.append(c)
        if len(assemble) > 0:
            choosen = effects.may_choose_one_of(instruction_text, player,
                                                assemble,
                                                source=self, hint=ai_hint.BEST)
            if choosen:
                player.deck.add(choosen.pop_self())
                return 0
        player.draw_card(1)
        return 0

    def defend(self, attacker=None, defender=None):
        instruction_text = "You may put a Hero from your discard pile into your hand, if you choose not to, you may draw a card."
        self.owner.discard_a_card(self)
        assemble = []
        for c in defender.discard.contents:
            if c.ctype_eq(cardtype.HERO):
                assemble.append(c)
        if len(assemble) > 0:
            choosen = effects.may_choose_one_of(instruction_text, defender,
                                                assemble,
                                                source=self, hint=ai_hint.BEST)
            if choosen:
                defender.hand.contents.append(choosen)
            else:
                answer = effects.ok_or_no("Would you like to draw a card?", defender, self, ai_hint.ALWAYS)
                if answer:
                    defender.draw_card(1)
        return


class soultaker_sword(card_frame.card):
    name = "Soultaker Sword"
    vp = 1
    cost = 4
    ctype = cardtype.EQUIPMENT
    text = ("+2 Power. You may destroy a card in your hand.")
    image = image_path + "Soultaker Sword 4.jpg"

    def play_action(self, player):
        instruction_text = "You may destroy a card in your hand."
        self._plus_power(player, 2)
        if len(player.hand.contents) > 0:
            card_to_destroy = effects.may_choose_one_of(instruction_text, player,
                                                        player.hand.contents,
                                                        source=self, hint=ai_hint.IFBAD)
            if card_to_destroy:
                card_to_destroy.destroy(player)
        return 0


class star_sapphire_power_ring(card_frame.card):
    name = "Star Sapphire Power Ring"
    vp = 0
    cost = 5
    ctype = cardtype.EQUIPMENT
    text = ("Reveal the top two cards of your deck. If they share a card "
            "type, put them back in any order. If not, draw them. At end of "
            "game, this card is worth 1 VP for each Power Ring in your deck.")
    image = image_path + "Star Sapphire Power Ring.jpg"

    def play_action(self, player):
        assemble = []
        for i in range(2):
            to_add = player.reveal_card(public=False)
            if to_add != None:
                assemble.append(to_add)
                player.deck.contents.pop()
        if assemble[0].ctype == assemble[1].ctype:
            while len(assemble) > 0:
                result = effects.choose_one_of(
                    f"Place card back on top of your deck.",
                    player, assemble, source=self, hint=ai_hint.WORST)
                assemble.remove(result)
                player.deck.contents.append(result)
        else:
            num_to_draw = len(assemble)
            player.hand.contents.extend(assemble)
            player.draw_card(num_to_draw)

        return 0


class white_lantern_power_battery(card_frame.card):
    name = "White Lantern Power Battery"
    vp = 2
    cost = 7
    ctype = cardtype.EQUIPMENT
    text = ("Gain all Power Rings in the Line-Up and put them into your hand. "
            "Then gain any card from the Line-Up and put it on top of your deck.")
    image = image_path + "White Lantern Power Battery.jpg"

    def play_action(self, player):
        assemble = []
        for card in globe.boss.lineup.contents.copy():
            if "power ring" in card.name.lower():
                player.gain(card, None, False)
                player.hand.contents.append(card.pop_self())
            else:
                assemble.append(card)

        instruction_text = "Gain any card from the Line-Up and put it on top of your deck."
        if len(assemble) > 0:
            choosen = effects.choose_one_of(instruction_text, player, assemble,
                                            source=self, hint=ai_hint.BEST)
            player.gain(choosen)
            player.deck.contents.append(choosen.pop_self())

        return 0


class yellow_lantern_power_ring(card_frame.card):
    name = "Yellow Lantern Corps Power Ring"
    vp = 0
    cost = 5
    attack = True
    attack_text = " Each foe discards a card."
    ctype = cardtype.EQUIPMENT
    text = ("+2 Power. Attack: Each foe discards a card. At end of game, "
            "this card is worth 1 VP for each Power Ring in your deck.")
    image = image_path + "Yellow Lantern Corps Power Ring.jpg"

    def play_action(self, player):
        self._plus_power(player, 2)
        self.attack_action(player)
        return 0

    def attack_action(self, by_player):
        instruction_text = "Each foe discards a card."
        for p in globe.boss.players:
            if p != by_player and effects.attack(p, self, by_player) and len(p.hand.contents) > 0:
                choosen = effects.choose_one_of(instruction_text, p,
                                                p.hand.contents,
                                                source=self, hint=ai_hint.WORST)
                p.discard_a_card(choosen)
        return

    def calculate_vp(self, all_cards):
        count = 0
        for card in all_cards:
            if card.ctype_eq(
                    cardtype.EQUIPMENT) and "power ring" in card.name.lower():
                count += 1
        return count


### Hero ###
class crimson_whirlwind(card_frame.card):
    name = "Crimson Whirlwind"
    vp = 1
    cost = 5
    ctype = cardtype.HERO
    text = ("+2 Power. You may put your deck into your discard pile.")
    image = image_path + "Crimson Whirlwind.jpg"

    def play_action(self, player):
        self._plus_power(player, 2)
        choice = effects.ok_or_no(f"Would you like to put your deck into your"
                                  f"discard pile?", player, self,
                                  ai_hint.ALWAYS)
        if choice:
            # I don't think this should count as discarding cards
            for card in player.deck.contents.copy():
                player.discard.contents.append(card.pop_self())
        return 0


class daughter_of_gotham_city(card_frame.card):
    name = "Daughter of Gotham City"
    vp = 1
    cost = 3
    ctype = cardtype.HERO
    text = ("+1 Power. You may put up to two Punch cards from your discard "
            "pile into your hand.")
    image = image_path + "Daughter of Gotham City.jpg"

    def play_action(self, player):
        self._plus_power(player, 1)

        punches = []
        if len(player.discard.contents) > 0:
            for card in player.discard.contents:
                if card.name == "Punch":
                    punches.append(card)
        received = 0
        while len(punches) > 0 and received < 2:
            instruction_text = f"Select up to two Punch cards to put into your hand. ({received + 1}/2)"
            choosen = effects.may_choose_one_of(instruction_text, player,
                                                punches, source=self, hint=ai_hint.ALWAYS)
            if choosen:
                player.hand.add(choosen.pop_self())
                punches.remove(choosen)
                received += 1
            else:
                break
        return 0


class deadman(card_frame.card):
    name = "Deadman"
    vp = 1
    cost = 4
    ctype = cardtype.HERO
    text = ("+2 Power. When you buy or gain this card, you may destroy up to "
            "two cards in our hand and/or discard pile.")
    image = image_path + "Deadman.jpg"

    def trigger(self, ttype, data, player, active, immediate):
        if trigger.test(not immediate, trigger.GAIN_CARD, self.trigger, player,
                        ttype) and data[1] == self:
            if globe.DEBUG:
                print("active", self.name, flush=True)
            collection = player.hand.contents.copy()
            collection.extend(player.discard.contents)

            destroyed = 0
            while len(collection) > 0 and destroyed < 2:
                instruction_text = f"You may destroy a card in your hand or discard pile ({destroyed + 1}/2)"
                card_to_destroy = effects.may_choose_one_of(instruction_text,
                                                            player, collection,
                                                            source=self, hint=ai_hint.IFBAD)
                if card_to_destroy is not None:
                    collection.remove(card_to_destroy)
                    card_to_destroy.destroy(player)
                    destroyed += 1
                else:
                    break

    def play_action(self, player):
        self._plus_power(player, 2)
        return 0

    def buy_action(self, player, bought, defeat):
        # player.gain_redirect.append(self.solomon_grundy_redirect)
        player.triggers.append(self.trigger)
        # Assume that card can be bought
        return True


class hawkgirl(card_frame.card):
    name = "Hawkgirl"
    vp = 1
    cost = 2
    ctype = cardtype.HERO
    text = ("+1 Power and an additional +1 Power for each Hero in your "
            "discard pile.")
    image = image_path + "Hawkgirl.jpg"

    def play_action(self, player):
        count = 1
        for card in player.discard.contents:
            if card.ctype_eq(cardtype.HERO):
                count += 1
        self._plus_power(player, count)
        return 0


class hero_of_the_future(card_frame.card):
    name = "Hero of the Future"
    vp = 1
    cost = 4
    ctype = cardtype.HERO
    text = ("+2 Power and an additional +2 Power for each Defense card you "
            "play or have played this turn.")
    image = image_path + "Hero of the Future.jpg"

    def trigger(self, ttype, data, player, active, immediate):
        if trigger.test(not immediate, trigger.PLAY, self.trigger, player,
                        ttype) and data[0].defense:
            if globe.DEBUG:
                print("active", self.name, flush=True)
            self._plus_power(player, 2)

    def play_action(self, player):
        self._plus_power(player, 2)
        player.triggers.append(self.trigger)
        for card in player.played.played_this_turn:
            if card.defense:
                self._plus_power(player, 2)
        return 0


class jason_blood(card_frame.card):
    name = "Jason Blood"
    vp = 2
    cost = 7
    ctype = cardtype.HERO
    text = ("+3 Power. You may put a Villain from your discard pile on top of "
            "your deck.")
    image = image_path + "Jason Blood.jpg"

    def play_action(self, player):
        instruction_text = "You may put a Villain from your discard pile on top of your deck."
        self._plus_power(player, 3)
        villians = []
        for card in player.discard.contents:
            if card.ctype_eq(cardtype.VILLAIN):
                villians.append(card)
        if len(villians) > 0:
            choosen = effects.may_choose_one_of(instruction_text, player,
                                                villians, source=self, hint=ai_hint.BEST)
            if choosen:
                player.deck.add(choosen.pop_self())
        return 0


class katana(card_frame.card):
    name = "Katana"
    vp = 1
    cost = 2
    ctype = cardtype.HERO
    defense = True
    text = ("+1 Power. Defense: You may discard this card to avoid an Attack. "
            "If you do, draw a card.")
    image = image_path + "Katana.jpg"

    def play_action(self, player):
        self._plus_power(player, 1)
        return 0

    def defend(self, attacker=None, defender=None):
        self.owner.discard_a_card(self)
        self.owner.draw_card(1)
        return


class kyle_rayner(card_frame.card):
    name = "Kyle Rayner"
    vp = 2
    cost = 7
    ctype = cardtype.HERO
    text = ("+3 Power. For each Power Ring in your discard pile or that you "
            "play or have played this turn, +2 Power. If you play or have "
            "played three Power Rings this turn, you win the game.")
    image = image_path + "Kyle Rayner.jpg"

    def trigger(self, ttype, data, player, active, immediate):
        if globe.DEBUG:
            print("test", self.name, flush=True)
        if trigger.test(not immediate, trigger.PLAY, self.trigger, player,
                        ttype) and "power ring" in data[0].name.lower():
            if globe.DEBUG:
                print("active", self.name, flush=True)
            self._plus_power(player, 2)
            count = 0
            for card in player.played.played_this_turn:
                if "power ring" in card.name.lower():
                    count += 1
            if count >= 3:
                print("Game ended due to power rings")
                player.vp += 1000
                # TODO: Find a better way to end the game.
                while len(globe.boss.supervillain_stack.contents) > 0:
                    globe.boss.supervillain_stack.contents.pop()

    def play_action(self, player):
        self._plus_power(player, 3)
        player.triggers.append(self.trigger)
        rings = []
        count = 0
        for card in player.discard.contents:
            if "power ring" in card.name.lower():
                rings.append(card)
        for card in player.played.played_this_turn:
            if "power ring" in card.name.lower():
                rings.append(card)
                count += 1
        self._plus_power(player, len(rings)*2)
        if count >= 3:
            # TODO: Find a better way to end the game.
            while len(globe.boss.supervillain_stack.contents) > 0:
                globe.boss.supervillain_stack.contents.pop()
        return 0


class plastic_man(card_frame.card):
    # Ruling on plastic man: https://boardgamegeek.com/thread/1331763/plastic-man-errata-card
    # He only gains the game text, not the name or type
    name = "Plastic Man"
    vp = 1
    cost = 3
    ctype = cardtype.HERO
    text = ("Choose an Equipment in your discard pile or that you played this "
            "turn. Plastic Man gains the game text of that card this turn.")
    image = image_path + "Plastic Man.jpg"
    copy_of = None

    def play_action(self, player):
        equipments = []
        for card in player.discard.contents:
            if card.ctype_eq(cardtype.EQUIPMENT):
                equipments.append(card)
        for card in player.played.played_this_turn:
            if card.ctype_eq(cardtype.EQUIPMENT):
                equipments.append(card)
        if len(equipments) > 0:
            choosen = effects.choose_one_of(self.text, player, equipments,
                                            source=self, hint=ai_hint.BEST)

            # There are edge cases where this wont work as expected.  For example, If the Indigo Tribe Power Ring is used on Plastic Man, he will always give 0 power.
            choosen.play_action(player)

            # self.backup_play_action = self.play_action
            # self.play_action = choosen.play_action

        # BEST            # sets the card name to the Equipment name
        #             self.name = choosen.name
        #
        #             # sets the ctype to the Equipment ctype
        #             self.ctype = choosen.ctype
        #
        #             # Making a backup reference of the
        #             # Card image to revert for end turn
        #             self.copy_of = self.texture

        # # setting the Card image as the Equipment card image
        # self.texture = choosen.texture

        return 0

    # def end_of_turn(self):
    #     pass
        # reverting the card back to the original
        # might be a better way to do so
        # if self.copy_of:
        #     self.name = "Plastic Man"
        #     self.ctype = cardtype.HERO
        #     self.texture = self.copy_of
        # self.play_action = self.backup_play_action


class raven(card_frame.card):
    name = "Raven"
    vp = 1
    cost = 3
    ctype = cardtype.HERO
    text = ("+1 Power and draw a card.")
    image = image_path + "Raven.jpg"

    def play_action(self, player):
        self._plus_power(player, 1)
        player.draw_card(1)
        return 0


class saint_walker(card_frame.card):
    name = "Saint Walker"
    vp = 0
    cost = 5
    ctype = cardtype.HERO
    text = ("Draw a card. At end of game, this card is worth 1 VP for each "
            "different Hero in your deck.")
    image = image_path + "Saint Walker.jpg"

    def play_action(self, player):
        player.draw_card(1)
        return 0

    def calculate_vp(self, all_cards):
        heroes = set()
        for card in all_cards:
            if card.ctype_eq(cardtype.HERO):
                heroes.add(card.name)
        return len(heroes)


class sonic_siren(card_frame.card):
    name = "Sonic Siren"
    vp = 1
    cost = 4
    ctype = cardtype.HERO
    text = ("+2 Power. You may destroy a card in the Line-Up and replace it.")
    image = image_path + "Sonic Siren 4.jpg"

    def play_action(self, player):
        self._plus_power(player, 2)
        if len(globe.boss.lineup.contents) > 0:
            instruction_text = "You may destroy a card in the Line-up."
            result = effects.may_choose_one_of(instruction_text, player,
                                               globe.boss.lineup.contents,
                                               source=self, hint=ai_hint.RANDOM)
            if result != None:
                result.destroy(player)
                card_to_add = globe.boss.main_deck.draw()
                if card_to_add != None:
                    globe.boss.lineup.add(card_to_add)
        return 0


class superboy(card_frame.card):
    name = "Superboy"
    vp = 1
    cost = 5
    ctype = cardtype.HERO
    text = (
        "+1 Power. Put a Super Power from your discard pile into your hand.")
    image = image_path + "Superboy.jpg"

    def play_action(self, player):
        instruction_text = "Put a Super Power from your discard pile into your hand"
        self._plus_power(player, 1)
        superpowers = []
        for card in player.discard.contents:
            if card.ctype_eq(cardtype.SUPERPOWER):
                superpowers.append(card)
        if len(superpowers) > 0:
            choosen = effects.choose_one_of(instruction_text, player, superpowers,
                                            source=self, hint=ai_hint.BEST)
            if choosen:
                player.hand.add(choosen.pop_self())
        return 0


class warrior_princess(card_frame.card):
    name = "Warrior Princess"
    vp = 2
    cost = 6
    ctype = cardtype.HERO
    text = ("+3 Power. If you play or have played one or more Starbolt cards "
            "this turn, gain a card from the Line-Up and put it into your hand.")
    image = image_path + "Warrior Princess.jpg"

    def trigger(self, ttype, data, player, active, immediate):
        instruction_text = "gain a card from the Line-Up and put it into your hand."
        if trigger.test(not immediate, trigger.PLAY, self.trigger, player,
                        ttype) and data[0].name == "Starbolt":
            if globe.DEBUG:
                print("active", self.name, flush=True)
            if len(globe.boss.lineup.content) > 0:
                choosen = effects.choose_one_of(instruction_text, player,
                                                globe.boss.lineup.contents,
                                                source=self, hint=ai_hint.BEST)
                if choosen:
                    player.gain(choosen)
                    player.hand.add(choosen.pop_self())
            player.triggers.remove(self.trigger)


    def play_action(self, player):
        instruction_text = "gain a card from the Line-Up and put it into your hand"
        self._plus_power(player, 3)
        for card in player.played.played_this_turn:
            if card.name == "Starbolt":
                if len(globe.boss.lineup.contents) > 0:
                    choosen = effects.choose_one_of(instruction_text, player,
                                                    globe.boss.lineup.contents,
                                                    source=self, hint=ai_hint.BEST)
                    player.gain(choosen, None, False)
                    player.hand.add(choosen.pop_self())
                return 0
        player.triggers.append(self.trigger)
        return 0


class winged_warrior(card_frame.card):
    name = "Winged Warrior"
    vp = 2
    cost = 6
    ctype = cardtype.HERO
    text = ("+2 Power. If you play or have played another Hero this turn, "
            "additional +3 Power.")
    image = image_path + "Winged Warrior.jpg"

    def trigger(self, ttype, data, player, active, immediate):
        if trigger.test(not immediate, trigger.PLAY, self.trigger, player,
                        ttype) and data[0].ctype_eq(cardtype.HERO):
            if globe.DEBUG:
                print("active", self.name, flush=True)
            self._plus_power(player, 3)
            player.triggers.remove(self.trigger)

    def play_action(self, player):
        self._plus_power(player, 2)
        played_hero = False
        for card in player.played.played_this_turn:
            if card.ctype_eq(cardtype.HERO):
                self._plus_power(player, 3)
                return 0
        player.triggers.append(self.trigger)
        return 0


class wonder_of_the_knight(card_frame.card):
    name = "Wonder of the Knight"
    vp = 1
    cost = 5
    ctype = cardtype.HERO
    text = (
        "Put an Equipment from your discard pile into your hand. Draw a card.")
    image = image_path + "Wonder of the Knight.jpg"

    def play_action(self, player):
        equipment = []
        for card in player.discard.contents:
            if card.ctype_eq(cardtype.EQUIPMENT):
                equipment.append(card)
        if len(equipment) > 0:
            choosen = effects.choose_one_of(self.text, player, equipment,
                                            source=self, hint=ai_hint.BEST)
            player.hand.add(choosen.pop_self())
        player.draw_card(1)
        return 0


class worlds_mightiest_mortal(card_frame.card):
    name = "World's Mightiest Mortal"
    vp = 3
    cost = 8
    ctype = cardtype.HERO
    text = ("+5 Power. Reveal the top two cards of the main deck. Put any "
            "number of them into the Line-Up and the rest back on top in any order.")
    image = image_path + "Worlds Mightiest Mortal.jpg"

    def play_action(self, player):
        self._plus_power(player, 5)
        top_cards = []
        for i in range(2):
            next_card = globe.boss.main_deck.contents[-1]
            if next_card is not None:
                next_card.pop_self()
                top_cards.append(next_card)
        effects.reveal("These two cards were on top of the main deck.", player, top_cards)
        while len(top_cards) > 0:
            result = effects.may_choose_one_of(
                f"You may put a card in the lineup.",
                player, top_cards, source=self, hint=ai_hint.RANDOM)
            if result:
                result.set_owner(owners.LINEUP)
                top_cards.remove(result)
                globe.boss.lineup.add(result)
            else:
                break

        while len(top_cards) > 0:
            result = effects.choose_one_of(
                f"Place card(s) back on top of the main deck.",
                player, top_cards, source=self, hint=ai_hint.RANDOM)
            top_cards.remove(result)
            result.set_owner(owners.MAINDECK)
            globe.boss.main_deck.add(result)
        return 0


### Locations ###
class apokolips(card_frame.card):
    name = "Apokolips"
    vp = 1
    cost = 5
    ctype = cardtype.LOCATION
    text = ("Ongoing: Once during each of your turns, reveal the top card of "
            "your deck. If it's a Villain, draw it. If not, you may discard it.")
    image = image_path + "Apokolips.jpg"
    ongoing = True

    def special_action_click(self, player):
        on_top = player.reveal_card()
        it = "Do you want to discard the card?"
        if on_top != None:
            if on_top.ctype_eq(cardtype.VILLAIN):
                player.draw_card()
            else:
                choosen = effects.ok_or_no(it, player, on_top, ai_hint.IFBAD)
                if choosen:
                    player.discard_a_card(on_top)
        player.played.special_options.remove(self.action)

    def play_action(self, player):
        if self not in player.ongoing.contents:
            player.ongoing.add(self.pop_self())
        self.action = actions.special_action("Apokolips", self.special_action_click)
        player.played.special_options.append(self.action)
        return 0


class gotham_city(card_frame.card):
    name = "Gotham City"
    vp = 1
    cost = 5
    ctype = cardtype.LOCATION
    text = ("Ongoing: Once during each of your turns, reveal the top card of "
            "your deck. If it's an Equipment, draw it. If not, you may discard "
            "it.")
    image = image_path + "Gotham City.jpg"
    ongoing = True

    def special_action_click(self, player):
        on_top = player.reveal_card()
        it = "Do you want to discard the card?"
        if on_top != None:
            if on_top.ctype_eq(cardtype.EQUIPMENT):
                player.draw_card()
            else:
                choosen = effects.ok_or_no(it, player, on_top, ai_hint.IFBAD)
                if choosen:
                    player.discard_a_card(on_top)
        player.played.special_options.remove(self.action)

    def play_action(self, player):
        if self not in player.ongoing.contents:
            player.ongoing.add(self.pop_self())
        self.action = actions.special_action("Gotham City", self.special_action_click)
        player.played.special_options.append(self.action)
        return 0


class metropolis(card_frame.card):
    name = "Metropolis"
    vp = 1
    cost = 5
    ctype = cardtype.LOCATION
    text = ("Ongoing: Once during each of your turns, reveal the top card of "
            "your deck. If it's a Super Power, draw it. If not, you may "
            "discard it.")
    image = image_path + "Metropolis Fixed.jpg"
    ongoing = True

    def special_action_click(self, player):
        on_top = player.reveal_card()
        it = "Do you want to discard the card?"
        if on_top != None:
            if on_top.ctype_eq(cardtype.SUPERPOWER):
                player.draw_card()
            else:
                choosen = effects.ok_or_no(it, player, on_top, ai_hint.IFBAD)
                if choosen:
                    player.discard_a_card(on_top)
        player.played.special_options.remove(self.action)

    def play_action(self, player):
        if self not in player.ongoing.contents:
            player.ongoing.add(self.pop_self())
        self.action = actions.special_action("Metropolis", self.special_action_click)
        player.played.special_options.append(self.action)
        return 0


class new_genesis(card_frame.card):
    name = "New Genesis"
    vp = 1
    cost = 5
    ctype = cardtype.LOCATION
    text = ("Ongoing: Once during each of your turns, reveal the top card of "
            "your deck. If it's a Hero, draw it. If not, you may discard it.")
    image = image_path + "New Genesis.jpg"
    ongoing = True

    def special_action_click(self, player):
        on_top = player.reveal_card()
        it = "Do you want to discard the card?"
        if on_top != None:
            if on_top.ctype_eq(cardtype.HERO):
                player.draw_card()
            else:
                choosen = effects.ok_or_no(it, player, on_top, ai_hint.IFBAD)
                if choosen:
                    player.discard_a_card(on_top)
        player.played.special_options.remove(self.action)

    def play_action(self, player):
        if self not in player.ongoing.contents:
            player.ongoing.add(self.pop_self())
        self.action = actions.special_action("New Genesis", self.special_action_click)
        player.played.special_options.append(self.action)
        return 0


class oa(card_frame.card):
    name = "OA"
    vp = 1
    cost = 5
    ctype = cardtype.LOCATION
    text = ("Ongoing: At the start of your turn, if the top card of the "
            "Super-Villain stack has cost 10 or greater, draw a card.")
    image = image_path + "OA.jpg"
    ongoing = True

    def play_action(self, player):
        if self in player.ongoing.contents:
            if globe.boss.supervillain_stack.contents[-1].cost >= 10:
                player.draw_card()
        else:
            player.ongoing.add(self.pop_self())
        return 0


### Super Powers ###
class canary_cry(card_frame.card):
    name = "Canary Cry"
    vp = 1
    cost = 4
    ctype = cardtype.SUPERPOWER
    defense = True
    text = (
        "You may put a Villain from your discard pile on top of your deck. "
        "If you choose not to, draw a card. Defense: You may discard this "
        "card to avoid an Attack. If you do, you may put a Villain with "
        "cost 7 or less from your discard pile into your hand or draw a "
        "card.")
    image = image_path + "Canary Cry 4.jpg"

    def play_action(self, player):
        instruction_text = ("You may put a Villain from your discard pile on "
                            "top of your deck.")
        villians = []
        choosen = None
        for card in player.discard.contents:
            if card.ctype_eq(cardtype.VILLAIN):
                villians.append(card)
        if len(villians) > 0:
            choosen = effects.may_choose_one_of(instruction_text, player, villians,
                                                source=self, hint=ai_hint.BEST)
        if choosen:
            player.deck.add(choosen.pop_self())
        else:
            player.draw_card()
        return 0

    def defend(self, attacker=None, defender=None):
        instruction_text = ("You may discard this "
                            "card to avoid an Attack. If you do, you may put a Villain with "
                            "cost 7 or less from your discard pile into your hand or draw a "
                            "card.")
        self.owner.discard_a_card(self)
        villians = []
        for card in defender.discard.contents:
            if card.ctype_eq(cardtype.VILLAIN) and card.cost <= 7:
                villians.append(card)
        if len(villians) > 0:
            choosen = effects.may_choose_one_of(instruction_text, defender, villians,
                                                source=self, hint=ai_hint.BEST)
            if choosen:
                defender.hand.add(choosen.pop_self())
            else:
                self.owner.draw_card()
        return


class force_field(card_frame.card):
    name = "Force Field"
    vp = 1
    cost = 3
    ctype = cardtype.SUPERPOWER
    defense = True
    text = ("Draw a card. Ongoing: Do not discard this card at the end of "
            "your turn. Defense: While this card is in play, you may put it "
            "into your discard pile to avoid an Attack.")
    image = image_path + "Force Field.jpg"
    ongoing = True

    # def trigger(self, ttype, data, player, active, immediate):
    #     player.draw_card()
    #     player.trigger.remove(self.trigger)

    def play_action(self, player):
        if self not in player.ongoing.contents:
            player.draw_card()
            player.ongoing.add(self.pop_self())
        return 0

    def defend(self, attacker=None, defender=None):
        defender.discard_a_card(self)
        return


class power_of_the_green(card_frame.card):
    name = "Power Of The Green"
    vp = 1
    cost = 3
    ctype = cardtype.SUPERPOWER
    text = ("Put a Location from your discard pile into play. If you control "
            "a Location, +3 Power. Otherwise, +2 Power.")
    image = image_path + "Power of the Green.jpg"

    def play_action(self, player):
        instruction_text = "Put a Location from your discard pile into play."
        locations = []
        power = 2
        for card in player.discard.contents:
            if card.ctype_eq(cardtype.LOCATION):
                locations.append(card)
        if len(locations) > 0:
            choosen = effects.choose_one_of(instruction_text, player, locations,
                                            source=self, hint=ai_hint.RANDOM)
            choosen.pop_self()
            player.played.play(choosen)
        if len(player.ongoing.contents) > 0:
            power = 3
        self._plus_power(player, power)
        return 0


class shazam(card_frame.card):
    name = "Shazam!"
    vp = 1
    cost = 7
    ctype = cardtype.SUPERPOWER
    text = ("+2 Power. Reveal and play the top card of the main deck, then "
            "return it to the top of the main deck.")
    image = image_path + "Shazam 7.jpg"
    top_card = None

    def play_action(self, player):
        self._plus_power(player, 2)
        instruction_text = (
            "Reveal and play the top card of the main deck, then "
            "return it to the top of the main deck.")
        top_card = globe.boss.main_deck.draw()
        player.play_and_return(top_card, globe.boss.main_deck)
        return 0


class starbolt(card_frame.card):
    name = "Starbolt"
    vp = 1
    cost = 5
    ctype = cardtype.SUPERPOWER
    text = ("+2 Power and an additional +1 Power for each Super Power in your "
            "discard pile.")
    image = image_path + "Starbolt.jpg"

    def play_action(self, player):
        power = 2
        for card in player.discard.contents:
            if card.ctype_eq(cardtype.SUPERPOWER):
                power += 1
        self._plus_power(player, power)
        return 0


class teleportation(card_frame.card):
    name = "Teleportation"
    vp = 1
    cost = 7
    ctype = cardtype.SUPERPOWER
    text = ("Gain the top card of the Main Deck and put it into your hand.")
    image = image_path + "Teleportation.jpg"

    def play_action(self, player):
        top_card = globe.boss.main_deck.draw()
        player.gain(top_card)
        player.hand.add(top_card.pop_self())
        return 0


class whirlwind(card_frame.card):
    name = "Whirlwind"
    vp = 1
    cost = 2
    ctype = cardtype.SUPERPOWER
    text = ("+1 Power. If this is the first card you have played this turn, "
            "you may discard your hand and draw four cards.")
    image = image_path + "Whirlwind.jpg"

    def play_action(self, player):
        self._plus_power(player, 1)
        if len(player.played.contents) <= 1:
            if effects.ok_or_no("Would you like to discard your hand and draw four cards?",
                                player, None, ai_hint.RANDOM):
                player.discard_hand()
                player.draw_card(4)
        return 0


### Super Villians ###
class amazo(card_frame.card):
    name = "Amazo"
    vp = 5
    cost = 10
    ctype = cardtype.VILLAIN
    owner_type = owners.VILLAINDECK
    text = ("You may choose another Villain and/or Hero you played this turn. "
            "Play them again this turn. If you choose not to, +3 Power. "
            "FIRST APPEARANCE -- ATTACK: Each player passes one card to the "
            "left and one card to the right. Put cards passed to you into "
            "your hand.")
    attack_text = ("Each player passes one card to the "
                   "left and one card to the right. Put cards passed to you into "
                   "your hand.")
    image = image_path + "Amazo 10.jpg"
    action = None

    def special_action_click(self, player):
        # if len(self.discarded_cards) > 0:
        result = False
        while result is not None and len(self.cards_to_play) > 0:
            result = effects.may_choose_one_of("Choose a card to play", player, self.cards_to_play, source=self, hint=ai_hint.BEST)
            if result is not None:
                player.play_and_return(result)

                self.cards_to_play.remove(result)
        if len(self.cards_to_play) == 0:
            player.played.special_options.remove(self.action)

    def play_action(self, player):
        cards = []
        self.cards_to_play = []
        instruction_text = ("You may choose another Villain and/or Hero you "
                            "played this turn. Play them again this turn. "
                            "If you choose not to, +3 Power. ")
        for card in player.played.played_this_turn:
            if card.ctype_eq(cardtype.HERO):
                cards.append(card)
        if len(cards) > 0:
            choice = effects.may_choose_one_of(instruction_text + "(1/2: Heros)", player,
                                               cards, source=self, hint=ai_hint.BEST)
            if choice is not None:
                self.cards_to_play.append(choice)
        cards = []
        for card in player.played.played_this_turn:
            if card.ctype_eq(cardtype.VILLAIN):
                cards.append(card)
        if len(cards) > 0:
            choice = effects.may_choose_one_of(instruction_text + "(2/2: Villains)", player,
                                               cards, source=self, hint=ai_hint.BEST)
            if choice is not None:
                self.cards_to_play.append(choice)
        if len(self.cards_to_play) == 0:
            self._plus_power(player, 3)
        else:
            self.action = actions.special_action("Amazo", self.special_action_click)
            player.played.special_options.append(self.action)

    def first_apearance(self):
        instruction_text = "Select a card to pass to the right."
        cards_to_pass = []
        instruction_text = "Choose a card to pass to the hand of the player to your left."
        contributing_players = []
        for p in globe.boss.players:
            if effects.attack(p, self):
                contributing_players.append(p)

        for p in contributing_players:
            card_set_to_pass = []
            if len(p.hand.contents) > 0:
                card_set_to_pass.append(
                    effects.choose_one_of("Choose a card to pass to the hand of the player to your left.", p,
                                          p.hand.contents, source=self, hint=ai_hint.WORST))
            else:
                card_set_to_pass.append(None)
            if len(p.hand.contents) > 0:
                card_set_to_pass.append(
                    effects.choose_one_of("Choose a card to pass to the hand of the player to your right.", p,
                                          p.hand.contents, source=self, hint=ai_hint.WORST))
            else:
                card_set_to_pass.append(None)
            cards_to_pass.append(card_set_to_pass)
        for i, p in enumerate(contributing_players):
            to_get = []
            to_get.append(cards_to_pass[i - 1][0])
            right_index = (i + 1)
            if right_index == len(contributing_players):
                right_index = 0
            to_get.append(cards_to_pass[right_index][1])
            for c in to_get:
                if c is not None:
                    c.pop_self()
                    c.set_owner(p)
                    p.hand.contents.append(c)
                    p.card_has_been_passed(c)


class arkillo(card_frame.card):
    name = "Arkillo"
    vp = 1
    cost = 10
    ctype = cardtype.VILLAIN
    owner_type = owners.VILLAINDECK
    text = ("+2 Power and put all Equipment from your discard pile into your "
            "hand. FIRST APPEARANCE -- ATTACK: Each player totals the cost of "
            "cards in his hand. The player(s) with the highest total gains "
            "three Weakness cards.")
    attack_text = (
        "FIRST APPEARANCE -- ATTACK: Each player totals the cost of "
        "cards in his hand. The player(s) with the highest total gains "
        "three Weakness cards.")
    image = image_path + "Arkillo 10.jpg"

    def play_action(self, player):
        self._plus_power(player, 2)
        for card in player.discard.contents:
            if card.ctype_eq(cardtype.EQUIPMENT):
                player.hand.add(card.pop_self())
        return 0

    def first_apearance(self):
        players = []
        for p in globe.boss.players:
            card_total = 0
            if effects.attack(p, self):
                for card in p.hand.contents:
                    card_total += card.cost
                players.append([p, card_total])
        players.sort(reverse=True, key=lambda x: x[1])
        if len(players) > 0:
            highest = players[0][1]
            p_gained = []
            for total in players:
                if total[1] == highest:
                    p_gained.append(total[0])
            for p in p_gained:
                p.gain_a_weakness()
                p.gain_a_weakness()
                p.gain_a_weakness()
        return


class black_adam(card_frame.card):
    name = "Black Adam"
    vp = 6
    cost = 11
    ctype = cardtype.VILLAIN
    owner_type = owners.VILLAINDECK
    text = ("+2 Power for each different card type you play or have played "
            "this turn. FIRST APPEARANCE -- ATTACK: Each player destroys a "
            "Hero in his hand or discard pile.")
    attack_text = ("FIRST APPEARANCE -- ATTACK: Each player destroys a "
                   "Hero in his hand or discard pile.")
    image = image_path + "Black Adam 11.jpg"

    # This was designed to be stateless, so that this can be played twice (like with plastic-man)
    def trigger(self, ttype, data, player, active, immediate):
        if trigger.test(not immediate, trigger.PLAY, self.trigger, player,
                        ttype):
            if data[0].ctype != cardtype.WEAKNESS:
                cards_played = set()
                for i in range(len(player.played.played_this_turn)-1):
                    cards_played.add(player.played.played_this_turn[i].ctype)
                if data[0].ctype not in cards_played:
                    self._plus_power(player, 2)

    def play_action(self, player):
        cards_played = set()
        for card in player.played.contents:
            if card.ctype != cardtype.WEAKNESS:
                cards_played.add(card.ctype)
        self._plus_power(player, len(cards_played) * 2)
        player.triggers.append(self.trigger)
        return 0

    def first_apearance(self):
        instruction_text = "Choose a hero to destroy."
        for p in globe.boss.players:
            if effects.attack(p, self):
                cards = []
                for card in p.hand.contents:
                    if card.ctype_eq(cardtype.HERO):
                        cards.append(card)
                for card in p.discard.contents:
                    if card.ctype_eq(cardtype.HERO):
                        cards.append(card)
                if len(cards) > 0:
                    card_to_destroy = effects.choose_one_of(instruction_text, p, cards,
                                                            source=self, hint=ai_hint.WORST)
                    card_to_destroy.destroy(p)
        return


class graves(card_frame.card):
    name = "Graves"
    vp = 5
    cost = 9
    ctype = cardtype.VILLAIN
    owner_type = owners.VILLAINDECK
    text = ("+4 Power and you may put a card from your discard pile on top of "
            "your deck. FIRST APPEARANCE -- ATTACK: Each player puts a card "
            "from his hand face down, then destroy those cards. If one player "
            "destroyed a card with cost higher than each other player, he "
            "draws two cards.")
    attack_text = ("FIRST APPEARANCE -- ATTACK: Each player puts a card "
                   "from his hand face down, then destroy those cards. If one player "
                   "destroyed a card with cost higher than each other player, he "
                   "draws two cards.")
    image = image_path + "Graves 9.jpg"

    def play_action(self, player):
        self._plus_power(player, 4)
        instruction_text = "Select a card to put on the top of your deck"
        if len(player.discard.contents) > 0:
            choosen = effects.may_choose_one_of(instruction_text, player,
                                                player.discard.contents,
                                                source=self, hint=ai_hint.RANDOM)
            if choosen:
                player.deck.add(choosen.pop_self())
        return 0

    def first_apearance(self):
        pcards = []
        it = "Select a card to be destroyed"
        for p in globe.boss.players:
            if effects.attack(p, self) and len(p.hand.contents) > 0:
                choosen = effects.choose_one_of(it, p, p.hand.contents,
                                                source=self, hint=ai_hint.WORST)
                pcards.append([p, choosen.cost])
                choosen.destroy(p)
        if len(pcards) > 0:
            pcards.sort(reverse=True, key=lambda x: x[1])
            highest = pcards[0][1]
            count = 0
            for x in pcards:
                if x[1] == highest:
                    count += 1
            if count == 1:
                pcards[0][0].draw_card(2)
        return


class hel(card_frame.card):
    name = "H'el"
    vp = 5
    cost = 9
    ctype = cardtype.VILLAIN
    owner_type = owners.VILLAINDECK
    text = ("Reveal and draw cards from the top of your deck until you have "
            "drawn 7 or greater cost worth of cards.  "
            "FIRST APPEARANCE -- ATTACK: Each player reveals the top three "
            "cards of his deck. Choose one of them with cost 1 or greater, "
            "then destroy it. Discard the rest.")
    attack_text = (
        "FIRST APPEARANCE -- ATTACK: Each player reveals the top three "
        "cards of his deck. Choose one of them with cost 1 or greater, "
        "then destroy it. Discard the rest.")
    image = image_path + "H El 9.jpg"

    def play_action(self, player):
        card_costs = 0
        while card_costs < 7:
            # card = player.reveal_card()
            drawn_card = player.draw_card()[0]
            effects.reveal(f"{player.persona.name} is drawing {drawn_card.name}",player,drawn_card)
            card_costs += drawn_card.cost
        return 0

    def first_apearance(self):
        instruction_text = ("choose one of them with cost 1 or greater, "
                            "then destroy it.")
        for p in globe.boss.players:
            if effects.attack(p, self):
                top_cards = []
                for i in range(3):
                    to_add = p.reveal_card()
                    if to_add is not None:
                        top_cards.append(to_add)
                        to_add.pop_self()
                    else:
                        break

                effects.reveal(f"There cards were on top of {p.persona.name}'s deck.",p,top_cards)

                to_maybe_destroy = []
                for card in top_cards:
                    if card.cost >= 1:
                        to_maybe_destroy.append(card)

                if len(to_maybe_destroy) > 0:
                    choosen = effects.choose_one_of(instruction_text, p, to_maybe_destroy, source=self, hint=ai_hint.WORST)
                    choosen.destroy(p)
                    top_cards.remove(choosen)
                for card in top_cards:
                    p.discard_a_card(card)
        return


class hector_hammond(card_frame.card):
    name = "Hector Hammond"
    vp = 6
    cost = 11
    ctype = cardtype.VILLAIN
    owner_type = owners.VILLAINDECK
    text = ("You may put up to two cards from your discard pile into your "
            "hand. If you choose not to, +3 Power. "
            "FIRST APPEARANCE -- ATTACK: Each player gains the top card of the "
            "main deck. If its cost is 4 or greater, they also gain two "
            "Weakness cards.")
    attack_text = (
        "FIRST APPEARANCE -- ATTACK: Each player gains the top card "
        "of the main deck. If its cost is 4 or greater, they also "
        "gain two Weakness cards.")
    image = image_path + "Hector Hammond 11.jpg"

    def play_action(self, player):
        instruction_text = ("You may put up to two cards from your discard "
                            "pile into your hand. If you choose not to, +3 "
                            "Power.")
        added = []
        for i in range(2):
            if len(player.discard.contents) > 0:
                choosen = effects.may_choose_one_of(instruction_text, player,
                                                    player.discard.contents,
                                                    source=self, hint=ai_hint.BEST)
                if choosen is not None:
                    player.hand.add(choosen.pop_self())
                    added.append(choosen)
                else:
                    break

        if len(added) == 0:
            self._plus_power(player, 3)
        return 0

    def first_apearance(self):
        for p in globe.boss.players:
            if effects.attack(p, self):
                card = globe.boss.main_deck.draw()
                p.gain(card)
                if card.cost >= 4:
                    p.gain_a_weakness()
                    p.gain_a_weakness()
        return


class helspont(card_frame.card):
    name = "Helspont"
    vp = 5
    cost = 10
    ctype = cardtype.VILLAIN
    owner_type = owners.VILLAINDECK
    text = ("You may put any number of cards of one card type and with cost 3 "
            "or less from your discard pile into your hand. If you choose not "
            "to, +3 Power. FIRST APPEARANCE -- ATTACK: Put a Location you "
            "control into your discard pile. If you cannot, discard two cards.")
    image = image_path + "Helspont 10.jpg"

    def play_action(self, player):
        cards = []
        it = (
            "You may put any number of cards of one card type and with cost 3 "
            "or less from your discard pile into your hand. If you choose not "
            "to, +3 Power.")
        choosen = None
        for card in player.discard.contents:
            if card.cost <= 3:
                cards.append(card)
        card_taken = False
        while len(cards) > 0:
            choosen = effects.may_choose_one_of(it, player, cards, source=self, hint=ai_hint.BEST)
            if choosen is None:
                break
            card_taken = True
            player.hand.add(choosen.pop_self())
            cards.remove(choosen)
        if not card_taken:
            self._plus_power(player, 3)
        return 0

    def first_apearance(self):
        it = "Discard a location you control"
        for p in globe.boss.players:
            if effects.attack(p, self):
                locations = []
                for card in p.ongoing.contents:
                    if card.ctype_eq(cardtype.LOCATION):
                        locations.append(card)
                if len(locations) > 0:
                    result = effects.choose_one_of(it, p, locations,
                                                   source=self, hint=ai_hint.WORST)
                    p.discard_a_card(result)
                else:
                    for i in range(2):
                        if len(p.hand.contents) > 0:
                            p.discard_a_card(
                                effects.choose_one_of(f"Discard a Card {i}/2", p, p.hand.contents,
                                                      source=self, hint=ai_hint.WORST))
        return


class mongul(card_frame.card):
    name = "Mongul"
    vp = 6
    cost = 11
    ctype = cardtype.VILLAIN
    owner_type = owners.VILLAINDECK
    text = ("+2 Power and draw two cards. Then destroy a card in your hand. "
            "FIRST APPEARANCE -- ATTACK: Each player discards a Power Ring or "
            "two random cards from his hand.")
    image = image_path + "Mongul 11.jpg"

    def play_action(self, player):
        self._plus_power(player, 2)
        player.draw_card(2)
        it = "Choose a card to destroy from your hand"
        if len(player.hand.contents) > 0:
            choosen = effects.choose_one_of(it, player, player.hand.contents,
                                            source=self, hint=ai_hint.WORST)
            choosen.destroy(player)
        return 0

    def first_apearance(self):
        for p in globe.boss.players:
            if effects.attack(p, self):
                cards = []
                it_ring = "You may discard a power right, if not, discard two random cards."
                it = "Select a random card to discard."
                has_ring = False
                for card in p.hand.contents:
                    if "power ring" in card.name.lower():
                        cards.append(card)

                if len(cards) > 0:
                    choosen = effects.may_choose_one_of(it_ring, p, cards,
                                                        source=self, hint=ai_hint.WORST)
                    if choosen is not None:
                        p.discard_a_card(choosen)
                        return
                for _ in range(2):
                    p.discard_a_card(random.choice(p.hand.contents))
        return


class mr_freeze(card_frame.card):
    name = "Mr. Freeze"
    vp = 5
    cost = 9
    ctype = cardtype.VILLAIN
    owner_type = owners.VILLAINDECK
    text = ("You may gain all Equipment from the Line-Up and put them into "
            "your hand. If you choose not to, +3 Power. "
            "FIRST APPEARANCE -- ATTACK: Destroy all Equipment in the Line-Up. "
            "Each player puts an Equipment from his hand or discard pile "
            "into the Line-Up.")
    image = image_path + "Mr Freeze 9.jpg"

    def play_action(self, player):
        it = ("You may gain all Equipment from the Line-Up and put them into "
              "your hand, (otherwise, +3 power)")
        cards = []
        choice = None
        for card in globe.boss.lineup.contents:
            if card.ctype_eq(cardtype.EQUIPMENT):
                cards.append(card)
        if len(cards) > 0:
            choice = effects.ok_or_no(it, player, None, ai_hint.ALWAYS)
            if choice:
                for card in cards:
                    player.gain(card)
                    player.hand.contents.append(card.pop_self())
                return 0
        self._plus_power(player, 3)
        return 0

    def first_apearance(self):
        it = "Choose a card to put into the lineup."
        for card in globe.boss.lineup.contents:
            if card.ctype_eq(cardtype.EQUIPMENT):
                card.destroy(None)

        for p in globe.boss.players:
            if effects.attack(p, self):
                cards = []
                for card in p.hand.contents:
                    if card.ctype_eq(cardtype.EQUIPMENT):
                        cards.append(card)
                for card in p.discard.contents:
                    if card.ctype_eq(cardtype.EQUIPMENT):
                        cards.append(card)
                if len(cards) > 0:
                    choosen = effects.choose_one_of(it, p, cards, source=self, hint=ai_hint.WORST)
                    choosen.set_owner(owners.LINEUP)
                    globe.boss.lineup.add(choosen.pop_self())
        return


class nekron(card_frame.card):
    name = "Nekron"
    vp = 6
    cost = 12
    ctype = cardtype.VILLAIN
    owner_type = owners.VILLAINDECK
    text = ("Destroy up to three cards in your hand and/or discard pile. "
            "For each you destroy, draw a card. "
            "FIRST APPEARANCE -- ATTACK: Each player totals the cost of the "
            "cards in his hand. The player(s) with the highest total destroys "
            "a random card in his hand. Each other player chooses and "
            "discards a card in his hand.")
    image = image_path + "Nekron 12.jpg"

    def play_action(self, player):

        it = ("Destroy up to three cards in your hand and/or discard pile. "
              "For each you destroy, draw a card.")
        cards = player.hand.contents.copy()
        cards.extend(player.discard.contents)

        destroyed_total = 0
        for i in range(3):
            if len(cards) > 0:
                choosen = effects.may_choose_one_of(it, player, cards,
                                                    source=self, hint=ai_hint.WORST)
                if choosen:
                    cards.remove(choosen)
                    choosen.destroy(player)
                    destroyed_total += 1
                else:
                    break
        if destroyed_total > 0:
            player.draw_card(destroyed_total)
        return 0

    def first_apearance(self):
        player_totals = []
        it = "Choose a card to discard"
        for p in globe.boss.players:
            if effects.attack(p, self):
                total_cost = 0
                for card in p.hand.contents:
                    total_cost += card.cost
                player_totals.append([p, total_cost])
        if len(player_totals) > 0:
            player_totals.sort(reverse=True, key=lambda x: x[1])
            for p in player_totals:
                if p[1] == player_totals[0][1]:
                    random.choice(p[0].hand.contents).destroy(p[0])
                elif len(p[0].hand.contents) > 0:
                    choosen = effects.choose_one_of(it, p[0], p[0].hand.contents,
                                                    source=self, hint=ai_hint.WORST)
                    p[0].discard_a_card(choosen)
        return


class trigon(card_frame.card):
    name = "Trigon"
    vp = 6
    cost = 12
    ctype = cardtype.VILLAIN
    owner_type = owners.VILLAINDECK
    text = ("Look at the top two cards of the main deck. Put one into your "
            "hand and the other on the bottom of the main deck. "
            "FIRST APPEARANCE -- ATTACK: Each player destroys a card with "
            "cost 1 or greater in his hand.")
    image = image_path + "Trigon 12.jpg"

    def play_action(self, player):
        it = "Choose a card to put into your hand, the other will be put on the bottom of the main text."
        top_cards = []
        for i in range(2):
            next_card = globe.boss.main_deck.contents[-1]
            if next_card is not None:
                next_card.pop_self()
                top_cards.append(next_card)
        if len(top_cards) > 0:
            choosen = effects.choose_one_of(it, player, top_cards, source=self, hint=ai_hint.BEST)
            player.gain(choosen)
            player.hand.add(choosen.pop_self())
            top_cards.remove(choosen)
        while len(top_cards) > 0:
            to_return = top_cards.pop()
            globe.boss.main_deck.add_bottom(to_return.pop_self())
        return 0

    def first_apearance(self):
        it = "Destroy a card with a cost of 1 or greater from your hand"
        for p in globe.boss.players:
            if effects.attack(p, self):
                cards = []
                for card in p.hand.contents:
                    if card.cost >= 1:
                        cards.append(card)
                if len(cards) > 0:
                    choosen = effects.choose_one_of(it, p, cards, source=self, hint=ai_hint.WORST)
                    choosen.destroy(p)
        return


class vandal_savage(card_frame.card):
    name = "Vandal Savage"
    vp = 4
    cost = 8
    ctype = cardtype.VILLAIN
    owner_type = owners.VILLAINDECK
    text = ("When you play this card, leave it in front of you for the rest "
            "of the game. Ongoing: +1 Power.")
    image = image_path + "Vandal Savage 8.jpg"
    ongoing = True

    def play_action(self, player):
        if self not in player.ongoing.contents:
            player.ongoing.add(self.pop_self())
        self._plus_power(player, 1)
        return 0


### Villains ###
class black_lantern_corps(card_frame.card):
    name = "Black Lantern Corps"
    vp = 2
    cost = 6
    ctype = cardtype.VILLAIN
    attack = True
    attack_text = "Each foe gains a Weakness"
    text = ("+2 Power. Attack: Each foe gains a Weakness. If one or more foes "
            "do not gain a Weakness, draw a card.")
    image = image_path + "Black Lantern Corps.jpg"

    def play_action(self, player):
        self._plus_power(player, 2)
        self.attack_action(player)
        return 0

    def attack_action(self, by_player):
        gained_a_weekness = 0
        for p in globe.boss.players:
            if p != by_player and effects.attack(p, self, by_player):
                if p.gain_a_weakness():
                    gained_a_weekness += 1
        if gained_a_weekness != len(globe.boss.players) - 1:
            by_player.draw_card()
        return


class brother_blood(card_frame.card):
    name = "Brother Blood"
    vp = 2
    cost = 6
    ctype = cardtype.VILLAIN
    text = ("+4 Power")
    image = image_path + "Brother Blood.jpg"

    def play_action(self, player):
        self._plus_power(player, 4)
        return 0


class deadshot(card_frame.card):
    name = "Deadshot"
    vp = 1
    cost = 2
    ctype = cardtype.VILLAIN
    attack = True
    attack_text = ("Reveal the top card of your deck. If it costs more than "
                   "1 discard it.")
    text = ("+1 Power. Attack: Each foe reveals the top card of his deck. "
            "If it costs 1 or greater, they discard it.")
    image = image_path + "Deadshot 2.jpg"

    def play_action(self, player):
        self._plus_power(player, 1)
        self.attack_action(player)
        return 0

    def attack_action(self, by_player):
        for p in globe.boss.players:
            if p != by_player and effects.attack(p, self, by_player):
                top_card = p.reveal_card(public=True)
                if top_card is not None and top_card.cost >= 1:
                    p.discard_a_card(top_card)
        return


class dr_sivana(card_frame.card):
    name = "Dr. Sivana"
    vp = 1
    cost = 4
    ctype = cardtype.VILLAIN
    text = ("+2 Power. You may put a Super Power from your discard pile on "
            "top of your deck.")
    image = image_path + "Dr Sivana.jpg"

    def play_action(self, player):
        it = ("You may pick a Super Power to put on top of your deck")
        self._plus_power(player, 2)
        cards = []
        for card in player.discard.contents:
            if card.ctype_eq(cardtype.SUPERPOWER):
                cards.append(card)
        if len(cards) > 0:
            choosen = effects.may_choose_one_of(it, player, cards, source=self, hint=ai_hint.BEST)
            if choosen:
                player.deck.add(choosen.pop_self())
        return 0


class granny_goodness(card_frame.card):
    name = "Granny Goodness"
    vp = 1
    cost = 5
    ctype = cardtype.VILLAIN
    text = ("Remove a Hero or Villain from the Line-Up. Play it, then return "
            "it to the Line-Up at the end of your turn.")
    image = image_path + "Granny Goodness.jpg"

    def play_action(self, player):
        instruction_text = ("Choose one of these from the line up, play it, "
                            "then return it at the end of the turn")
        assemble = []
        for c in globe.boss.lineup.contents:
            if c.ctype_eq(cardtype.VILLAIN) or c.ctype_eq(cardtype.HERO):
                assemble.append(c)
        if len(assemble) > 0:
            choosen = effects.choose_one_of(instruction_text, player, assemble, source=self,
                                            hint=ai_hint.BEST)
            player.play_and_return(choosen, globe.boss.lineup)
        return 0


class jervis_tetch(card_frame.card):
    name = "Jervis Tetch"
    vp = 1
    cost = 3
    ctype = cardtype.VILLAIN
    text = ("+1 Power. Look at the top card of your deck. Destroy it or "
            "discard it.")
    image = image_path + "Jervis Tetch.jpg"

    def play_action(self, player):
        self._plus_power(player, 1)
        it = "Would you like to destroy this card? If not this card will be discarded"
        top_card = player.reveal_card()
        if effects.ok_or_no(it, player, top_card, ai_hint.IFBAD):
            top_card.destroy(player)
        else:
            player.discard_a_card(top_card)
        return 0


class killer_croc(card_frame.card):
    name = "Killer Croc"
    vp = 1
    cost = 4
    ctype = cardtype.VILLAIN
    text = ("If you play or have played another Villain this turn, +3 Power. "
            "Otherwise, +2 Power.")
    image = image_path + "Killer Croc.jpg"
    power = 2

    def trigger(self, ttype, data, player, active, immediate):
        if trigger.test(not immediate,
                        trigger.PLAY,
                        self.trigger,
                        player, ttype) and data[0].ctype_eq(cardtype.VILLAIN) and data[0] != self:
            if globe.DEBUG:
                print("active", self.name, flush=True)
            self._plus_power(player, 1)
            player.triggers.remove(self.trigger)

    def play_action(self, player):
        found = False
        for card in player.played.played_this_turn:
            if card.ctype_eq(cardtype.VILLAIN) and card.name != self.name:
                self._plus_power(player, 3)
                return 0
        self._plus_power(player, 2)
        player.triggers.append(self.trigger)
        return 0


class larfleeze(card_frame.card):
    name = "Larfleeze"
    vp = 0
    cost = 7
    ctype = cardtype.VILLAIN
    text = (
        "You may gain up to 5 cost worth of cards from the Line-Up and put "
        "them into your hand. If you choose not to, +3 Power. "
        "At end of game, this card is worth 1 VP for every seven cards "
        "in your deck.")
    image = image_path + "Larfleeze.jpg"

    def get_cards(self, cost, deck):
        cards = []
        for card in deck:
            if card.cost <= cost:
                cards.append(card)
        return cards

    def play_action(self, player):
        it = (
            "You may gain up to 5 cost worth of cards from the Line-Up and put "
            "them into your hand, if not +3 power")
        total_cost = 5
        cards = self.get_cards(total_cost, globe.boss.lineup.contents)
        gained_card = False
        while len(cards) > 0:
            choosen = effects.may_choose_one_of(it, player, cards, source=self, hint=ai_hint.BEST)
            if choosen:
                total_cost -= choosen.cost
                player.gain(choosen)
                player.hand.add(choosen.pop_self())
                gained_card = True
            else:
                break
            cards = self.get_cards(total_cost, globe.boss.lineup.contents)
        if not gained_card:
            self._plus_power(player, 3)
        return 0

    def calculate_vp(self, all_cards):
        return int(len(all_cards) / 7)


class manhunter(card_frame.card):
    name = "Manhunter"
    vp = 1
    cost = 3
    ctype = cardtype.VILLAIN
    text = ("+1 Power and an additional +2 Power for each Manhunter in your "
            "discard pile.")
    image = image_path + "Manhunter.jpg"

    def play_action(self, player):
        power_total = 1
        for card in player.discard.contents:
            if card.name == self.name:
                power_total += 2
        self._plus_power(player, power_total)
        return 0


class mr_zsasz(card_frame.card):
    name = "Mr. Zsasz"
    vp = 1
    cost = 3
    ctype = cardtype.VILLAIN
    attack = True
    attack_text = ("Each foe reveals the top card of his deck. "
                   "If its cost is odd, that player gains a Weakness.")
    text = ("+2 Power. Attack: Each foe reveals the top card of his deck. "
            "If its cost is odd, that player gains a Weakness.")
    image = image_path + "Mr Zsasz.jpg"

    def play_action(self, player):
        self._plus_power(player, 2)
        self.attack_action(player)
        return 0

    def attack_action(self, by_player):
        for p in globe.boss.players:
            if p != by_player and effects.attack(p, self, by_player):
                top_card = p.reveal_card(public=True)
                if top_card.cost % 2 == 1:
                    p.gain_a_weakness()
        return


class ocean_master(card_frame.card):
    name = "Ocean Master"
    vp = 1
    cost = 2
    ctype = cardtype.VILLAIN
    text = ("If you play or have played another Villain this turn, you may "
            "destroy a card in your hand or discard pile.")
    image = image_path + "Ocean Master.jpg"

    def destroy_a_card_in_hand_or_discard(self, player):
        it = "You may destroy a card in your hand or discard pile."
        cards = []
        cards.extend(player.discard.contents)
        cards.extend(player.hand.contents)
        if len(cards) > 0:
            choosen = effects.may_choose_one_of(it, player, cards,
                                                source=self, hint=ai_hint.WORST)
            if choosen:
                choosen.destroy(player)
                return True
        return False

    def trigger(self, ttype, data, player, active, immediate):
        if trigger.test(not immediate,
                        trigger.PLAY,
                        self.trigger,
                        player, ttype) and data[0].ctype_eq(cardtype.VILLAIN):
            if globe.DEBUG:
                print("active", self.name, flush=True)
            if self.destroy_a_card_in_hand_or_discard(player):
                player.triggers.remove(self.trigger)

    def play_action(self, player):
        found = False
        for card in player.played.played_this_turn:
            if card.ctype_eq(cardtype.VILLAIN) and not found:
                found = True
                self.destroy_a_card_in_hand_or_discard(player)
        if not found:
            player.triggers.append(self.trigger)
        return 0


# EDITED UP TO HERE
class parasite(card_frame.card):
    name = "Parasite"
    vp = 1
    cost = 4
    ctype = cardtype.VILLAIN
    attack = True
    attack_text = ("Each foe reveals his hand and discards a card "
                   "with cost 3 or greater. Each who does may put a Punch card from "
                   "his discard pile into his hand.")
    text = ("+2 Power. Attack: Each foe reveals his hand and discards a card "
            "with cost 3 or greater. Each who does may put a Punch card from "
            "his discard pile into his hand.")
    image = image_path + "Parasite.jpg"

    def play_action(self, player):
        self._plus_power(player, 2)
        self.attack_action(player)
        return 0

    def attack_action(self, by_player):
        it = "Choose a card from your hand to discard with a cost of 3 or greater"
        for p in globe.boss.players:
            if p != by_player and effects.attack(p, self, by_player):
                effects.reveal(f"This was {p.persona.name}'s hand", p, p.hand.contents)
                discarded = False
                cards = []
                for card in p.hand.contents:
                    if card.cost >= 3:
                        cards.append(card)
                if len(cards) > 0:
                    choosen = effects.choose_one_of(it, p, cards, source=self, hint=ai_hint.WORST)
                    p.discard_a_card(choosen)
                    for card in p.discard.contents:
                        if card.name == "Punch":
                            it_ok = "Would you like to put a punch from your discard pile into your hand?"
                            if effects.ok_or_no(it_ok, p, self,
                                                ai_hint.ALWAYS):
                                p.hand.add(card.pop_self())
                            break
        return


class red_lantern_corps(card_frame.card):
    name = "Red Lantern Corps"
    vp = 1
    cost = 5
    ctype = cardtype.VILLAIN
    text = (
        "You may destroy a card in your hand. If you do, +3 Power. Otherwise, +1 Power.")
    image = image_path + "Red Lantern Corps.jpg"

    def play_action(self, player):
        it = "You may destroy a card in your hand, If you do +3 Power."
        choosen = None
        if len(player.hand.contents) > 0:
            choosen = effects.may_choose_one_of(it, player, player.hand.contents,
                                                source=self, hint=ai_hint.WORST)
        if choosen:
            choosen.destroy(player)
            self._plus_power(player, 3)
        else:
            self._plus_power(player, 1)
        return 0


class talon(card_frame.card):
    name = "Talon"
    vp = 1
    cost = 1
    ctype = cardtype.VILLAIN
    text = (
        "+2 Power if you play or have played a Starter card this turn. Otherwise, no power.")
    image = image_path + "Talon.jpg"

    def trigger(self, ttype, data, player, active, immediate):
        if trigger.test(not immediate,
                        trigger.PLAY,
                        self.trigger,
                        player, ttype) and data[0].ctype_eq(cardtype.STARTER):
            if globe.DEBUG:
                print("active", self.name, flush=True)
            self._plus_power(player, 2)
            player.triggers.remove(self.trigger)

    def play_action(self, player):
        found = False
        for card in player.played.played_this_turn:
            if card.ctype_eq(cardtype.STARTER):
                self._plus_power(player, 2)
                found = True
                break
        if not found:
            player.triggers.append(self.trigger)
        return 0


class the_demon_etrigan(card_frame.card):
    name = "The Demon Etrigan"
    vp = 2
    cost = 7
    ctype = cardtype.VILLAIN
    text = (
        "+4 Power. You may put a Hero from your discard pile on top of your deck.")
    image = image_path + "The Demon Etrigan.jpg"

    def play_action(self, player):
        self._plus_power(player, 4)
        it = "You may put a Hero from your discard pile on top of your deck."
        cards = []
        for card in player.discard.contents:
            if card.ctype_eq(cardtype.HERO):
                cards.append(card)
        if len(cards) > 0:
            choosen = effects.may_choose_one_of(it, player, cards, source=self, hint=ai_hint.BEST)
            if choosen:
                player.deck.add(choosen.pop_self())
        return 0
