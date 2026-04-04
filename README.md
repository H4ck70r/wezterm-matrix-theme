# dotfiles

Personal dotfiles and terminal configurations.

## WezTerm Matrix Terminal

A Matrix-themed WezTerm terminal with animated rain background, green-on-black color scheme, and Fira Code ligatures.

### Features

- Animated Matrix digital rain background (two modes: video capture & Python-generated with depth layers)
- Green phosphorescent text on pure black
- Fira Code font with ligatures
- Blinking green cursor
- Window transparency (85%)
- Background switcher script (`matrix-bg`)

### Quick Install

```bash
git clone git@github.com:H4ck70r/dotfiles.git
cd dotfiles
bash wezterm/install.sh
```

### Screenshots

Launch with `wezterm start` or use keyboard shortcuts.

### Background Modes

```bash
matrix-bg generated   # Python-generated rain with depth layers (blurry bg + sharp fg)
matrix-bg video       # Real Matrix rain captured from YouTube
matrix-bg off         # Disable background
```

### Regenerate Matrix Rain

The Python generator (`gen_matrix_depth.py`) creates a custom Matrix rain GIF with:
- 3 depth layers (far/blurry, mid, near/sharp)
- 4 speed tiers (crawl, slow, medium, brisk)
- Half-width katakana characters (authentic Matrix film style)
- Character change flash effect

```bash
python3 ~/.config/wezterm/gen_matrix_depth.py
```

Requires: `python3`, `Pillow`, `ffmpeg`
