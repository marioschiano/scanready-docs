# Troubleshooting

This page covers common ScanReady workflow problems and offers solutions for baking, UVs, optimization, memory usage and realtime preparation.

Processing scans can be demanding because high-poly scans, texture baking, UV generation and memory depend on the source model and hardware.

For support, bug reports or workflow questions, contact:

<a href="mailto:support.marioschiano3d@gmail.com"><strong>support.marioschiano3d@gmail.com</strong></a>

---

## The ScanReady Panel Does Not Appear

Check that:

- the add-on is enabled in **Edit > Preferences > Add-ons**;
- you are in the **3D Viewport**;
- you pressed **N** to open the Sidebar;
- the **Scan Ready** tab exists;
- in some cases Blender needs restarting after enabling the add-on.

---

## One Click Bake Does Not Start

Make sure that:

- a mesh object is selected;
- the selected object is the high-poly scan to process;
- Blender is in Object Mode;
- the object is visible and not hidden;
- the scene is not already running another modal operation.

If necessary, save the file, restart Blender and try again.

---

## The Preview Mesh Is Too Heavy

If the optimized preview is still too dense:

- lower **Optimize / Reduce**;
- lower **Final Faces**;
- increase cleanup only with caution;
- recreate the low-poly preview.

**Optimize / Reduce** and **Final Faces** are linked: both control how lightweight the low-poly preview will be.

For VR and video game assets, the mesh must remain light enough to handle in the viewport, export without problems and use in realtime.

---

## The Preview Mesh Has Lost Too Much Detail

If the optimized preview looks oversimplified:

- increase **Optimize / Reduce**;
- increase **Final Faces**;
- avoid overly aggressive reduction on very thin or delicate objects;
- recreate the preview.

**Optimize / Reduce** and **Final Faces** are linked: both control how much geometric detail is kept in the low-poly preview.

For important silhouettes, keep enough geometry to preserve the shape.

---

## UVs Look Stretched

If the checker pattern shows heavily stretched areas:

- try another **Smart UV Preset** in Step 2;
- lower or raise **Smart UV Angle**;
- check **UV Padding** for separation between islands; padding does not correct stretching within an island;
- use a more detailed UV preset;
- generate UVs again.

Clean UVs are important for good baked textures.

---

## The Bake Loses Details

If parts of the scan's detail are missing from the baked texture:

- enable **Show Cage** and check the cage;
- slightly increase **Cage Extrusion** or use **Auto Cage Extrusion**;
- make sure the cage completely covers the high-poly source;
- increase **Texture Size** if bake resolution is too low;
- make sure the original high-poly object is still available.

!!! tip "Cage adjustment"
    Use the smallest cage value that captures details cleanly.

---

## Why Does the Baked Texture Look Low Quality?

Bake quality depends on:

- texture resolution;
- polygon density;
- UV space usage;
- number of materials.

### Increase Texture Resolution

First try increasing texture resolution.

Example:

- 1024 -> low detail
- 2048 -> standard quality
- 4096 -> high quality
- 8192 -> very high detail

Higher resolutions increase memory usage.

### Increase Polygon Density

If the optimized mesh is reduced too aggressively, important details may be lost before baking.

Try:

- increasing **Final Faces**;
- using a less aggressive **Optimize / Reduce** value.

### Use More Materials

If increasing texture resolution is not enough, the asset may require more materials.

Each material gets its own texture space, allowing much greater preservation of model detail.

Increasing polygon density alone is not always the best solution.

Very dense meshes can be heavier to process, slower to bake and harder to use in realtime applications.

ScanReady can therefore recommend an appropriate number of bake materials based on scan complexity and size.

Example:

- 1 material -> lower texture detail
- 2 materials -> improved texture quality
- 4 materials -> much higher texture detail

Using more materials is often a better solution than simply increasing polygon density.

This is particularly useful for:

- large scans;
- environment assets;
- museum objects;
- complex photogrammetry assets;
- fine surface details.

---

## The Bake Captures the Wrong Areas

If the bake includes details from the wrong part of the model:

- reduce **Cage Extrusion**;
- check the cage preview;
- make sure objects do not overlap;
- hide or move unrelated objects if necessary;
- bake again.

A cage that is too large can project unwanted nearby surfaces.

---

## Textures Are Not Saved

Check that:

- **Save Images** is enabled;
- **Output Folder** is valid;
- the Blender file has been saved if you use a relative path such as `//bake/`;
- you have write permissions for the selected folder;
- the bake completed successfully.

Relative paths are saved beside the current `.blend` file.

After a successful bake, use **Bake Folder** in Step 3 to open the latest texture folder. If the button is not yet visible, first perform a bake with **Save Images** enabled.

---

## Why Is Baking Very Slow?

Baking can be slow with large scans or high-resolution textures.

To speed it up:

- lower **Texture Size**;
- lower **Bake Samples**;
- reduce the number of bake materials if possible;
- disable maps you do not need;
- use a smaller final mesh when appropriate.

High-resolution normal maps and AO can increase bake time.

---

## Blender Runs Out of Memory

Large scans can use a lot of memory during baking.

Try:

- enabling **Safe Memory Bake**;
- enabling **Force CPU Baking** if GPU memory is limited;
- lowering **Texture Size**;
- lowering the number of bake materials;
- closing other demanding applications;
- saving and restarting Blender before baking.

!!! info "CPU and GPU baking"
    Force CPU Baking is usually slower, but can be safer on systems with little VRAM.

    ScanReady automatically enables **Force CPU Baking** when the number of bake materials is set to `2` or more.

    For single-material bakes, GPU baking can still be used when available.

---

## The Normal Map Looks Too Strong or Too Weak

Adjust **Normal Strength**.

It changes the strength of the Normal Map node in the final material.

It affects the material's appearance, not the baked normal image.

If the original high-poly material has a connected normal texture, ScanReady transfers that normal map to the new UV layout.

If no normal texture is connected, ScanReady generates a new normal map by projecting high-poly geometry detail onto the low-poly mesh.

---

## Roughness Information Is Missing

ScanReady can transfer roughness only when the original high-poly material already contains a roughness texture or usable roughness input.

If no roughness information exists in the original material, a roughness transfer cannot be generated automatically.

Check the original material's node tree and make sure roughness information is available before baking.

---

## Ambient Occlusion Is Too Dark

Try:

- lowering **AO Mix** in **Advanced > Bake Settings > Occlusion Settings**;
- reducing **AO Distance** if automatic distance is disabled;
- using more controlled AO settings;
- checking whether the AO source is suitable for the asset.

AO should add depth, not hide scan details.

---

## Why Does the Bake Contain Black or Missing Areas?

If the baked texture contains black areas, missing details or incorrect projections, cage extrusion is usually too small.

In this case some parts of the high-poly scan are not properly reached during baking.

Black areas can also appear when parts of the optimized low-poly mesh lie in front of or behind the high-poly source, so bake rays do not hit the intended surface.

To correct this:

- enable **Show Cage**;
- slightly increase **Cage Extrusion** or use **Auto Cage Extrusion**;
- check the cage around the model before baking;
- make sure the cage completely covers the high-poly source.

The cage must completely surround the high-poly surface.

Green indicates that coverage passes ScanReady's automatic check. Because the check samples the surface, also inspect the bake result in thin, concave or closely spaced areas.

If some areas are still missing, adjust extrusion in small increments and also check normals, UVs and source materials. A cage that is too large can capture unwanted surfaces.

When the cage looks correct, bake again to check whether the missing or black areas are fixed.

!!! tip "Recommended cage value"
    Use the smallest value that completely covers the scan without capturing unwanted nearby surfaces.

---

## When Should I Use Convert Source Materials?

Leave **Convert Source Materials** disabled if baking works correctly. If Base Color is black or incomplete and the cage is correct, check the imported shader and try conversion in **Advanced > Mesh Settings**.

Enable the checkbox, then press **Create Lowpoly Preview** to apply it. Materials that are already standard are preserved; those requiring conversion are rebuilt in a Principled BSDF configuration. Check the result before baking again.

---

## Which Adaptive Reduce Preset Should I Use?

Adaptive Reduce changes how ScanReady distributes mesh reduction across the scan before UVs and baking.

| Preset | Ideal for | Result |
|---|---|---|
| **Balanced** | Most scans | Good general behavior. Try it first. |
| **Preserve Details** | Complex scans with sculptural forms, folds, engravings, damage or small details | Protects important detailed areas more strongly. |
| **Flat Surfaces** | Objects with broad simple surfaces, panels, walls, floors or flat architectural areas | Reduces simple areas more aggressively to save polygons. |

If the optimized preview loses important details, try **Preserve Details** and recreate the preview.

If the preview keeps too much geometry on simple areas, try **Flat Surfaces** and recreate the preview.

For vehicles or hard-surface scans, start with **Balanced**, keep **Protect Feature Edges** enabled and check the silhouette and main panel breaks. Use **Flat Surfaces** if broad panels remain unnecessarily dense.

---

## I Changed Too Many Values and Don't Know How to Go Back

If you changed many settings and the result became difficult to control, use **Reset Defaults**.

This is useful when you have changed several Advanced values, such as Occlusion, Bake, UV, Adaptive Reduce or memory settings, and no longer know which parameter is causing the problem.

**Reset Defaults** returns ScanReady to a clean starting point.

After resetting:

1. Start again with **Balanced** as the Adaptive Reduce preset.
2. Recreate the low-poly preview.
3. Generate UVs again.
4. Check the cage.
5. First perform a simple bake, for example Base Color only.

!!! tip "Enable one control at a time"
    Once the basic workflow works, re-enable the other controls one at a time.

---

## Recommended First Steps

If the result is not good, use this order:

1. Check the low-poly preview
2. Check UVs with the checker view
3. Check the cage preview
4. Bake Base Color only first
5. Add Normal Map, Roughness Map and Occlusion Map after Base Color works
6. Increase texture resolution only when the workflow is correct

!!! note "Why this order helps"
    This makes it easier to isolate problems.
