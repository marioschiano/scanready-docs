# Step 3 - Bake / Output

Step 3 bakes texture information from the original high-poly scan onto the optimized mesh.

This is the final step that turns the simplified object into a more usable asset for **VR, videogames, AR, realtime visualization, and interactive environments**.

The goal is to keep much of the visual detail of the original scan while using a lighter mesh that is easier to render and manage.

<p align="center">
  <img src="img/high-to-low-workflow.png" alt="Baked scan result with reduced polygon count and preserved visual detail" style="max-width:760px;width:100%;">
</p>

---

## Why Baking Matters

A raw scan often carries detail through heavy geometry.

That can be beautiful, but it is not always practical for realtime use.

Baking transfers visual information from the high-poly scan to texture maps on the optimized mesh.

This makes it possible to use:

- A lighter model.
- Fewer polygons.
- Texture-based detail.
- More manageable assets.
- Better performance in realtime workflows.

---

## Texture Settings

### Texture Size

Sets the output resolution for baked maps.

Higher values preserve more detail but increase bake time, memory usage, and file size.

Common choices:

- `1024` for lightweight assets.
- `2048` for general-purpose assets.
- `4096` or higher for close-up assets.

### Bake Materials

Splits the bake into multiple material groups.

Higher values can improve texture detail on large scans, but they also increase bake time and create more output materials.

### Bake Samples

Controls Cycles bake samples.

Higher values can reduce noise, especially for Ambient Occlusion, but they also make baking slower.

### Bake Margin

Adds extra pixel padding around baked UV islands.

This helps reduce visible seams and texture bleeding.

---

## Bake Maps

### Bake Base Color

Bakes the diffuse or color information from the original scan.

This is usually the most important map when preserving the visual appearance of a captured object.

### Bake Normal

Bakes a normal map.

Normal maps help preserve the impression of surface detail without keeping all the original geometry.

This is especially useful for VR and videogame assets, where geometry must stay lighter.

### Bake Occlusion

Bakes an Ambient Occlusion map.

AO can help add contact shadows and depth to the final material.

### AO Source

Controls how Ambient Occlusion is baked.

You can bake AO from the high-poly source to the lowpoly target, or calculate it from the lowpoly mesh only.

### AO Auto Distance

Automatically calculates the AO distance from the size of the model.

### AO Distance

Manual AO ray distance when automatic distance is disabled.

### AO Samples

Controls the quality of the AO bake.

Higher values are cleaner but slower.

### Normal Strength

Controls the strength of the Normal Map node on the final material.

This affects how strongly the normal map appears in the material.

---

## Output Settings

### Save Images

Saves baked textures to disk.

Enable this when you need image files for external workflows, game engines, archives, or delivery.

### Image Format

Available output formats:

- **JPG** for compact base color textures.
- **PNG** for lossless image output.
- **TIFF** for higher precision workflows.

### JPG Quality

Controls JPG compression quality.

Higher values preserve more image detail but create larger files.

### TIFF 16-bit

Saves TIFF textures with higher precision.

This can be useful for detailed normal maps, close-up assets, or archival workflows.

### Output Folder

Defines where baked textures are saved.

Relative paths such as `//bake/` are saved next to the current Blender file.

---

## Memory Safety

### Safe Memory Bake

Uses a safer bake workflow designed to reduce memory pressure on large scans and heavy Blender scenes.

### Force CPU Baking

Forces baking on CPU to avoid GPU memory limits.

This is usually slower, but it can be safer on systems with low VRAM.

---

## Action

Click **Bake Textures** to start the bake.

When the bake is complete, check the final material and the saved texture files in the output folder.

---

## What to Check

After baking, inspect:

- The baked Base Color texture.
- The Normal map if enabled.
- The Ambient Occlusion map if enabled.
- Texture seams.
- Missing details.
- Incorrect projections.
- Final material appearance.
- Saved files in the output folder.

If details are missing, adjust the cage extrusion or texture resolution and bake again.

---

## Practical Advice for VR and Games

For realtime assets, the final result should balance quality and performance.

A good baked asset should:

- Use a lighter mesh.
- Preserve the recognizable appearance of the original scan.
- Use textures to carry visual detail.
- Be easier to export.
- Be easier to render in VR or game engines.
- Avoid unnecessary geometry density.

The bake is what allows the optimized model to look detailed without keeping the full high-poly scan.
