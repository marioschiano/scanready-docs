# Step 3 - Bake / Output

<p align="center"><img src="../img/high-to-low-workflow.jpg" alt="Baked scan with reduced polygons and preserved visual detail" style="max-width:900px;width:100%;" decoding="async" fetchpriority="high"></p>
<p align="center"><b>High-poly scan -> optimized low-poly mesh -> baked realtime-ready asset.</b></p>

---

Step 3 transfers texture detail from the original high-poly scan to the optimized mesh.

It is the final stage of the ScanReady workflow, turning the low-poly object into a lighter realtime-ready asset for:

- VR
- video games
- AR
- realtime visualization
- interactive environments

The goal is to preserve much of the original scan's appearance while drastically reducing polygon density.

---

## Why Baking Matters

A raw scan often retains detail through extremely heavy geometry. Although visually impressive, it is not always practical for realtime use.

Baking transfers visual information from the high-poly scan into texture maps on the optimized mesh.

This allows the final asset to use:

- fewer polygons;
- lighter geometry;
- texture-based detail;
- more manageable assets;
- better realtime performance.

Instead of rendering millions of polygons in realtime, ScanReady transfers surface detail into textures.

This allows the optimized mesh to remain lightweight while retaining much of the original appearance.

---

## Texture Settings

### Texture Preset / Texture Size

Sets the output resolution of baked textures.

Higher values preserve more detail but increase bake time, memory usage and file size.

Common choices:

- `1024` -> lightweight assets
- `2048` -> general assets
- `4096` -> close-up or high-detail assets
- `8192` -> very large or close-up assets, if memory and source permit

Higher resolutions greatly increase memory usage.

<p align="center"><img src="../img/step3-texture-size-comparison.jpg" alt="Texture resolution comparison" style="max-width:1100px;width:100%;" loading="lazy" decoding="async"></p>

---

### Bake Materials

Divides the bake into multiple material groups.

Using more materials increases available texture space and can preserve more detail on large scans.

<p align="center"><img src="../img/step3-material-count.jpg" alt="Optimization from four 8K materials to a single material for realtime use" style="max-width:1100px;width:100%;" loading="lazy" decoding="async"></p>

| Materials | Typical use |
|---|---|
| 1 material | Lightweight assets |
| 2 materials | Moderate detail preservation |
| 4 materials | Large scans and high-detail assets |

Increasing polygon density alone is not always the best solution.

In many cases, increasing the number of bake materials produces cleaner, sharper textures while keeping the mesh lightweight.

!!! info "Multi-material baking"
    When **Bake Materials** is set to `2` or more, ScanReady automatically enables **Force CPU Baking** as a safer default for multi-material workflows.

    You can still disable it manually if your GPU can safely handle the bake.

---

## Texture Detail Analysis

**Texture Detail** analysis is available in **Advanced**.

Use **Analyze Texture Detail** after generating UVs when you want to estimate whether the current bake setup can preserve enough texture detail.

ScanReady looks for the matching high-poly source and optimized UV mesh, then compares original texture usage with the current bake setup.

It shows **Texture match**, **Detail estimate** and **UV Space**, along with a resolution and material-count recommendation. These are estimates of available detail, not a guarantee of final quality.

<p align="center"><img src="../img/step3-texture-detail.jpg" alt="Comparison of visual detail retained after texture optimization" style="max-width:1000px;width:100%;" loading="lazy" decoding="async"></p>

<div class="sr-uv-compare" data-uv-compare>
  <div class="sr-uv-compare__image">
    <img src="../img/step3-model-high-poly.jpg" alt="Original high-poly model without wireframe" class="sr-uv-compare__base" loading="lazy" decoding="async">
    <div class="sr-uv-compare__overlay"><img src="../img/step3-model-optimized.jpg" alt="ScanReady optimized model without wireframe" class="sr-uv-compare__top" loading="lazy" decoding="async"></div>
    <span class="sr-uv-compare__label sr-uv-compare__label--left">Original model · 1,011,823 faces</span>
    <span class="sr-uv-compare__label sr-uv-compare__label--right">ScanReady optimized · 30,351 faces</span>
    <span class="sr-uv-compare__material sr-uv-compare__material--left"><strong>4 materials</strong><small>8K textures</small></span>
    <span class="sr-uv-compare__material sr-uv-compare__material--right"><strong>1 material</strong><small>8K texture</small></span>
    <button class="sr-uv-compare__handle" type="button" aria-label="Compare the high-poly and ScanReady optimized models" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50"><span></span></button>
  </div>
</div>

<p align="center"><strong>Use the slider to compare the original and optimized models.</strong></p>

<div class="sr-uv-compare" data-uv-compare>
  <div class="sr-uv-compare__image">
    <img src="../img/step3-wireframe-high-poly.jpg" alt="Original high-poly model wireframe" class="sr-uv-compare__base" loading="lazy" decoding="async">
    <div class="sr-uv-compare__overlay"><img src="../img/step3-wireframe-optimized.jpg" alt="ScanReady optimized model wireframe" class="sr-uv-compare__top" loading="lazy" decoding="async"></div>
    <span class="sr-uv-compare__label sr-uv-compare__label--left">Original wireframe · 1,011,823 faces</span>
    <span class="sr-uv-compare__label sr-uv-compare__label--right">Optimized wireframe · 30,351 faces</span>
    <button class="sr-uv-compare__handle" type="button" aria-label="Compare high-poly and optimized wireframes" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50"><span></span></button>
  </div>
</div>

<p align="center"><strong>Use the slider to compare wireframe density before and after optimization.</strong></p>

This is useful when deciding whether to:

- keep a single bake material;
- increase **Bake Materials**;
- raise or lower **Texture Size**;
- improve UV packing before baking.

If ScanReady cannot automatically find a matching high-to-UV pair, it analyzes the active mesh.

---

## Check the Cage Before Baking

!!! warning "Check the cage before baking"
    Before baking, check that the cage completely covers the high-poly scan surface.

    If the cage is too small, bake rays can miss details and produce black areas, missing details or incorrect projections.

    Enable **Show Cage** and inspect the cage preview. Then slightly increase **Cage Extrusion** or use **Auto Cage Extrusion**.

    Use the smallest cage value that captures scan details without projecting unwanted nearby surfaces.

---

## Bake Maps

### Bake Base Color

<div class="sr-doc-row" style="display:grid; grid-template-columns:minmax(0,1fr) 280px; gap:32px; align-items:start; margin-top:16px; margin-bottom:28px;">
<div style="min-width:0;"><p>Bakes diffuse or color information from the original scan.</p><p>Enabled by default, it is usually the most important texture for preserving the captured object's appearance.</p></div>
<div style="text-align:center;"><img src="../img/step3-bake-base-color.png" alt="Bake Base Color enabled in Step 3" style="max-width:100%;width:100%;" loading="lazy" decoding="async"></div>
</div>

---

### Bake Normal Map

<div class="sr-doc-row" style="display:grid; grid-template-columns:minmax(0,1fr) 280px; gap:32px; align-items:start; margin-top:16px; margin-bottom:28px;">
<div style="min-width:0;"><p>Bakes a normal map.</p><p>Normal maps preserve the appearance of surface detail without retaining the original high-poly geometry.</p></div>
<div style="text-align:center;"><img src="../img/step3-bake-normal-map.png" alt="Bake Normal Map enabled in Step 3" style="max-width:100%;width:100%;" loading="lazy" decoding="async"></div>
</div>

This is particularly useful for VR and video game assets where geometry must remain lightweight.

If the original high-poly material already contains a connected normal map, ScanReady transfers that normal texture to the new UV layout.

If no connected normal map is found, ScanReady performs a geometric high-to-low normal bake.

Normal textures are treated as technical **Non-Color** data.

The **Normal Strength** material control is available in **Advanced > Bake Settings** when **Bake Normal Map** is enabled.

---

### Bake Roughness Map

Bakes or transfers roughness information from the high-poly material.

Use it when the original material already contains roughness information that should be preserved on the final low-poly asset.

!!! info "Bake Roughness Map"
    The **Bake Roughness Map** checkbox is shown only when ScanReady finds a connected Roughness input in the high-poly material.

    If the source material has no connected roughness, ScanReady cannot transfer it and the option is not shown.

Roughness textures are also treated as technical **Non-Color** data.

---

### Bake Occlusion Map

<div class="sr-doc-row" style="display:grid; grid-template-columns:minmax(0,1fr) 280px; gap:32px; align-items:start; margin-top:16px; margin-bottom:28px;">
<div style="min-width:0;"><p>Bakes an Ambient Occlusion map.</p><p>AO can help add contact shadows and surface depth to the final material.</p></div>
<div style="text-align:center;"><img src="../img/step3-bake-occlusion-map.png" alt="Bake Occlusion Map enabled in Step 3" style="max-width:100%;width:100%;" loading="lazy" decoding="async"></div>
</div>

The **AO Mix** material control is available in **Advanced > Bake Settings > Occlusion Settings** when **Bake Occlusion Map** is enabled. Its default value is `1.0`, which applies the full baked AO texture to the final material.

---

<p align="center"><img src="../img/step3-bake-maps.jpg" alt="Base Color, Normal, Roughness and Occlusion maps generated on the new UV atlas" style="max-width:1100px;width:100%;" loading="lazy" decoding="async"></p>

---

## Output Settings

### Save Images

Saves baked textures to disk.

Enable it when exporting assets for game engines, archives, external workflows or final delivery.

---

### Open Folder After Bake

<div class="sr-doc-row" style="display:grid; grid-template-columns:minmax(0,1fr) 280px; gap:32px; align-items:start; margin-top:16px; margin-bottom:28px;">
<div style="min-width:0;"><p>Automatically opens the bake folder when <strong>Save Images</strong> is enabled and texture saving is complete.</p><p>Useful for immediately checking generated files, copying them to an external project or bringing them into a game engine.</p></div>
<div style="text-align:center;"><img src="../img/step3-open-folder-after-bake.png" alt="Open Folder After Bake enabled in Step 3" style="max-width:100%;width:100%;" loading="lazy" decoding="async"></div>
</div>

---

### Image Format

Available output formats:

- **JPG** -> compact Base Color textures
- **PNG** -> lossless texture output
- **TIFF** -> higher-precision workflows

PNG is generally recommended for most realtime workflows.

---

### JPG Quality

Controls JPG compression quality.

Higher values preserve more image detail but produce larger files.

---

### TIFF 16-bit

Saves TIFF textures at higher precision.

Useful for high-detail assets, archival workflows or detailed normal maps.

---

### Output Folder

<div class="sr-doc-row" style="display:grid; grid-template-columns:minmax(0,1fr) 280px; gap:32px; align-items:start; margin-top:16px; margin-bottom:28px;">
<div style="min-width:0;">
<p>Defines where baked textures are saved.</p>
<p>Relative paths such as <code>//bake/</code> are saved beside the current Blender file.</p>
<p>When you choose or change the path, ScanReady shows the destination folder in the <strong>Bake Folder</strong> panel. After baking, use the folder button to quickly open the generated files' location.</p>
</div>
<div style="text-align:center;">
  <p style="margin-top:0;"><strong>Output Folder</strong></p>
  <img src="../img/step3-output-folder.png" alt="Output Folder and Bake Folder settings in ScanReady Step 3" style="max-width:100%;width:100%;" loading="lazy" decoding="async">
</div>
</div>

---

### Bake Folder

Step 3 includes the **Bake Folder** panel. Before the first save it may show **No bake folder yet**.

It shows the folder used by the last bake and includes a folder button that opens it directly in the operating system's file browser.

!!! tip "Output Folder and Bake Folder"
    Use **Output Folder** to choose where ScanReady should save textures.

    Use **Bake Folder** after baking to quickly open the folder actually used.

---

## When to Start Baking

Click **Bake Textures** when UVs, cage, texture size, materials and bake maps are ready.

Large scans can take several minutes depending on:

- texture resolution;
- number of materials;
- bake settings;
- hardware performance.

When baking is complete, check the final material and use **Bake Folder** to open the saved textures.

---

## What to Check

After baking, check:

- Base Color texture;
- Normal Map;
- Ambient Occlusion map;
- texture sharpness;
- texture seams;
- missing details;
- incorrect projections;
- final material appearance;
- saved output files;
- that Bake Folder opens the last saved texture folder.

!!! tip "If the bake needs correction"
    If details are missing, enable **Show Cage** and slightly increase **Cage Extrusion** or use **Auto Cage Extrusion**.

    If the bake is too soft or lacks detail, increase texture resolution before baking again.

    If the final mesh is still too heavy, you can return to **Step 1 - Preview / Reduce** even after reaching Step 3. Lower **Final Faces** or **Optimize / Reduce**, click **Create Lowpoly Preview** again, then run **Generate UVs** and **Bake Textures** again. Baking should always use the most recent optimized UV mesh.

---

## Realtime Optimization

<p align="center"><img src="../img/step3-final-result.jpg" alt="Final result: a scan of over one million faces converted to an optimized asset of around twenty thousand faces" style="max-width:1100px;width:100%;" loading="lazy" decoding="async"></p>

For realtime workflows, the final result should balance visual quality and performance.

A good baked asset should:

- use a lightweight mesh;
- preserve the original scan's recognizable appearance;
- use textures to carry surface detail;
- be easier to export;
- be easier to render in VR and game engines;
- avoid unnecessary geometry density.

Baking allows a lightweight optimized mesh to retain much of the original high-poly scan's visual richness.

---

## Final Mesh Created at the End of Step 3

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:28px; align-items:center; margin:20px 0 28px;">
<div style="flex:1 1 320px; min-width:260px;">
<p>The final mesh created in Step 3 receives the <strong>3_</strong> prefix.</p>
<p><strong>3_MeshName_final</strong> identifies the mesh ready for baking and export.</p>
</div>
<div style="flex:0 0 300px; text-align:center;"><img src="../img/outliner-final.jpg" alt="Step 3 final mesh in the Outliner" style="width:100%; max-width:300px;" loading="lazy" decoding="async"></div>
</div>
