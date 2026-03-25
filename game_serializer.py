"""
Serialize game state to JSON-compatible dicts for the web frontend.
"""
import globe
from constants import owners, option
from constants2 import CardType
from frames.card_frame import card as CardBase
from frames.persona_frame import persona as PersonaBase
from frames.actions import special_action

CARDTYPE_NAMES = {
    CardType.ANY: "any",
    CardType.STARTER: "starter",
    CardType.WEAKNESS: "weakness",
    CardType.HERO: "hero",
    CardType.VILLAIN: "villain",
    CardType.SUPERPOWER: "superpower",
    CardType.EQUIPMENT: "equipment",
    CardType.LOCATION: "location",
    CardType.SPECIALSV: "special_sv",
}

OPTION_LABELS = {
    option.NO: "No",
    option.OK: "OK",
    option.DONE: "Done",
    option.EVEN: "Even",
    option.ODD: "Odd",
    option.CANNOT: "Cannot",
}


def serialize_card(c):
    if c is None:
        return None
    return {
        "id": getattr(c, 'card_id', str(id(c))),
        "name": c.name,
        "cost": c.cost,
        "vp": c.vp,
        "type": CARDTYPE_NAMES.get(c.ctype, "unknown"),
        "text": getattr(c, 'text', ""),
        "attack_text": getattr(c, 'attack_text', ""),
        "image": c.image,
        "defense": getattr(c, 'defense', False),
        "has_attack": getattr(c, 'attack', False),
        "frozen": list(c.frozen),
        "rotation": getattr(c, 'rotation', 0),
        "has_stack_ongoing": getattr(c, 'has_stack_ongoing', False),
    }


def serialize_persona(p):
    if p is None:
        return None
    return {
        "id": p.name.replace(" ", "_").replace("'", ""),
        "name": p.name,
        "text": getattr(p, 'text', ""),
        "image": p.image,
        "active": getattr(p, 'active', True),
        "rotation": getattr(p, 'rotation', 0),
    }


def serialize_option(opt):
    """Serialize a query option - could be a card, persona, or button constant."""
    if isinstance(opt, CardBase) and hasattr(opt, 'cost'):
        result = serialize_card(opt)
        result["opt_type"] = "card"
        return result
    elif isinstance(opt, PersonaBase):
        return {
            "opt_type": "persona",
            "id": opt.name.replace(" ", "_").replace("'", ""),
            "name": opt.name,
            "text": getattr(opt, 'text', ""),
            "image": opt.image,
        }
    elif isinstance(opt, int) and opt in OPTION_LABELS:
        return {
            "opt_type": "button",
            "action": opt,
            "label": OPTION_LABELS[opt],
        }
    else:
        return {
            "opt_type": "unknown",
            "value": str(opt),
        }


def serialize_query(query):
    if query is None:
        return None
    return {
        "text": query.text,
        "context_card": serialize_card(query.card) if query.card else None,
        "options": [serialize_option(opt) for opt in query.options],
    }


def serialize_player(p, human_pid=None):
    if p.persona is None:
        persona_data = None
    else:
        persona_data = serialize_persona(p.persona)

    special_opts = [
        {"id": opt.action_id, "text": opt.button_text}
        for opt in p.played.special_options
    ]

    discard_top = None
    if p.discard.contents:
        discard_top = serialize_card(p.discard.contents[-1])

    is_human = _is_human_web(p)

    return {
        "pid": p.pid,
        "is_human": is_human,
        "persona": persona_data,
        "power": p.played.power,
        "vp": p.vp,
        "score": p.score,
        "deck_size": p.deck.size(),
        "discard_size": p.discard.size(),
        "discard_top": discard_top,
        # Show full hand only for human player; AI hand shows count only
        "hand": [serialize_card(c) for c in p.hand.contents] if is_human else [],
        "hand_size": p.hand.size(),
        # Full discard list for all players (used by discard popup, including opponent view)
        "discard_cards": [serialize_card(c) for c in p.discard.contents],
        "played": [serialize_card(c) for c in p.played.contents],
        "played_this_turn": [serialize_card(c) for c in p.played.played_this_turn],
        "ongoing": [serialize_card(c) for c in p.ongoing.contents],
        "under_persona": [serialize_card(c) for c in p.under_superhero.contents],
        "over_persona": [serialize_card(c) for c in p.over_superhero.contents],
        "special_options": special_opts,
    }


def _is_human_web(player):
    from controlers import human_web
    return isinstance(player.controler, human_web)


def find_card_by_id(card_id):
    """Search all piles for a card with the given UUID."""
    if not globe.boss:
        return None
    boss = globe.boss

    all_piles = [
        boss.lineup,
        boss.main_deck,
        boss.kick_stack,
        boss.weakness_stack,
        boss.supervillain_stack,
        boss.destroyed_stack,
    ]
    for pile in all_piles:
        for c in pile.contents:
            if getattr(c, 'card_id', None) == card_id:
                return c

    for p in boss.players:
        for pile in [p.hand, p.deck, p.discard, p.played,
                     p.ongoing, p.under_superhero, p.over_superhero]:
            for c in pile.contents:
                if getattr(c, 'card_id', None) == card_id:
                    return c

    # Also search query options (persona objects don't have card_id)
    if globe.bus and globe.bus.display:
        for opt in globe.bus.display.options:
            if isinstance(opt, CardBase) and getattr(opt, 'card_id', None) == card_id:
                return opt

    return None


def find_persona_by_id(persona_id):
    """Search persona list for a persona with the given ID (name-derived)."""
    if not globe.boss:
        return None
    for p in globe.boss.persona_list:
        pid = p.name.replace(" ", "_").replace("'", "")
        if pid == persona_id:
            return p
    # Also check already-assigned personas
    for player in globe.boss.players:
        if player.persona:
            pid = player.persona.name.replace(" ", "_").replace("'", "")
            if pid == persona_id:
                return player.persona
    return None


def _card_positions(boss):
    """Flat dict: card_id_str → pile_name for every card in the game."""
    positions = {}

    def add(cards, name):
        for c in cards:
            cid = str(getattr(c, 'card_id', ''))
            if cid:
                positions[cid] = name

    add(boss.lineup.contents,              'lineup')
    add(boss.main_deck.contents,           'main_deck')
    add(boss.kick_stack.contents,          'kick_stack')
    add(boss.weakness_stack.contents,      'weakness_stack')
    add(boss.supervillain_stack.contents,  'sv_stack')
    add(boss.destroyed_stack.contents,     'destroyed')
    for p in boss.players:
        pid = p.pid
        add(p.hand.contents,               f'p{pid}_hand')
        add(p.deck.contents,               f'p{pid}_deck')
        add(p.discard.contents,            f'p{pid}_discard')
        add(p.played.contents,             f'p{pid}_played')
        add(p.ongoing.contents,            f'p{pid}_ongoing')
        add(p.under_superhero.contents,    f'p{pid}_under')
        add(p.over_superhero.contents,     f'p{pid}_over')
    return positions


def serialize_state():
    """Serialize the complete current game state."""
    if not globe.boss:
        return {"phase": "lobby"}

    boss = globe.boss

    # Determine phase
    if len(boss.player_score) > 0:
        phase = "game_over"
    elif boss.game_ongoing:
        phase = "playing"
    elif boss.turn_number == 0:
        phase = "choosing_persona"
    else:
        phase = "playing"

    # Lineup
    lineup = [serialize_card(c) for c in boss.lineup.contents]

    # SV stack
    sv_top = None
    if boss.supervillain_stack.contents:
        sv_top = serialize_card(boss.supervillain_stack.contents[-1])

    # Players
    players = [serialize_player(p) for p in boss.players]

    # Active query
    query = None
    if globe.bus and globe.bus.display:
        query = serialize_query(globe.bus.display)

    # Flush recent events for animation hints
    events = globe.flush_events()

    return {
        "phase": phase,
        "whose_turn": boss.whose_turn,
        "turn_number": boss.turn_number,
        "main_deck_size": boss.main_deck.size(),
        "destroyed_count": boss.destroyed_stack.size(),
        "destroyed_cards": [serialize_card(c) for c in boss.destroyed_stack.contents],
        "card_positions": _card_positions(boss),
        "lineup": lineup,
        "sv_stack": {
            "top": sv_top,
            "count": boss.supervillain_stack.size(),
            "current_sv_id": getattr(boss.supervillain_stack.current_sv, 'card_id', None)
                             if boss.supervillain_stack.current_sv else None,
        },
        "kick_stack": {
            "count": boss.kick_stack.size(),
            "top_id": getattr(boss.kick_stack.contents[-1], 'card_id', None) if boss.kick_stack.contents else None,
            "top": serialize_card(boss.kick_stack.contents[-1]) if boss.kick_stack.contents else None,
        },
        "weakness_stack": {
            "count": boss.weakness_stack.size(),
            "top_id": getattr(boss.weakness_stack.contents[-1], 'card_id', None) if boss.weakness_stack.contents else None,
        },
        "players": players,
        "query": query,
        "game_ongoing": boss.game_ongoing,
        "player_scores": boss.player_score,
        "end_reason": getattr(boss, 'end_reason', 'regular'),
        "events": events,
    }
