from . import cards
from . import persona
import random
from frames import deck_frame


def initialize_supervillains():
    assemble = []
    assemble.append(cards.blackfire())
    assemble.append(cards.brother_blood())
    assemble.append(cards.cheshire())
    assemble.append(cards.clock_king())
    assemble.append(cards.dr_light())
    assemble.append(cards.harvest())
    assemble.append(cards.psimon())
    assemble.append(cards.superboy_prime())
    assemble.append(cards.terra())
    assemble.append(cards.the_brain_and_monsieur_mallah())
    random.shuffle(assemble)
    assemble.append(cards.slade_wilson())
    assemble.insert(0,cards.trigon())
    return assemble





deck = {cards.acrobatic_agility: 2,
        cards.aqualad: 2,
        cards.arsenal: 2,
        cards.azarath: 1,
        cards.azarath_metrion_zinthos: 1,
        cards.birdarang: 2,
        cards.bumblebee: 2,
        cards.bunker: 1,
        cards.cadmus_labs: 1,
        cards.cassie_sandsmark: 2,
        cards.cinderblock: 2,
        cards.cloak_of_raven: 2,
        cards.colony_suit: 3,
        cards.conner_kent: 1,
        cards.cybernetic_enhancement: 3,
        cards.daughter_of_trigon: 1,
        cards.demonic_influence: 2,
        cards.detonator: 3,
        cards.dick_greyson: 2,
        cards.energy_absorption: 2,
        cards.flight_wings: 3,
        cards.garfield_logan: 1,
        cards.geokinesis:2,
        cards.gizmo:3}


def initialize_deck():
    assemble = []
    for card, num in deck.items():
        for i in range(num):
            assemble.append(card())
    random.shuffle(assemble)
    return assemble


this_set = deck_frame.deck_set("Teen Titans", persona.get_personas, initialize_deck, initialize_supervillains, True)
