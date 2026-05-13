# Advanced Settings

Advanced settings give you fine control over mesh cleanup, UV generation, baking quality, image output, presets, utilities, and memory safety.

You do not need to change every setting to use ScanReady 1.0.

For most scans, start with the default values. Adjust advanced settings only when you need more control over performance, quality, or bake accuracy.

<p align="center">
  <img src="../img/advanced-overview.png" alt="ScanReady Advanced settings overview" style="width:340px; max-width:100%;">
</p>

<p align="center">
<b>Advanced controls for cleanup, UVs, baking, presets, utilities, and updates.</b>
</p>

---

# Mesh Settings

These settings control scan cleanup and mesh preparation before generating the lowpoly preview.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

<h3>Weld Distance</h3>

<p>
Merges vertices that are very close together.
</p>

<p>
This can help clean small scan artifacts, tiny gaps, or overlapping points before reduction.
</p>

<hr>

<h3>Auto Fix Normals</h3>

<p>
Automatically recalculates high-poly mesh normals before creating the lowpoly preview.
</p>

<p>
Enable this when the scan has inverted normals, broken shading, or bake artifacts caused by incorrect normal direction.
</p>

<hr>

<h3>Use Texture View</h3>

<p>
Displays the model in a flat texture-oriented view without scene lighting.
</p>

<p>
This is useful for inspecting baked or previewed texture results more clearly.
</p>

<hr>

<h3>Recalculate Outside Normals</h3>

<p>
Runs normal recalculation manually on the selected high-poly mesh.
</p>

<p>
Use this when the scan appears inside-out or has inconsistent shading.
</p>

</div>

<div style="flex:0 0 340px; text-align:center;">
  <img src="../img/advanced-mesh-settings.png" alt="ScanReady Mesh Settings interface" style="width:340px; max-width:100%;">
</div>

</div>

---

# UV Settings

These settings control how Smart UV Project unwraps the optimized mesh.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

<h3>Smart UV Angle</h3>

<p>
Controls how aggressively Smart UV Project splits the mesh into UV islands.
</p>

<p>
Lower values create more cuts and more UV islands.
</p>

<p>
Higher values create larger islands.
</p>

<p>
You can manually adjust this value for finer control, but ScanReady also includes simplified UV presets inside Step 2:
</p>

<ul>
<li><strong>Balanced</strong> → general-purpose unwrap for most scans</li>
<li><strong>Detailed</strong> → creates more UV islands to preserve texture detail</li>
<li><strong>Large Islands</strong> → creates larger UV islands with fewer cuts</li>
</ul>

<p>
These presets automatically adjust the Smart UV Angle for common workflows.
</p>

<hr>

<h3>UV Padding</h3>

<p>
Sets spacing between UV islands.
</p>

<p>
Increase padding to reduce texture bleeding, especially at lower texture resolutions.
</p>

</div>

<div style="flex:0 0 340px; text-align:center;">
  <img src="../img/advanced-uv-settings.png" alt="ScanReady UV Settings interface" style="width:340px; max-width:100%;">
</div>

</div>

---

# Bake Settings

These settings control baking quality, texture padding, image format quality, occlusion options, and memory safety.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

<h3>Bake Samples</h3>

<p>
Sets the number of Cycles samples used for baking.
</p>

<p>
Higher values can reduce noise, especially for Ambient Occlusion, but they also increase bake time.
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

<h3>JPG Quality</h3>

<p>
Controls JPG compression quality when the selected image format is JPG.
</p>

<p>
Higher values preserve more image detail but create larger files.
</p>

<hr>

<h3>TIFF 16-bit</h3>

<p>
Enables higher precision TIFF output when the selected image format is TIFF.
</p>

<p>
This can be useful for detailed assets, archival workflows, or technical texture output.
</p>

</div>

<div style="flex:0 0 340px; text-align:center;">
  <img src="../img/advanced-bake-settings.png" alt="ScanReady Bake Settings interface" style="width:340px; max-width:100%;">
</div>

</div>

---

# Occlusion Settings

These options appear when **Bake Occlusion** is enabled.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

<h3>AO Source</h3>

<p>
Controls whether Ambient Occlusion is baked from the high-poly source to the lowpoly target, or calculated from the lowpoly mesh only.
</p>

<hr>

<h3>AO Auto Distance</h3>

<p>
Automatically calculates AO distance based on the model size.
</p>

<hr>

<h3>AO Distance</h3>

<p>
Manual AO ray distance when automatic distance is disabled.
</p>

<hr>

<h3>AO Samples</h3>

<p>
Controls Ambient Occlusion bake quality.
</p>

<p>
Higher values produce cleaner AO but increase bake time.
</p>

</div>

<div style="flex:0 0 340px; text-align:center;">
  <img src="../img/advanced-occlusion-settings.png" alt="ScanReady Occlusion Settings interface" style="width:340px; max-width:100%;">
</div>

</div>

---

# Memory Safety

These options help reduce memory-related problems during heavy baking operations.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

<h3>Safe Memory Bake</h3>

<p>
Uses a safer bake workflow designed to reduce memory pressure on large scans and heavy Blender scenes.
</p>

<p>
Leave this enabled when working with dense photogrammetry assets or high texture resolutions.
</p>

<hr>

<h3>Force CPU Baking</h3>

<p>
Forces baking on the CPU to avoid GPU memory limits.
</p>

<p>
This is usually slower, but it can be safer on systems with low VRAM.
</p>

<p>
ScanReady 1.0 can enable this automatically when multi-material baking is used.
</p>

</div>

<div style="flex:0 0 340px; text-align:center;">
  <img src="../img/advanced-memory-safety.png" alt="ScanReady Memory Safety interface" style="width:340px; max-width:100%;">
</div>

</div>

---

# Presets

ScanReady 1.0 can save, reload, and delete named presets.

Presets store the current workflow settings so you can reuse them later.

Use presets when processing multiple scans with similar requirements, such as:

- VR assets
- Game props
- Museum objects
- Repeated bake settings
- Standard studio workflows

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

<h3>Preset Name</h3>

<p>
Defines the name of the preset to save.
</p>

<hr>

<h3>Save Preset</h3>

<p>
Saves the current ScanReady settings as a reusable preset.
</p>

<hr>

<h3>Preset Selector</h3>

<p>
Lets you choose an existing preset.
</p>

<hr>

<h3>Reload Preset</h3>

<p>
Loads the selected preset.
</p>

<hr>

<h3>Delete Preset</h3>

<p>
Deletes the selected preset.
</p>

</div>

<div style="flex:0 0 340px; text-align:center;">
  <img src="../img/advanced-presets.png" alt="ScanReady Presets interface" style="width:340px; max-width:100%;">
</div>

</div>

---

# Utilities

Utility tools help reset or restore the addon configuration.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

<h3>Reset Defaults</h3>

<p>
Restores ScanReady settings to their default values.
</p>

<p>
Use this if the current settings are producing unexpected results or if you want to return to a clean starting configuration.
</p>

</div>

<div style="flex:0 0 340px; text-align:center;">
  <img src="../img/advanced-utilities.png" alt="ScanReady Utilities interface" style="width:340px; max-width:100%;">
</div>

</div>

---

# Addon Preferences / Updates

ScanReady includes update preferences in the Blender Add-on Preferences panel.

These options help check for new versions, open release notes, and configure publishing links.

<div style="display:flex; flex-wrap:wrap; gap:32px; align-items:flex-start; margin-top:20px;">

<div style="flex:1 1 500px; min-width:320px;">

<h3>Check for Updates</h3>

<p>
Checks whether a newer version of ScanReady is available.
</p>

<hr>

<h3>Release Notes</h3>

<p>
Opens the ScanReady documentation or release notes page.
</p>

<hr>

<h3>Update</h3>

<p>
Opens or downloads the configured update package for manual installation.
</p>

<hr>

<h3>Publishing Links</h3>

<p>
These links are used to configure update manifest, download URL, and release notes URL after publishing.
</p>

</div>

<div style="flex:0 0 340px; text-align:center;">
  <img src="../img/advanced-addon-preferences.png" alt="ScanReady Addon Preferences and Updates interface" style="width:340px; max-width:100%;">
</div>

</div>

---

# Practical Advice

For VR, videogames, and realtime workflows, always balance quality and performance.

Use advanced settings to find the right compromise between:

- Mesh cleanup
- UV quality
- Bake quality
- Texture resolution
- File size
- Memory usage
- Realtime performance

The goal is not to preserve every polygon from the original scan.

The goal is to preserve the visual identity of the scan in a lighter asset that is easier to use.
