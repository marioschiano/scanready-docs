# Step 1 - Preview / Reduce

Create a lightweight, optimized preview from the high-poly scan.

Processing time depends on scan density and computer performance: a scan with millions of polygons can take around a minute or more on a mid-range PC.

<div style="width:100%; text-align:left;">
  <img decoding="async" fetchpriority="high" src="../img/step1-reduce.gif" alt="ScanReady Optimize Reduce control updating low-poly preview density" style="max-width:820px;width:100%;">
</div>

<p style="font-size:0.9em; opacity:0.75; margin-top:6px;">Optimize / Reduce controls how much geometry is kept in the low-poly preview. The default value of 0.10 creates a preview with approximately 90% fewer polygons.</p>

---

## Adaptive Optimization

Optimization is not applied uniformly across the whole model.

ScanReady preserves important surface detail while simplifying flat or less detailed regions more aggressively.

This helps create cleaner, more efficient low-poly assets for realtime workflows.

### Adaptive Reduce

Adaptive Reduce is enabled by default and helps ScanReady distribute polygon reduction more intelligently across the scan.

Instead of treating every surface alike, it allows flat areas to be reduced more and protects regions where surface detail is more important.

This is the main difference between a simple Blender Decimate pass and the ScanReady workflow. Standard decimation can reduce useful edges and noisy flat regions with the same priority. ScanReady first creates adaptive weights, then uses them to reduce broad surfaces more aggressively while better protecting strong normal changes, silhouettes, edges and important shape transitions.

### Viewing Adaptive Weights

The same model can be displayed with its normal material or in **Show Adaptive Reduction** mode. Colors show where ScanReady tends to protect detail and where it can reduce geometry more aggressively.

<div class="sr-uv-compare" data-uv-compare>
  <div class="sr-uv-compare__image">
    <img loading="lazy" decoding="async" src="../img/adaptive-original.png" alt="Original textured scan" class="sr-uv-compare__base">
    <div class="sr-uv-compare__overlay">
      <img loading="lazy" decoding="async" src="../img/adaptive-weights.png" alt="Adaptive Reduce weights displayed in color" class="sr-uv-compare__top">
    </div>
    <span class="sr-uv-compare__label sr-uv-compare__label--left">Original scan</span>
    <span class="sr-uv-compare__label sr-uv-compare__label--right">Adaptive reduction</span>
    <span class="sr-uv-compare__adaptive-gradient" aria-label="Adaptive weight gradient from minimum to high reduction"><span class="sr-uv-compare__adaptive-gradient-bar"></span><span class="sr-uv-compare__adaptive-gradient-labels"><span>Minimum reduction</span><span>Medium reduction</span><span>High reduction</span></span></span>
    <button class="sr-uv-compare__handle" type="button" aria-label="Compare the original scan and Adaptive Reduce weights" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50"><span></span></button>
  </div>
</div>

<p align="center" style="font-size:0.9em; margin-top:10px;"><strong>Blue:</strong> preserved detail. <strong>Red:</strong> greater polygon reduction.</p>
<p align="center"><strong>Move the slider to compare the scan and the distribution of adaptive weights.</strong></p>

### Geometry Comparison

<div class="sr-uv-compare" data-uv-compare>
  <div class="sr-uv-compare__image">
    <img loading="lazy" decoding="async" src="../img/step1-decimate-wireframe.png" alt="Wireframe of the scan reduced with Blender Decimate without Adaptive Reduce" class="sr-uv-compare__base">
    <div class="sr-uv-compare__overlay">
      <img loading="lazy" decoding="async" src="../img/step1-adaptive-wireframe.png" alt="Wireframe of the scan reduced with ScanReady Adaptive Reduce" class="sr-uv-compare__top">
    </div>
    <span class="sr-uv-compare__label" style="left:50%; transform:translateX(-50%); white-space:nowrap;">101,177 faces</span>
    <span class="sr-uv-compare__material sr-uv-compare__material--left" style="top:auto; bottom:12px; left:25%; transform:translateX(-50%); min-width:0; width:46%; white-space:normal;">Blender Decimate</span>
    <span class="sr-uv-compare__material sr-uv-compare__material--right" style="top:auto; bottom:12px; left:75%; transform:translateX(-50%); min-width:0; width:46%; white-space:normal;">ScanReady Adaptive Reduce</span>
    <button class="sr-uv-compare__handle" type="button" aria-label="Compare Blender Decimate and ScanReady Adaptive Reduce" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50"><span></span></button>
  </div>
</div>

<p align="center"><strong>Move the slider to compare the distribution of geometry.</strong></p>

At the same face count, Adaptive Reduce tends to reduce flat surfaces more aggressively while retaining more geometry in areas with reliefs, edges and decorations. ScanReady uses Blender Decimate, guiding its reduction with adaptive weights.

Use an Adaptive Reduce preset as a quick starting point:

- **Balanced** for most scans and general realtime assets.
- **Preserve Details** when the scan contains important folds, sculptural forms, engravings or close-up details.
- **Flat Surfaces** when the object contains broad simple areas that can be simplified more aggressively.

Keep **Adaptive Method** on **Best Quality** for normal work. **Legacy** retains the original Adaptive Reduce calculation for compatibility with older projects.

<p align="center">
  <img loading="lazy" decoding="async" src="../img/step1-blender-decimate-vs-scanready.jpg" alt="Comparison between the original high-poly scan and the low-poly result optimized by ScanReady" style="max-width:1000px;width:100%;">
</p>
<p align="center">
  <b>Blender Decimate vs ScanReady Adaptive Reduce</b><br>
  <span style="font-size:0.9em; opacity:0.75;">Illustrative comparison in preparation: same scan and similar final density.</span>
</p>

## Performance Improvement

Heavy scans can quickly become difficult to manage in Blender.

### Example

- Original scan: over 1 million polygons.
- Possible test target: 20,000 polygons.

This is an example, not a guaranteed result: choose the target based on silhouette, viewing distance and target platform.

This helps improve viewport responsiveness and makes the asset easier to process in realtime workflows.

---

## Separate Preview and High-poly Source

Reduction is applied to a **separate preview**, while the high-poly mesh remains available as the bake source.

!!! warning "Keep a copy of the original scan"
    Preparation can modify the source: apply scale, combine parts, correct normals, remove sharp markings or fragments and convert materials, depending on enabled options.

    Save a copy of the `.blend` file before Step 1, especially if you need an archival original.

---

## Why Reduction Matters

High-poly scans are often too heavy for direct use.

They can cause:

- slow viewport performance;
- heavy Blender scenes;
- difficult exports;
- poor realtime performance;
- VR assets too dense to display smoothly;
- game objects too heavy and difficult to manage in production.

Preview / Reduce creates a lighter version of the scan before continuing with UVs and baking.

It also helps remove small mesh artifacts generated by photogrammetry or 3D capture, such as detached polygons, isolated vertices and floating fragments.

---

Step 1 creates an optimized low-poly preview from the selected high-poly scan.

This is the first important step when preparing a scanned object for **VR, AR, video games, realtime visualization or interactive scenes**.

ScanReady first cleans common unwanted scan fragments, then reduces the model while preserving the original scan's overall shape and visual identity.

---

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:28px; align-items:flex-start; margin-top:24px; margin-bottom:28px;">
<div style="flex:1 1 320px; min-width:260px;">
<h3>Optimize / Reduce</h3>
<p>The default value is <strong>0.10</strong>.</p>
<p>It keeps approximately <strong>10% of the original polygons</strong>, creating a lighter low-poly preview with approximately <strong>90% fewer polygons</strong>.</p>
<p>After clicking <strong>Create Lowpoly Preview</strong>, you can still adjust this value to try lighter or more detailed results.</p>
<p>Very dense scans with millions of polygons may still take time to process.</p>
<p>Realtime updates depend on scan complexity and Blender performance.</p>
</div>
<div style="flex:0 0 360px; text-align:center;">
  <p style="margin-top:0;"><strong>Optimize / Reduce</strong></p>
  <img loading="lazy" decoding="async" src="../img/step1-slider_reduce.gif" alt="ScanReady Optimize Reduce slider updating the low-poly preview value" style="width:360px; max-width:100%;">
</div>
</div>

---

## Main Settings

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:28px; align-items:flex-start;">
<div style="flex:1 1 360px; min-width:260px;">
<h3>Final Faces</h3>
<p>Sets the target face count for the optimized low-poly mesh.</p>
<p>Use lower values for lightweight VR or game assets.</p>
<p>Use higher values when the object needs to retain more silhouette detail.</p>
<h3>Optimize / Reduce</h3>
<p>Controls how much ScanReady reduces the selected high-poly scan.</p>
<p>The default value is <strong>0.10</strong>, which keeps approximately <strong>10% of the original polygons</strong>.</p>
<p>Lower values produce lighter assets.</p>
<p>Higher values preserve more shape detail.</p>
<h3>Reduction</h3>
<p>Shows the current reduction percentage based on the selected optimization settings.</p>
</div>
<div style="flex:0 0 320px; text-align:center;">
  <p style="margin-top:0;"><strong>Create Lowpoly Preview</strong></p>
  <img loading="lazy" decoding="async" src="../img/step1-preview-reduce_optimize.png" alt="ScanReady Step 1 Preview Reduce panel with Create Lowpoly Preview button" style="width:320px; max-width:100%;">
</div>
</div>

---

## View Options

<div style="float:right; width:320px; max-width:42%; margin:0 0 18px 28px; text-align:center;">
  <p style="margin-top:0;"><strong>View Options</strong></p>
  <img loading="lazy" decoding="async" src="../img/step1-preview-view options.jpg" alt="ScanReady View Options panel with Show Wireframe and Show Checker" style="width:100%; max-width:100%;">
</div>

In the current ScanReady panel, **Show Wireframe** and **Show Checker** appear before **STEP 1**.

These preview tools help check topology and UV readability without changing the baking workflow.

<div style="clear:both;"></div>

---

## Show Wireframe

Shows the topology of the preview object.

Use it to check whether the mesh is still too dense or has been reduced too aggressively.

<div style="width:100%; text-align:left;">
  <img loading="lazy" decoding="async" src="../img/step1-wireframe.gif" alt="ScanReady Show Wireframe preview on an optimized scan" style="max-width:820px;width:100%;">
</div>

---

## Show Checker

Shows a checker texture on the preview mesh.

It helps check UV density and texture distortion.

<div style="width:100%; text-align:left;">
  <img loading="lazy" decoding="async" src="../img/step1-checker.gif" alt="ScanReady Show Checker preview on an optimized scan" style="max-width:820px;width:100%;">
</div>

---

## Checker Mix / Checker UV Scale

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:28px; align-items:flex-start; margin-bottom:24px;">
<div style="flex:1 1 360px; min-width:260px;">
<h3>Checker Mix</h3>
<p>Controls how strongly the checker overlay appears on the model's surface.</p>
<h3>Checker UV Scale</h3>
<p>Changes the size of the checker squares.</p>
<p>Smaller squares make UV stretching and distortion easier to see.</p>
<p>Larger squares are useful for quick general checks.</p>
</div>
<div style="flex:0 0 320px; text-align:center;">
  <p style="margin-top:0;"><strong>Checker Mix / Checker UV Scale</strong></p>
  <img loading="lazy" decoding="async" src="../img/step1-checker mix-scale.jpg" alt="ScanReady Checker Mix and Checker UV Scale controls" style="width:320px; max-width:100%;">
</div>
</div>

<div style="width:100%; text-align:left; margin-bottom:20px;">
  <img loading="lazy" decoding="async" src="../img/step1-checker-mix.gif" alt="ScanReady Checker Mix control adjusting checker overlay strength" style="max-width:820px;width:100%;">
</div>
<p style="font-size:0.9em; opacity:0.75; margin-top:6px;">Checker Mix adjusts how visible the checker overlay is on the model's surface.</p>

<div style="width:100%; text-align:left; margin-bottom:20px;">
  <img loading="lazy" decoding="async" src="../img/step1-checker-scale.gif" alt="ScanReady Checker UV Scale control changing checker square size" style="max-width:820px;width:100%;">
</div>
<p style="font-size:0.9em; opacity:0.75; margin-top:6px;">Checker UV Scale changes the checker pattern size to make UV stretching easier to inspect.</p>

---

## When to Recreate the Preview

!!! tip "When to return to Step 1"
    Use **Create Lowpoly Preview** again when you change density or want to test a different reduction.

    If the preview is too heavy or too simplified, adjust **Optimize / Reduce** or **Final Faces** and recreate it.

    You can return to Step 1 at any time. If you are already in Step 2 or Step 3 and decide the model needs to be lighter or more detailed, change reduction settings here, click **Create Lowpoly Preview** again, then generate UVs and bake again.

<div style="width:100%; text-align:left;">
  <img loading="lazy" decoding="async" src="../img/step1-cleaner.gif" alt="ScanReady mesh cleanup before the low-poly preview" style="max-width:820px;width:100%;">
</div>

ScanReady cleans the selected high-poly scan, removes common mesh noise such as detached polygons or isolated vertices, then creates an optimized preview object.

Before the Decimate modifier is added, ScanReady can also perform **Pre-Decimate Merge** cleanup on the duplicated preview mesh. This helps reduce overlapping scan polygons before optimization.

When the preview is correct, continue with:

[Step 2 - UV / Cage](step2.md)

---

## What to Check

After creating the preview, check:

- overall silhouette;
- important edges and shape details;
- polygon density;
- wireframe readability;
- whether the scan is light enough for the target platform;
- whether too much visual information has been lost.

!!! note "Reading the preview"
    If the preview is too heavy, reduce it further.

    If the preview loses important shape details, increase the target density and recreate it.

---

## Realtime Optimization Goals

For VR and video game workflows, the goal is not visual quality alone.

The asset must remain light enough for smooth realtime performance.

A good preview should:

- preserve the recognizable shape of the original scan;
- remove unnecessary scan density;
- improve Blender viewport responsiveness;
- be suitable for UV generation;
- be ready for texture baking in the next step.

---

## Mesh Created at the End of Step 1

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:28px; align-items:center; margin:20px 0 28px;">
<div style="flex:1 1 320px; min-width:260px;">
<p>The mesh created at the end of Step 1 receives the <strong>1_</strong> prefix.</p>
<p><strong>1_MeshName_preview</strong> identifies the optimized preview mesh used as the basis for subsequent steps.</p>
</div>
<div style="flex:0 0 300px; text-align:center;"><img src="../img/outliner-preview.jpg" alt="Step 1 preview mesh in the Outliner" style="width:100%; max-width:300px;" loading="lazy" decoding="async"></div>
</div>

