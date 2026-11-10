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

Intro animations (backgrounds/intros/<name>.mp4) go to <theme>/intros/, as in
Omarchy. Each one animates into the wallpaper of the same name, so it's only
kept when that wallpaper is here.

Every wallpaper also gets a small JPEG preview in .previews/<theme>/<file>.jpg,
so apps like oms can show them all without downloading the full pictures. An
intro's preview (.previews/<theme>/intros/<file>.jpg) is its wallpaper's.

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
PREVIEWS = ROOT / ".previews"
# Big enough for a terminal preview pane; about 200 KB each.
PREVIEW_SIZE = (1600, 1000)
PREVIEW_QUALITY = 80
INTROS = "intros"
VIDEO_SUFFIXES = {".mp4", ".m4v", ".mov", ".webm", ".mkv"}

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


def pictures(d):
    """A theme folder's wallpapers (not its intros folder)."""
    return sorted(f for f in d.iterdir() if f.is_file())


def intros(d):
    folder = d / INTROS
    return sorted(f for f in folder.iterdir() if f.is_file()) if folder.is_dir() else []


def still_of(intro, names):
    """The wallpaper (from `names`) an intro animates into: the same name."""
    return next((n for n in sorted(names) if Path(n).stem == intro.stem), None)


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


def mirror(files, local, prefix, sources, changed):
    """Makes `local` hold exactly `files` ({output name: upstream file})."""
    local.mkdir(exist_ok=True)
    for f in local.iterdir():
        if f.is_file() and f.name not in files:
            print(f"- {prefix}/{f.name}")
            f.unlink()
    for name, f in files.items():
        dest, key = local / name, f"{prefix}/{name}"
        digest = hashlib.sha256(f.read_bytes()).hexdigest()
        if dest.exists() and sources.get(key) == digest:
            continue
        print(f"{'~' if dest.exists() else '+'} {key}")
        write(f, dest)
        sources[key] = digest
        changed.add(key)


def sync(src):
    """Mirrors the wallpapers. Returns the "<theme>/<file>" keys it wrote."""
    changed = set()
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
        mirror(wanted, local, slug, sources, changed)

        upstream_intros = backgrounds / INTROS
        clips = {
            f.name: f
            for f in (sorted(upstream_intros.iterdir()) if upstream_intros.is_dir() else [])
            if f.is_file() and f.suffix.lower() in VIDEO_SUFFIXES and still_of(f, wanted)
        }
        if clips:
            mirror(clips, local / INTROS, f"{slug}/{INTROS}", sources, changed)
        elif (local / INTROS).exists():
            print(f"- {slug}/{INTROS}/")
            shutil.rmtree(local / INTROS)

    existing = {
        str(f.relative_to(ROOT)) for d in theme_dirs() for f in [*pictures(d), *intros(d)]
    }
    sources = {k: v for k, v in sorted(sources.items()) if k in existing}
    SOURCES.write_text(json.dumps(sources, indent=2) + "\n")
    return changed


def previews(changed):
    """Makes missing or outdated previews and deletes ones without a wallpaper."""
    wanted = set()
    for d in theme_dirs():
        for f in pictures(d):
            key = f"{d.name}/{f.name}"
            dest = PREVIEWS / d.name / f"{f.name}.jpg"
            wanted.add(dest)
            if dest.exists() and key not in changed:
                continue
            if not dest.exists() and key not in changed:
                # A new wallpaper is already listed by sync(); only report repairs.
                print(f"+ .previews/{key}.jpg")
            dest.parent.mkdir(parents=True, exist_ok=True)
            image = Image.open(f)
            image.thumbnail(PREVIEW_SIZE)
            image.convert("RGB").save(dest, quality=PREVIEW_QUALITY, optimize=True)
        for f in intros(d):
            # It ends on its wallpaper, so that's what it looks like.
            still = still_of(f, [p.name for p in pictures(d)])
            source = PREVIEWS / d.name / f"{still}.jpg"
            dest = PREVIEWS / d.name / INTROS / f"{f.name}.jpg"
            wanted.add(dest)
            if source.exists() and (not dest.exists() or dest.read_bytes() != source.read_bytes()):
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, dest)
    for f in sorted(PREVIEWS.rglob("*.jpg")) if PREVIEWS.exists() else []:
        if f not in wanted:
            f.unlink()
    # Deepest first, so a theme's empty intros folder goes before the theme's.
    for d in sorted(PREVIEWS.rglob("*"), reverse=True) if PREVIEWS.exists() else []:
        if d.is_dir() and not any(d.iterdir()):
            d.rmdir()


def pretty(name):
    """ "0-black-moon.mp4" -> "Black Moon"."""
    words = Path(name).stem.lstrip("0123456789-_ ").replace("_", "-").split("-")
    return " ".join(w.capitalize() for w in words if w)


def readme(commit):
    gallery, total, animations = [], 0, 0
    for d in theme_dirs():
        files = [f.name for f in pictures(d)]
        clips = [f.name for f in intros(d)]
        total += len(files)
        animations += len(clips)
        imgs = " ".join(f'<img src="{d.name}/{f}" width="160" alt="{title(d.name)}: {f}">' for f in files)
        links = ", ".join(f"[{pretty(c)}]({d.name}/{INTROS}/{c})" for c in clips)
        intro_line = f"<br>\n<sub>▶ Intros: {links}</sub>" if clips else ""
        gallery.append(f"**[{title(d.name)}]({d.name})** <sub>{len(files)}</sub><br>\n{imgs}{intro_line}\n")
    themes = len(gallery)

    return f"""<div align="center">

# Omarchy wallpapers

All {total} wallpapers from the {themes} [Omarchy](https://github.com/omacom/omarchy) themes, in one folder per theme, and their {animations} intro animations.

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

## Intros

Some wallpapers come with a short animation that plays into them, in the theme's `intros` folder with the same name (`nord/intros/0-black-moon.mp4` ends on `nord/0-black-moon.jpg`). In Omarchy they play when you switch to that wallpaper; [oms](https://github.com/Mr-Sunglasses/oms) lists them as `▶ intro` wallpapers that play once and then rest on the picture.

## Wallpapers

""" + "\n".join(gallery) + f"""
## Contributing

This repo copies Omarchy's wallpapers automatically every day, so please don't add or change pictures here. To suggest a wallpaper, contribute it to [Omarchy](https://github.com/omacom/omarchy) and it will show up here after the next sync.

The sync is [`sync.py`](sync.py), run daily by a [GitHub Action](.github/workflows/sync.yml). It also converts Omarchy's WebP files to JPEG or PNG so they open anywhere, copies the intro animations as they are, and keeps a small preview of each wallpaper in `.previews/`. Last synced from Omarchy commit `{commit}`.

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

    previews(sync(src))
    (ROOT / "README.md").write_text(readme(commit or "unknown"))


if __name__ == "__main__":
    main()
