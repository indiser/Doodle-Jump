# 🐸 Doodle Jump — Pygame Edition

A faithful, feature-rich clone of the classic **Doodle Jump** arcade game, built from scratch in Python using Pygame. Gravity is the enemy. Platforms are your allies. Bats will ruin your day.

---

## 🚀 Features

- **Procedural platform generation** — infinite vertical world generated on-the-fly using weighted random rolls, so no two runs are the same
- **5 platform types** — standard, breakable, explosive (3-phase timed detonation), horizontal moving, and vertical moving
- **Dynamic difficulty scaling** — moving platform speed increases by `1` per every `3000` points scored. It gets mean.
- **Entity system** — feeders (1.8× jump boost), trampolines (2.5× boost + rotation animation), and bat monsters with sinusoidal hover anchored to their parent platform
- **Camera / world-shift system** — instead of moving the player up, the world scrolls down. Score is derived directly from the accumulated vertical shift (`score -= player.y_velocity`)
- **Death fall sequence** — dedicated `DEATH_FALL` state where the world rises past the player before transitioning to `GAME_OVER`
- **Persistent high score** — serialized to `highest_score.json` via the `json` module. Survives restarts. Unlike your dignity after a bat collision.
- **PyInstaller-compatible asset loading** — `get_path()` in `assets.py` resolves paths relative to `sys._MEIPASS` when bundled, so the executable just works

---

## 🗂️ Project Structure

```
Doodle/
├── main.py              # Game loop, state machine, collision resolution, camera
├── Doodle.py            # Player class — movement, gravity, jump, rotation flip
├── Platform.py          # Platform, ExplodingPlatform, MovingPlatform
├── Monster.py           # Bat enemy — sinusoidal hover, frame animation, platform anchoring
├── Feeder.py            # Spring feeder — 1.8× jump boost item
├── Trampoline.py        # Trampoline — 2.5× jump boost + flip animation trigger
├── assets.py            # Centralised asset loader (images + sounds), PyInstaller-safe
├── config.py            # All magic numbers live here (dimensions, physics constants)
├── cleanup.py           # Utility script
├── bg_remover.py        # Background removal utility (uses rembg)
├── highest_score.json   # Persisted high score
├── requirements.txt     # Runtime dependencies
└── Game_Assests/        # Sprites, sounds, fonts, UI covers
```

---

## ⚙️ Tech Stack

| Concern | Solution |
|---|---|
| Rendering & input | `pygame` |
| Image processing | `pillow` |
| Background removal | `rembg` |
| Persistence | `json` (stdlib) |
| Packaging | `pyproject.toml` + PyInstaller |
| Python version | `>= 3.11` |

---

## 🎮 Game States

The game runs a single `while` loop driven by a `game_state` string — a lightweight finite state machine:

```
MENU → PLAYING → PAUSED → PLAYING
                        ↓
                   DEATH_FALL → GAME_OVER → MENU / PLAYING
```

| State | Description |
|---|---|
| `MENU` | Animated doodle bounces on a fake platform. Press `SPACE` or click Play. |
| `PLAYING` | Full physics, collision, camera, and entity update loop. |
| `PAUSED` | All updates halt. Resume via button or `SPACE`. |
| `DEATH_FALL` | Player falls off screen; world rises until all platforms are gone. |
| `GAME_OVER` | Score summary screen. High score saved if beaten. |

---

## 🧱 Platform Spawn Weights

Platforms are generated via a `random.randint(1, 100)` roll in `make_platform()`:

| Roll | Type | Probability |
|---|---|---|
| 1–10 | Horizontal moving | 10% |
| 11–20 | Vertical moving | 10% |
| 21–35 | Explosive | 15% |
| 36–50 | Breakable | 15% |
| 51–100 | Standard | 50% |

---

## 🦇 Entity Spawn Logic

Entities only spawn on non-breakable standard platforms, gated by score thresholds:

| Roll | Entity | Condition |
|---|---|---|
| 1–5 | Trampoline | Score > 1000 |
| 6–15 | Feeder | Score > `FEEDER_THRESHOLD` (3000) |
| 16–25 | Monster (bat) | Score > 1 (always, basically) |

---

## 🔧 Installation & Running

```bash
# Clone the repo
git clone https://github.com/indiser/Doodle-Jump.git
cd Doodle-Jump

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

---

## 🕹️ Controls

| Key / Action | Effect |
|---|---|
| `←` / `→` Arrow Keys | Move left / right |
| `SPACE` | Start / Pause / Resume / Restart |
| Click buttons | Navigate menus |

> Wrapping is supported — walk off the left edge, appear on the right. Physics respects no walls.

---

## 📐 Physics Constants (`config.py`)

| Constant | Value | Notes |
|---|---|---|
| `GRAVITY` | `0.6` | Applied every frame to `y_velocity` |
| `JUMP_STRENGTH` | `-20` | Negative = upward in Pygame's coordinate system |
| `MOVE_SPEED` | `5` | Horizontal pixels per frame |
| `FEEDER_THRESHOLD` | `3000` | Minimum score before feeders start spawning |

---

## 📦 Building an Executable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico main.py
```

`assets.py` uses `sys._MEIPASS` detection so all assets resolve correctly inside the bundle. No `FileNotFoundError` surprises at 2 AM.

---

*Built with Python, Pygame, and an unhealthy amount of `random.randint`.*
