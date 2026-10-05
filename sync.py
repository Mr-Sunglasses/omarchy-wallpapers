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
    gallery, total = [], 0
    for d in theme_dirs():
        files = sorted(f.name for f in d.iterdir())
        total += len(files)
        imgs = " ".join(f'<img src="{d.name}/{f}" width="160" alt="{title(d.name)}: {f}">' for f in files)
        gallery.append(f"**[{title(d.name)}]({d.name})** <sub>{len(files)}</sub><br>\n{imgs}\n")
    themes = len(gallery)

    return f"""<div align="center">

# Omarchy wallpapers

All {total} wallpapers from the {themes} [Omarchy](https://github.com/omacom/omarchy) themes, in one folder per theme.

</div>

## Download

```sh
git clone https://github.com/Mr-Sunglasses/omarchy-wallpapers
```

Just one theme:

```sh
git clone --filter=blob:none --sparse https://github.com/Mr-Sunglasses/omarchy-wallpapers
cd omarchy-wallpapers && git sparse-checkout set tokyo-night
```

## Use them on a Mac

- **Easiest:** [oms](https://github.com/Mr-Sunglasses/oms) picks a theme's wallpaper (and terminal colors) for you and sets it on every desktop.
- **System Settings:** go to **Wallpaper → Add Folder…**, choose a theme folder, then click a picture. Pick **Auto-Rotate** to cycle through it.
- **Terminal:** `./wallpaper.sh tokyo-night` sets the next Tokyo Night wallpaper. Run `./wallpaper.sh` to list themes.

## Wallpapers

""" + "\n".join(gallery) + f"""
## Contributing

This repo copies Omarchy's wallpapers automatically every day, so please don't add or change pictures here. To suggest a wallpaper, contribute it to [Omarchy](https://github.com/omacom/omarchy) and it will show up here after the next sync.

The sync is [`sync.py`](sync.py), run daily by a [GitHub Action](.github/workflows/sync.yml). It also converts Omarchy's WebP files to JPEG or PNG so they open anywhere. Last synced from Omarchy commit `{commit}`.

## Credits

The wallpapers come from [Omarchy](https://github.com/omacom/omarchy) and the artists who made them. All credit goes to them. [MIT License](LICENSE).
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
