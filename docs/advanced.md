# Advanced Settings

<p align="center">
  <img src="../img/quick-start-one-click.png" alt="ScanReady 1.0 panel with workflow sections and progress controls" style="width:320px; max-width:100%;">
</p>

<p align="center">
<b>Advanced controls for optimization, UVs, baking, output, and memory safety.</b>
</p>

---

Advanced settings give you fine control over mesh cleanup, UV generation, baking quality, image output, presets, and memory safety.

You do not need to change every setting to use ScanReady 1.0.

For most scans, start with the default values. Adjust advanced settings only when you need more control over performance, quality, or bake accuracy.

---

# Mesh Settings

These settings control how the high-poly scan is cleaned and reduced.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

<h3>Weld Distance</h3>

<p>
Merges vertices that are very close together.
</p>

<p>
This helps clean small scan artifacts, tiny gaps, or overlapping geometry before reduction.
</p>

<hr>

<h3>Auto Fix Normals</h3>

<p>
Recalculates high mesh normals automatically before creating the lowpoly preview.
</p>

<p>
Useful for scans with broken shading or inverted normals.
</p>

<hr>

<h3>Recalculate Outside Normals</h3>

<p>
Runs Blender normal recalculation manually on the selected high mesh.
</p>

<p>
Use this when the scan appears inside-out or displays inconsistent shading.
</p>

<hr>

<h3>Use Texture View</h3>

<p>
Displays the model in a flat texture-oriented view without scene lighting.
</p>

<p>
Useful for inspecting texture results more clearly.
</p>

<hr>

<h3>Final Faces</h3>

<p>
Sets the target face count for the optimized lowpoly mesh.
</p>

<p>
Lower values create lighter assets.
</p>

<p>
Higher values preserve more shape detail.
</p>

<hr>

<h3>Optimize / Reduce</h3>

<p>
Controls the decimation ratio.
</p>

<p>
Lower values create stronger reduction.
</p>

<p>
Higher values keep more geometry.
</p>

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

<h3>Smart UV Preset</h3>

<p>
Applies a recommended Smart UV angle.
</p>

<p>
Useful as a fast starting point for common scan types.
</p>

<hr>

<h3>Smart UV Angle</h3>

<p>
Controls how aggressively Smart UV Project splits the mesh into islands.
</p>

<p>
Lower values create more cuts and more islands.
</p>

<p>
Higher values create larger UV islands.
</p>

<hr>

<h3>UV Padding</h3>

<p>
Sets spacing between UV islands.
</p>

<p>
Increase padding to reduce texture bleeding.
</p>

<hr>

<h3>Auto Pack UV</h3>

<p>
Automatically packs UV islands after unwrap.
</p>

<p>
Leave enabled unless you want to arrange UVs manually.
</p>

</div>

<div style="flex:0 0 340px; text-align:center;">
  <img src="../img/advanced-uv-settings.png" alt="ScanReady UV settings interface" style="width:340px; max-width:100%;">
</div>

</div>

---

# Cage Workflow

Detailed cage setup and baking projection workflow are explained inside:

[Step 2 - UV / Cage](step2.md)

The cage controls how surface detail is projected from the high-poly scan onto the optimized mesh during baking.

Proper cage setup is important for avoiding:

- Missing details
- Black bake artifacts
- Incorrect projection
- Surface overlap problems

<div style="text-align:center; margin-top:20px;">
  <img src="../img/advanced-cage-settings.png" alt="ScanReady cage workflow interface" style="width:340px; max-width:100%;">
</div>

---

# Bake Settings

These settings control texture baking quality and output.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

<h3>Texture Size</h3>

<p>
Sets baked texture resolution.
</p>

<p>
Higher values preserve more detail but increase bake time and memory usage.
</p>

<hr>

<h3>Bake Materials</h3>

<p>
Splits the bake into multiple material groups.
</p>

<p>
This can improve texture detail on large scans.
</p>

<p>
When this value is greater than <code>1</code>, ScanReady automatically enables <strong>Force CPU Baking</strong> as a safer default.
</p>

<hr>

<h3>UV Texture Efficiency</h3>

<p>
Analyzes UV usage and texture/detail balance before baking.
</p>

<p>
Use <strong>Analyze UV Usage</strong> to estimate whether the current setup preserves enough texture detail.
</p>

<hr>

<h3>Bake Samples</h3>

<p>
Controls Cycles bake samples.
</p>

<p>
Higher values reduce noise but increase bake time.
</p>

<hr>

<h3>Bake Margin</h3>

<p>
Adds pixel padding around baked UV islands.
</p>

<p>
This helps reduce visible seams and texture bleeding.
</p>

<hr>

<h3>Bake Base Color</h3>

<p>
Transfers the main surface color from the original scan.
</p>

<hr>

<h3>Bake Normal</h3>

<p>
Generates or transfers normal maps.
</p>

<p>
If a linked normal texture exists, ScanReady transfers it automatically.
</p>

<p>
Otherwise, a geometric high-to-low bake is performed.
</p>

<hr>

<h3>Bake Roughness</h3>

<p>
Transfers or bakes roughness information from the original material.
</p>

<hr>

<h3>Bake Occlusion</h3>

<p>
Generates Ambient Occlusion maps for additional surface depth.
</p>

<hr>

<h3>AO Source</h3>

<p>
Controls whether AO is baked from the high-poly source or generated from the lowpoly mesh.
</p>

<hr>

<h3>AO Auto Distance</h3>

<p>
Automatically estimates AO ray distance from model size.
</p>

<hr>

<h3>AO Distance</h3>

<p>
Manual AO ray distance when automatic mode is disabled.
</p>

<hr>

<h3>AO Samples</h3>

<p>
Controls Ambient Occlusion quality.
</p>

<p>
Higher values are cleaner but slower.
</p>

<hr>

<h3>Normal Strength</h3>

<p>
Controls how strongly the normal map appears in the final material.
</p>

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

<h3>Save Images</h3>

<p>
Saves baked textures to disk.
</p>

<p>
Useful for export, delivery, archives, and game engines.
</p>

<hr>

<h3>Image Format</h3>

<p>
Available formats:
</p>

<ul>
<li><strong>JPG</strong> → compact color textures</li>
<li><strong>PNG</strong> → lossless texture output</li>
<li><strong>TIFF</strong> → high precision workflows</li>
</ul>

<hr>

<h3>JPG Quality</h3>

<p>
Controls JPG compression quality.
</p>

<p>
Higher values preserve more detail but create larger files.
</p>

<hr>

<h3>TIFF 16-bit</h3>

<p>
Enables higher precision TIFF output.
</p>

<p>
Useful for detailed assets and archival workflows.
</p>

<hr>

<h3>Output Folder</h3>

<p>
Defines where baked textures are saved.
</p>

<p>
Relative paths such as <code>//bake/</code> are saved next to the current Blender file.
</p>

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

<h3>Safe Memory Bake</h3>

<p>
Uses a safer bake workflow designed to reduce memory pressure on heavy scenes and large scans.
</p>

<p>
Recommended for dense photogrammetry assets and high texture resolutions.
</p>

<hr>

<h3>Force CPU Baking</h3>

<p>
Forces baking on the CPU to avoid GPU VRAM limitations.
</p>

<p>
This is slower, but safer on systems with limited GPU memory.
</p>

<p>
When <strong>Bake Materials</strong> is set to <code>2</code> or more, ScanReady enables this automatically as a conservative safety measure.
</p>

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
