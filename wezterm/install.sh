#!/bin/bash
# WezTerm Matrix Setup - Install script
# Installs WezTerm + Matrix rain backgrounds + helper scripts
set -e

echo "=== WezTerm Matrix Setup ==="

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

# 1. Install WezTerm (AppImage, no root needed)
if ! command -v wezterm &>/dev/null && [ ! -f "$HOME/.local/bin/wezterm" ]; then
    echo "[1/5] Installing WezTerm..."
    mkdir -p ~/.local/bin
    WEZTERM_URL="https://github.com/wezterm/wezterm/releases/download/20240203-110809-5046fc22/WezTerm-20240203-110809-5046fc22-Ubuntu20.04.AppImage"
    curl -L -o ~/.local/bin/wezterm "$WEZTERM_URL"
    chmod +x ~/.local/bin/wezterm
else
    echo "[1/5] WezTerm already installed, skipping."
fi

# 2. Install Fira Code font
if ! fc-list | grep -qi "fira code"; then
    echo "[2/5] Installing Fira Code font..."
    mkdir -p ~/.local/share/fonts
    cd /tmp
    curl -sL "https://github.com/tonsky/FiraCode/releases/download/6.2/Fira_Code_v6.2.zip" -o FiraCode.zip
    unzip -o FiraCode.zip -d FiraCode > /dev/null
    cp FiraCode/ttf/*.ttf ~/.local/share/fonts/
    fc-cache -f ~/.local/share/fonts
    rm -rf FiraCode FiraCode.zip
else
    echo "[2/5] Fira Code already installed, skipping."
fi

# 3. Copy WezTerm config
echo "[3/5] Copying WezTerm config..."
mkdir -p ~/.config/wezterm
cp "$SCRIPT_DIR/wezterm.lua" ~/.config/wezterm/
cp "$SCRIPT_DIR/gen_matrix_depth.py" ~/.config/wezterm/
cp "$SCRIPT_DIR/matrix-rain-generated.gif" ~/.config/wezterm/matrix-rain.gif
cp "$SCRIPT_DIR/matrix-rain-generated.gif" ~/.config/wezterm/
if [ -f "$SCRIPT_DIR/matrix-rain-video.gif" ]; then
    cp "$SCRIPT_DIR/matrix-rain-video.gif" ~/.config/wezterm/
fi

# 4. Install helper scripts
echo "[4/5] Installing helper scripts..."
mkdir -p ~/.local/bin
cp "$REPO_DIR/scripts/matrix-bg" ~/.local/bin/
cp "$REPO_DIR/scripts/wezterm-video" ~/.local/bin/
cp "$REPO_DIR/scripts/wezterm-generated" ~/.local/bin/
chmod +x ~/.local/bin/matrix-bg ~/.local/bin/wezterm-video ~/.local/bin/wezterm-generated

# 5. Ensure ~/.local/bin is in PATH
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
    echo "[5/5] Adding ~/.local/bin to PATH..."
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    echo "  Added to ~/.bashrc - restart your shell or run: source ~/.bashrc"
else
    echo "[5/5] PATH already configured."
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Launch WezTerm:"
echo "  wezterm start"
echo ""
echo "Switch backgrounds:"
echo "  matrix-bg generated   # Python-generated Matrix rain with depth layers"
echo "  matrix-bg video       # Real Matrix rain from YouTube"
echo "  matrix-bg off         # No background"
echo ""
echo "Regenerate Matrix rain (customize speeds/density):"
echo "  python3 ~/.config/wezterm/gen_matrix_depth.py"
echo ""
echo "Keyboard shortcuts (configure manually in your DE):"
echo "  Ctrl+Alt+W -> bash /home/\$USER/.local/bin/wezterm-video"
echo "  Ctrl+Alt+G -> bash /home/\$USER/.local/bin/wezterm-generated"
