# Step 1 - Preview / Reduce

Step 1 creates an optimized lowpoly preview from the selected high-poly scan.

This is the first important step when preparing a scanned object for **VR, AR, videogames, realtime visualization, or interactive scenes**. A raw scan can contain a very high number of polygons, making it difficult to move, preview, export, or use in realtime.

ScanReady 1.0 first cleans common scan debris, then reduces the model while keeping the overall shape and visual identity of the original scan.

This cleanup can remove loose polygons, floating fragments, isolated vertices, and small unwanted mesh artifacts before the lowpoly preview is generated.

<div style="width:100%; text-align:left;">
  <img src="../img/step1-reduce.gif" alt="ScanReady 1.0 Optimize Reduce control updating the lowpoly preview density" style="max-width:820px;width:100%;">
</div>

---

## Why This Step Matters

High-poly scans are often too heavy for direct use.

They may cause:

- Slow viewport performance.
- Heavy Blender scenes.
- Difficult exports.
- Poor realtime performance.
- VR assets that are too dense to display smoothly.
- Game objects that are too expensive for production.

The Preview / Reduce step gives you a lighter version of the scan before continuing with UVs and baking.

It also helps remove small pieces of mesh dirt that can come from photogrammetry or 3D capture, such as loose polygons, isolated vertices, and floating fragments.

---

## Main Settings

<div style="display:flex; flex-wrap:wrap; gap:28px; align-items:flex-start;">

<div style="flex:1 1 360px; min-width:260px;">

<h3>Final Faces</h3>

<p>
Sets the target face count for the optimized lowpoly mesh.
</p>

<p>
Use a lower value for lightweight VR or game assets. Use a higher value when the object has important silhouette detail.
</p>

<h3>Optimize / Reduce</h3>

<p>
Controls the reduction strength.
</p>

<p>
Lower values create a stronger reduction and a lighter object. Higher values preserve more geometry.
</p>

<h3>Reduction</h3>

<p>
Shows the current reduction percentage based on the selected optimization settings.
</p>

</div>

<div style="flex:0 0 320px; text-align:center;">
  <img src="../img/step1-preview-reduce.png" alt="ScanReady 1.0 Step 1 Preview Reduce panel with Create Lowpoly Preview button" style="width:320px; max-width:100%;">
</div>

</div>

## View Options

<div style="display:flex; flex-wrap:wrap; gap:28px; align-items:flex-start;">

<div style="flex:1 1 360px; min-width:260px;">

<h3>Show Wireframe</h3>

Displays the topology of the preview object.

Use it to check whether the mesh is still too dense or has been reduced too much.

</div>

<div style="width:100%; text-align:left;">
  <img src="../img/step1-wireframe.gif" alt="ScanReady 1.0 Show Wireframe preview on an optimized scan" style="max-width:820px;width:100%;">
</div>

</div>

<h3>Show Checker</h3>

Displays a checker texture.

This helps inspect UV density and distortion during later checks.

<div style="width:100%; text-align:left;">
  <img src="../img/step1-checker.gif" alt="ScanReady 1.0 Show Checker preview on an optimized scan" style="max-width:820px;width:100%;">
</div>

<h3>Use Texture View</h3>

Shows the model in a flat texture-oriented view without scene lighting.

This is useful when inspecting baked or previewed texture results.

<div style="width:100%; text-align:left;">
  <img src="../img/step1-use-texture-view.gif" alt="ScanReady 1.0 Use Texture View preview on an optimized scan" style="max-width:820px;width:100%;">
</div>

<h3>Checker Mix / Checker Scale</h3>

<div style="display:flex; flex-wrap:wrap; gap:28px; align-items:flex-start; margin-bottom:24px;">

<div style="flex:1 1 360px; min-width:260px;">

<p>
<strong>Checker Mix</strong> controls how strongly the checker overlay appears on the model.
</p>

<p>
<strong>Checker Scale</strong> changes the size of the checker squares.
</p>

<p>
Smaller squares make UV stretching and distortion easier to notice. Larger squares are useful for a quick general check.
</p>

</div>

<div style="flex:0 0 320px; text-align:center;">
  <img src="../img/step1-checker-mix-scale.png" alt="ScanReady 1.0 Checker Mix and Checker Scale controls" style="width:320px; max-width:100%;">
</div>

<div style="width:100%; text-align:left; margin-bottom:20px;">
  <img src="../img/step1-checker-mix.gif" alt="ScanReady 1.0 Checker Mix control adjusting checker overlay strength" style="max-width:820px;width:100%;">
  <p style="font-size:0.9em; opacity:0.75; margin-top:6px;">
    Checker Mix adjusts how visible the checker overlay is on top of the model surface.
  </p>
</div>



<div style="width:100%; text-align:left; margin-bottom:20px;">
  <img src="../img/step1-checker-scale.gif" alt="ScanReady 1.0 Checker Scale control changing checker square size" style="max-width:820px;width:100%;">
  <p style="font-size:0.9em; opacity:0.75; margin-top:6px;">
    Checker Scale changes the size of the checker pattern to make UV stretching easier to inspect.
  </p>
</div>

</div>

---

## Action

Click **Create Lowpoly Preview**.

ScanReady 1.0 cleans the selected high-poly scan, removes common mesh noise such as loose polygons or isolated vertices, then creates an optimized preview object.

<div style="width:100%; text-align:left;">
  <img src="../img/step1-cleaner.gif" alt="ScanReady 1.0 mesh cleanup before lowpoly preview" style="max-width:820px;width:100%;">
</div>

When the preview looks correct, continue to:

[Step 2 - UV / Cage](step2.md)

---

## What to Check

After creating the preview, inspect:

- The overall silhouette.
- Important edges and shape details.
- Polygon density.
- Wireframe readability.
- Whether the scan is now light enough for the target use.
- Whether too much visual information was lost.

If the preview is too heavy, reduce it more.

If the preview loses important shape, increase the target density and create it again.

---

## Practical Advice for VR and Games

For VR and videogame workflows, the goal is not only to make the model look good.

The model must also be light enough to run smoothly.

A good preview should:

- Keep the recognizable shape of the original scan.
- Remove unnecessary scan density.
- Be easier to orbit and inspect in Blender.
- Be suitable for UV generation.
- Be ready for texture baking in the next steps.
