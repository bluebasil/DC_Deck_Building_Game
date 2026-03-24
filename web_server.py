"""
Web server for DC Deck Building Game.
Run with: python web_server.py
Serves the game API via Flask-SocketIO and static frontend files.
In production (Cloud Run), gevent is used for WebSocket support.
"""
# Use gevent monkey-patching in production for WebSocket support
import os
_USE_GEVENT = os.environ.get('USE_GEVENT', '1') == '1'
if _USE_GEVENT:
    try:
        from gevent import monkey
        monkey.patch_all()
    except ImportError:
        _USE_GEVENT = False

import sys
import threading
import time
import traceback

from flask import Flask, send_from_directory, abort
from flask_socketio import SocketIO, emit

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import globe
import deck_builder
import game_serializer
from event_bus import event_bus
from frames.actions import ENDTURN

app = Flask(__name__, static_folder='frontend', static_url_path='')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dc-deck-builder-dev-secret')

_ASYNC_MODE = 'gevent' if _USE_GEVENT else 'threading'

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode=_ASYNC_MODE,
    logger=False,
    engineio_logger=False,
)

# Store socketio in globe for game-thread emission
globe.socketio_instance = socketio

# ── Game lifecycle state ──────────────────────────────────────────────────────
_game_lock = threading.Lock()
_game_thread = None
_game_active = False


def _emit_state():
    """Thread-safe state emission to all connected clients."""
    try:
        state = game_serializer.serialize_state()
        socketio.emit('state_update', state, namespace='/')
    except Exception as e:
        print(f"[emit_state error] {e}", flush=True)


def _run_game(set_indices, player_configs):
    """Game loop executed in a background thread."""
    global _game_active
    try:
        # Web mode: CPUs must not try to print to a view that doesn't exist
        globe.CPU_TERMINAL_INVISIBLE = True

        # Reset and configure deck sets
        deck_builder.choose_sets_programmatic(set_indices)

        # Create event bus with state-change callback
        bus = event_bus()
        bus.on_state_change = _emit_state
        globe.bus = bus

        # Emit initial lobby→starting state
        socketio.emit('state_update', {"phase": "starting"}, namespace='/')

        # Create and run game
        import model
        globe.boss = model.model(player_configs=player_configs)

        # Emit after model init (persona selection will follow)
        _emit_state()

        globe.boss.start_game()

        # Emit final game-over state
        _emit_state()

    except globe.GameAborted:
        print("[game thread] Game aborted by user.", flush=True)
    except Exception as e:
        err = traceback.format_exc()
        print(f"[game thread error]\n{err}", flush=True)
        socketio.emit('game_error', {'message': str(e), 'detail': err}, namespace='/')
    finally:
        _game_active = False
        globe.boss = None


# ── Static file routes ────────────────────────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')


@app.route('/card-images/<path:filename>')
def card_image(filename):
    """Serve card/persona images from the project root."""
    base = os.path.dirname(os.path.abspath(__file__))
    full = os.path.normpath(os.path.join(base, filename))
    if not full.startswith(base):
        abort(403)
    directory = os.path.dirname(full)
    fname = os.path.basename(full)
    return send_from_directory(directory, fname)


# ── Socket.IO events ──────────────────────────────────────────────────────────

@socketio.on('connect')
def handle_connect():
    state = game_serializer.serialize_state()
    emit('state_update', state)
    emit('available_sets', deck_builder.get_available_sets())


@socketio.on('get_sets')
def handle_get_sets():
    emit('available_sets', deck_builder.get_available_sets())


@socketio.on('start_game')
def handle_start_game(data):
    global _game_thread, _game_active

    with _game_lock:
        if _game_active:
            emit('game_error', {'message': 'A game is already in progress. Refresh to abandon it.'})
            return

        set_indices = data.get('sets', [0])
        num_ai = max(1, min(3, int(data.get('num_ai', 1))))

        player_configs = [{'type': 'human_web'}]
        for _ in range(num_ai):
            player_configs.append({'type': 'cpu'})

        _game_active = True
        _game_thread = threading.Thread(
            target=_run_game,
            args=(set_indices, player_configs),
            daemon=True,
        )
        _game_thread.start()


@socketio.on('action')
def handle_action(data):
    if not globe.bus or not globe.boss:
        emit('game_error', {'message': 'No active game.'})
        return

    action_type = data.get('type')

    if action_type == 'card':
        card_id = data.get('card_id')
        card = game_serializer.find_card_by_id(card_id)
        if card is not None:
            globe.bus.card_clicked(card)
        else:
            # Try to match as persona by id
            persona = game_serializer.find_persona_by_id(card_id)
            if persona is not None:
                globe.bus.card_clicked(persona)

    elif action_type == 'button':
        raw = data.get('action')
        if raw == 'end_turn':
            globe.bus.button_clicked(ENDTURN)
        elif isinstance(raw, int):
            globe.bus.button_clicked(raw)
        elif isinstance(raw, str) and raw.isdigit():
            globe.bus.button_clicked(int(raw))

    elif action_type == 'special':
        special_id = data.get('special_id')
        if globe.boss:
            cp = globe.boss.get_current_player()
            if cp:
                for opt in cp.played.special_options:
                    if opt.action_id == special_id:
                        globe.bus.button_clicked(opt)
                        break

    # Give game thread a moment to process, then push updated state
    time.sleep(0.15)
    _emit_state()


@socketio.on('abandon_game')
def handle_abandon():
    global _game_active
    _game_active = False
    globe.boss = None
    globe.bus = None
    emit('state_update', {'phase': 'lobby'})


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"Starting DC Deck Builder server on port {port}", flush=True)
    socketio.run(app, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
