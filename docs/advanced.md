# Advanced Settings

Advanced settings give you fine control over mesh cleanup, UV generation, cage projection, baking quality, image output, presets, and memory safety.

You do not need to change every setting to use ScanReady 1.0.

For most scans, start with the default values. Adjust advanced settings when you need more control over performance, quality, or bake accuracy.

<p align="center">
  <img src="../img/quick-start-one-click.png" alt="ScanReady 1.0 panel with workflow sections and progress controls" style="width:280px; max-width:100%;">
</p>

---

## Mesh Settings

These settings control how the high-poly scan is cleaned and reduced.

### Weld Distance

Merges vertices that are very close together.

This can help clean small scan artifacts, tiny gaps, or overlapping points before reduction.

### Auto Fix Normals

Recalculates the high mesh normals before creating the lowpoly preview.

Enable this when the scan has inverted normals, broken shading, or bake artifacts caused by normal direction.

### Recalculate Outside Normals

Runs normal recalculation manually on the selected high mesh.

Use this when the scan appears inside-out or has inconsistent shading.

### Use Texture View

Shows the model in a flat texture-oriented view without scene lighting.

This is useful for inspecting baked or previewed texture results, but it is now kept in **Advanced** because most users do not need to change it often.

### Final Faces

Sets the target face count for the optimized lowpoly mesh.

Lower values create lighter assets.

Higher values preserve more shape detail.

### Optimize / Reduce

Controls the decimation ratio.

Lower values create stronger reduction.

Higher values keep more geometry.

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


---

## Cage Settings

The cage controls how details are projected from the high-poly scan to the optimized mesh during baking.

### Show Cage

Displays the cage preview.

Use it to visually check whether the cage covers the optimized mesh correctly.

### Auto Cage Extrusion

Automatically estimates cage extrusion by sampling the distance from the optimized mesh to the original high-poly scan.

This is useful when you want a fast cage setup without manually guessing a value.

### Cage Extrusion

Manual cage distance.

Increase it if the bake misses details or creates gaps.

Use the smallest value that captures the surface cleanly.

### Cage Alpha

Controls cage preview opacity.

This only affects viewport display. It does not change the bake.

---

## Bake Settings

These settings control texture baking quality and output.

### Texture Size

Sets the baked texture resolution.

Higher values preserve more detail but increase bake time, memory usage, and file size.

### Bake Materials

Splits the bake into multiple material groups.

This can help large scans keep more texture detail, but it increases bake time and output complexity.

When this value is greater than `1`, ScanReady 1.0 automatically enables **Force CPU Baking** as a safer default.

This helps reduce GPU memory problems during multi-material bakes. You can still disable **Force CPU Baking** manually if you prefer to use the GPU.

### UV Texture Efficiency

Analyzes the high-poly source and the optimized UV mesh to estimate texture/detail match before baking.

Use **Analyze UV Usage** when deciding whether the current **Texture Size** and **Bake Materials** settings are enough for the asset.

The analysis can recommend more or fewer bake materials and warns when UV usage is inefficient, overlapping, or likely to produce softer texture detail.

### Bake Samples

Sets the number of Cycles samples used for baking.

Higher values can reduce noise but make baking slower.

### Bake Margin

Adds pixel padding around baked UV islands.

This helps reduce visible seams and texture bleeding.

### Bake Base Color

Enables base color baking.

This transfers the main color appearance of the original scan.

### Bake Normal

Enables normal map baking.

Normal maps help preserve surface detail without keeping all the original geometry.

If the high-poly material already has a linked normal texture, ScanReady transfers that texture to the new low-poly UV layout.

If no linked normal texture is found, ScanReady falls back to a geometric high-to-low normal bake.

### Bake Roughness

Enables roughness map baking.

Use this when the high-poly material has a roughness texture or a bakeable roughness input that should be transferred to the low-poly final material.

The roughness map is saved as a technical texture and linked to the **Roughness** input of the final material.

Linked roughness textures are transferred to the new UV layout when available.

### Bake Occlusion

Enables Ambient Occlusion baking.

AO can add depth and contact shadow information to the final material.

### AO Source

Controls whether AO is baked from the high-poly source to the lowpoly target, or calculated from the lowpoly mesh only.

### AO Auto Distance

Automatically calculates AO distance from model size.

### AO Distance

Manual AO ray distance when automatic distance is disabled.

### AO Samples

Controls Ambient Occlusion bake quality.

Higher values are cleaner but slower.

### Normal Strength

Controls the strength of the Normal Map node on the final material.

This changes how strongly the normal map appears in Blender.

---

## Output Settings

These settings control how baked images are saved.

### Save Images

Saves baked textures to disk.

Enable this when you need texture files for export, delivery, game engines, or archives.

### Image Format

Chooses the output image format.

Available formats:

- **JPG** for compact color textures.
- **PNG** for lossless output.
- **TIFF** for high precision workflows.

### JPG Quality

Controls JPG compression quality.

Higher values preserve more image detail but create larger files.

### TIFF 16-bit

Saves TIFF textures with higher precision.

This can be useful for close-up assets, detailed normal maps, or archival workflows.

### Output Folder

Sets the folder where baked images are saved.

Relative paths such as `//bake/` are saved next to the current Blender file.

---

## Presets

ScanReady 1.0 can save, load, and delete named presets.

Presets store the current workflow settings so you can reuse them later.

Use presets when processing multiple scans with similar requirements, such as:

- A batch of VR assets.
- A set of game props.
- Museum objects with similar resolution targets.
- Repeated bake settings.
- A standard studio workflow.

Presets help keep results consistent across multiple assets.

---

## Progress and Status

The panel includes workflow status and global progress.

During One Click Bake, ScanReady 1.0 reports the active phase:

- Preview.
- UV Mapping.
- Cage.
- Bake.

This helps you understand what the addon is doing during long operations.

---

## Memory Safety

Large scans can be demanding during baking.

These options help reduce the chance of memory-related failures.

### Safe Memory Bake

Uses a safer bake workflow designed to reduce memory pressure on heavy scenes and large scans.

Leave this enabled when working with dense scans or high texture resolutions.

### Force CPU Baking

Forces baking on CPU to avoid GPU memory issues.

This is usually slower, but it can be safer on systems with low VRAM.

ScanReady 1.0 keeps this disabled by default for a single material bake.

When **Bake Materials** is set to `2` or more, it is enabled automatically. This is a conservative safety choice for heavier multi-material bakes.

---

## Practical Advice

For VR, videogames, and realtime assets, always balance quality and performance.

Use advanced settings to find the right compromise between:

- Mesh density.
- Texture resolution.
- Bake quality.
- File size.
- Viewport performance.
- Realtime performance.

The goal is not to keep every polygon from the original scan.

The goal is to preserve the visual identity of the scan in a lighter asset that is easier to use.
