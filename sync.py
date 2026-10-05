#!/usr/bin/env python3
"""Sync wallpapers from Omarchy into one folder per theme and rebuild README.md.

Mirrors every themes/<theme>/backgrounds/ folder from Omarchy: new wallpapers
and themes are added, changed ones updated, and ones removed upstream deleted.

    ./sync.py                 # clones omarchy into a temp dir
    ./sync.py ~/src/omarchy   # or use an existing checkout
"""

import filecmp
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = "https://github.com/omacom/omarchy"
ROOT = Path(__file__).resolve().parent

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


def sync(src):
    upstream = {d.parent.name: d for d in src.glob("themes/*/backgrounds") if d.is_dir() and any(d.iterdir())}

    for local in theme_dirs():
        if local.name not in upstream:
            print(f"- {local.name}/")
            shutil.rmtree(local)

    for slug, backgrounds in sorted(upstream.items()):
        local = ROOT / slug
        local.mkdir(exist_ok=True)
        wanted = {f.name: f for f in backgrounds.iterdir() if f.is_file()}
        for f in local.iterdir():
            if f.name not in wanted:
                print(f"- {slug}/{f.name}")
                f.unlink()
        for name, f in sorted(wanted.items()):
            dest = local / name
            if not dest.exists() or not filecmp.cmp(f, dest, shallow=False):
                print(f"{'~' if dest.exists() else '+'} {slug}/{name}")
                shutil.copy2(f, dest)


def readme(commit):
    rows, gallery, total = [], [], 0
    for d in theme_dirs():
        files = sorted(f.name for f in d.iterdir())
        total += len(files)
        rows.append(f"| [{title(d.name)}]({d.name}) | `{d.name}/` | {len(files)} |")
        imgs = " ".join(f'<img src="{d.name}/{f}" width="200" alt="{title(d.name)}: {f}">' for f in files)
        gallery.append(f"### {title(d.name)}\n\n{imgs}\n")

    return f"""# Omarchy wallpapers

All {total} wallpapers that ship with the {len(rows)} [Omarchy](https://github.com/omacom/omarchy) themes, sorted into one folder per theme. They were copied from each theme's `backgrounds/` folder at Omarchy commit `{commit}`.

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
