from __future__ import annotations
import enum

class CardType(enum.Enum):
    ANY = "ANY"
    STARTER = "Starter"
    WEAKNESS = "Weakness"
    HERO = "Hero"
    VILLAIN = "Villain"
    SUPERPOWER = "Superpower"
    EQUIPMENT = "Equipment"
    LOCATION = "Location"
    SPECIALSV = "SPECIALSV"

    # valid_cardtypes = {STARTER, HERO, VILLAIN, SUPERPOWER, EQUIPMENT, LOCATION}

    @classmethod
    def valid_cardtypes(cls) -> set[CardType]:
        return {cls.STARTER, cls.HERO, cls.VILLAIN, cls.SUPERPOWER, cls.EQUIPMENT, cls.LOCATION}


    # valid_cardtypes = {CardType.STARTER, CardType.HERO, CardType.VILLAIN, CardType.SUPERPOWER, CardType.EQUIPMENT,
    #                CardType.LOCATION}
