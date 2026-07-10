#!/usr/bin/env bash
set -e

INSTALL_DIR="$HOME/.tui"
BIN_DIR="${XDG_BIN_HOME:-$HOME/.local/bin}"
REPO="https://raw.githubusercontent.com/gliddd4/tui/main"

BOLD='\033[1m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${BLUE}${BOLD}Installing tui...${NC}"

mkdir -p "$INSTALL_DIR/demo" "$BIN_DIR"

echo "  downloading tui.py..."
curl -fsSL "$REPO/tui.py" -o "$INSTALL_DIR/tui.py"

echo "  downloading demo..."
curl -fsSL "$REPO/demo/tui_demo.py" -o "$INSTALL_DIR/demo/tui_demo.py"

cat > "$INSTALL_DIR/tui" << 'EOF'
#!/usr/bin/env bash
cd "$(dirname "$(readlink -f "$0")")/demo" && python3 tui_demo.py
EOF

chmod +x "$INSTALL_DIR/tui"

[ -L "$BIN_DIR/tui" ] && rm "$BIN_DIR/tui"
ln -s "$INSTALL_DIR/tui" "$BIN_DIR/tui"

hash -r 2>/dev/null || true
echo -e "${GREEN}Done! Run 'tui' to start.${NC}"
