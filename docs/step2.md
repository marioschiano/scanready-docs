# Step 2 - UV / Cage

Step 2 generates a new UV layout and prepares the baking cage.

After the scan has been simplified in Step 1, the optimized mesh needs a new UV layout so textures can be baked onto it correctly.

Generating new UVs ensures that the optimized mesh has clean texture coordinates before baking. The cage then helps transfer details from the original high-poly scan to the lighter object.

This step is essential when preparing assets for **VR, videogames, AR, realtime visualization, and interactive environments**, because it allows the optimized mesh to preserve much of the visual richness of the original scan.

---

## Why UVs Are Needed

A simplified mesh is lighter and easier to manage, but it still needs coherent texture coordinates.

UVs define how the surface of the 3D model is unwrapped into 2D space.

After reduction, the original scan UVs should not be trusted on the optimized mesh.

Because geometry has been merged and simplified, old UVs can become:

- Stretched
- Dirty
- Overlapping
- Distorted
- Mismatched with the new surface

Without a fresh UV layout, ScanReady 1.0 cannot properly bake texture information from the original scan onto the optimized mesh.

Creating new UVs on the lowpoly mesh is a necessary step.

Clean and coherent UVs are what allow ScanReady 1.0 to transfer textures and details from the high-poly version to the optimized asset, producing a clean, readable, and accurate bake.

---

## Better UV Space Usage

New UVs also help use texture space more efficiently.

Scanned models often come with several materials and UV layouts that do not fill the full 0-1 UV space efficiently, which wastes texture resolution.

After optimization, ScanReady 1.0 can prepare the lowpoly asset with a cleaner UV layout that uses the available 0-1 space more effectively.

In many cases, a scan that originally used multiple poorly packed materials can be baked into a simpler material setup with a better packed texture.

The result is a model optimized not only in polygon count, but also in texture usage, material count, and overall material efficiency.

Good UVs help produce:

- Cleaner baked textures
- Fewer visible seams
- Better texture resolution
- More predictable results in game engines
- More usable assets for realtime workflows

---

## Textures Replace Geometry

The goal of baking is to preserve the visual richness of the original scan while reducing polygon density.

Instead of keeping millions of polygons, ScanReady transfers surface information into textures.

This allows the optimized mesh to remain lightweight while still preserving much of the original appearance.

---

## Why the Cage Is Needed

The cage controls how Blender projects details from the high-poly scan onto the optimized mesh during baking.

If the cage is too small, some details may be missed.

If the cage is too large, the bake may capture details from the wrong areas.

ScanReady 1.0 includes cage tools to make this process faster and easier.

---

## UV Method

ScanReady 1.0 uses **Smart UV Project** to generate UVs for the optimized mesh.

Smart UV Project is Blender's automatic UV unwrap method.

It is useful for scanned objects because it can quickly create UV islands without requiring manual seam placement.

ScanReady 1.0 exposes Smart UV controls so you can adjust how the unwrap behaves before baking.

<p align="center">
  <img src="../img/step2-uv-layout.png" alt="ScanReady 1.0 UV layout generated from the optimized mesh" style="max-width:760px;width:100%;">
</p>

### Smart UV Project

Uses Blender Smart UV Project.

This is a good general-purpose option for many standard scans.

---

## UV Settings

These settings control how Smart UV Project unwraps the optimized mesh.

### Smart UV Preset

Applies a recommended Smart UV angle.

Use it as a fast starting point for common scan types.

### Smart UV Angle

Controls how aggressively Smart UV Project splits the mesh into islands.

Lower values create more cuts and more UV islands.

Higher values create larger islands.

### UV Padding

Sets spacing between UV islands.

Increase padding to reduce texture bleeding, especially at lower texture resolutions.

### Auto Pack UV

Automatically packs UV islands after unwrap.

Leave this enabled unless you want to arrange UV islands manually.

Better UV packing helps maximize texture resolution.

Well-packed UV islands allow the bake to preserve more detail across the optimized mesh.

---

## Checker Preview

Use **Show Checker** to inspect UV stretching before baking.

The checker texture helps reveal:

- UV stretching
- Distortion
- Uneven texel density
- Problematic UV islands

A clean checker pattern usually indicates a healthier UV layout for baking.

---

## Cage Controls

### Show Cage

Displays the cage preview.

Use it before baking to check that the cage covers the optimized mesh correctly.

### Auto Cage Extrusion

Automatically estimates cage extrusion by sampling the distance between the optimized mesh and the original high-poly scan.

This is useful when you want a fast cage setup without manually guessing the distance.

### Cage Extrusion

Controls the cage distance manually.

Increase it if the bake misses scan details or creates gaps.

Use the smallest value that captures the details cleanly.

### Cage Alpha

Controls the cage preview opacity.

This only affects viewport display.

It does not change the baked result.

---

## Action

Click **Generate UVs** after creating the lowpoly preview.

Then inspect the UV result and cage before moving to:

[Step 3 - Bake / Output](step3.md)

---

## What to Check

Before baking, check:

- UVs are generated on the optimized object
- The checker pattern does not show extreme stretching
- UV islands have enough padding
- The cage covers the areas that need to receive baked detail
- The cage is not so large that it captures unwanted nearby surfaces

---

## Realtime Optimization

For VR and videogame assets, UVs and baking are what allow a lighter model to still look detailed.

The optimized mesh should carry the important visual information through textures, not through millions of polygons.

Good UVs and a correct cage help keep the asset:

- Lighter
- Easier to render
- Easier to export
- More reliable in realtime engines
- Visually closer to the original scan
