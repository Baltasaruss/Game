# Bugfixes — Graphics & Loading

7 регрессий от оптимизации Части 1, исправленных после отчёта пользователя.

## Файл
`index.html` — заменить в репозитории (15 399 строк, 732 КБ).

## Исправления

### 1. Чёрный экран после splash screen
**Симптом:** после исчезновения loading-overlay главное меню не отображается — чёрный экран.
**Причина:** `#main-menu-overlay` получил `position: relative` (для canvas-фона), что сломало базовое `.overlay` позиционирование (`position: absolute; width:100%; height:100%`). Overlay схлопывался в normal flow.
**Фикс:** вернул `position: absolute; top:0; left:0; width:100%; height:100%` + добавил непрозрачный `background: var(--bg-dark)` (вместо полупрозрачного rgba из `.overlay`).

### 2. Огромный квадрат вместо пушки при переключении оружия
**Симптом:** при переключении оружия (1/2/3) в руке героя вырастает гигантский квадрат 1×1×1 вместо пушки.
**Причина:** `switchWeapon()` вызывал `gun.scale.set(1.0, 1.0, 0.6)` — без учёта, что пушка создана на unit-геометрии (`BoxGeometry(1,1,1)`) с базовым масштабом 0.12. Перезапись scale на 1.0 раздувала пушку в ~8 раз.
**Фикс:**
```js
// pistol:  gun.scale.set(0.12, 0.12, 0.6);
// rifle:   gun.scale.set(0.12, 0.12, 1.15);
// shotgun: gun.scale.set(0.18, 0.12, 0.85);
```

### 3. Костры — только свет на полу, без пламени
**Симптом:** горящие бочки/костры показывают только свет на полу, пламя-конус исчез.
**Причина:** после перевода пламени на unit-геометрию (`ConeGeometry(1,1,6)` + `scale.set(0.25, 0.5, 0.25)`), flicker-анимация по-прежнему делала `fm.mesh.scale.set(~1.0, ~1.0, ~1.0)` — перезаписывая базовый масштаб. Конус раздувался до 1×1×1, уходил под пол.
**Фикс:** `flickeringMeshes` теперь хранит `baseScaleX/Y/Z`, а анимация умножает базу на колебания: `fm.mesh.scale.set(bx * flickXZ, by * flickY, bz * flickXZ)`. Применено ко всем 3 сайтам (fire barrel, ruined car fire, campfire).

### 4. Adaptive FPS silently понижал качество и сохранял в localStorage
**Симптом:** на high quality игра сама "падала" до medium/low, тени отключались, и это сохранялось — пользователь не мог вернуться на high.
**Причина:** порог 30 FPS слишком низкий, при кратковременных просадках `graphicsQuality` падал `high→medium→low`, отключал `renderer.shadowMap.enabled` и `sunLight.castShadow`, и сохранял выбор в `localStorage.setItem('game_graphics_quality', ...)`.
**Фикс:** adaptive downgrade теперь только уменьшает pixel ratio (fill-rate) на 0.4, не трогает тени, не сохраняется в localStorage, порог 25 FPS. Пользовательский выбор quality больше не перезаписывается.

### 5. Camera far 200 → 400
**Симптом:** дальние локации срезались раньше времени.
**Причина:** я переусердствовал с `far=200` (считал, что top-down камера на y≈13-19 не видит дальше). На больших локациях (N=50) дальние стены пропадали.
**Фикс:** `camera.far = 400` — компромисс между perf и видимостью.

### 6. Flashlight shadow map 256 → 512 на high
**Симптом:** тени фонарика на high стали грубыми/пиксельными.
**Причина:** я урезал shadow map фонарика до 256² для всех tier.
**Фикс:** `(graphicsQuality === 'high') ? 512 : 256` — 512 на high (производительность позволяет), 256 на medium.

### 7. Тени убраны со слишком многих деталей
**Симптом:** силуэт героя и зомби выглядел плоским при анимации ходьбы.
**Причина:** я убрал `castShadow=true` со всех "мелких" деталей, включая руки и ботинки — но они заметны при анимации.
**Фикс:** вернул `castShadow=true` на `armL`, `armR`, `bootL`, `bootR`. Оставил `false` только на truly мелких (hands, shoulder pads, neck, bedroll, gun).

## Как установить

```bash
# 1. Клонируй свой репо (если ещё нет локально)
git clone https://github.com/Baltasaruss/Game.git
cd Game

# 2. Распакуй архив поверх
tar -xzvf last-suv-bugfixes.tar.gz

# 3. Закоммить и залей
git add index.html BUGFIXES.md
git commit -m "fix: visual regressions — splash black screen, weapon scale, fire flicker, adaptive FPS, shadows"
git push origin main
```

## Важно

Если качество застряло на medium из-за старой версии adaptive FPS — сбрось его:
- В настройках игры выбери High заново, ИЛИ
- В DevTools Console: `localStorage.removeItem('game_graphics_quality')`

GitHub Pages обновится через 1-2 минуты после push.
