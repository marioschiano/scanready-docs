# Troubleshooting

This page covers common ScanReady 1.0 workflow issues and provides solutions for baking, UVs, optimization, memory usage, and realtime preparation.

Scan processing can be demanding because high-poly scans, texture baking, UV generation, and memory usage all depend on the source model and system hardware.

---

## The ScanReady 1.0 Panel Does Not Appear

Check the following:

- Make sure the addon is enabled in **Edit > Preferences > Add-ons**
- Make sure you are in the **3D Viewport**
- Press **N** to open the Sidebar
- Look for the **Scan Ready** tab
- Restart Blender after enabling the addon

---

## One Click Bake Does Not Start

Make sure:

- A mesh object is selected
- The selected object is the high-poly scan you want to process
- Blender is in Object Mode
- The object is visible and not hidden
- The scene is not currently running another modal operation

If needed, save the file, restart Blender, and try again.

---

## The Preview Mesh Is Too Heavy

If the optimized preview is still too dense:

- Lower **Final Faces**
- Lower **Optimize / Reduce**
- Increase cleanup only carefully
- Create the lowpoly preview again

For VR and videogame assets, the mesh should remain light enough to orbit, inspect, and export comfortably.

---

## The Preview Mesh Lost Too Much Detail

If the optimized preview looks too simplified:

- Increase **Final Faces**
- Increase **Optimize / Reduce**
- Avoid reducing very thin or delicate objects too aggressively
- Create the preview again

For important silhouettes, keep enough geometry to preserve the shape.

---

## UVs Look Stretched

If the checker pattern shows strong stretching:

- Try a different UV method
- Lower or raise **Smart UV Angle**
- Increase UV island separation with **UV Padding**
- Use a more detailed UV preset
- Generate UVs again

Clean UVs are important for good baked textures.

---

## The Bake Misses Details

If parts of the scan detail are missing in the baked texture:

- Increase **Cage Extrusion** slightly
- Use **Auto Cage Extrusion**
- Enable **Show Cage** and inspect the cage
- Increase **Texture Size** if the bake is too low resolution
- Make sure the original high-poly object is still available

Use the smallest cage value that captures the details cleanly.

---

## The Bake Captures Wrong Areas

If the bake includes details from the wrong part of the model:

- Reduce **Cage Extrusion**
- Inspect the cage preview
- Make sure objects are not overlapping
- Hide or move unrelated objects if needed
- Bake again

A cage that is too large can project unwanted nearby surfaces.

---

## The Bake Looks Blurry or Low Quality

Bake quality depends on several factors:

- Texture resolution
- Polygon density
- UV space usage
- Number of materials

### Increase Texture Resolution

Try increasing the texture resolution first.

Example:

- 1024 → low detail
- 2048 → standard quality
- 4096 → high quality
- 8192 → very high detail

Higher resolutions increase memory usage.

### Increase Polygon Density

If the optimized mesh is too aggressive, important details may be lost before baking.

Try:

- Increasing **Final Faces**
- Using a less aggressive **Optimize / Reduce** value

### Use Multiple Materials

If increasing texture resolution is still not enough, the asset may require multiple materials.

Each material receives its own texture space, allowing much higher detail preservation across the model.

Increasing polygon density alone is not always the best solution.

Very dense meshes can become heavier to process, slower to bake, and more difficult to use in realtime applications.

For this reason, ScanReady can recommend an appropriate number of bake materials depending on the complexity and size of the scan.

Example:

- 1 material → lower texture detail
- 2 materials → improved texture quality
- 4 materials → significantly higher texture detail

Using multiple materials is often a better solution than simply increasing polygon density.

This is especially useful for:

- Large scans
- Environment assets
- Museum objects
- Complex photogrammetry assets
- Fine surface details

---

## Textures Are Not Saved

Check:

- **Save Images** is enabled
- **Output Folder** is valid
- The Blender file has been saved if you use a relative path like `//bake/`
- You have permission to write in the selected folder
- The bake completed successfully

Relative paths are saved next to the current `.blend` file.

---

## The Bake Is Very Slow

Baking can be slow with large scans or high resolution textures.

To speed it up:

- Lower **Texture Size**
- Lower **Bake Samples**
- Reduce the number of bake materials if possible
- Disable maps you do not need
- Use a smaller final mesh when appropriate

High resolution Normal and AO maps can increase bake time.

---

## Blender Runs Out of Memory

Large scans can use a lot of memory during baking.

Try:

- Enable **Safe Memory Bake**
- Enable **Force CPU Baking** if GPU memory is limited
- Lower **Texture Size**
- Lower the number of bake materials
- Close other heavy applications
- Save and restart Blender before baking

Force CPU Baking is usually slower, but it can be safer on low VRAM systems.

ScanReady 1.0 automatically enables **Force CPU Baking** when the number of bake materials is set to `2` or more.

For single-material baking, GPU baking can still be used when available.

---

## Normal Map Looks Too Strong or Too Weak

Adjust **Normal Strength**.

This changes the strength of the Normal Map node in the final material.

It affects the material appearance, not the baked normal image itself.

If the original high-poly material has a linked normal texture, ScanReady transfers that normal map to the new UV layout.

If no normal texture is linked, ScanReady generates the normal information from the high-poly geometry.

---

## Roughness Information Is Missing

ScanReady can only transfer roughness information when the original high-poly material already contains a roughness texture or usable roughness input.

If no roughness information exists in the original material, no roughness transfer can be generated automatically.

Check the original material node tree and verify that roughness information is available before baking.

---

## Ambient Occlusion Looks Too Dark

Try:

- Lowering AO strength in your final material
- Reducing **AO Distance** if automatic distance is disabled
- Using more controlled AO settings
- Checking whether the AO source is appropriate for the asset

AO should add depth, not hide scan details.

---

## Best First Fix

If the result is not good, use this order:

1. Check the lowpoly preview
2. Check UVs with the checker view
3. Check the cage preview
4. Bake only Base Color first
5. Add Normal, Roughness, and AO after the Base Color works
6. Increase texture resolution only when the workflow is correct

This makes problems easier to isolate.
