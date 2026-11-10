# Project Genesis v1.0

A rule-based artificial-life ecosystem simulation with a holographic 3D OpenGL renderer.

## Setup (Windows PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

If the virtual environment already exists, activate it and install the requirements.

## Controls

- Left mouse drag: rotate camera
- Mouse wheel: zoom
- Space: pause/resume
- Up/down: simulation speed
- R: reset camera
- S: export analytics CSV to `data/genesis_history.csv`
- Escape or Q: quit

## Model notes

- Organisms wander using rule-based movement.
- Low-energy organisms seek food within their vision radius.
- Food restores energy.
- Starvation damages health and can cause death.
- Organisms reproduce asexually when energy and cooldown conditions are met.
- Offspring inherit speed, vision and metabolism with bounded random mutation.
- A maximum population cap prevents unbounded growth.

This is a simplified computational model, not a validated biological model. Outcomes depend on parameters and random initialization. Run multiple seeds and compare exported histories before drawing research conclusions.


## Bioluminescent renderer

The visualization is now a top-down, black-space particle ecosystem inspired by
the supplied reference. Organisms are rendered as animated cellular colonies
with cyan, lime, and magenta particles. The simulation rules, genetics,
reproduction, energy, food-seeking, and analytics remain unchanged.

Controls:
- `SPACE`: pause/resume
- `UP` / `DOWN`: simulation speed
- `TAB`: show/hide compact statistics
- `S`: export analytics CSV
- `ESC` / `Q`: quit

The statistics overlay is hidden by default so the visual stays close to the
reference. This is a visualization of a simplified rule-based simulation, not
a claim that the organisms are biologically real.


## Cosmic-life renderer

The renderer now presents each organism as a miniature particle galaxy:
many small orbiting particles, subtle elliptical orbital traces, a tiny nucleus,
and a few distant satellites. The world uses a deep-space background, sparse
star points, faint nebula haze, and a dense cyan/lime/magenta particle palette.
This is a visualization-only redesign; the rule-based simulation, genetics,
reproduction, food seeking, and analytics are unchanged.

Press `TAB` to toggle the optional statistics overlay.


## Fluorescence microscopy renderer

The display is now inspired by fluorescence microscopy: near-black field,
irregular cell silhouettes, granular indigo/violet texture, subtle cyan/green
fluorescence, and a small offset nucleus. There are no galaxy arms, orbit
guides, nebula clouds, star fields, or large glowing cores. This is a
visualization-only change; the rule-based simulation mechanics are unchanged.
