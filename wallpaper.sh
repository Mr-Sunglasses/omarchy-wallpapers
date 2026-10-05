#!/bin/bash
# Set an Omarchy wallpaper on macOS, on every display.
#
#   ./wallpaper.sh                        list themes
#   ./wallpaper.sh tokyo-night            next wallpaper of the theme (cycles)
#   ./wallpaper.sh tokyo-night random     a random one
#   ./wallpaper.sh tokyo-night 3          the 3rd one (see the list below)
#   ./wallpaper.sh tokyo-night list       list the theme's wallpapers
#   ./wallpaper.sh random                 a random wallpaper from any theme
set -euo pipefail

ROOT=$(cd "$(dirname "$0")" && pwd)
STATE="${XDG_CACHE_HOME:-$HOME/.cache}/omarchy-wallpapers"

themes() {
    for d in "$ROOT"/*/; do
        d=${d%/}
        compgen -G "$d/*.jpg" >/dev/null || compgen -G "$d/*.png" >/dev/null || continue
        echo "${d##*/}"
    done
}

wallpapers() {
    find "$ROOT/$1" -maxdepth 1 -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' \) | sort
}

set_wallpaper() {
    # NSWorkspace sets the picture for the current Space on each display and
    # needs no Automation permission, unlike scripting System Events.
    osascript -l JavaScript - "$1" >/dev/null <<'EOF'
ObjC.import('AppKit')
function run(argv) {
    const url = $.NSURL.fileURLWithPath(argv[0])
    const screens = $.NSScreen.screens
    for (let i = 0; i < screens.count; i++) {
        const err = Ref()
        if (!$.NSWorkspace.sharedWorkspace.setDesktopImageURLForScreenOptionsError(url, screens.objectAtIndex(i), $({}), err))
            throw new Error('could not set wallpaper: ' + argv[0])
    }
}
EOF
    echo "${1#"$ROOT"/}"
}

if [ $# -eq 0 ]; then
    themes
    exit 0
fi

theme=$1
choice=${2:-next}

if [ "$theme" = random ]; then
    theme=$(themes | sort -R | head -1)
    choice=random
fi

if [ ! -d "$ROOT/$theme" ]; then
    echo "unknown theme: $theme (run $0 to list them)" >&2
    exit 1
fi

files=()
while IFS= read -r f; do files+=("$f"); done < <(wallpapers "$theme")

case $choice in
list)
    for i in "${!files[@]}"; do echo "$((i + 1)) ${files[$i]##*/}"; done
    ;;
random)
    set_wallpaper "${files[RANDOM % ${#files[@]}]}"
    ;;
next)
    mkdir -p "$STATE"
    last=$(cat "$STATE/$theme" 2>/dev/null || echo -1)
    i=$(((last + 1) % ${#files[@]}))
    echo "$i" >"$STATE/$theme"
    set_wallpaper "${files[$i]}"
    ;;
*[!0-9]* | 0)
    echo "expected next, random, list or a number from 1 to ${#files[@]}" >&2
    exit 1
    ;;
*)
    if [ "$choice" -gt "${#files[@]}" ]; then
        echo "$theme has ${#files[@]} wallpapers" >&2
        exit 1
    fi
    set_wallpaper "${files[$((choice - 1))]}"
    ;;
esac
