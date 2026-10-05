#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pillow"]
# ///
"""Sync wallpapers from Omarchy into one folder per theme and rebuild README.md.

Mirrors every themes/<theme>/backgrounds/ folder from Omarchy: new wallpapers
and themes are added, changed ones updated, and ones removed upstream deleted.
WebP files are converted so they work everywhere: lossless or transparent ones
to PNG, the rest to JPEG. Other formats are copied as they are.

    ./sync.py                 # clones omarchy into a temp dir
    ./sync.py ~/src/omarchy   # or use an existing checkout
"""

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

REPO = "https://github.com/omacom/omarchy"
ROOT = Path(__file__).resolve().parent
# Maps each wallpaper here to the sha256 of the upstream file it was made from,
# so converted files are only redone when the upstream file changes.
SOURCES = ROOT / "sources.json"
JPEG_QUALITY = 92

# Display names that don't follow from the folder name.
NAME_OVERRIDES = {
    "catppuccin": "Catppuccin Mocha",
    "catppuccin-latte": "Catppuccin Latte",
    "retro-82": "Retro 82",
    "rose-pine": "Rose Pine Dawn",
}


def title(slug):
    return NAME_OVERRIDES.get(slug, slug.replace("-", " ").title())


def theme_dirs():
    return sorted(p for p in ROOT.iterdir() if p.is_dir() and not p.name.startswith("."))


def webp_kind(path):
    """Return "png" for lossless or transparent WebP, else "jpg"."""
    data = path.read_bytes()
    chunks, pos = set(), 12
    while pos + 8 <= len(data):
        tag, size = data[pos : pos + 4], int.from_bytes(data[pos + 4 : pos + 8], "little")
        chunks.add(tag)
        pos += 8 + size + (size & 1)
    return "png" if chunks & {b"VP8L", b"ALPH"} else "jpg"


def output_name(f):
    if f.suffix.lower() != ".webp":
        return f.name
    return f"{f.stem}.{webp_kind(f)}"


def write(f, dest):
    if f.suffix.lower() != ".webp":
        shutil.copy2(f, dest)
    elif dest.suffix == ".png":
        Image.open(f).save(dest, optimize=True)
    else:
        Image.open(f).convert("RGB").save(dest, quality=JPEG_QUALITY, optimize=True)


def sync(src):
    upstream = {d.parent.name: d for d in src.glob("themes/*/backgrounds") if d.is_dir() and any(d.iterdir())}
    sources = json.loads(SOURCES.read_text()) if SOURCES.exists() else {}

    for local in theme_dirs():
        if local.name not in upstream:
            print(f"- {local.name}/")
            shutil.rmtree(local)

    for slug, backgrounds in sorted(upstream.items()):
        local = ROOT / slug
        local.mkdir(exist_ok=True)
        wanted = {}
        for f in sorted(backgrounds.iterdir()):
            if f.is_file():
                name = output_name(f)
                if name in wanted:
                    sys.exit(f"{slug}: {f.name} and {wanted[name].name} both become {name}")
                wanted[name] = f
        for f in local.iterdir():
            if f.name not in wanted:
                print(f"- {slug}/{f.name}")
                f.unlink()
        for name, f in wanted.items():
            dest, key = local / name, f"{slug}/{name}"
            digest = hashlib.sha256(f.read_bytes()).hexdigest()
            if dest.exists() and sources.get(key) == digest:
                continue
            print(f"{'~' if dest.exists() else '+'} {key}")
            write(f, dest)
            sources[key] = digest

    existing = {f"{d.name}/{f.name}" for d in theme_dirs() for f in d.iterdir()}
    sources = {k: v for k, v in sorted(sources.items()) if k in existing}
    SOURCES.write_text(json.dumps(sources, indent=2) + "\n")


def readme(commit):
    rows, gallery, total = [], [], 0
    for d in theme_dirs():
        files = sorted(f.name for f in d.iterdir())
        total += len(files)
        rows.append(f"| [{title(d.name)}]({d.name}) | `{d.name}/` | {len(files)} |")
        imgs = " ".join(f'<img src="{d.name}/{f}" width="200" alt="{title(d.name)}: {f}">' for f in files)
        gallery.append(f"### {title(d.name)}\n\n{imgs}\n")

    return f"""# Omarchy wallpapers

All {total} wallpapers that ship with the {len(rows)} [Omarchy](https://github.com/omacom/omarchy) themes, sorted into one folder per theme. They were copied from each theme's `backgrounds/` folder at Omarchy commit `{commit}`, with Omarchy's WebP files converted to JPEG (or PNG for lossless ones) so they work in any app or OS.

They pair well with [ghostty-omarchy-themes](https://github.com/Mr-Sunglasses/ghostty-omarchy-themes), which ports the same themes to Ghostty.

## Get them

```sh
git clone https://github.com/Mr-Sunglasses/omarchy-wallpapers
```

Want just one theme? Use a sparse checkout:

```sh
git clone --filter=blob:none --sparse https://github.com/Mr-Sunglasses/omarchy-wallpapers
cd omarchy-wallpapers
git sparse-checkout set tokyo-night
```

## Use them on macOS

### Switch from the terminal

[`wallpaper.sh`](wallpaper.sh) sets a wallpaper on every display:

```sh
./wallpaper.sh                        # list themes
./wallpaper.sh tokyo-night            # next Tokyo Night wallpaper (run again to cycle)
./wallpaper.sh tokyo-night random     # a random one
./wallpaper.sh tokyo-night list       # list its wallpapers
./wallpaper.sh tokyo-night 3          # the 3rd one from that list
./wallpaper.sh random                 # anything from any theme
```

Add an alias to your shell config to switch from anywhere:

```sh
alias wall="$HOME/path/to/omarchy-wallpapers/wallpaper.sh"
```

It changes the wallpaper for the Space you're on. Other Spaces keep their own wallpaper.

### Use System Settings

1. Open **System Settings → Wallpaper**.
2. Click **Add Folder…** and choose a theme folder, such as `tokyo-night`.
3. The folder's wallpapers now appear in the Wallpaper settings. Click one to use it.
4. To rotate through a theme automatically, choose the folder's **Auto-Rotate** option and pick how often it changes.

Add a folder for every theme you like, and switching is one click.

## Staying up to date

A [GitHub Action](.github/workflows/sync.yml) runs [`sync.py`](sync.py) every day. When Omarchy adds, changes or removes a wallpaper or theme, the action commits the change here.

## Themes

| Theme | Folder | Wallpapers |
|---|---|---|
""" + "\n".join(rows) + "\n\n## Preview\n\n" + "\n".join(gallery) + """
## Credits

These wallpapers come from [Omarchy](https://github.com/omacom/omarchy) by David Heinemeier Hansson and its contributors, which is released under the [MIT License](LICENSE). Some of the images were made by the original theme authors and other artists. All credit for them goes to their creators.
"""


def main():
    if len(sys.argv) > 1:
        src = Path(sys.argv[1])
    else:
        src = Path(tempfile.mkdtemp()) / "omarchy"
        subprocess.run(["git", "clone", "--quiet", "--depth", "1", REPO, str(src)], check=True)

    commit = subprocess.run(
        ["git", "-C", str(src), "rev-parse", "--short", "HEAD"], capture_output=True, text=True
    ).stdout.strip()

    sync(src)
    (ROOT / "README.md").write_text(readme(commit or "unknown"))


if __name__ == "__main__":
    main()
