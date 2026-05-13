# Advanced Settings

<p align="center">
  <img src="../img/quick-start-one-click.png" alt="ScanReady 1.0 panel with workflow sections and progress controls" style="width:320px; max-width:100%;">
</p>

<p align="center">
<b>Advanced controls for optimization, UVs, baking, output, and memory safety.</b>
</p>

---

Advanced settings give you fine control over mesh cleanup, UV generation, cage projection, baking quality, image output, presets, and memory safety.

You do not need to change every setting to use ScanReady 1.0.

For most scans, start with the default values. Adjust advanced settings only when you need more control over performance, quality, or bake accuracy.

---

# Mesh Settings

These settings control how the high-poly scan is cleaned and reduced.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

### Weld Distance

Merges vertices that are very close together.

This helps clean small scan artifacts, tiny gaps, or overlapping geometry before reduction.

---

### Auto Fix Normals

Recalculates high mesh normals automatically before creating the lowpoly preview.

Useful for scans with broken shading or inverted normals.

---

### Recalculate Outside Normals

Runs Blender normal recalculation manually on the selected high mesh.

Use this when the scan appears inside-out or displays inconsistent shading.

---

### Use Texture View

Displays the model in a flat texture-oriented view without scene lighting.

Useful for inspecting texture results more clearly.

---

### Final Faces

Sets the target face count for the optimized lowpoly mesh.

Lower values create lighter assets.

Higher values preserve more shape detail.

---

### Optimize / Reduce

Controls the decimation ratio.

Lower values create stronger reduction.

Higher values keep more geometry.

</div>

<div style="flex:0 0 340px; text-align:center;">
  <img src="../img/advanced-mesh-settings.png" alt="ScanReady mesh settings interface" style="width:340px; max-width:100%;">
</div>

</div>

---

# UV Settings

These settings control how Smart UV Project unwraps the optimized mesh.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

### Smart UV Preset

Applies a recommended Smart UV angle.

Useful as a fast starting point for common scan types.

---

### Smart UV Angle

Controls how aggressively Smart UV Project splits the mesh into islands.

Lower values create more cuts and more islands.

Higher values create larger UV islands.

---

### UV Padding

Sets spacing between UV islands.

Increase padding to reduce texture bleeding.

---

### Auto Pack UV

Automatically packs UV islands after unwrap.

Leave enabled unless you want to arrange UVs manually.

</div>

<div style="flex:0 0 340px; text-align:center;">
  <img src="../img/advanced-uv-settings.png" alt="ScanReady UV settings interface" style="width:340px; max-width:100%;">
</div>

</div>

---

# Cage Settings

The cage controls how details are projected from the high-poly scan onto the optimized mesh during baking.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

### Show Cage

Displays the cage preview.

Use it to verify that the cage fully covers the optimized mesh.

---

### Auto Cage Extrusion

Automatically estimates cage distance based on the scan surface.

Useful when you want a fast automatic setup.

---

### Cage Extrusion

Controls cage distance manually.

Increase it if details are missing or black artifacts appear during baking.

Use the smallest value that fully covers the surface cleanly.

---

### Cage Alpha

Controls cage preview opacity.

This only affects viewport visualization.

</div>

<div style="flex:0 0 340px; text-align:center;">
  <img src="../img/advanced-cage-settings.png" alt="ScanReady cage settings interface" style="width:340px; max-width:100%;">
</div>

</div>

---

# Bake Settings

These settings control texture baking quality and output.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

### Texture Size

Sets baked texture resolution.

Higher values preserve more detail but increase bake time and memory usage.

---

### Bake Materials

Splits the bake into multiple material groups.

This can improve texture detail on large scans.

When this value is greater than `1`, ScanReady automatically enables **Force CPU Baking** as a safer default.

---

### UV Texture Efficiency

Analyzes UV usage and texture/detail balance before baking.

Use **Analyze UV Usage** to estimate whether the current setup preserves enough texture detail.

---

### Bake Samples

Controls Cycles bake samples.

Higher values reduce noise but increase bake time.

---

### Bake Margin

Adds pixel padding around baked UV islands.

This helps reduce visible seams and texture bleeding.

---

### Bake Base Color

Transfers the main surface color from the original scan.

---

### Bake Normal

Generates or transfers normal maps.

If a linked normal texture exists, ScanReady transfers it automatically.

Otherwise, a geometric high-to-low bake is performed.

---

### Bake Roughness

Transfers or bakes roughness information from the original material.

---

### Bake Occlusion

Generates Ambient Occlusion maps for additional surface depth.

---

### AO Source

Controls whether AO is baked from the high-poly source or generated from the lowpoly mesh.

---

### AO Auto Distance

Automatically estimates AO ray distance from model size.

---

### AO Distance

Manual AO ray distance when automatic mode is disabled.

---

### AO Samples

Controls Ambient Occlusion quality.

Higher values are cleaner but slower.

---

### Normal Strength

Controls how strongly the normal map appears in the final material.

</div>

<div style="flex:0 0 340px; text-align:center;">
  <img src="../img/advanced-bake-settings.png" alt="ScanReady bake settings interface" style="width:340px; max-width:100%;">
</div>

</div>

---

# Output Settings

These settings control how baked textures are saved.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

### Save Images

Saves baked textures to disk.

Useful for export, delivery, archives, and game engines.

---

### Image Format

Available formats:

- **JPG** → compact color textures
- **PNG** → lossless texture output
- **TIFF** → high precision workflows

---

### JPG Quality

Controls JPG compression quality.

Higher values preserve more detail but create larger files.

---

### TIFF 16-bit

Enables higher precision TIFF output.

Useful for detailed assets and archival workflows.

---

### Output Folder

Defines where baked textures are saved.

Relative paths such as `//bake/` are saved next to the current Blender file.

</div>

<div style="flex:0 0 340px; text-align:center;">
  <img src="../img/advanced-output-settings.png" alt="ScanReady output settings interface" style="width:340px; max-width:100%;">
</div>

</div>

---

# Presets

ScanReady 1.0 can save, load, and delete named presets.

Presets store the current workflow settings so you can reuse them later.

Use presets when processing multiple scans with similar requirements, such as:

- VR assets
- Game props
- Museum objects
- Repeated bake workflows
- Standardized studio pipelines

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

Presets help maintain consistent results across multiple assets.

</div>

<div style="flex:0 0 340px; text-align:center;">
  <img src="../img/advanced-presets.png" alt="ScanReady presets interface" style="width:340px; max-width:100%;">
</div>

</div>

---

# Progress and Status

The panel includes workflow status and global progress indicators.

During One Click Bake, ScanReady reports the active stage:

- Preview
- UV Mapping
- Cage
- Bake

This helps track long operations and understand what the addon is currently processing.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

Large scans may require several minutes depending on texture size and bake settings.

</div>

<div style="flex:0 0 340px; text-align:center;">
  <img src="../img/advanced-progress-status.png" alt="ScanReady progress and status interface" style="width:340px; max-width:100%;">
</div>

</div>

---

# Memory Safety

Large scans can become demanding during baking.

These options help reduce the chance of memory-related failures.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

### Safe Memory Bake

Uses a safer bake workflow designed to reduce memory pressure on heavy scenes and large scans.

Recommended for dense photogrammetry assets and high texture resolutions.

---

### Force CPU Baking

Forces baking on the CPU to avoid GPU VRAM limitations.

This is slower, but safer on systems with limited GPU memory.

When **Bake Materials** is set to `2` or more, ScanReady enables this automatically as a conservative safety measure.

</div>

<div style="flex:0 0 340px; text-align:center;">
  <img src="../img/advanced-memory-safety.png" alt="ScanReady memory safety interface" style="width:340px; max-width:100%;">
</div>

</div>

---

# Practical Advice

For VR, videogames, and realtime workflows, always balance quality and performance.

Use advanced settings to find the right compromise between:

- Mesh density
- Texture resolution
- Bake quality
- File size
- Viewport performance
- Realtime performance

The goal is not to preserve every polygon from the original scan.

The goal is to preserve the visual identity of the scan in a lighter and more usable realtime asset.
