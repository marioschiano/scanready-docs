# Step 3 - Bake / Output

<p align="center">
  <img src="../img/high-to-low-workflow.png" alt="Baked scan result with reduced polygon count and preserved visual detail" style="max-width:900px;width:100%;">
</p>

<p align="center">
<b>High-poly scan → optimized lowpoly mesh → baked realtime-ready asset.</b>
</p>

---

Step 3 transfers texture detail from the original high-poly scan onto the optimized mesh.

This is the final stage of the ScanReady workflow, transforming the lowpoly object into a lighter realtime-ready asset for:

- VR
- Videogames
- AR
- Realtime visualization
- Interactive environments

The goal is to preserve much of the original scan appearance while dramatically reducing polygon density.

---

## Why Baking Matters

A raw scan often stores detail through extremely heavy geometry.

While visually impressive, this is not always practical for realtime use.

Baking transfers visual information from the high-poly scan into texture maps on the optimized mesh.

This allows the final asset to use:

- Fewer polygons
- Lighter geometry
- Texture-based detail
- More manageable assets
- Better realtime performance

Instead of rendering millions of polygons in realtime, ScanReady transfers surface detail into textures.

This allows the optimized mesh to remain lightweight while still preserving much of the original scan appearance.

---

## Texture Settings

### Texture Size

Sets the output resolution for baked textures.

Higher values preserve more detail but increase bake time, memory usage, and file size.

Common choices:

- `1024` → lightweight assets
- `2048` → general-purpose assets
- `4096` → close-up or high-detail assets
- `8192` → very large or archival-quality assets

Higher resolutions increase memory usage significantly.

<!-- Replace placeholder with ../img/step3-texture-size-comparison.png -->
<p align="center">
  <img src="../img/placeholder-image.svg" alt="Texture resolution comparison placeholder" style="max-width:1100px;width:100%;">
</p>

---

### Bake Materials

Splits the bake into multiple material groups.

Using more materials increases available texture space and can preserve more detail on large scans.

<!-- Replace placeholder with ../img/step3-material-count.png -->
<p align="center">
  <img src="../img/placeholder-image.svg" alt="Bake material count comparison placeholder" style="max-width:1100px;width:100%;">
</p>

| Materials | Typical Use |
|---|---|
| 1 Material | Lightweight assets |
| 2 Materials | Medium detail preservation |
| 4 Materials | Large scans and high-detail assets |

Increasing polygon density alone is not always the best solution.

In many cases, increasing the number of bake materials produces cleaner and sharper textures while keeping the mesh lightweight.

When **Bake Materials** is set to more than `1`, ScanReady 1.0 automatically enables **Force CPU Baking** as a safer default for multi-material workflows.

You can still disable it manually if your GPU can handle the bake safely.

---

## Texture Detail

The **Texture Detail** box helps estimate whether the current bake setup is likely to preserve enough texture detail.

Click **Analyze Texture Detail** after generating UVs.

ScanReady searches for the matching high-poly source and optimized UV mesh, then compares the original texture usage with the current bake setup.

It reports a compact **Detail Match** estimate and recommends whether the current texture size and material count are balanced.

<!-- Replace placeholder with ../img/step3-texture-detail.png -->
<p align="center">
  <img src="../img/placeholder-image.svg" alt="Texture Detail analysis placeholder" style="max-width:1000px;width:100%;">
</p>

This is useful when deciding whether to:

- Keep one baked material
- Increase **Bake Materials**
- Raise or lower **Texture Size**
- Improve UV packing before baking

If ScanReady cannot find a matching high-to-UV pair automatically, it falls back to analyzing the active mesh.

---

## Cage Check Before Bake

Before baking, check that the cage fully covers the high-poly scan surface.

If the cage is too small, bake rays may miss details and produce black areas, empty details, or incorrect projections.

Use **Auto Cage Extrusion** for a quick starting point, then adjust **Cage Extrusion** manually if some areas still need coverage.

Use the smallest cage value that captures the scan details without projecting onto unwanted nearby surfaces.

---

### Bake Samples

Controls Cycles bake samples.

Higher values can reduce noise, especially for Ambient Occlusion, but they also increase bake time.

---

### Bake Margin

Adds extra pixel padding around baked UV islands.

This helps reduce visible seams and texture bleeding.

---

## Bake Maps

### Bake Base Color

Bakes the diffuse or color information from the original scan.

This is usually the most important texture for preserving the appearance of the captured object.

---

### Bake Normal

Bakes a normal map.

Normal maps preserve the appearance of surface detail without keeping the original high-poly geometry.

This is especially useful for VR and videogame assets where geometry must remain lightweight.

If the original high-poly material already contains a linked normal map, ScanReady transfers that normal texture onto the new UV layout.

If no linked normal map is found, ScanReady performs a geometric high-to-low normal bake.

Normal textures are treated as **Non-Color** technical data.

---

### Bake Roughness

Bakes or transfers roughness information from the high-poly material.

Use this when the original material already contains roughness information that should be preserved on the final lowpoly asset.

Roughness textures are also handled as **Non-Color** technical data.

---

### Bake Occlusion

Bakes an Ambient Occlusion map.

AO can help add contact shadows and surface depth to the final material.

---

<!-- Replace placeholder with ../img/step3-bake-maps.png -->
<p align="center">
  <img src="../img/placeholder-image.svg" alt="Bake maps screenshot placeholder" style="max-width:1100px;width:100%;">
</p>

---

### AO Source

Controls how Ambient Occlusion is generated.

You can bake AO from the high-poly source or calculate it directly from the lowpoly mesh.

---

### AO Auto Distance

Automatically estimates the AO distance from the overall model size.

---

### AO Distance

Controls AO ray distance manually when automatic distance is disabled.

---

### AO Samples

Controls Ambient Occlusion bake quality.

Higher values produce cleaner AO but increase bake time.

---

### Normal Strength

Controls the strength of the Normal Map node in the final material.

This affects the material appearance, not the baked normal texture itself.

---

## Output Settings

### Save Images

Saves baked textures to disk.

Enable this when exporting assets for game engines, archives, external workflows, or delivery.

---

### Image Format

Available output formats:

- **JPG** → compact Base Color textures
- **PNG** → lossless texture output
- **TIFF** → higher precision workflows

PNG is generally recommended for most realtime workflows.

---

### JPG Quality

Controls JPG compression quality.

Higher values preserve more image detail but generate larger files.

---

### TIFF 16-bit

Saves TIFF textures with higher precision.

Useful for high-detail assets, archival workflows, or detailed normal maps.

---

### Output Folder

Defines where baked textures are saved.

Relative paths such as `//bake/` are saved next to the current Blender file.

---

## Memory Safety

Large photogrammetry scans can easily exceed GPU memory limits during baking.

ScanReady includes safer bake workflows designed for heavy production scenes.

<!-- Replace placeholder with ../img/step3-memory-safety.png -->
<p align="center">
  <img src="../img/placeholder-image.svg" alt="Safe memory bake settings placeholder" style="max-width:1000px;width:100%;">
</p>

---

### Safe Memory Bake

Uses a safer baking workflow designed to reduce memory pressure on heavy scenes and large scans.

---

### Force CPU Baking

Forces baking on the CPU to avoid GPU memory limitations.

This is usually slower, but it can be safer on systems with limited VRAM.

By default, **Force CPU Baking** remains disabled for single-material bakes.

When **Bake Materials** is set to `2` or more, ScanReady automatically enables it because multi-material workflows require more memory and additional bake passes.

The user can still disable it manually.

---

## Action

Click **Bake Textures** to start the bake.

Large scans may require several minutes depending on:

- Texture resolution
- Material count
- Bake settings
- Hardware performance

When the bake is complete, inspect the final material and the saved textures inside the output folder.

---

## What to Check

After baking, inspect:

- Base Color texture
- Normal Map
- Ambient Occlusion map
- Texture sharpness
- Texture seams
- Missing details
- Incorrect projections
- Final material appearance
- Saved output files

If details are missing, adjust the cage extrusion or increase texture resolution before baking again.

---

## Realtime Optimization

<!-- Replace placeholder with ../img/step3-final-result.png -->
<p align="center">
  <img src="../img/placeholder-image.svg" alt="Final baked realtime-ready asset placeholder" style="max-width:1100px;width:100%;">
</p>

For realtime workflows, the final result should balance visual quality and performance.

A good baked asset should:

- Use a lightweight mesh
- Preserve the recognizable appearance of the original scan
- Use textures to carry surface detail
- Be easier to export
- Be easier to render in VR and game engines
- Avoid unnecessary geometry density

The bake is what allows a lightweight optimized mesh to preserve much of the visual richness of the original high-poly scan.
