# 🚗 The Last SUV: 3D Apocalypse Survival

"The Last SUV" is an atmospheric 3D browser shooter/survival (3D Top-Down Shooter) with a top-down view in a zombie apocalypse world. The game is built with pure HTML5 using the **Three.js** library for WebGL 3D graphics rendering and the **Web Audio API** for procedural sound effect generation.

The game features stylized low-poly graphics (in the aesthetic of Roblox characters), dynamic lighting, shadows, and a developed survival and crafting system.

---

## 🎮 How to play right now (GitHub Pages)

The game is deployed and accessible via GitHub Pages!

👉 **Game link:** [https://baltasaruss.github.io/Game/](https://baltasaruss.github.io/Game/)

---

## 🕹️ Controls

* **W, A, S, D** — Character movement (full strafe in all directions).
* **Mouse movement** — Aiming (the character on PC always faces the mouse cursor).
* **Left Mouse Button (LMB)** — Shooting.
  - Pistol and Shotgun require single clicks.
  - The AK-74 Assault Rifle supports **automatic fire** (hold LMB).
* **Hold Shift** — Sprint (consumes Stamina ⚡).
* **Keys 1, 2, 3** — Weapon selection:
  - `1` — Pistol 🔫 (high accuracy, 9x18mm rounds)
  - `2` — AK-74 Assault Rifle 💥 (high rate of fire, automatic fire when held)
  - `3` — MP-133 Shotgun 🔥 (powerful buckshot spread at close range)
* **Keys 4, 5, 6, 7** — Use quick-access items:
  - `4` — Eat Canned Stew 🥫 (+35 hunger, +12 health)
  - `5` — Drink Clean Water 🥤 (+45 thirst, with filter installed +75 auto)
  - `6` — Use Medkit ➕ (+50–100 health)
  - `7` — Replace Gas Mask Filter 🎭 (quick crafted refresh for radiation protection)
* **Space** (or hold button on mobile screen) — Collect gasoline from canisters ⛽ or scrap from junk piles ⚙️.
* **Key E** — Enter the SUV (when you are next to the vehicle).
* **ESC** — Pause.

---

## ⚙️ Game Features and Mechanics

1. **Vital Stats**: Monitor health (HP), hunger, thirst, and radiation level (Rad ☢️).
2. **Radiation System**: In contaminated zones (e.g., outskirts), radiation rises quickly. The gas mask filter charge protects you, and at 100% exposure, health begins to plummet.
3. **Armored RV SUV 🚗**: Your mobile base.
   - **Refueling**: Pour collected gasoline into the fuel tank to travel further (1 canister = +12 fuel).
   - **RV Upgrades**: Upgrade the engine (reduces fuel consumption), armor (protects from raiders on the road), and trunk (allows carrying more gasoline).
   - **Workbench**: Allows crafting ammo, medkits, body armor (reduces damage by 30%), water filters, and gas mask filters.
4. **Character Progression**: Earn experience by killing zombies and collecting resources. Each level-up grants skill points to distribute in the character menu (Strength, Agility, Survival).
5. **Interactive 3D NPCs**: You will encounter survivors at locations — stalkers warming by campfires, wounded ones asking for medkits, or armed sentries. They have dynamic dialogue bubbles that react to events.
6. **Diverse Locations**: 7 detailed levels from the starting camp to the secret military bunker "Omega" with the final boss — a giant Super Mutant.
7. **Auto-save 💾**: All your progress is automatically saved to LocalStorage upon arriving at new safe camps.

---

## 🛠️ Tech Stack

* **Three.js** (WebGL 3D renderer, dynamic SpotLight/PointLight sources, soft shadows, skeletal micro-animation of limbs).
* **Procedural 3D Object Generation**: All models (gasoline canisters, water bottles, medkits, ammo boxes, broken burning cars, ruined buildings with broken window glass, trees, and walls) are generated programmatically using Three.js geometry primitives without loading heavy external assets.
* **InstancedMesh**: Optimized ground mesh rendering with 4 random texture variations for grass, sand, and asphalt, eliminating visual monotony.
* **Web Audio API**: Procedural sound synthesis (gunshots, explosions, zombie growls, SUV engine hum, and ambient background).