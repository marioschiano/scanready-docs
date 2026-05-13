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

# Cage Settings

The cage controls how details are projected from the high-poly scan onto the optimized mesh during baking.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

<h3>Show Cage</h3>

<p>
Displays the cage preview.
</p>

<p>
Use it to verify that the cage fully covers the optimized mesh.
</p>

<hr>

<h3>Auto Cage Extrusion</h3>

<p>
Automatically estimates cage distance based on the scan surface.
</p>

<p>
Useful when you want a fast automatic setup.
</p>

<hr>

<h3>Cage Extrusion</h3>

<p>
Controls cage distance manually.
</p>

<p>
Increase it if details are missing or black artifacts appear during baking.
</p>

<p>
Use the smallest value that fully covers the surface cleanly.
</p>

<hr>

<h3>Cage Alpha</h3>

<p>
Controls cage preview opacity.
</p>

<p>
This only affects viewport visualization.
</p>

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
