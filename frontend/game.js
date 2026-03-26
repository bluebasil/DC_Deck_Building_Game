/* ═══════════════════════════════════════════════════════════════
   DC DECK BUILDING GAME — Frontend Client
   ═══════════════════════════════════════════════════════════════ */

'use strict';

// ── Config ─────────────────────────────────────────────────────────────────
const SERVER_URL = window.location.hostname === 'localhost'
    ? window.location.origin
    : 'https://dc-deck-builder-16370628759.us-central1.run.app';
const IMG_ROOT   = 'card-images/';

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

// Drag-to-play state
let draggedCard = null;
let draggedEl   = null;

// Action log - list of {playerName, cardName, verb}
const actionLog = [];

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
  $('conn-dropdown').classList.add('hidden');
});

// Toggle dropdown on badge click (only when connected)
$('connection-status').addEventListener('click', e => {
  if (!$('connection-status').classList.contains('connected')) return;
  e.stopPropagation();
  $('conn-dropdown').classList.toggle('hidden');
});

// Restart game
$('restart-btn').addEventListener('click', () => {
  $('conn-dropdown').classList.add('hidden');
  socket.emit('abandon_game');
});

// Close dropdown when clicking outside
document.addEventListener('click', e => {
  if (!$('conn-wrapper').contains(e.target)) {
    $('conn-dropdown').classList.add('hidden');
  }
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
  updateActionLog(newState);

  // Calculate card movement animations BEFORE re-rendering (needs old cardRegistry positions)
  const pendingAnims = calcAnimations(
    old && old.card_positions,
    newState.card_positions,
    old
  );

  renderGameBoard(old);
  renderQuery();
  renderTurnIndicator(old, newState);

  // Play animations as overlays after board is updated
  playAnimations(pendingAnims);
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
  // Clear action log on new game
  actionLog.length = 0;
  renderActionLog();
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
function renderGameBoard(old) {
  renderOpponents();
  renderSVStack();
  renderLineup(old);
  renderPlayArea();
  renderPlayerHUD();
}

function renderOpponents() {
  if (!state) return;
  const strip = $('opponents-panels');
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
        <div class="opp-stat opp-discard-btn" title="View discard pile">♻ <span>${p.discard_size}</span></div>
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

  div.querySelector('.opp-discard-btn').addEventListener('click', e => {
    e.stopPropagation();
    const current = state.players.find(pl => pl.pid === p.pid);
    openDiscardModal(current || p);
  });

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

    const badge = document.createElement('div');
    badge.className = 'card-cost-badge';
    badge.textContent = sv.top.cost;
    svCard.appendChild(badge);

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

  // Kick pile — show top card face-up
  // const kickPileCard = $('pile-kick').querySelector('.pile-card');
  const kickCard  = $('kick-card');
  const kickCount = $('kick-count');
  const kick = state.kick_stack;

  kickCount.textContent = kick.count;
  kickCard.innerHTML = '';

  if (kick.top) {
    const img = document.createElement('img');
    img.src = imgUrl(kick.top.image);
    img.alt = kick.top.name;
    img.onerror = () => img.style.display = 'none';
    kickCard.appendChild(img);

    const badge = document.createElement('div');
    badge.className = 'card-cost-badge';
    badge.textContent = kick.top.cost;
    kickCard.appendChild(badge);

    const me = getMyPlayer();
    if (me && isMyTurn() && me.power >= kick.top.cost) {
      kickCard.classList.add('buyable');
    } else {
      kickCard.classList.remove('buyable');
    }

    kickCard.onclick = () => {
      if (isMyTurn()) sendCardAction(kick.top.id);
    };
    addHover(kickCard, kick.top);
  }

  $('weakness-count').textContent  = state.weakness_stack.count;
  $('main-deck-count').textContent = state.main_deck_size;
  $('destroyed-count').textContent = state.destroyed_count || 0;
}

function renderLineup(old) {
  if (!state) return;
  const container = $('lineup');
  const me = getMyPlayer();

  const oldIds = old && old.lineup ? new Set(old.lineup.map(c => c.id)) : new Set();

  container.innerHTML = '';
  state.lineup.forEach(card => {
    const el = buildGameCard(card, 'lineup');
    const isNew = !oldIds.has(card.id);

    if (me && isMyTurn() && me.power >= card.cost) {
      el.classList.add('buyable');
    }
    el.onclick = () => { if (isMyTurn()) sendCardAction(card.id); };
    addHover(el, card);

    container.appendChild(el);
    cardRegistry[card.id] = el;

    if (isNew && old) {
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

  // Drop hint when play area is empty
  if ((me.played || []).length === 0) {
    const hint = document.createElement('div');
    hint.className = 'drop-hint';
    hint.textContent = isMyTurn() ? 'Drag or click cards from hand to play' : '—';
    playedContainer.appendChild(hint);
  }

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
    // Persona hover shows ability text
    addPersonaHover(personaWrap, me.persona);
  }

  const ongoingZone = $('my-ongoing');
  ongoingZone.innerHTML = '';
  (me.ongoing || []).forEach(card => {
    const el = buildGameCard(card, 'ongoing', true);
    addHover(el, card);
    ongoingZone.appendChild(el);
    cardRegistry[card.id] = el;
  });

  // Above/under persona pile count buttons
  const overCount  = (me.over_persona  || []).length;
  const underCount = (me.under_persona || []).length;
  const btnOver  = $('btn-over-persona');
  const btnUnder = $('btn-under-persona');
  $('over-persona-count').textContent  = overCount;
  $('under-persona-count').textContent = underCount;
  btnOver.classList.toggle('hidden',  overCount  === 0);
  btnUnder.classList.toggle('hidden', underCount === 0);
}

function renderPlayerHUD() {
  if (!state) return;
  const me = getMyPlayer();
  if (!me) return;

  $('power-value').textContent   = me.power;
  $('score-value').textContent   = me.score;
  $('deck-value').textContent    = me.deck_size;
  $('discard-value').textContent = me.discard_size;

  // Power bar near lineup
  const powerBar = $('power-bar');
  const myTurn = isMyTurn();
  $('lineup-power-value').textContent = me.power;
  $('lineup-turn-num').textContent    = state.turn_number || 1;
  $('power-bar-status').textContent   = myTurn ? 'YOUR TURN' : 'WAITING';
  powerBar.classList.toggle('my-turn', myTurn);

  // End turn button
  const btnEnd = $('btn-end-turn');
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
  const cardW = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--hand-card-w'), 10) || 120;
  const spread = Math.min((maxW - cardW) / Math.max(count - 1, 1), 88);
  const maxRot = Math.min(3 * count, 18);
  const totalW = (count - 1) * spread + cardW;
  const startX = (maxW - totalW) / 2;

  cards.forEach((card, i) => {
    const fraction = count > 1 ? (i / (count - 1)) - 0.5 : 0;
    const rot   = fraction * maxRot * 2;
    const yOff  = Math.abs(fraction) * 14;
    const xPos  = startX + i * spread;

    const el = buildGameCard(card, 'hand');
    el.classList.add('hand-card');

    if (isMyTurn()) {
      el.classList.add('playable');
      el.onclick = () => playCard(card);
    }

    el.style.left            = xPos + 'px';
    el.style.bottom          = yOff + 'px';
    el.style.zIndex          = i;
    el.style.transform       = `rotate(${rot}deg)`;
    el.style.transformOrigin = 'center bottom';

    // Drag to play
    if (isMyTurn()) {
      el.draggable = true;
      el.addEventListener('dragstart', e => {
        draggedCard = card;
        draggedEl   = el;
        el.classList.add('dragging');
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/plain', card.id);
      });
      el.addEventListener('dragend', () => {
        draggedCard = null;
        draggedEl   = null;
        el.classList.remove('dragging');
        $('played-cards').classList.remove('drop-active');
      });
    }

    addHover(el, card, isMyTurn()); // skipTouch=true when playable — addTouchDrag handles it
    if (isMyTurn()) addTouchDrag(el, card);
    zone.appendChild(el);
    cardRegistry[card.id] = el;
  });
}

// ── Drop zone ───────────────────────────────────────────────────────────────
function initDropZone() {
  const zone = $('played-cards');
  zone.addEventListener('dragover', e => {
    if (!isMyTurn() || !draggedCard) return;
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    zone.classList.add('drop-active');
  });
  zone.addEventListener('dragleave', e => {
    // Only remove class if actually leaving the zone (not entering a child)
    if (!zone.contains(e.relatedTarget)) {
      zone.classList.remove('drop-active');
    }
  });
  zone.addEventListener('drop', e => {
    e.preventDefault();
    zone.classList.remove('drop-active');
    if (draggedCard && isMyTurn()) {
      const card = draggedCard;
      draggedCard = null;
      draggedEl   = null;
      playCard(card);
    }
  });
}

// ── Touch drag-to-play (mobile) ──────────────────────────────────────────────
function createGhostCard(sourceEl, rect) {
  const ghost = document.createElement('div');
  ghost.style.cssText = `
    position:fixed; left:${rect.left}px; top:${rect.top}px;
    width:${rect.width}px; height:${rect.height}px;
    z-index:9999; pointer-events:none;
    border-radius:8px; overflow:hidden;
    border:2px solid rgba(201,162,39,.9);
    box-shadow:0 12px 32px rgba(0,0,0,.75), 0 0 20px rgba(201,162,39,.5);
    transform-origin:center center;
  `;
  const img = sourceEl.querySelector('img');
  if (img) {
    const gi = document.createElement('img');
    gi.src = img.src;
    gi.style.cssText = 'width:100%;height:100%;object-fit:cover;display:block;';
    gi.draggable = false;
    ghost.appendChild(gi);
  } else {
    ghost.style.background = getComputedStyle(sourceEl).background;
  }
  document.body.appendChild(ghost);
  return ghost;
}

// Attach immediate touch drag-to-play to a hand card element.
// - Tap  (<8 px movement, <500 ms) → lets the existing onclick fire.
// - Hold (>500 ms, no movement)    → shows card preview.
// - Drag (>8 px movement)          → ghost card follows finger; release over
//   play area plays the card; release elsewhere snaps ghost back.
function addTouchDrag(el, card) {
  el.addEventListener('touchstart', e => {
    const t0        = e.touches[0];
    const startX    = t0.clientX;
    const startY    = t0.clientY;
    const touchOffX = t0.clientX - el.getBoundingClientRect().left;
    const touchOffY = t0.clientY - el.getBoundingClientRect().top;
    const startRect = el.getBoundingClientRect();   // snapshot before any layout shift
    let isDragging  = false;
    let ghost       = null;

    // Long-hold without movement → show preview
    let holdTimer = setTimeout(() => {
      holdTimer = null;
      if (!isDragging) showPreviewAtRect(el.getBoundingClientRect(), card);
    }, 500);

    function onMove(e) {
      const t  = e.touches[0];
      const dx = t.clientX - startX;
      const dy = t.clientY - startY;

      if (!isDragging) {
        if (Math.abs(dx) < 8 && Math.abs(dy) < 8) return;
        // Movement threshold crossed — start drag
        isDragging = true;
        if (holdTimer !== null) { clearTimeout(holdTimer); holdTimer = null; }
        hidePreview();
        ghost = createGhostCard(el, startRect);
        el.style.opacity = '0.3';
        gsap.fromTo(ghost, { scale: 1 }, { scale: 1.12, duration: 0.15, ease: 'back.out(2)' });
      }

      e.preventDefault(); // prevent page scroll while dragging

      // Ghost follows finger, offset so it appears where the card was grabbed
      ghost.style.left = (t.clientX - touchOffX) + 'px';
      ghost.style.top  = (t.clientY - touchOffY) + 'px';

      // Highlight drop zone
      const over = document.elementFromPoint(t.clientX, t.clientY);
      $('played-cards').classList.toggle('drop-active', $('played-cards').contains(over));
    }

    function cleanup() {
      el.removeEventListener('touchmove', onMove);
      el.removeEventListener('touchend',   onEnd);
      el.removeEventListener('touchcancel', onCancel);
    }

    function onEnd(e) {
      if (holdTimer !== null) { clearTimeout(holdTimer); holdTimer = null; }
      cleanup();
      if (!isDragging) return; // was a tap — let onclick fire normally

      e.preventDefault(); // suppress click since drag handled interaction
      el.style.opacity = '';
      const t = e.changedTouches[0];
      const over = document.elementFromPoint(t.clientX, t.clientY);
      const dropZone = $('played-cards');
      dropZone.classList.remove('drop-active');

      if (dropZone.contains(over)) {
        // Fly ghost into play area, then play the card
        const dest = dropZone.getBoundingClientRect();
        gsap.to(ghost, {
          left:  dest.left + (dest.width  - startRect.width)  / 2,
          top:   dest.top  + (dest.height - startRect.height) / 2,
          scale: 0.85, opacity: 0, duration: 0.2, ease: 'power2.in',
          onComplete: () => ghost.remove(),
        });
        playCard(card);
      } else {
        // Snap ghost back to where the card lives
        gsap.to(ghost, {
          left: startRect.left, top: startRect.top,
          scale: 1, opacity: 0, duration: 0.25, ease: 'power2.out',
          onComplete: () => ghost.remove(),
        });
      }
    }

    function onCancel() {
      if (holdTimer !== null) { clearTimeout(holdTimer); holdTimer = null; }
      cleanup();
      if (isDragging) {
        el.style.opacity = '';
        if (ghost) ghost.remove();
        $('played-cards').classList.remove('drop-active');
      }
    }

    el.addEventListener('touchmove',   onMove);   // not passive — needs preventDefault
    el.addEventListener('touchend',    onEnd);
    el.addEventListener('touchcancel', onCancel);
  }, { passive: true });
  // Suppress Chrome's native long-press context menu on images
  el.addEventListener('contextmenu', e => e.preventDefault());
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

function playCard(card) {
  // Send action immediately; state-diff animation will fire on state update
  // using the card's current position in cardRegistry as the source rect.
  sendCardAction(card.id);
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

  const ctxEl = $('query-context-card');
  ctxEl.innerHTML = '';
  if (q.context_card) {
    const img = document.createElement('img');
    img.src = imgUrl(q.context_card.image);
    img.alt = q.context_card.name;
    img.onerror = () => img.style.display = 'none';
    ctxEl.appendChild(img);
  }

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
      if (opt.action === 2) btn.classList.add('ok');
      if (opt.action === 1) btn.classList.add('no');
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
        gsap.to(banner, { opacity: 0, delay: 2.5, duration: 0.4, onComplete: () => banner.classList.add('hidden') });
      }
    }
  );
}

// ── Game over ───────────────────────────────────────────────────────────────
function renderGameOver() {
  if (!state) return;

  const endReason    = state.end_reason || 'regular';
  const scores       = state.player_scores || [];
  const everyoneLost = endReason === 'main_deck';

  const ranked = state.players.slice()
    .map((p, i) => ({
      name:    p.persona ? p.persona.name : `Player ${p.pid}`,
      image:   p.persona ? imgUrl(p.persona.image) : '',
      score:   scores[i] !== undefined ? scores[i] : p.score,
      isHuman: p.is_human,
    }))
    .sort((a, b) => b.score - a.score);

  const humanWon = ranked.findIndex(p => p.isHuman) === 0;

  // ── Result heading ──────────────────────────────────────────
  const resultEl = $('gameover-result');
  const reasonEl = $('gameover-reason');

  if (everyoneLost) {
    resultEl.textContent = 'EVERYONE LOST';
    resultEl.className   = 'gameover-result everyone-lost';
    reasonEl.textContent = 'The main deck ran out of cards';
  } else if (humanWon) {
    resultEl.textContent = 'YOU WIN!';
    resultEl.className   = 'gameover-result win';
    reasonEl.textContent = 'All supervillains defeated';
  } else {
    resultEl.textContent = 'YOU LOSE';
    resultEl.className   = 'gameover-result lose';
    reasonEl.textContent = 'All supervillains defeated';
  }

  gsap.fromTo(resultEl,
    { scale: 1.45, opacity: 0 },
    { scale: 1, opacity: 1, duration: 0.55, ease: 'back.out(2.2)' }
  );
  gsap.from(reasonEl, { opacity: 0, y: 8, duration: 0.35, delay: 0.45 });

  // ── Score table ─────────────────────────────────────────────
  const scoresEl = $('gameover-scores');
  scoresEl.innerHTML = '';

  ranked.forEach((p, i) => {
    const isWinner = i === 0 && !everyoneLost;
    const row = document.createElement('div');
    row.className = ['score-row', isWinner ? 'winner' : '', p.isHuman ? 'human' : ''].filter(Boolean).join(' ');
    row.innerHTML = `
      <div class="score-rank ${isWinner ? 'first' : ''}">${i + 1}</div>
      ${p.image ? `<img class="score-persona-img" src="${p.image}" alt="${p.name}" onerror="this.style.display='none'">` : ''}
      <div class="score-name">${p.name}${p.isHuman ? '<span class="you-badge">YOU</span>' : ''}</div>
      <div class="score-pts">${p.score} <span>VP</span></div>
      ${isWinner ? '<div class="score-trophy">🏆</div>' : ''}
    `;
    scoresEl.appendChild(row);
    gsap.from(row, { x: -50, opacity: 0, delay: 0.6 + i * 0.12, duration: 0.38, ease: 'power2.out' });
  });
}

// ── Action log ───────────────────────────────────────────────────────────────
// Uses the events array from the server (populated by globe.add_event()) rather
// than comparing played_this_turn, so CPU actions are always captured.
function updateActionLog(newState) {
  if (!newState) return;
  const events = newState.events || [];
  events.forEach(event => {
    const player = newState.players && newState.players.find(p => p.pid === event.pid);
    if (!player) return;
    const name = player.persona ? player.persona.name : `P${event.pid}`;
    if (event.type === 'play') addLogEntry(name, event.card_name, 'played', player.is_human);
    if (event.type === 'gain') addLogEntry(name, event.card_name, 'bought', player.is_human);
  });
}

function addLogEntry(playerName, cardName, verb, isHuman) {
  actionLog.unshift({ playerName, cardName, verb: verb || 'played', isHuman: !!isHuman });
  if (actionLog.length > 15) actionLog.pop();
  renderActionLog();
}

function renderActionLog() {
  const container = $('action-log-entries');
  if (!container) return;
  container.innerHTML = '';
  if (actionLog.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'log-entry';
    empty.style.opacity = '0.35';
    empty.textContent = 'No moves yet';
    container.appendChild(empty);
    return;
  }
  actionLog.forEach(entry => {
    const div = document.createElement('div');
    div.className = 'log-entry';
    if (entry.isHuman) div.classList.add('log-entry-human');
    const verbClass = entry.verb === 'bought' ? 'log-verb-buy' : 'log-verb-play';
    div.innerHTML = `<span class="log-player">${entry.playerName}</span> <span class="${verbClass}">${entry.verb}</span> <span class="log-card">${entry.cardName}</span>`;
    container.appendChild(div);
  });
}

// ── Discard pile popup ────────────────────────────────────────────────────────
function openDiscardModal(player) {
  const p = player || getMyPlayer();
  if (!p) return;

  const titleEl = $('discard-modal').querySelector('.discard-panel-title');
  if (titleEl) {
    const name = p.persona ? p.persona.name : `Player ${p.pid}`;
    titleEl.textContent = p.is_human ? 'YOUR DISCARD PILE' : `${name}'s DISCARD PILE`;
  }

  const grid = $('discard-cards-grid');
  grid.innerHTML = '';

  const cards = p.discard_cards || [];
  if (cards.length === 0) {
    grid.innerHTML = '<div class="discard-empty">Discard pile is empty</div>';
  } else {
    // Show most recent first (reverse order)
    [...cards].reverse().forEach(card => {
      const el = buildGameCard(card, 'discard');
      addHover(el, card);
      grid.appendChild(el);
    });
  }

  $('discard-modal').classList.remove('hidden');
}

function closeDiscardModal() {
  $('discard-modal').classList.add('hidden');
  hidePreview();
}

$('hud-discard').addEventListener('click', () => openDiscardModal());
$('btn-close-discard').addEventListener('click', closeDiscardModal);
$('discard-backdrop').addEventListener('click', closeDiscardModal);

// ── Persona pile modals ───────────────────────────────────────────────────────
function openPersonaPileModal(which) {
  const me = getMyPlayer();
  if (!me) return;
  const cards  = which === 'over' ? (me.over_persona || []) : (me.under_persona || []);
  const gridId = which === 'over' ? 'over-persona-cards-grid' : 'under-persona-cards-grid';
  const modalId = which === 'over' ? 'over-persona-modal' : 'under-persona-modal';
  const grid = $(gridId);
  grid.innerHTML = '';
  if (cards.length === 0) {
    grid.innerHTML = '<div class="discard-empty">No cards here</div>';
  } else {
    cards.forEach(card => { const el = buildGameCard(card); addHover(el, card); grid.appendChild(el); });
  }
  $(modalId).classList.remove('hidden');
}
function closePersonaPileModal(which) {
  const modalId = which === 'over' ? 'over-persona-modal' : 'under-persona-modal';
  $(modalId).classList.add('hidden');
  hidePreview();
}
$('btn-over-persona').addEventListener('click',       () => openPersonaPileModal('over'));
$('btn-under-persona').addEventListener('click',      () => openPersonaPileModal('under'));
$('btn-close-over-persona').addEventListener('click', () => closePersonaPileModal('over'));
$('btn-close-under-persona').addEventListener('click',() => closePersonaPileModal('under'));
$('over-persona-backdrop').addEventListener('click',  () => closePersonaPileModal('over'));
$('under-persona-backdrop').addEventListener('click', () => closePersonaPileModal('under'));

// ── Destroyed pile modal ──────────────────────────────────────────────────────
function openDestroyedModal() {
  const grid = $('destroyed-cards-grid');
  grid.innerHTML = '';
  const cards = (state && state.destroyed_cards) || [];
  if (cards.length === 0) {
    grid.innerHTML = '<div class="discard-empty">No destroyed cards</div>';
  } else {
    cards.forEach(card => { const el = buildGameCard(card); addHover(el, card); grid.appendChild(el); });
  }
  $('destroyed-modal').classList.remove('hidden');
}
function closeDestroyedModal() {
  $('destroyed-modal').classList.add('hidden');
  hidePreview();
}
$('pile-destroyed').addEventListener('click', openDestroyedModal);
$('btn-close-destroyed').addEventListener('click', closeDestroyedModal);
$('destroyed-backdrop').addEventListener('click', closeDestroyedModal);

// ── Card preview tooltip ─────────────────────────────────────────────────────
const preview = $('card-preview');
let previewTimeout = null;
let previewFromTouch = false;

// skipTouch: pass true for hand cards — addTouchDrag handles their touch events.
function addHover(el, card, skipTouch = false) {
  el.addEventListener('mouseenter', e => {
    clearTimeout(previewTimeout);
    previewTimeout = setTimeout(() => showPreview(e, card), 200);
  });
  el.addEventListener('mousemove', e => movePreview(e));
  el.addEventListener('mouseleave', () => {
    clearTimeout(previewTimeout);
    hidePreview();
  });

  if (skipTouch) return;

  // Mobile: long-press (500ms) shows preview for non-draggable cards
  let touchHoldTimer = null;
  el.addEventListener('touchstart', () => {
    touchHoldTimer = setTimeout(() => {
      touchHoldTimer = null;
      showPreviewAtRect(el.getBoundingClientRect(), card);
    }, 500);
  }, { passive: true });
  el.addEventListener('touchend',   () => { if (touchHoldTimer !== null) { clearTimeout(touchHoldTimer); touchHoldTimer = null; } });
  el.addEventListener('touchmove',  () => { if (touchHoldTimer !== null) { clearTimeout(touchHoldTimer); touchHoldTimer = null; } }, { passive: true });
  el.addEventListener('touchcancel',() => { if (touchHoldTimer !== null) { clearTimeout(touchHoldTimer); touchHoldTimer = null; } });
  // Suppress Chrome's native long-press context menu on images
  el.addEventListener('contextmenu', e => e.preventDefault());
}

// Persona hover using the same tooltip mechanism
function addPersonaHover(el, persona) {
  const fakeCard = {
    image: persona.image,
    name:  persona.name,
    text:  persona.text || '',
    attack_text: '',
    cost: '—',
    vp:   '—',
    type: 'persona',
  };
  addHover(el, fakeCard);
}

function showPreview(e, card) {
  if (previewFromTouch) return;  // don't let synthesized mouseenter override a touch preview
  $('preview-img').src  = imgUrl(card.image);
  $('preview-img').alt  = card.name;
  $('preview-name').textContent = card.name;
  $('preview-text').textContent = card.text || card.attack_text || '';
  $('preview-cost').textContent = `⚡ ${card.cost}`;
  $('preview-vp').textContent   = `★ ${card.vp}`;
  $('preview-type').textContent = (card.type || '').toUpperCase();
  preview.classList.remove('hidden');
  movePreview(e);
}

function movePreview(e) {
  if (preview.classList.contains('hidden')) return;
  if (previewFromTouch) return;
  const pw = 340, ph = 420;
  let x = e.clientX + 18;
  let y = e.clientY - 100;
  if (x + pw > window.innerWidth  - 8) x = e.clientX - pw - 18;
  if (y + ph > window.innerHeight - 8) y = window.innerHeight - ph - 8;
  if (y < 8) y = 8;
  preview.style.left = x + 'px';
  preview.style.top  = y + 'px';
}

function hidePreview() {
  previewFromTouch = false;
  preview.classList.add('hidden');
}

// Show preview anchored to an element rect (used by mobile long-press).
// autoHide=true: dismiss after 3 s (view-only cards).
// autoHide=false: caller manages dismissal (drag-to-play mode).
function showPreviewAtRect(_rect, card, autoHide = false) {
  previewFromTouch = true;
  $('preview-img').src  = imgUrl(card.image);
  $('preview-img').alt  = card.name;
  $('preview-name').textContent = card.name;
  $('preview-text').textContent = card.text || card.attack_text || '';
  $('preview-cost').textContent = `⚡ ${card.cost}`;
  $('preview-vp').textContent   = `★ ${card.vp}`;
  $('preview-type').textContent = (card.type || '').toUpperCase();
  preview.classList.remove('hidden');

  const pw = Math.min(240, window.innerWidth * 0.80);
  preview.style.left = ((window.innerWidth - pw) / 2) + 'px';
  preview.style.top  = '15%';

  if (autoHide) setTimeout(hidePreview, 3000);
}

// Hide the preview on any click or touch (card removed from DOM before mouseleave fires)
document.addEventListener('mousedown', () => {
  clearTimeout(previewTimeout);
  hidePreview();
});
document.addEventListener('touchstart', e => {
  if (!preview.contains(e.target)) {
    clearTimeout(previewTimeout);
    hidePreview();
  }
}, { passive: true });

// ── Card movement animations ─────────────────────────────────────────────────
// Called BEFORE renderGameBoard so old cardRegistry positions are still valid.
// Uses full card_positions diff for resilient detection of any card movement.

// Reference card dimensions for each pile element (width × height in px, maintaining ~5:7 ratio)
const PILE_CARD_SIZE = {
  'lineup':            { w: 110, h: 154 },
  'pile-kick':         { w: 55, h: 77 },
  'pile-weakness':     { w: 55, h: 77 },
  'pile-main-deck':    { w: 55, h: 77 },
  'pile-destroyed':    { w: 55, h: 77 },
  'sv-stack':          { w: 88, h: 124 },
  'hud-discard':       { w: 55, h: 77 },
  'hud-player-deck':   { w: 55, h: 77 },
  'played-cards':      { w: 88, h: 124 },
  'hand-zone':         { w: 88, h: 124 },
  'my-ongoing':        { w: 66, h: 93 },
  'btn-under-persona': { w: 55, h: 77 },
  'btn-over-persona':  { w: 55, h: 77 },
};

// Whether a pile shows cards face-down (card back visible)
function isFaceDown(pileName) {
  if (!pileName) return false;
  if (pileName === 'main_deck') return true;
  if (pileName.endsWith('_deck')) return true;          // all player decks
  if (myPid !== null) {
    if (pileName === `p${myPid}_hand`)  return false;   // human hand: face-up
    if (pileName === `p${myPid}_under`) return false;   // human under-hero: face-up
  }
  if (pileName.endsWith('_hand'))  return true;         // opponent hands
  if (pileName.endsWith('_under')) return true;         // opponent under-hero
  return false;                                         // everything else: face-up
}

function getPileElementId(pileName) {
  if (!pileName) return null;
  if (pileName === 'main_deck')      return 'pile-main-deck';
  if (pileName === 'lineup')         return 'lineup';
  if (pileName === 'kick_stack')     return 'pile-kick';
  if (pileName === 'weakness_stack') return 'pile-weakness';
  if (pileName === 'sv_stack')       return 'sv-stack';
  if (pileName === 'destroyed')      return 'pile-destroyed';
  if (myPid !== null) {
    if (pileName === `p${myPid}_discard`) return 'hud-discard';
    if (pileName === `p${myPid}_played`)  return 'played-cards';
    if (pileName === `p${myPid}_ongoing`) return 'my-ongoing';
    if (pileName === `p${myPid}_under`)   return 'btn-under-persona';
    if (pileName === `p${myPid}_over`)    return 'btn-over-persona';
    if (pileName === `p${myPid}_hand`)    return 'hand-zone';
    if (pileName === `p${myPid}_deck`)    return 'hud-player-deck';
    // All opponent piles → their opponent panel element
    const m = pileName.match(/^p(\d+)_/);
    if (m && parseInt(m[1]) !== myPid) return `opponent-${m[1]}`;
  }
  return null;  // no mapping found
}

function findCardData(cardId, snapshot) {
  if (!snapshot) return null;
  const allArrays = [
    snapshot.lineup || [],
    ...(snapshot.players || []).flatMap(p => [
      p.hand || [], p.played || [], p.ongoing || [],
      p.under_persona || [], p.over_persona || [],
    ]),
  ];
  for (const arr of allArrays) {
    const found = arr.find(c => c && c.id === cardId);
    if (found) return found;
  }
  return null;
}

function calcAnimations(oldPositions, newPositions, oldState) {
  if (!oldPositions || !newPositions || myPid === null) return [];
  const anims = [];
  const seen  = new Set();

  for (const [cardId, newPile] of Object.entries(newPositions)) {
    const oldPile = oldPositions[cardId];
    if (!oldPile || oldPile === newPile) continue;  // new card or unchanged
    if (seen.has(cardId)) continue;
    seen.add(cardId);

    const srcId  = getPileElementId(oldPile);
    const destId = getPileElementId(newPile);

    // Skip if either pile has no element mapping (shouldn't happen with full coverage)
    if (!srcId || !destId) continue;

    // Get source rect — always try cardRegistry first (exact individual card position).
    // Only use entry if element is still in the DOM; stale entries from cleared containers
    // return {left:0,top:0,w:0,h:0} and cause 0,0 animations.
    let fromRect = null;
    const registryEl = cardRegistry[cardId];
    if (registryEl && registryEl.isConnected) {
      const r = registryEl.getBoundingClientRect();
      if (r.width > 0 || r.height > 0) fromRect = r;
    }
    // Fallback: use pile element rect
    if (!fromRect) {
      const el = $(srcId);
      if (el) fromRect = el.getBoundingClientRect();
    }
    if (!fromRect) continue;

    const destEl = $(destId);
    if (!destEl) continue;

    const faceDown = isFaceDown(oldPile);
    const cardData = findCardData(cardId, oldState);
    anims.push({ card: cardData || { id: cardId }, fromRect, toId: destId, srcId, faceDown });
  }

  return anims;
}

function playAnimations(anims) {
  anims.forEach((anim, i) => {
    flyCardOverlay(anim.card, anim.fromRect, anim.toId, anim.srcId, i * 0.08, anim.faceDown);
  });
}

function flyCardOverlay(cardData, fromRect, toId, srcId, delay, faceDown) {
  const toEl = $(toId);
  if (!toEl || !fromRect) return;
  const toRect = toEl.getBoundingClientRect();

  // Determine start size from srcId hint, falling back to clamped fromRect
  // Opponent panels are large containers — treat them as small-card size
  const srcSize = PILE_CARD_SIZE[srcId] || (srcId && srcId.startsWith('opponent-') ? { w: 55, h: 77 } : null);
  const rawW = Math.min(fromRect.width  || 88, 140);
  const rawH = Math.min(fromRect.height || 124, 196);
  // Enforce ~5:7 card aspect ratio
  const aspect = 5 / 7;
  let startW, startH;
  if (srcSize) {
    startW = srcSize.w; startH = srcSize.h;
  } else if (rawW / rawH > aspect + 0.15) {
    startH = rawH; startW = Math.round(rawH * aspect);
  } else if (rawW / rawH < aspect - 0.15) {
    startW = rawW; startH = Math.round(rawW / aspect);
  } else {
    startW = rawW; startH = rawH;
  }

  // Destination size for scale animation
  const destSize = PILE_CARD_SIZE[toId] || (toId && toId.startsWith('opponent-') ? { w: 55, h: 77 } : { w: 88, h: 124 });
  const endScale = destSize.w / startW;

  // Position overlay so its center aligns with the source rect center
  const startX = fromRect.left + fromRect.width  / 2 - startW / 2;
  const startY = fromRect.top  + fromRect.height / 2 - startH / 2;

  // Build card clone as overlay
  const el = document.createElement('div');
  el.style.cssText = `
    position:fixed; left:${startX}px; top:${startY}px;
    width:${startW}px; height:${startH}px; z-index:9999; pointer-events:none;
    border-radius:8px; overflow:hidden; border:2px solid rgba(201,162,39,.9);
    box-shadow:0 0 20px rgba(201,162,39,.6); transform-origin:center center;
  `;
  if (faceDown) {
    el.classList.add('deck-back');
  } else if (cardData && cardData.image) {
    const img = document.createElement('img');
    img.src = imgUrl(cardData.image);
    img.style.cssText = 'width:100%;height:100%;object-fit:cover;display:block;';
    img.draggable = false;
    el.appendChild(img);
  } else {
    el.style.background = '#1a2030';
  }
  document.body.appendChild(el);

  // Fly center of card to center of destination
  const destX = toRect.left + toRect.width  / 2 - startW / 2;
  const destY = toRect.top  + toRect.height / 2 - startH / 2;

  gsap.to(el, {
    left: destX, top: destY, scale: endScale,
    delay, duration: 0.4, ease: 'power2.out',
    onComplete: () => {
      gsap.to(el, {
        opacity: 0, duration: 0.2, ease: 'power1.in',
        onComplete: () => el.remove(),
      });
    },
  });
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

  $('btn-start-game').disabled = true;

  // Set up drag-and-drop drop zone (once, on the static played-cards element)
  initDropZone();

  // Initial empty action log
  renderActionLog();
})();
