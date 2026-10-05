# Omarchy wallpapers

All 92 wallpapers that ship with the 22 [Omarchy](https://github.com/omacom/omarchy) themes, sorted into one folder per theme. They were copied from each theme's `backgrounds/` folder at Omarchy commit `65c0f33`, with Omarchy's WebP files converted to JPEG (or PNG for lossless ones) so they work in any app or OS.

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
| [Catppuccin Mocha](catppuccin) | `catppuccin/` | 4 |
| [Catppuccin Latte](catppuccin-latte) | `catppuccin-latte/` | 2 |
| [Ethereal](ethereal) | `ethereal/` | 3 |
| [Everforest](everforest) | `everforest/` | 2 |
| [Flexoki Light](flexoki-light) | `flexoki-light/` | 2 |
| [Gruvbox](gruvbox) | `gruvbox/` | 6 |
| [Hackerman](hackerman) | `hackerman/` | 3 |
| [Kanagawa](kanagawa) | `kanagawa/` | 2 |
| [Last Horizon](last-horizon) | `last-horizon/` | 4 |
| [Lumon](lumon) | `lumon/` | 3 |
| [Lupine](lupine) | `lupine/` | 6 |
| [Matte Black](matte-black) | `matte-black/` | 4 |
| [Miasma](miasma) | `miasma/` | 3 |
| [Nord](nord) | `nord/` | 4 |
| [Osaka Jade](osaka-jade) | `osaka-jade/` | 4 |
| [Retro 82](retro-82) | `retro-82/` | 9 |
| [Ristretto](ristretto) | `ristretto/` | 5 |
| [Rose Pine Dawn](rose-pine) | `rose-pine/` | 4 |
| [Solitude](solitude) | `solitude/` | 5 |
| [Tokyo Night](tokyo-night) | `tokyo-night/` | 8 |
| [Vantablack](vantablack) | `vantablack/` | 5 |
| [White](white) | `white/` | 4 |

## Preview

### Catppuccin Mocha

<img src="catppuccin/1-totoro.jpg" width="200" alt="Catppuccin Mocha: 1-totoro.jpg"> <img src="catppuccin/2-waves.png" width="200" alt="Catppuccin Mocha: 2-waves.png"> <img src="catppuccin/3-blue-eye.png" width="200" alt="Catppuccin Mocha: 3-blue-eye.png"> <img src="catppuccin/omarchy.png" width="200" alt="Catppuccin Mocha: omarchy.png">

### Catppuccin Latte

<img src="catppuccin-latte/1-color-fade.jpg" width="200" alt="Catppuccin Latte: 1-color-fade.jpg"> <img src="catppuccin-latte/omarchy.png" width="200" alt="Catppuccin Latte: omarchy.png">

### Ethereal

<img src="ethereal/1-cosmic.jpg" width="200" alt="Ethereal: 1-cosmic.jpg"> <img src="ethereal/2-meadow.jpg" width="200" alt="Ethereal: 2-meadow.jpg"> <img src="ethereal/omarchy.png" width="200" alt="Ethereal: omarchy.png">

### Everforest

<img src="everforest/1-tree-tops.jpg" width="200" alt="Everforest: 1-tree-tops.jpg"> <img src="everforest/omarchy.png" width="200" alt="Everforest: omarchy.png">

### Flexoki Light

<img src="flexoki-light/1-orb.png" width="200" alt="Flexoki Light: 1-orb.png"> <img src="flexoki-light/2-omarchy.png" width="200" alt="Flexoki Light: 2-omarchy.png">

### Gruvbox

<img src="gruvbox/1-the-backwater.jpg" width="200" alt="Gruvbox: 1-the-backwater.jpg"> <img src="gruvbox/2-flower-basket.jpg" width="200" alt="Gruvbox: 2-flower-basket.jpg"> <img src="gruvbox/3-village-square.jpg" width="200" alt="Gruvbox: 3-village-square.jpg"> <img src="gruvbox/4-idyllic-procession.jpg" width="200" alt="Gruvbox: 4-idyllic-procession.jpg"> <img src="gruvbox/5-leaves.jpg" width="200" alt="Gruvbox: 5-leaves.jpg"> <img src="gruvbox/omarchy.png" width="200" alt="Gruvbox: omarchy.png">

### Hackerman

<img src="hackerman/1-synth-scape.jpg" width="200" alt="Hackerman: 1-synth-scape.jpg"> <img src="hackerman/2-geometric.jpg" width="200" alt="Hackerman: 2-geometric.jpg"> <img src="hackerman/omarchy.png" width="200" alt="Hackerman: omarchy.png">

### Kanagawa

<img src="kanagawa/1-kanagawa.jpg" width="200" alt="Kanagawa: 1-kanagawa.jpg"> <img src="kanagawa/omarchy.png" width="200" alt="Kanagawa: omarchy.png">

### Last Horizon

<img src="last-horizon/1-eyes-wide.jpg" width="200" alt="Last Horizon: 1-eyes-wide.jpg"> <img src="last-horizon/2-blink.jpg" width="200" alt="Last Horizon: 2-blink.jpg"> <img src="last-horizon/3-bokeh.jpg" width="200" alt="Last Horizon: 3-bokeh.jpg"> <img src="last-horizon/4-new-horizons.jpg" width="200" alt="Last Horizon: 4-new-horizons.jpg">

### Lumon

<img src="lumon/01-united-in-severance.jpg" width="200" alt="Lumon: 01-united-in-severance.jpg"> <img src="lumon/02-opinions-equally.jpg" width="200" alt="Lumon: 02-opinions-equally.jpg"> <img src="lumon/omarchy.png" width="200" alt="Lumon: omarchy.png">

### Lupine

<img src="lupine/01-cherry-blossom-bokeh.jpg" width="200" alt="Lupine: 01-cherry-blossom-bokeh.jpg"> <img src="lupine/02-cherry-blossom-white.jpg" width="200" alt="Lupine: 02-cherry-blossom-white.jpg"> <img src="lupine/03-pastel-clouds.jpg" width="200" alt="Lupine: 03-pastel-clouds.jpg"> <img src="lupine/04-elegant-blue-wave.jpg" width="200" alt="Lupine: 04-elegant-blue-wave.jpg"> <img src="lupine/05-abstract-wave.jpg" width="200" alt="Lupine: 05-abstract-wave.jpg"> <img src="lupine/06-omarchy.png" width="200" alt="Lupine: 06-omarchy.png">

### Matte Black

<img src="matte-black/0-ship-at-sea.jpg" width="200" alt="Matte Black: 0-ship-at-sea.jpg"> <img src="matte-black/1-dark-waters.jpg" width="200" alt="Matte Black: 1-dark-waters.jpg"> <img src="matte-black/2-dot-hands.png" width="200" alt="Matte Black: 2-dot-hands.png"> <img src="matte-black/omarchy.png" width="200" alt="Matte Black: omarchy.png">

### Miasma

<img src="miasma/01-nature-of-fear.jpg" width="200" alt="Miasma: 01-nature-of-fear.jpg"> <img src="miasma/02-crowned.jpg" width="200" alt="Miasma: 02-crowned.jpg"> <img src="miasma/omarchy.png" width="200" alt="Miasma: omarchy.png">

### Nord

<img src="nord/0-black-moon.jpg" width="200" alt="Nord: 0-black-moon.jpg"> <img src="nord/1-city-view.png" width="200" alt="Nord: 1-city-view.png"> <img src="nord/2-night-hawks.png" width="200" alt="Nord: 2-night-hawks.png"> <img src="nord/omarchy.png" width="200" alt="Nord: omarchy.png">

### Osaka Jade

<img src="osaka-jade/1-glowing-city.jpg" width="200" alt="Osaka Jade: 1-glowing-city.jpg"> <img src="osaka-jade/2-shaded-entrance.jpg" width="200" alt="Osaka Jade: 2-shaded-entrance.jpg"> <img src="osaka-jade/3-mountain-moon.jpg" width="200" alt="Osaka Jade: 3-mountain-moon.jpg"> <img src="osaka-jade/omarchy.png" width="200" alt="Osaka Jade: omarchy.png">

### Retro 82

<img src="retro-82/1-in-the-groove.jpg" width="200" alt="Retro 82: 1-in-the-groove.jpg"> <img src="retro-82/2-dusk-guardian.jpg" width="200" alt="Retro 82: 2-dusk-guardian.jpg"> <img src="retro-82/3-glassy-lines.jpg" width="200" alt="Retro 82: 3-glassy-lines.jpg"> <img src="retro-82/4-gateway.jpg" width="200" alt="Retro 82: 4-gateway.jpg"> <img src="retro-82/5-zen-boat.jpg" width="200" alt="Retro 82: 5-zen-boat.jpg"> <img src="retro-82/6-abstract-pyramids.jpg" width="200" alt="Retro 82: 6-abstract-pyramids.jpg"> <img src="retro-82/7-the-journey.jpg" width="200" alt="Retro 82: 7-the-journey.jpg"> <img src="retro-82/8-glitter-glass.jpg" width="200" alt="Retro 82: 8-glitter-glass.jpg"> <img src="retro-82/omarchy.png" width="200" alt="Retro 82: omarchy.png">

### Ristretto

<img src="ristretto/0-launch.png" width="200" alt="Ristretto: 0-launch.png"> <img src="ristretto/1-color-curves.jpg" width="200" alt="Ristretto: 1-color-curves.jpg"> <img src="ristretto/2-coffee-beans.jpg" width="200" alt="Ristretto: 2-coffee-beans.jpg"> <img src="ristretto/3-industrial-moon.jpg" width="200" alt="Ristretto: 3-industrial-moon.jpg"> <img src="ristretto/omarchy.png" width="200" alt="Ristretto: omarchy.png">

### Rose Pine Dawn

<img src="rose-pine/1-funky-shapes.jpg" width="200" alt="Rose Pine Dawn: 1-funky-shapes.jpg"> <img src="rose-pine/2-dot-map.jpg" width="200" alt="Rose Pine Dawn: 2-dot-map.jpg"> <img src="rose-pine/3-omarchy-plants.jpg" width="200" alt="Rose Pine Dawn: 3-omarchy-plants.jpg"> <img src="rose-pine/omarchy.png" width="200" alt="Rose Pine Dawn: omarchy.png">

### Solitude

<img src="solitude/1-on-pole.jpg" width="200" alt="Solitude: 1-on-pole.jpg"> <img src="solitude/2-wreakage.jpg" width="200" alt="Solitude: 2-wreakage.jpg"> <img src="solitude/3-climb.jpg" width="200" alt="Solitude: 3-climb.jpg"> <img src="solitude/4-ether.jpg" width="200" alt="Solitude: 4-ether.jpg"> <img src="solitude/5-eyed.jpg" width="200" alt="Solitude: 5-eyed.jpg">

### Tokyo Night

<img src="tokyo-night/0-winding-road.jpg" width="200" alt="Tokyo Night: 0-winding-road.jpg"> <img src="tokyo-night/1-quattro.jpg" width="200" alt="Tokyo Night: 1-quattro.jpg"> <img src="tokyo-night/2-swirl-buck.jpg" width="200" alt="Tokyo Night: 2-swirl-buck.jpg"> <img src="tokyo-night/3-sunset-lake.jpg" width="200" alt="Tokyo Night: 3-sunset-lake.jpg"> <img src="tokyo-night/4-omakub.jpg" width="200" alt="Tokyo Night: 4-omakub.jpg"> <img src="tokyo-night/5-oma-cityscape.jpg" width="200" alt="Tokyo Night: 5-oma-cityscape.jpg"> <img src="tokyo-night/6-oma.jpg" width="200" alt="Tokyo Night: 6-oma.jpg"> <img src="tokyo-night/omarchy.png" width="200" alt="Tokyo Night: omarchy.png">

### Vantablack

<img src="vantablack/0-dot-hands.png" width="200" alt="Vantablack: 0-dot-hands.png"> <img src="vantablack/1-twisted-stairs.jpg" width="200" alt="Vantablack: 1-twisted-stairs.jpg"> <img src="vantablack/2-layers-deep.jpg" width="200" alt="Vantablack: 2-layers-deep.jpg"> <img src="vantablack/3-layers-stacked.jpg" width="200" alt="Vantablack: 3-layers-stacked.jpg"> <img src="vantablack/omarchy.png" width="200" alt="Vantablack: omarchy.png">

### White

<img src="white/1-white.jpg" width="200" alt="White: 1-white.jpg"> <img src="white/2-white.jpg" width="200" alt="White: 2-white.jpg"> <img src="white/3-white.jpg" width="200" alt="White: 3-white.jpg"> <img src="white/omarchy.png" width="200" alt="White: omarchy.png">

## Credits

These wallpapers come from [Omarchy](https://github.com/omacom/omarchy) by David Heinemeier Hansson and its contributors, which is released under the [MIT License](LICENSE). Some of the images were made by the original theme authors and other artists. All credit for them goes to their creators.
