# ScanReady

ScanReady is a Blender addon designed to turn heavy 3D scans into optimized, game-ready assets.

High-poly scans from photogrammetry or 3D capture can be too dense for realtime use. ScanReady helps simplify those models, generate UVs, prepare baking, and create lighter assets that are easier to use in **VR, AR, videogames, realtime visualization, and interactive environments**.

<br>

<p align="center">
  <img src="img/hero.png" width="700">
</p>

<br>

<p align="center">
  <b>High-Poly Scan > Optimized Mesh > UVs > Bake > Realtime Asset</b>
</p>

---

## Why ScanReady?

3D scans are often beautiful but difficult to use in production.

They can contain:

- Millions of polygons.
- Heavy geometry that slows Blender.
- Dense meshes that are not suitable for VR.
- No clean UV layout.
- Materials or textures that need to be transferred to a lighter object.
- Bake settings that are time-consuming to prepare manually.

ScanReady simplifies this process inside Blender.

It helps you convert a heavy scan into a lighter, cleaner, baked asset that can be used more easily in realtime workflows.

---

## One Click Bake

The fastest way to use ScanReady is the **ONE CLICK BAKE** workflow.

ScanReady can automatically perform:

- Mesh optimization.
- Lowpoly preview creation.
- UV generation.
- Automatic cage setup.
- Texture baking.
- Final asset and material setup.
- Texture saving when output saving is enabled.

Start with One Click Bake for most scans. Use the manual steps when you need more control.
<p align="center">
  <img src="img/high-to-low-workflow.png" style="max-width:560px;width:100%;">

</p>

---

## Key Features

| Feature | Description |
|---|---|
| **One Click Workflow** | Runs the main scan-to-asset pipeline automatically. |
| **Scan Simplification** | Reduces heavy scan geometry into a lighter optimized mesh. |
| **VR and Realtime Ready** | Helps make captured models easier to handle in VR, AR, videogames, and realtime viewers. |
| **Preview / Reduce** | Lets you preview the optimized mesh before UVs and baking. |
| **Smart UV Project** | Uses Blender Smart UV Project to generate UVs for the optimized mesh. |
| **Auto Cage** | Estimates cage extrusion for high-to-low baking. |
| **Texture Baking** | Transfers visual detail from the original scan to the optimized mesh. |
| **Base Color, Normal, and AO Maps** | Supports common texture maps used in game and realtime pipelines. |
| **Memory Safety** | Includes safer bake options for heavy scenes and large scans. |
| **Reusable Presets** | Saves workflow settings for repeated scan processing. |

---

## Workflow Overview

ScanReady follows a simple 3-step workflow.

### 1. Preview / Reduce

Create an optimized lowpoly preview from your high-poly scan.

This step helps reduce the model so it becomes lighter and easier to use in realtime applications.

### 2. UV / Cage

Generate UVs and prepare the baking cage.

This step prepares the optimized mesh to receive texture detail from the original scan.

### 3. Bake / Output

Bake texture information from the original high-poly object to the optimized mesh.

The result is a lighter asset that keeps much of the visual detail of the scan while being easier to use in VR, games, and realtime scenes.

---

## Recommended Use Cases

ScanReady is ideal for:

- Photogrammetry scans.
- Cultural heritage objects.
- Museum and archive assets.
- Game props.
- Environment objects.
- Real-world captured models.
- VR and AR experiences.
- Realtime visualization.
- Interactive installations.
- Educational and historical reconstructions.

---

## What ScanReady Creates

After the workflow, ScanReady can generate:

- Optimized lowpoly mesh.
- UV-ready object.
- Baking cage.
- Final baked mesh.
- Final material setup.
- Texture files saved to the selected output folder.

The goal is to preserve the visual identity of the original scan while making it lighter and more practical for production.

---

## Get Started

New users should begin here:

[Quick Start](quick-start.md)

For the full automatic workflow, continue with:

[One Click Bake](one-click.md)
