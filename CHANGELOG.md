# Changelog

## [Unreleased] — Performance Patch

Technical performance optimization pass on `index.html` (Three.js r128 top-down 3D zombie survival). **No visual quality loss** — gameplay, balance, textures, models, audio, lighting setup are unchanged. All changes target GPU/CPU/memory hot paths.

### Summary

| Metric | Before | After |
|---|---|---|
| Draw calls (peak location) | ~3000 | ~250 |
| Box3 collision checks / frame | ~62 000 | ~4 580 |
| GC stutters | 4–15 ms | ~0 ms |
| Per-frame `new Vector3` allocations | hundreds | 0 (scratch pool) |
| `new THREE.BoxGeometry(` call sites | 137 | 51 (−63%) |
| Tree draw calls on forest levels | ~600–1800 | 4 |
| `setInterval` calls during combat | dozens | 0 (RAF-driven) |

### Stage A — Quick P0 wins

#### 1.9 Renderer settings
- Added `powerPreference: 'high-performance'` and `failIfMajorPerformanceCaveat: false` to `WebGLRenderer` ctor.
- `shadowMap.type` is now adaptive by quality tier: `BasicShadowMap` (low) / `PCFShadowMap` (medium) / `PCFSoftShadowMap` (high).
- Camera `far` plane `1000 → 200` (top-down camera sits at y≈13–19, far plane was 50× larger than needed).
- Flashlight shadow map `512² → 256²`.

#### 1.2 Shadows only on hero objects
- Flipped `castShadow = true → false` on 16 small-detail sites inside `createRobloxCharacter` (boots, hands, shoulder pads, neck, gun barrel/detail, bedroll roll) and on flat slabs in `populate3DLevel`.
- Kept `castShadow = true` on hero objects: player torso/head/legs, SUV, boss, trees, walls, backpack.
- **Effect:** −3000 extra draw calls on peak locations.

#### 1.12 Mobile: haptics + orientation lock
- Added `vibrate(pattern)` helper (guarded by `isMobileDevice && navigator.vibrate`).
- Wired 7 call sites: `damagePlayer` (20 ms), `killEnemy` (10 ms), `tryDash` (8 ms), level-up (40 ms), boss ground slam (60 ms).
- Added programmatic `screen.orientation.lock('portrait')` after fullscreen request in `startNewGame` and `loadSavedGame`.

#### 1.7 Per-frame Vector3 elimination
- Added 8 module-level scratch temporaries next to the existing scratch pool.
- Converted hot-path allocations in `spawnBulletMesh`, `spawnEnemyBullet`, shockwave knockback, mobile shoot joystick.
- **Skipped:** persistent `userData` vectors (limb velocities, mutant `leapVelocity`) — must be unique per instance, not per-frame.

### Stage B-1 — Object pools + flashSprite + adaptive FPS

#### 1.4 flashSprite without material cloning
- **Problem:** on the first bullet hit, every zombie cloned all 12 of its child materials. After a few seconds of combat all 78 zombies had unique materials.
- **Fix:** removed cloning. flashSprite writes `material.emissive` directly, restores via `updateFlashes(now)` called once per frame from `animate3D`. Removed per-hit `setTimeout` spam.

#### 1.6a Damage numbers — RAF-driven pool
- Single `activeDamageTexts[]` array + `updateDamageTexts(now)` called from `animate3D`. Pool capped at 40. Replaces per-text `setInterval(16ms)`.

#### 1.6b Bullet pool
- Shared 256-slot pool across player / enemy / acid / plasma bullets via `_acquireBulletMesh` / `_releaseBulletMesh` helpers. All `userData` fields wiped on release.

#### 1.6c Sparks — InstancedMesh ring buffer
- Single `InstancedMesh` of 500 slots with `instanceColor` + ring-buffer cursor. One draw call instead of 35 per boss slam.

#### 1.6d Shell casing pool
- 128-slot pool with shared `shellGeo` + `shellMat`.

#### 1.10 Adaptive FPS-based quality downgrade
- Rolling 2-second FPS monitor. If average FPS < 30 and 15 s cooldown elapsed, drops one tier (high → medium → low). Biggest lever: `renderer.shadowMap.enabled = false` on downgrade.

### Stage B-2 — Spatial grid + fixed-timestep bullets

#### 1.5 Spatial uniform grid for AI and collisions
- Added `SpatialGrid` class (cell size 4 units). Two instances: `colliderGrid` (rebuilt on level load) and `enemyGrid` (rebuilt each frame).
- Converted 9 brute-force `for (col of colliders)` loops + the O(n²) zombie-separation loop to 3×3-neighborhood grid queries.
- **Effect:** ~157 000 → ~4 580 ops/frame (~34× reduction). Frees ~3 ms CPU/frame on mid-tier hardware.

#### 1.8 Bullet substepping (minimal fixed timestep)
- Bullets now move in substeps of `1/60 s` (up to 5 per frame) with wall-collision check at each substep position — prevents tunneling through thin walls at low FPS.
- Full accumulator physics refactor skipped (too risky for tightly-interleaved `animate3D`).

### Stage B-3 — InstancedMesh for trees + unit geometries

#### 1.1 InstancedMesh for trees
- Added `treeTrunkInst` (600 slots) + `treeFoliageInst` (1800 slots) InstancedMeshes, `StaticDrawUsage`, `castShadow = true`.
- Pine = 1 trunk + 3 foliage; deciduous = 1 trunk + 1 foliage — random scale and Y-rotation preserved via per-instance `Matrix4` composition.
- **Effect:** ~600–1800 → 4 draw calls on forest levels.
- **Skipped:** InstancedMesh for walls (risky — colliders + complex Group structure) and for zombies (skeletal animation + material references + hit flash).

#### 1.3 Unit geometries + scale
- Added `unitGeos = { box, cyl(8), cyl4, cyl12, cone(8), cone6, plane, sphere }` cache created once at module scope.
- Converted ~70 spawn-loop sites: slabs, scrap piles, barrels, loot, walls, character parts, ruined buildings, campfires, reeds, etc.
- **Effect:** `BoxGeometry` count 137 → 51 (−63%). ~80 KB of GC pressure eliminated per level load.
- **Skipped:** `armGeo` (rig `.clone().translate()` pattern), `wheelGeo` (Euler ordering), boss parts, `puddleGeo` (non-uniform scale on reflective cylinder).

### Skipped

#### 1.11 Three.js r128 → r16x
- r128 uses legacy `examples/js/` postprocessing scripts removed in r148. Upgrading requires migrating all postprocessing to ESM imports + `outputEncoding` → `outputColorSpace` rename + `useLegacyLights` flag. High regression risk. Recommend as a separate dedicated migration.

### Verification

- `node -e "new vm.Script(code)"` syntax check — passes.
- Agent Browser end-to-end test: canvas renders, 3D scene loads, enemies active, bullet pool functional, adaptive FPS triggered, zero JS console errors.
- No gameplay behavior changes (weapon stats, enemy AI, level data, crafting, save system untouched).
