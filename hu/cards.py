from constants import cardtype
from constants import owners
import effects
from constants import option
import globe
from constants import ai_hint
import random
import arcade
from frames import actions
from frames import card_frame
from constants import trigger

image_path = "hu/images/cards/"

### Equipment ###
class batarang(card_frame.card):

    name = "Batarang"
    vp = 1
    cost = 2
    ctype = cardtype.EQUIPMENT
    text = "+2 power"
    image = image_path + "Batarang.jpg"

    def play_action(self,player):
        player.played.plus_power(2)
        return 0

class blue_lantern_power_ring(card_frame.card):

    name = "Blue Lantern Power Ring"
    vp = "*"
    cost = 5
    ctype = cardtype.EQUIPMENT
    text = ("+1 Power and an additional +1 Power for each Hero in your discard " 
            "pile and that you play or have played this turn. At end of game, "
            "this card is worth 1 VP for each Power Ring in your deck.")
    image = image_path + "Blue Lantern Power Ring.jpg"

    def play_action(self, player):
        power =  1
        for discarded_card in player.discard.contents:
            if discarded_card.ctype_eq(cardtype.HERO):
                power += 1
        for played_card in player.playing.played_this_turn:
            if played_card.ctype_eq(cardtype.HERO):
                power += 1
        player.played.plus_power(power)
        return 0

    def calculate_vp(self, all_cards):
        count = 0
        for card in all_cards:
            if card.ctype_eq(cardtype.EQUIPMENT) and "power ring" in card.name.lower():
                count += 1
        return count

class green_lantern_power_ring(card_frame.card):

    name = "Green Lantern Power Ring"
    vp = "*"
    cost = 5
    ctype = cardtype.EQUIPMENT
    defence = True
    text = ("+2 Power. Defense: You may discard this card to avoid an Attack. "
            "If you do, draw two cards. At end of game, "
            "this card is worth 1 VP for each Power Ring in your deck.")
    image = image_path + "Green Lantern Power Ring.jpg"

    def play_action(self, player):
        player.played.plus_power(2)
        return 0

    def defend(self, attacker=None, defender=None):
        self.owner.discard_a_card(self)
        self.owner.draw_card(2)
        return

    def calculate_vp(self, all_cards):
        count = 0
        for card in all_cards:
            if card.ctype_eq(cardtype.EQUIPMENT) and "power ring" in card.name.lower():
                count += 1
        return count

class helmet_of_fate(card_frame.card):

    name = "Helmet of Fate"
    vp = 1
    cost = 3
    ctype = cardtype.EQUIPMENT
    defence = True
    text = ("+2 Power Defense: You may discard this card and any number of "
            "other cards to avoid an Attack. If you do, draw cards equal to "
            "the number of other cards discarded.")
    image = image_path + "Helmet of Fate.jpg"

    def play_action(self,player):
        player.played.plus_power(2)
        return 0

    def defend(self, attacker=None, defender=None):
        instruction_text = ("You may discard this card and any number of "
            "other cards to avoid an Attack. If you do, draw cards equal to "
            "the number of other cards discarded")
        collection = player.hand.contents.copy()
        self.owner.discard_a_card(self)
        # cards_to_discard = effects.may_choose_one_of(
        #     instruction_text, player, collection, ai_hint.IFBAD
        # )
        result = effects.choose_however_many(
            "Choose any number to discard", player, assemble,
            ai_hint.IFBAD)
        for c in result:
            player.deck.contents.append(c)
            player.discard_a_card(c)

        redraw = len(result)

        self.owener.draw_card(redraw)
        return

class indigo_tribe_power_ring(card_frame.card):

    name = "Indigo Tribe Power Ring"
    vp = "*"
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
        for c in player.played.contents:
            if c.name != self.name and c != player.played_this_turn[-1]:
                assemble.append(c)
        if len(assemble) > 0:
            choosen = effects.choose_one_of(instruction_text, player, assemble, ai_hint.BBST)
        player.played.plus_power(choosen.power)
        return 0


    def calculate_vp(self, all_cards):
        count = 0
        for card in all_cards:
            if card.ctype_eq(cardtype.EQUIPMENT) and "power ring" in card.name.lower():
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
        self.owner.draw_card(1)
        return 0


class mind_control_hat(card_frame.card):

    name = "Mind Control Hat"
    vp =2
    cost = 7
    attack = True
    attack_text = "Each foe discards a random card."
    ctype = cardtype.EQUIPMENT
    text = ("Draw two cards. Attack: Each foe discards a random card. "
            "If you play or have played Jervis Tetch this turn, you may play "
            "each Hero and Villain in the Line-Up, then return them to the "
            "Line-Up.")
    image = image_path + "Mind Control Hat.jpg"

    def play_action(self, player):
        self.attack_action(player)
        self.owner.draw_card(2)
        jervis_played = False
        instruction_text = ("If you play or have played Jervis Tetch "
                            "this turn, you may play "
                            "each Hero and Villain in the Line-Up, "
                            "then return them to the Line-Up.")
        assemble = []
        for card in player.played.contents:
            if card.name == "Jervis Tetch":
                jervis_played = True
        if jervis_played:
            for c in globe.boss.lineup.contents:
                if c.ctype_eq(cardtype.HERO) or c.ctype_eq(cardtype.VILLAIN):
                    assemble.append(c)
            for ac in assemble:
                self.played_card = ac
                assemble.pop_self(ac)
                player.played.play(ac)
        return 0


    def attack_action(self,by_player):
        instruction_text = "Each foe discards a random card."
        for p in globe.boss.players:
            if p != by_player:
                choosen = effects.may_choose_one_of(instruction_text, p, p.hand.contents, hint=ai_hint.IFBAD)
                if choosen:
                    p.discard_a_card(choosen)
        return


class orange_lantern_power_ring(card_frame.card):

    name = "Orange Lantern Power Ring"
    vp = "*"
    cost = 5
    ctype = cardtype.EQUIPMENT
    text = ("You may gain an Equipment with cost 5 or less from the Line-Up "
            "and put it into your hand. If you choose not to, +2 Power. At end "
            "of game, this card is worth 1 VP for each Power Ring in your deck.")
    image = image_path + "Orange Lantern Power Ring.jpg"

    def play_action(self,player):
        instruction_text = "Choose a one of these to gain from the Line-Up"
        assemble = []
        for c in globe.boss.lineup.contents:
            if c.cost <= 5 and len(c.frozen) == 0:
                assemble.append(c)
        if len(assemble) > 0:
            choosen = effects.may_choose_one_of(instruction_text, player, assemble,
                                            ai_hint.BEST)
            if choosen != None
                player.gain(choosen)
            else:
                player.played.plus_power(2)
        return 0

    def calculate_vp(self, all_cards):
        count = 0
        for card in all_cards:
            if card.ctype_eq(cardtype.EQUIPMENT) and "power ring" in card.name.lower():
                count += 1
        return count


class red_lantern_power_ring(card_frame.card):

    name = "Red Lantern Power Ring"
    vp = "*"
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
            to_add = player.reveal_card(public=False)
            if to_add != None:
                assemble.append(to_add)
                player.deck.contents.pop()
        if len(assemble) > 0:
            result = effects.choose_one_of(
                "Choose any number to discard", player, assemble,
                ai_hint.IFBAD)
            if result != None:
                player.deck.contents.append(result)
                result.destroy(player)
                assemble.remove(result)

        total_times = len(assemble)
        while len(assemble) > 0:
            result = assemble[0]
            assemble.remove(result)
            player.deck.contents.append(result)
        return 0

    def calculate_vp(self, all_cards):
        count = 0
        for card in all_cards:
            if card.ctype_eq(cardtype.EQUIPMENT) and "power ring" in card.name.lower():
                count += 1
        return count


class sciencell(card_frame.card):

    name = "Sciencell"
    vp = "*"
    cost = 6
    ctype = cardtype.EQUIPMENT
    text = ("+2 Power. At end of game, this card is worth 1 VP for each "
            "different Villain in your deck.")
    image = image_path + "Sciencell.jpg"

    def play_action(self,player):
        player.played.plus_power(2)

    def calculate_vp(self,all_cards):
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
    defence = True
    text = ("You may put a Hero from your discard pile on top of your deck. "
            "If you choose not to, draw a card. Defense: You may discard this "
            "card to avoid an attack. If you do, you may put a Hero from your "
            "discard pile into your hand or draw a card.")
    image = image_path + "Skeets.jpg"

    def play_action(self,player):
        instruction_text = "Choose a Hero from your discard pile to put onto your deck"
        assemble = []
        for c in player.discard.contents:
            if c.ctype_eq(cardtype.HERO):
                assemble.append(c)
        if len(assemble) > 0:
            choosen = effects.may_choose_one_of(instruction_text, player, assemble,
                                            ai_hint.BEST)
            if choosen:
                player.deck.contents.append(choosen)
            else:
                self.owner.draw_card(1)
        return 0

    def defend(self,attacker = None,defender = None):
        self.owner.discard_a_card(self)
        assemble = []
        for c in player.discard.contents:
            if c.ctype_eq(cardtype.HERO):
                assemble.append(c)
        if len(assemble) > 0:
            choosen = effects.may_choose_one_of(instruction_text, player,
                                                assemble,
                                                ai_hint.BEST)
            if choosen:
                player.hand.contents.append(choosen)
            else:
                self.owner.draw_card(1)
        return


class soultaker_sword(card_frame.card):

    name = "Soultaker Sword"
    vp = 1
    cost = 4
    ctype = cardtype.EQUIPMENT
    text = ("+2 Power. You may destroy a card in your hand.")
    image = image_path + "Soultaker Sword 4.jpg"

    def play_action(self,player):
        instruction_text = "You may destroy a card in your hand."
        player.played.plus_power(2)
        card_to_destroy = effects.may_choose_one_of(instruction_text, player, player.hand.contents, ai_hint.IFBAD)
        if card_to_destroy:
            card_to_destroy.destroy(player)
        return 0


class star_sapphire_power_ring(card_frame.card):

    name = "Star Sapphire Power Ring"
    vp = "*"
    cost = 5
    ctype = cardtype.EQUIPMENT
    text = ("Reveal the top two cards of your deck. If they share a card "
            "type, put them back in any order. If not, draw them. At end of "
            "game, this card is worth 1 VP for each Power Ring in your deck.")
    image = image_path + "Star Sapphire Power Ring.jpg"

    def play_action(self,player):
        assemble = []
        for i in range(2):
            to_add = player.reveal_card(public=False)
            if to_add != None:
                assemble.append(to_add)
                player.deck.contents.pop()
        if assemble[0].ctype == assemble[1].ctype:
            while len(assemble) > 0:
                result = effects.choose_one_of(
                    f"Place card back on top of your deck "
                    f"({total_times - len(assemble) + 1}/{total_times})?",
                    player, assemble, ai_hint.WORST)
                assemble.remove(result)
                player.deck.contents.append(result)
        else:
            for card in assemble:
                player.hand.contents.append(card)
        return 0


class white_lantern_power_battery(card_frame.card):

    name = "White Lantern Power Battery"
    vp = 2
    cost = 7
    ctype = cardtype.EQUIPMENT
    text = ("Gain all Power Rings in the Line-Up and put them into your hand. "
            "Then gain any card from the Line-Up and put it on top of your deck.")
    image = image_path + "White Lantern Power Battery.jpg"

    def play_action(self,player):
        assemble = []
        for card in globe.boss.lineup.contents:
            if "power ring" in c.name.lower():
                player.hand.contents.append(card)
                globe.boss.lineup.contents.pop(card)
            assemble.append(card)

        if len(assemble) > 0:
            choosen = effects.choose_one_of(instruction_text, player, assemble, ai_hint.BEST)
            player.deck.contents.append(choosen)

        return 0

class yellow_lantern_power_ring(card_frame.card):

    name = "Yellow Lantern Corps Power Ring"
    vp = "*"
    cost = 5
    attack = True
    attack_text = " Each foe discards a card."
    ctype = cardtype.EQUIPMENT
    text = ("+2 Power. Attack: Each foe discards a card. At end of game, "
            "this card is worth 1 VP for each Power Ring in your deck.")
    image = image_path + "Yellow Lantern Corps Power Ring.jpg"

    def play_action(self,player):
        player.played.plus_power(2)
        self.attack_action(player)

    def attack_action(self,by_player):
        instruction_text = "Each foe discards a random card."
        for p in globe.boss.players:
            if p != by_player:
                choosen = effects.may_choose_one_of(instruction_text, p, p.hand.contents, hint=ai_hint.IFBAD)
                if choosen:
                    p.discard_a_card(choosen)
        return

    def calculate_vp(self, all_cards):
        count = 0
        for card in all_cards:
            if card.ctype_eq(cardtype.EQUIPMENT) and "power ring" in card.name.lower():
                count += 1
        return count

### Hero ###