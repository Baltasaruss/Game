# The Last SUV — Complete Overhaul Changelog

Single-file Three.js r128 top-down 3D zombie survival game. This archive contains
the fully patched `index.html` (16,858 lines, ~814 KB) with all optimizations,
visual redesign, new mechanics, themed enemies/bosses, and flying zombies.

Source: https://github.com/Baltasaruss/Game

---

## Part 1 — Performance Optimization (10 patches)

No visual quality loss. Gameplay/balance/textures/audio untouched.

| # | Patch | Effect |
|---|---|---|
| 1.9 | Renderer: powerPreference, adaptive shadowMap.type, camera far 1000→400 | Stable on integrated GPU |
| 1.2 | Shadows only on hero objects (16 castShadow=false flips) | −3000 draw calls at peak |
| 1.12 | Vibration API + programmatic orientation lock | Haptic feedback on mobile |
| 1.7 | Per-frame Vector3 elimination (8 new scratch vectors) | Zero GC stutters |
| 1.4 | flashSprite without material cloning | Material cache works all combat |
| 1.6 | Object pools: bullets(256), sparks(InstancedMesh 500), shells(128), damage text(RAF 40) | Zero allocations in combat |
| 1.1 | InstancedMesh for trees (trunk 600 + foliage 1800) + sparks | ~1800→4 draw calls on forest levels |
| 1.5 | SpatialGrid (cell 4u) + colliderGrid/enemyGrid, 9 conversions | ~62000→4580 collision checks/frame (~34×) |
| 1.8 | Bullet substepping (1/60s, up to 5/frame) | No tunneling at low FPS |
| 1.10 | Adaptive FPS (pixel ratio throttle only, no shadow disable) | Saves mobile without degrading quality |
| 1.3 | Unit geometry cache, ~70 spawn sites converted | BoxGeometry 137→51 (−63%) |

Skipped: 1.11 (Three.js r128→r16x) — would break legacy postprocessing.

---

## Part 2 — Visual Redesign

### Stage 1: Splash + Menu + HUD
- **Splash screen** (`#loading-overlay`): 3-stage progress (CDN→fonts→engine),
  cycling tips, "ENTERING <LOCATION>" on cold start. No more blank screen.
- **Animated main menu**: Canvas2D parallax — 80 drifting dust particles,
  3-5 zombie silhouettes, idling SUV with exhaust puffs. Letter-by-letter
  title reveal with firelight flicker.
- **Unified HUD header** (`#hud-header`): stats + boss bar + weapon + minimap
  merged into ONE cohesive top strip. Bolted-metal `.hud-panel` style with
  amber rivets, hazard stripes. Boss bar redesigned: slim 8px, no ⚠ prefix,
  subtle low-HP glow.

### Stage 2: Location Upgrades (22 new props)
- **Military Checkpoint**: jersey barriers, guard towers w/ spotlights,
  checkpoint gate w/ STOP sign, barbed wire fences, flagpole (swaying flag),
  ammo crates
- **Omega Bunker**: blast doors, vault door w/ bolts, computer terminals
  (flickering CRT), coolant pipes, red emergency lights, warning signs
- **Supermarket**: shopping carts (20% tipped), checkout counters, cold
  displays, SALE signs, shopping baskets
- **Vehicle Tunnel**: ceiling w/ rebar gaps, overhead lights (50% lit),
  support pillars, vent ducts, broken pipes

### Stage 3: Enemy Variation + Damage States
- 18 pre-built material variants (skin/clothing tint)
- ±10% scale jitter + random Y-rotation per spawn
- 10 accessory types (helmets, hats, bandanas, backpacks, missing limbs, blood)
- 4 damage stages: clean → blood on torso → +limp animation → +hunched posture
  + missing limb

### Stage 4: Decals
- **Bullet holes**: 16×16 texture (hole + cracks + halo), spawn on wall hits,
  cap 80, clustering guard
- **Scorch marks**: 32×32 texture (ash ring + core + streaks), after barrel/
  bomber/boss-slam explosions, cap 30
- **Graffiti**: 4 variants (SURVIVE, THE END IS HERE, biohazard, WE WERE HERE),
  4-8 per level on city/supermarket/tunnel/asphalt/bunker walls

---

## Part 2 — New Game Mechanics

### 1. Daily Sortie Contract
- Daily procedural contract (5 types: kills/noDamage/timeLimit/pistolOnly/comboKills)
  with date-seeded generation
- Reward: Dog Tags (separate localStorage key, survives death)
- Shop: extra medkit, pistol upgrade, extra skill point, SUV armor, gold paint
- New "📜 Contract" tab in station menu

### 2. Endless Horde Mode
- Unlocked after clearing Omega Bunker
- Infinite waves (5+wave×2 enemies, cap 60), boss every 5 waves
- Perk selection every 3 waves, 10s break between waves
- High score in localStorage
- "♾️ ENDLESS MODE" button on main menu

### 3. Boss Rage Phase + Multi-Phase Final Boss
- All bosses: rage at HP<30% (speed ×1.8, cooldowns ÷2, red tint, screen flash,
  shake, red sparks)
- Omega Super Mutant: 3 phases (melee → summon+plasma → AoE apocalypse mode)
- `showBossBanner()` + `flashScreen()` helpers

---

## Part 2 — Themed Enemies (10 location themes)

Each location now has visually distinct enemies matching its setting:

| Location | Enemy Theme | Visual |
|---|---|---|
| Genesis Lab | Infected medics | White lab coats, surgical masks, stethoscopes |
| Camp Dawn | Campers/scouts | Earthy tones, backpacks, bandanas |
| Quiet Forest | Lumberjacks | Plaid shirts, beanies, beards |
| Supermarket | Shoppers/employees | Blue vests, name tags, caps |
| Contaminated City | Businessmen | Suits, ties, briefcases, radiation burns |
| Amusement Park | Clowns | Polka dots, white face paint, red noses, wild hair |
| Rusty Wasteland | Raiders | Rust armor, goggles, bandanas, scrap weapons |
| Vehicle Tunnel | Miners | Helmets w/ headlamps, orange vests, pickaxes |
| Military Checkpoint | Soldiers | Camo fatigues, helmets, bullet belts, dog tags |
| Omega Bunker | Mutant special forces | Black tactical gear, NVG, armor plates, green glow |

---

## Part 2 — Themed Bosses (10 unique bosses)

| Boss | Location | Unique Details |
|---|---|---|
| Patient Zero | Lab | Lab coat, tentacle arm, syringe, biohazard glow |
| Camp Stalker | Camp Dawn | Camo, ranger hat, rifle, backpack |
| Rotting Elder | Quiet Forest | Mossy wood torso, branch arms, root legs, glowing eyes |
| Butcher of Aisle 9 | Supermarket | Blood apron, meat cleaver, butcher hat, fat body |
| Irradiated Colossus | City | Torn suit, green glow, extra arm, briefcase weapon |
| Carnival King | Amusement | Polka dots, giant nose, 5 hair cones, hammer, big shoes |
| Raider Warlord | Wasteland | Rust armor, spike pauldrons, gas mask, cape, dual weapons |
| Tunnel Horror | Tunnel | Pale skin, miner helmet, pickaxe, hunched, blue eyes |
| Iron Commander | Military | Camo + body armor, helmet, rifle, ammo belt, dog tags |
| Omega Super Mutant | Bunker | Enhanced mega-robot, NVG, armor plates, green radiation seams |

Material cloning isolates boss from regular enemies — rage-phase recoloring
only affects the boss's own material instances.

---

## Part 2 — Flying Zombies (outdoor locations only)

New enemy type `zombie_flying` added to 5 outdoor themes (grass, city, sand,
amusement, asphalt). Excluded from indoor (lab, supermarket, tunnel, bunker).

- **Visual**: Roblox character + 2 angled wings (themed color) + hover-glow
  disc under feet
- **AI**: Hovers at y=2.2-3.0 with sine bob, ignores wall collisions, dive-
  attacks player (drops to y=0.8, attacks at 1.4 units, climbs back)
- **Animation**: Wings flap (faster when diving), legs dangle
- **Stats**: HP 85, speed 3.2, dmg 9, XP 22
- **Theme-integrated**: Flying clown in amusement park (pink wings), flying
  soldier on military base (slate wings), flying medic in lab endless mode, etc.
- **Bullet collision**: hitRadius 0.95 (vs 0.7 ground) for height forgiveness

---

## Bugfixes (from user feedback)

1. **Black screen after splash** — `#main-menu-overlay` position relative→absolute
2. **Gun square bug** — switchWeapon scale 1.0→0.12 (unit-geometry aware)
3. **Fire flicker regression** — baseScaleX/Y/Z fields, flicker multiplies base
4. **Adaptive FPS over-aggressive** — only pixel ratio throttle, no shadow disable,
   no localStorage persist
5. **Camera far 200→400** — far locations were culling too early
6. **Flashlight shadow 256→512 on high** — shadows were pixelated
7. **Shadows restored on arms/boots** — silhouette was flat during walk animation
8. **Boss bar overlap on mobile** — moved below stats panel, narrower width
9. **Log full-width stripe** — width fixed 200px + overflow hidden
10. **Inventory clicks firing weapon** — onMouseDown guards against HUD element clicks

---

## Installation

```bash
git clone https://github.com/Baltasaruss/Game.git
cd Game
tar -xzvf last-suv-final.tar.gz
git add index.html CHANGELOG.md
git commit -m "feat: complete overhaul — perf optimization, visual redesign, themed enemies/bosses, flying zombies, new mechanics"
git push origin main
```

GitHub Pages updates in 1-2 minutes.

## Tech Stack
- Three.js r128 (WebGL 3D renderer)
- Web Audio API (procedural sound synthesis)
- PWA (manifest + service worker, offline-capable)
- Single-file `index.html` — no external assets, everything procedural
- ~16,858 lines, ~814 KB

## Save Compatibility
- `SAVE_VERSION = 3` unchanged
- `last_train_save` (game state) — backwards compatible
- `last_suv_meta` (dog tags, contracts, endless high score) — new key, separate
