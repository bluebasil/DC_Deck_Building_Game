/* ═══════════════════════════════════════════════════════════════
   DC DECK BUILDING GAME — Frontend Client
   ═══════════════════════════════════════════════════════════════ */

'use strict';

// ── Config ─────────────────────────────────────────────────────────────────
const SERVER_URL = window.location.origin;   // same origin as Flask
const IMG_ROOT   = '/card-images/';

// ── Socket.IO ───────────────────────────────────────────────────────────────
const socket = io(SERVER_URL, { transports: ['websocket', 'polling'] });

// ── State ───────────────────────────────────────────────────────────────────
let state       = null;
let prevState   = null;
let myPid       = null;   // determined once persona is chosen
let selectedSets     = [];
let numAI            = 1;
let selectedPersonaId = null;
let availableSets    = [];

// Card position registry: card_id → DOM element  (for animation source tracking)
const cardRegistry = {};

// ── DOM refs ────────────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);
const screens = {
  lobby:     $('screen-lobby'),
  persona:   $('screen-persona'),
  game:      $('screen-game'),
  gameover:  $('screen-gameover'),
};

// ── Utilities ───────────────────────────────────────────────────────────────
function imgUrl(path) {
  if (!path) return '';
  return IMG_ROOT + path;
}

function cardTypeClass(type) {
  return type || 'unknown';
}

function showScreen(name) {
  Object.values(screens).forEach(s => s.classList.remove('active'));
  screens[name].classList.add('active');
}

function getMyPlayer() {
  if (!state || !state.players) return null;
  return state.players.find(p => p.is_human) || null;
}

// ── Connection ──────────────────────────────────────────────────────────────
socket.on('connect', () => {
  $('connection-status').textContent = 'Connected';
  $('connection-status').className = 'conn-status connected';
});
socket.on('disconnect', () => {
  $('connection-status').textContent = 'Disconnected';
  $('connection-status').className = 'conn-status disconnected';
});
socket.on('available_sets', data => {
  availableSets = data;
  renderSetList();
});
socket.on('state_update', newState => {
  handleStateUpdate(newState);
});
socket.on('game_error', data => {
  console.error('Game error:', data);
  alert('Game error: ' + data.message);
});

// ── Handle state updates ────────────────────────────────────────────────────
function handleStateUpdate(newState) {
  const old = state;
  state = newState;

  if (!newState.phase || newState.phase === 'lobby') {
    showScreen('lobby');
    return;
  }
  if (newState.phase === 'starting') {
    // Loading - keep lobby screen but show indicator
    return;
  }
  if (newState.phase === 'choosing_persona') {
    showScreen('persona');
    renderPersonaSelection();
    return;
  }
  if (newState.phase === 'game_over') {
    showScreen('gameover');
    renderGameOver();
    return;
  }

  // Playing phase
  showScreen('game');
  determineMyPid();
  renderGameBoard(old, newState);
  renderQuery();
  renderTurnIndicator(old, newState);
}

function determineMyPid() {
  if (myPid !== null) return;
  if (!state || !state.players) return;
  const human = state.players.find(p => p.is_human);
  if (human) myPid = human.pid;
}

// ── Lobby ───────────────────────────────────────────────────────────────────
function renderSetList() {
  const container = $('set-list');
  container.innerHTML = '';
  availableSets.forEach(s => {
    const div = document.createElement('div');
    div.className = 'set-item';
    div.dataset.id = s.id;
    div.innerHTML = `
      <div class="set-checkbox"></div>
      <span class="set-name">${s.name}</span>
      <span class="set-badge ${s.large ? 'large' : 'small'}">${s.large ? 'Large' : 'Small'}</span>
    `;
    div.addEventListener('click', () => toggleSet(s.id, div));
    container.appendChild(div);
  });
  // Select base set by default
  const base = container.querySelector('[data-id="0"]');
  if (base) toggleSet(0, base);
}

function toggleSet(id, el) {
  if (selectedSets.includes(id)) {
    selectedSets = selectedSets.filter(x => x !== id);
    el.classList.remove('selected');
  } else {
    selectedSets.push(id);
    el.classList.add('selected');
  }
  $('btn-start-game').disabled = selectedSets.length === 0;
}

document.querySelectorAll('.ai-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.ai-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    numAI = parseInt(btn.dataset.num, 10);
  });
});

$('btn-start-game').addEventListener('click', () => {
  if (selectedSets.length === 0) return;
  socket.emit('start_game', { sets: selectedSets, num_ai: numAI });
  $('btn-start-game').disabled = true;
  $('btn-start-game').textContent = 'Starting…';
});

$('btn-new-game').addEventListener('click', () => {
  socket.emit('abandon_game');
  $('btn-start-game').disabled = selectedSets.length === 0;
  $('btn-start-game').textContent = 'START GAME';
  myPid = null;
  state = null;
  showScreen('lobby');
});

// ── Persona Selection ───────────────────────────────────────────────────────
function renderPersonaSelection() {
  if (!state || !state.query) return;
  const query = state.query;
  const grid  = $('persona-grid');
  grid.innerHTML = '';

  query.options.forEach(opt => {
    if (opt.opt_type !== 'persona') return;
    const div = document.createElement('div');
    div.className = 'persona-thumb';
    div.dataset.id = opt.id;
    div.innerHTML = `
      <img src="${imgUrl(opt.image)}" alt="${opt.name}" onerror="this.style.display='none'" />
      <div class="persona-label">${opt.name}</div>
    `;
    div.addEventListener('click', () => selectPersonaThumb(opt, div));
    grid.appendChild(div);
  });
}

function selectPersonaThumb(opt, el) {
  document.querySelectorAll('.persona-thumb').forEach(t => t.classList.remove('selected'));
  el.classList.add('selected');
  selectedPersonaId = opt.id;

  const detail = $('persona-detail');
  $('persona-detail-img').src = imgUrl(opt.image);
  $('persona-detail-name').textContent = opt.name;
  $('persona-detail-ability').textContent = opt.text || '';
  detail.classList.remove('hidden');
}

$('btn-confirm-persona').addEventListener('click', () => {
  if (!selectedPersonaId) return;
  socket.emit('action', { type: 'card', card_id: selectedPersonaId });
  $('persona-detail').classList.add('hidden');
  selectedPersonaId = null;
});

// ── Game Board ──────────────────────────────────────────────────────────────
function renderGameBoard(old, newState) {
  renderOpponents();
  renderSVStack();
  renderLineup(old);
  renderPlayArea();
  renderPlayerHUD();
}

function renderOpponents() {
  if (!state) return;
  const strip = $('opponents-strip');
  strip.innerHTML = '';
  state.players.forEach(p => {
    if (p.is_human) return;
    const panel = buildOpponentPanel(p);
    strip.appendChild(panel);
  });
}

function buildOpponentPanel(p) {
  const isActive = state.whose_turn === p.pid && state.game_ongoing;
  const div = document.createElement('div');
  div.className = 'opponent-panel' + (isActive ? ' active-turn' : '');
  div.id = `opponent-${p.pid}`;

  const imgSrc = p.persona ? imgUrl(p.persona.image) : '';
  const personaName = p.persona ? p.persona.name : `Player ${p.pid}`;
  const isTurn = state.whose_turn === p.pid;

  div.innerHTML = `
    <img class="opponent-persona-img" src="${imgSrc}" alt="${personaName}" onerror="this.style.display='none'" />
    <div class="opponent-info">
      <div class="opponent-name">${personaName}${isTurn ? ' ▶' : ''}</div>
      <div class="opponent-stats">
        <div class="opp-stat">⚡ <span>${p.power}</span></div>
        <div class="opp-stat">★ <span>${p.score}</span></div>
        <div class="opp-stat">🂠 <span>${p.hand_size}</span></div>
        <div class="opp-stat">🃏 <span>${p.deck_size}</span></div>
      </div>
      <div class="opponent-played">
        ${(p.played_this_turn || []).map(c =>
          `<div class="opp-card-mini" title="${c.name}">
             <img src="${imgUrl(c.image)}" alt="${c.name}" onerror="this.style.display='none'" />
           </div>`
        ).join('')}
      </div>
    </div>
  `;
  return div;
}

function renderSVStack() {
  if (!state) return;
  const svCard  = $('sv-card');
  const svCount = $('sv-count');
  const sv      = state.sv_stack;

  svCount.textContent = sv.count;
  svCard.innerHTML = '';

  if (sv.top) {
    const img = document.createElement('img');
    img.src = imgUrl(sv.top.image);
    img.alt = sv.top.name;
    img.onerror = () => img.style.display = 'none';
    svCard.appendChild(img);

    // Cost badge
    const badge = document.createElement('div');
    badge.className = 'card-cost-badge';
    badge.textContent = sv.top.cost;
    svCard.appendChild(badge);

    // Make buyable if human can afford
    const me = getMyPlayer();
    if (me && isMyTurn() && me.power >= sv.top.cost) {
      svCard.classList.add('buyable');
    } else {
      svCard.classList.remove('buyable');
    }

    svCard.onclick = () => {
      if (isMyTurn()) sendCardAction(sv.top.id);
    };
    addHover(svCard, sv.top);
  }

  $('kick-count').textContent    = state.kick_stack.count;
  $('weakness-count').textContent = state.weakness_stack.count;
  $('main-deck-count').textContent = state.main_deck_size;
}

function renderLineup(old) {
  if (!state) return;
  const container = $('lineup');
  const me = getMyPlayer();

  // Detect newly added lineup cards for slide-in animation
  const oldIds = old && old.lineup ? new Set(old.lineup.map(c => c.id)) : new Set();

  container.innerHTML = '';
  state.lineup.forEach(card => {
    const el = buildGameCard(card, 'lineup');
    const isNew = !oldIds.has(card.id);

    // Check if affordable
    if (me && isMyTurn() && me.power >= card.cost) {
      el.classList.add('buyable');
    }
    el.onclick = () => { if (isMyTurn()) sendCardAction(card.id); };
    addHover(el, card);

    container.appendChild(el);
    cardRegistry[card.id] = el;

    if (isNew && old) {
      // Slide in from deck position
      gsap.from(el, { y: -30, opacity: 0, duration: 0.4, ease: 'back.out(1.4)' });
    }
  });

  // Pad to 5 slots
  const existing = container.querySelectorAll('.game-card').length;
  for (let i = existing; i < 5; i++) {
    const slot = document.createElement('div');
    slot.className = 'lineup-slot';
    slot.textContent = '—';
    container.appendChild(slot);
  }
}

function renderPlayArea() {
  if (!state) return;
  const me = getMyPlayer();
  if (!me) return;

  // Played cards
  const playedContainer = $('played-cards');
  playedContainer.innerHTML = '';
  (me.played || []).forEach(card => {
    const el = buildGameCard(card, 'played');
    addHover(el, card);
    playedContainer.appendChild(el);
    cardRegistry[card.id] = el;
  });

  // Special options (buttons)
  const specialContainer = $('special-options');
  specialContainer.innerHTML = '';
  if (isMyTurn()) {
    (me.special_options || []).forEach(opt => {
      const btn = document.createElement('button');
      btn.className = 'btn-special';
      btn.textContent = opt.text;
      btn.onclick = () => sendSpecialAction(opt.id);
      specialContainer.appendChild(btn);
    });
  }

  // My persona + ongoing
  const personaWrap = $('my-persona-card');
  personaWrap.innerHTML = '';
  if (me.persona) {
    const img = document.createElement('img');
    img.src = imgUrl(me.persona.image);
    img.alt = me.persona.name;
    img.onerror = () => img.style.display = 'none';
    personaWrap.appendChild(img);
    $('my-persona-name').textContent = me.persona.name;
  }

  const ongoingZone = $('my-ongoing');
  ongoingZone.innerHTML = '';
  (me.ongoing || []).forEach(card => {
    const el = buildGameCard(card, 'ongoing', true);
    addHover(el, card);
    ongoingZone.appendChild(el);
  });

  const underZone = $('my-under');
  underZone.innerHTML = '';
  (me.under_persona || []).forEach(card => {
    const el = buildGameCard(card, 'under', true);
    addHover(el, card);
    underZone.appendChild(el);
  });
}

function renderPlayerHUD() {
  if (!state) return;
  const me = getMyPlayer();
  if (!me) return;

  $('power-value').textContent   = me.power;
  $('score-value').textContent   = me.score;
  $('deck-value').textContent    = me.deck_size;
  $('discard-value').textContent = me.discard_size;

  // End turn button
  const btnEnd = $('btn-end-turn');
  const myTurn = isMyTurn();
  btnEnd.disabled = !myTurn;
  btnEnd.classList.toggle('my-turn', myTurn);

  renderHand(me);
}

function renderHand(me) {
  const zone = $('hand-zone');
  zone.innerHTML = '';

  const cards = me.hand || [];
  const count = cards.length;
  const maxW  = zone.offsetWidth || 600;
  const cardW = 88;
  const spread = Math.min((maxW - cardW) / Math.max(count - 1, 1), 80);
  const maxRot = Math.min(3 * count, 18);
  const totalW = (count - 1) * spread + cardW;
  const startX = (maxW - totalW) / 2;

  cards.forEach((card, i) => {
    const fraction = count > 1 ? (i / (count - 1)) - 0.5 : 0;
    const rot   = fraction * maxRot * 2;
    const yOff  = Math.abs(fraction) * 12;
    const xPos  = startX + i * spread;

    const el = buildGameCard(card, 'hand');
    el.classList.add('hand-card');

    // Is it playable on my turn?
    if (isMyTurn()) {
      el.classList.add('playable');
      el.onclick = () => playCard(card, el);
    }

    el.style.left            = xPos + 'px';
    el.style.bottom          = yOff + 'px';
    el.style.zIndex          = i;
    el.style.transform       = `rotate(${rot}deg)`;
    el.style.transformOrigin = 'center bottom';

    addHover(el, card);
    zone.appendChild(el);
    cardRegistry[card.id] = el;
  });
}

// ── Card building ───────────────────────────────────────────────────────────
function buildGameCard(card, context, small = false) {
  const el = document.createElement('div');
  el.className = `game-card ${cardTypeClass(card.type)}`;
  el.dataset.cardId = card.id;
  if (small) el.style.transform = 'scale(0.75)';

  if (card.frozen && card.frozen.length > 0) el.classList.add('frozen');

  const img = document.createElement('img');
  img.src  = imgUrl(card.image);
  img.alt  = card.name;
  img.draggable = false;
  img.onerror = () => {
    img.style.display = 'none';
    el.style.background = getCardColor(card.type);
    el.innerHTML += `<div style="padding:8px;font-size:10px;color:#fff;text-align:center;position:absolute;bottom:0;left:0;right:0">${card.name}</div>`;
  };
  el.appendChild(img);

  // Cost badge for lineup/sv
  if (context === 'lineup' || context === 'sv') {
    const badge = document.createElement('div');
    badge.className = 'card-cost-badge';
    badge.textContent = card.cost;
    el.appendChild(badge);
  }

  return el;
}

function getCardColor(type) {
  const map = {
    hero: '#0d2a5e', villain: '#3b0000', superpower: '#2a0050',
    equipment: '#002a12', location: '#2a1400', starter: '#1a2030',
    weakness: '#1a0030', special_sv: '#3b0000',
  };
  return map[type] || '#1a2030';
}

// ── Actions ─────────────────────────────────────────────────────────────────
function isMyTurn() {
  if (!state) return false;
  const me = getMyPlayer();
  if (!me) return false;
  return state.whose_turn === me.pid && state.game_ongoing && !state.query;
}

function sendCardAction(cardId) {
  socket.emit('action', { type: 'card', card_id: cardId });
}

function sendButtonAction(value) {
  socket.emit('action', { type: 'button', action: value });
}

function sendSpecialAction(specialId) {
  socket.emit('action', { type: 'special', special_id: specialId });
}

function playCard(card, el) {
  // Animate card from hand to play area, then send action
  const playArea = $('played-cards');
  const targetRect = playArea.getBoundingClientRect();
  const sourceRect = el.getBoundingClientRect();

  // Create flying clone
  const clone = el.cloneNode(true);
  clone.style.cssText = `
    position:fixed; left:${sourceRect.left}px; top:${sourceRect.top}px;
    width:${sourceRect.width}px; height:${sourceRect.height}px;
    z-index:200; pointer-events:none; border-radius:8px; overflow:hidden;
  `;
  document.body.appendChild(clone);

  const destX = targetRect.left + targetRect.width / 2 - sourceRect.width / 2;
  const destY = targetRect.top  + targetRect.height / 2 - sourceRect.height / 2;

  gsap.to(clone, {
    left: destX, top: destY, duration: 0.35,
    ease: 'power2.out',
    onComplete: () => {
      clone.remove();
      sendCardAction(card.id);
    }
  });
}

$('btn-end-turn').addEventListener('click', () => {
  if (!isMyTurn()) return;
  sendButtonAction('end_turn');
  $('btn-end-turn').disabled = true;
  $('btn-end-turn').classList.remove('my-turn');
});

// ── Query modal ─────────────────────────────────────────────────────────────
function renderQuery() {
  const modal = $('query-modal');
  if (!state || !state.query) {
    modal.classList.add('hidden');
    return;
  }
  modal.classList.remove('hidden');
  const q = state.query;

  $('query-text').textContent = q.text;

  // Context card
  const ctxEl = $('query-context-card');
  ctxEl.innerHTML = '';
  if (q.context_card) {
    const img = document.createElement('img');
    img.src = imgUrl(q.context_card.image);
    img.alt = q.context_card.name;
    img.onerror = () => img.style.display = 'none';
    ctxEl.appendChild(img);
  }

  // Options
  const optContainer = $('query-options');
  optContainer.innerHTML = '';

  q.options.forEach(opt => {
    if (opt.opt_type === 'card') {
      const wrap = document.createElement('div');
      wrap.className = 'query-option-card';
      const el = buildGameCard(opt, 'query');
      addHover(el, opt);
      el.onclick = () => {
        modal.classList.add('hidden');
        sendCardAction(opt.id);
      };
      wrap.appendChild(el);
      optContainer.appendChild(wrap);
    } else if (opt.opt_type === 'persona') {
      const wrap = document.createElement('div');
      wrap.className = 'query-option-card persona-thumb';
      wrap.style.cssText = 'width:90px;cursor:pointer;';
      wrap.innerHTML = `
        <img src="${imgUrl(opt.image)}" style="width:100%;border-radius:6px;" alt="${opt.name}" onerror="this.style.display='none'" />
        <div class="persona-label">${opt.name}</div>
      `;
      wrap.onclick = () => {
        modal.classList.add('hidden');
        sendCardAction(opt.id);
      };
      optContainer.appendChild(wrap);
    } else if (opt.opt_type === 'button') {
      const btn = document.createElement('button');
      btn.className = 'query-btn';
      if (opt.action === 2) btn.classList.add('ok'); // OK
      if (opt.action === 1) btn.classList.add('no'); // NO
      btn.textContent = opt.label;
      btn.onclick = () => {
        modal.classList.add('hidden');
        sendButtonAction(opt.action);
      };
      optContainer.appendChild(btn);
    }
  });
}

// ── Turn indicator ──────────────────────────────────────────────────────────
function renderTurnIndicator(old, newState) {
  if (!old || !newState) return;
  if (old.whose_turn === newState.whose_turn) return;
  if (newState.whose_turn < 0) return;

  const banner = $('turn-banner');
  const p = newState.players[newState.whose_turn];
  const name = p && p.persona ? p.persona.name : `Player ${newState.whose_turn}`;
  const isMe = p && p.is_human;
  banner.textContent = isMe ? `YOUR TURN` : `${name}'s Turn`;
  banner.classList.remove('hidden');
  gsap.fromTo(banner,
    { scale: 1.4, opacity: 0 },
    {
      scale: 1, opacity: 1, duration: 0.3, ease: 'back.out(2)',
      onComplete: () => {
        gsap.to(banner, { opacity: 0, delay: 1.5, duration: 0.4, onComplete: () => banner.classList.add('hidden') });
      }
    }
  );
}

// ── Game over ───────────────────────────────────────────────────────────────
function renderGameOver() {
  if (!state) return;
  const scoresEl = $('gameover-scores');
  scoresEl.innerHTML = '';

  // Build sorted scores
  const players = state.players.slice();
  const scores  = state.player_scores || [];
  const ranked  = players.map((p, i) => ({
    name: p.persona ? p.persona.name : `Player ${p.pid}`,
    score: scores[i] !== undefined ? scores[i] : p.score,
    isHuman: p.is_human,
  })).sort((a, b) => b.score - a.score);

  ranked.forEach((p, i) => {
    const row = document.createElement('div');
    row.className = 'score-row';
    row.innerHTML = `
      <div class="score-rank ${i === 0 ? 'first' : ''}">${i + 1}</div>
      <div class="score-name">${p.name}${p.isHuman ? ' (You)' : ''}</div>
      <div class="score-pts">${p.score} <span>VP</span></div>
    `;
    scoresEl.appendChild(row);
    gsap.from(row, { x: -40, opacity: 0, delay: i * 0.15, duration: 0.4, ease: 'power2.out' });
  });
}

// ── Card preview tooltip ─────────────────────────────────────────────────────
const preview = $('card-preview');
let previewTimeout = null;

function addHover(el, card) {
  el.addEventListener('mouseenter', e => {
    clearTimeout(previewTimeout);
    previewTimeout = setTimeout(() => showPreview(e, card), 200);
  });
  el.addEventListener('mousemove', e => movePreview(e));
  el.addEventListener('mouseleave', () => {
    clearTimeout(previewTimeout);
    hidePreview();
  });
}

function showPreview(e, card) {
  $('preview-img').src  = imgUrl(card.image);
  $('preview-img').alt  = card.name;
  $('preview-name').textContent = card.name;
  $('preview-text').textContent = card.text || card.attack_text || '';
  $('preview-cost').textContent = `⚡${card.cost}`;
  $('preview-vp').textContent   = `★${card.vp}`;
  $('preview-type').textContent = (card.type || '').toUpperCase();
  preview.classList.remove('hidden');
  movePreview(e);
}

function movePreview(e) {
  if (preview.classList.contains('hidden')) return;
  const pw = 240, ph = 320;
  let x = e.clientX + 16;
  let y = e.clientY - 80;
  if (x + pw > window.innerWidth  - 8) x = e.clientX - pw - 16;
  if (y + ph > window.innerHeight - 8) y = window.innerHeight - ph - 8;
  if (y < 8) y = 8;
  preview.style.left = x + 'px';
  preview.style.top  = y + 'px';
}

function hidePreview() {
  preview.classList.add('hidden');
}

// ── Kick/Weakness pile clicks ─────────────────────────────────────────────────
$('pile-kick').addEventListener('click', () => {
  if (isMyTurn() && state && state.kick_stack.count > 0 && state.kick_stack.top_id) {
    sendCardAction(state.kick_stack.top_id);
  }
});

$('pile-weakness').addEventListener('click', () => { /* weakness cannot be bought by player */ });

// ── Init ─────────────────────────────────────────────────────────────────────
(function init() {
  socket.emit('get_sets');
  showScreen('lobby');

  // Restore "start game" button state
  $('btn-start-game').disabled = true;
})();
