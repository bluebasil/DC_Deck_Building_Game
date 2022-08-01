from constants import cardtype
import effects
from constants import ai_hint
import globe
from frames import persona_frame
from constants import trigger


def get_personas():
    # return [auquaman(),batman(),the_flash()]
    return [auquaman(), batman(), cyborg(), the_flash(), green_lantern(), superman(), wonder_woman(),
            martian_manhunter()]


class auquaman(persona_frame.persona):
    name = "Aquaman"
    text = "You may put any cards with cost 5 or less you buy or gain during your turn on top of your deck."
    image = "base/images/personas/Aquaman MC.jpg"

    def trigger(self, ttype, data, player, active, immediate):
        if globe.DEBUG:
            print("test", self.name, flush=True)
        if trigger.test(immediate, trigger.GAIN_CARD, self.trigger, player, ttype, active) and data[0] == False and \
                data[1].cost <= 5 and effects.ok_or_no(f"Would you like to put {data[1].name} on top of your deck?",
                                                       player, data[1],
                                                       ai_hint.ALWAYS):
            if globe.DEBUG:
                print("active", self.name, flush=True)
            player.deck.contents.append(data[1])
            return True

    def ready(self):
        self.player.triggers.append(self.trigger)


class batman(persona_frame.persona):
    name = "Batman"
    text = "+1 Power for each Equipment you play during your turn."
    image = "base/images/personas/Batman MC.jpg"

    def ai_overvalue(self, card):
        if card.ctype_eq(cardtype.EQUIPMENT):
            return persona_frame.overvalue()
        return 0

    def trigger(self, ttype, data, player, active, immediate):
        if globe.DEBUG:
            print("test", self.name, flush=True)
        if trigger.test(not immediate,
                        trigger.PLAY,
                        self.trigger,
                        player, ttype, active) and data[0].ctype_eq(cardtype.EQUIPMENT):
            if globe.DEBUG:
                print("active", self.name, flush=True)
            player.played.plus_power(1)

    def ready(self):
        self.player.triggers.append(self.trigger)


class cyborg(persona_frame.persona):
    name = "Cyborg"
    text = "+1 power for first super power played, and draw a card for the first equipment played"
    image = "base/images/personas/Cyborg MC.jpg"

    def ai_overvalue(self, card):
        if card.ctype_eq(cardtype.SUPERPOWER) or card.ctype_eq(cardtype.EQUIPMENT):
            return persona_frame.overvalue()
        return 0

    def triggerEQ(self, ttype, data, player, active, immediate):
        if globe.DEBUG:
            print("test - EQ", self.name, flush=True)
        if trigger.test(not immediate,
                        trigger.PLAY,
                        self.triggerEQ,
                        player, ttype) and data[0].ctype_eq(cardtype.EQUIPMENT):
            if globe.DEBUG:
                print("active - EQ", self.name, flush=True)
            if active:
                player.draw_card(from_card=False)
            player.triggers.remove(self.triggerEQ)

    def triggerSP(self, ttype, data, player, active, immediate):
        if globe.DEBUG:
            print("test - SP", self.name, flush=True)
        if trigger.test(not immediate,
                        trigger.PLAY,
                        self.triggerSP,
                        player, ttype) and data[0].ctype_eq(cardtype.SUPERPOWER):
            if globe.DEBUG:
                print("active - SP", self.name, flush=True)
            if active:
                player.played.plus_power(1)
            player.triggers.remove(self.triggerSP)

    def ready(self):
        self.player.triggers.append(self.triggerSP)
        self.player.triggers.append(self.triggerEQ)


class the_flash(persona_frame.persona):
    name = "The Flash"
    text = "You go first.  The first time a card tells you to draw one or more cards during each of your turns, draw an additional card."
    image = "base/images/personas/The Flash MC.jpg"

    def ai_overvalue(self, card):
        if card.text.lower().count('draw') > 0:
            return persona_frame.overvalue()
        return 0

    def trigger(self, ttype, data, player, active, immediate):
        if globe.DEBUG:
            print("test", self.name, flush=True)
        if trigger.test(not immediate,
                        trigger.DRAW,
                        self.trigger,
                        player, ttype) and data[1] == True:
            if globe.DEBUG:
                print("active", self.name, flush=True)
            if active:
                player.draw_card(from_card=False)
            player.triggers.remove(self.trigger)

    def ready(self):
        self.player.triggers.append(self.trigger)


class green_lantern(persona_frame.persona):
    name = "Green Lantern"
    text = "If you play three or more cards with different names and cost 1 or more during your turn, +3 Power."
    image = "base/images/personas/Green Lantern MC.jpg"

    # accounted_for = False

    def trigger(self, ttype, data, player, active, immediate):
        if globe.DEBUG:
            print("test", self.name, flush=True)
        if trigger.test(not immediate, trigger.PLAY, self.trigger, player, ttype, active):
            if globe.DEBUG:
                print("active", self.name, flush=True)
            names = set()
            for c in player.played.played_this_turn:
                if c.cost >= 1:
                    names.add(c.name)
            if len(names) >= 3:
                player.played.plus_power(3)
                player.triggers.remove(self.trigger)

    def ready(self):
        self.player.triggers.append(self.trigger)


class hawkman(persona_frame.persona):
    name = "Hawkman"
    text = "+1 Power for each Hero you play during your turn."

    # image = "base/images/personas/Aquaman MC.jpg"

    def ai_overvalue(self, card):
        if card.ctype_eq(cardtype.HERO):
            return persona_frame.overvalue()
        return 0

    def trigger(self, ttype, data, player, active, immediate):
        if globe.DEBUG:
            print("test", self.name, flush=True)
        if trigger.test(not immediate,
                        trigger.PLAY,
                        self.trigger,
                        player, ttype, active) and data[0].ctype_eq(cardtype.HERO):
            if globe.DEBUG:
                print("active", self.name, flush=True)
            player.played.plus_power(1)

    def ready(self):
        self.player.triggers.append(self.trigger)


class superman(persona_frame.persona):
    name = "Superman"
    text = "+1 Power for each different Super Power you play during your turn."
    image = "base/images/personas/Superman MC.jpg"

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
            already_played = False
            for c in player.played.played_this_turn:
                if c != data[0] and data[0].name == c.name:
                    already_played = True
            if not already_played:
                player.played.plus_power(1)

    def ready(self):
        self.player.triggers.append(self.trigger)


class wonder_woman(persona_frame.persona):
    name = "Wonder Woman"
    text = "For each Villain you buy or gain during your turn, draw an extra card at the end of your turn."
    image = "base/images/personas/Wonder Woman MC.jpg"

    def ai_overvalue(self, card):
        if card.ctype_eq(cardtype.VILLAIN):
            return persona_frame.overvalue()
        return 0

    # the reset is specifically timed for this to be possible
    def reset(self):
        if self.active:
            for c in self.player.gained_this_turn:
                if c.ctype_eq(cardtype.VILLAIN):
                    self.player.draw_card(from_card=False)


class martian_manhunter(persona_frame.persona):
    name = "Martian Manhunter"
    text = "If you play two or more Villains during your turn, +3 Power.\nIf you play two or more Heros during your turn, +3 Power."
    image = "base/images/personas/Martian Manhunter MC.jpg"

    def ai_overvalue(self, card):
        if card.ctype_eq(cardtype.VILLAIN) or card.ctype_eq(cardtype.HERO):
            return persona_frame.overvalue()
        return 0

    def triggerVI(self, ttype, data, player, active, immediate):
        if globe.DEBUG:
            print("test - VI", self.name, flush=True)
        if trigger.test(not immediate,
                        trigger.PLAY,
                        self.triggerVI,
                        player, ttype, active) and data[0].ctype_eq(cardtype.VILLAIN):

            if globe.DEBUG:
                print("active - VI", self.name, flush=True)
            villain_count = 0
            for c in player.played.played_this_turn:
                if c.ctype_eq(cardtype.VILLAIN):
                    villain_count += 1
            if villain_count >= 2:
                player.played.plus_power(3)
                player.triggers.remove(self.triggerVI)

    def triggerHE(self, ttype, data, player, active, immediate):
        if globe.DEBUG:
            print("test - HE", self.name, flush=True)
        if trigger.test(not immediate,
                        trigger.PLAY,
                        self.triggerHE,
                        player, ttype, active) and data[0].ctype_eq(cardtype.HERO):
            if globe.DEBUG:
                print("active - HE", self.name, flush=True)
            villain_count = 0
            for c in player.played.played_this_turn:
                if c.ctype_eq(cardtype.HERO):
                    villain_count += 1
            if villain_count >= 2:
                player.played.plus_power(3)
                player.triggers.remove(self.triggerHE)

    def ready(self):
        self.player.triggers.append(self.triggerVI)
        self.player.triggers.append(self.triggerHE)
