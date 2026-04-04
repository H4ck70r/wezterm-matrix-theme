# wezterm-matrix-theme

## WezTerm Matrix Terminal

A Matrix-themed WezTerm terminal with animated rain background, green-on-black color scheme, and Fira Code ligatures.

Terminal temática de Matrix con lluvia animada de fondo, esquema verde sobre negro y fuente Fira Code con ligaduras.

### Features / Funcionalidades

- Animated Matrix digital rain background (two modes: video capture & Python-generated with depth layers)
- Green phosphorescent text on pure black
- Fira Code font with ligatures
- Blinking green cursor
- Window transparency (85%)
- Background switcher script (`matrix-bg`)

---

- Fondo animado de lluvia Matrix (dos modos: video capturado y generado con Python con capas de profundidad)
- Texto verde fosforescente sobre negro puro
- Fuente Fira Code con ligaduras
- Cursor verde parpadeante
- Transparencia de ventana (85%)
- Script para cambiar fondos (`matrix-bg`)

### Quick Install / Instalacion Rapida

```bash
git clone git@github.com:H4ck70r/wezterm-matrix-theme.git
cd wezterm-matrix-theme
bash wezterm/install.sh
```

### Background Modes / Modos de Fondo

```bash
matrix-bg generated   # Python-generated rain with depth layers / Lluvia generada con capas de profundidad
matrix-bg video       # Real Matrix rain from YouTube / Lluvia Matrix real de YouTube
matrix-bg off         # Disable background / Sin fondo
```

### Regenerate Matrix Rain / Regenerar Lluvia Matrix

The Python generator (`gen_matrix_depth.py`) creates a custom Matrix rain GIF with:

El generador Python (`gen_matrix_depth.py`) crea un GIF personalizado de lluvia Matrix con:

- 3 depth layers: far/blurry, mid, near/sharp — 3 capas de profundidad: lejos/borroso, medio, cerca/nitido
- 4 speed tiers: crawl, slow, medium, brisk — 4 velocidades: muy lento, lento, medio, rapido
- Half-width katakana characters (authentic Matrix film style) — Caracteres katakana de medio ancho (estilo autentico de la pelicula)
- Character change flash effect — Efecto de flash al cambiar caracteres

```bash
python3 ~/.config/wezterm/gen_matrix_depth.py
```

**Requires / Requiere:** `python3`, `Pillow`, `ffmpeg`

### Keyboard Shortcuts / Atajos de Teclado

Configure in your desktop environment / Configura en tu entorno de escritorio:

| Shortcut / Atajo | Command / Comando | Description / Descripcion |
|---|---|---|
| `Ctrl+Alt+W` | `bash ~/.local/bin/wezterm-video` | WezTerm with video background / WezTerm con fondo de video |
| `Ctrl+Alt+G` | `bash ~/.local/bin/wezterm-generated` | WezTerm with generated background / WezTerm con fondo generado |

### Structure / Estructura

```
wezterm/
  wezterm.lua              # WezTerm config
  gen_matrix_depth.py      # Matrix rain generator
  matrix-rain-generated.gif # Generated background
  matrix-rain-video.gif    # Video background
  install.sh               # Install script
scripts/
  matrix-bg                # Background switcher + WezTerm restart
  wezterm-video            # Launch with video background
  wezterm-generated        # Launch with generated background
```
