# Manual Quick Guide

Use this guide when you want to follow ScanReady step by step instead of using **One Click Bake**.

The manual workflow lets you control reduction, UVs, cage and baking separately. It is useful when you want to decide more precisely how much to optimize the mesh, how to generate UVs and which textures to create.

---

## <span class="sr-addon-icon sr-icon-decim" title="Step 1 Preview / Reduce"></span>Step 1 - Create the Low-poly Preview

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin:22px 0 30px;">
<div style="flex:1 1 0; min-width:280px;">
  <ol>
    <li>Select the high-poly scan in Blender's viewport.</li>
    <li>Open <strong>STEP 1 Preview / Reduce</strong>.</li>
    <li>Adjust <strong>Optimize / Reduce</strong> or <strong>Final Faces</strong> if you want a lighter or more detailed mesh.</li>
    <li>Click <strong>Create Lowpoly Preview</strong>.</li>
  </ol>
  <p>ScanReady prepares the high-poly source and creates a separate preview to which reduction is applied. UVs are generated from the preview; the high-poly remains the reference for cage and baking.</p>
  <p>Preparation options can combine parts, clean the source, correct normals or convert materials. Keep a copy of the original file before starting.</p>
  <p>When the preview looks correct, continue to <strong>Step 2 - UV / Cage</strong>.</p>
</div>
<div style="flex:0 0 260px; max-width:260px; text-align:center;">
  <p style="margin-top:0;"><strong>Create Lowpoly Preview</strong></p>
  <img src="../img/manual-step1.jpg" alt="STEP 1 Preview Reduce panel with Create Lowpoly Preview button" style="width:100%;" decoding="async" fetchpriority="high">
</div>
</div>

---

## <span class="sr-addon-icon sr-icon-step2" title="Step 2 UV / Cage"></span>Step 2 - Generate UVs and Check the Cage

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin:22px 0 30px;">
<div style="flex:1 1 0; min-width:280px;">
  <ol>
    <li>Start with the low-poly preview created in Step 1.</li>
    <li>Open <strong>STEP 2 UV / Cage</strong>.</li>
    <li>Click <strong>Generate UVs</strong>.</li>
  </ol>
  <p>ScanReady creates a new UV layout on the optimized mesh. This prepares the asset to receive baked textures on the new low-poly surface.</p>
  <p>After generating UVs, prepare the cage for baking:</p>
  <ul>
    <li>use <strong>Auto Cage Extrusion</strong> for an automatic estimate;</li>
    <li>adjust <strong>Cage Extrusion</strong> if you need to correct the distance manually;</li>
    <li>check coverage of the high-poly; green indicates that the automatic check passed, but still inspect thin and concave areas before baking.</li>
  </ul>
</div>
<div style="flex:0 0 320px; max-width:320px; display:flex; flex-direction:column; gap:14px; text-align:center;">
  <div>
    <p style="margin-top:0;"><strong>Generate UVs</strong></p>
    <img src="../img/manual-step2.jpg" alt="STEP 2 UV Cage interface with Generate UVs button" style="width:100%;" loading="lazy" decoding="async">
  </div>
  <div>
    <p style="margin-top:0;"><strong>Show Cage / Cage Controls</strong></p>
    <img src="../img/manual-step2_cage.jpg" alt="STEP 2 UV Cage interface with Show Cage and cage controls" style="width:100%;" loading="lazy" decoding="async">
  </div>
</div>
</div>

---

## <span class="sr-addon-icon sr-icon-step3" title="Step 3 Bake / Output"></span>Step 3 - Bake

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin:22px 0 30px;">
<div style="flex:1 1 0; min-width:280px;">
  <ol>
    <li>Open <strong>STEP 3 Bake / Output</strong>.</li>
    <li>Choose <strong>Texture Preset / Texture Size</strong>.</li>
    <li>Choose how many <strong>Bake Materials</strong> to use.</li>
    <li>Enable the maps you want to generate, such as <strong>Bake Base Color</strong>, <strong>Bake Normal Map</strong>, <strong>Bake Roughness Map</strong> or <strong>Bake Occlusion Map</strong>.</li>
    <li>Click <strong>Bake Textures</strong>.</li>
  </ol>
  <p>ScanReady bakes one texture at a time, connects the generated textures to the final material and creates a lighter asset ready for realtime, VR, video games, AR and interactive scenes.</p>
  <div class="admonition info">
    <p class="admonition-title">Bake Roughness Map</p>
    <p>The <strong>Bake Roughness Map</strong> checkbox is shown only if the high-poly material has a connected Roughness input.</p>
    <p>If no roughness is connected, ScanReady cannot transfer it and the checkbox is not shown.</p>
  </div>
  <p>Before clicking <strong>Bake Textures</strong>, check that the cage covers the high-poly scan. If the cage is too small, black areas, missing details or incorrect projections may appear.</p>
</div>
<div style="flex:0 0 260px; max-width:260px; text-align:center;">
  <p style="margin-top:0;"><strong>Bake Textures</strong></p>
  <img src="../img/manual-step3.jpg" alt="ScanReady panel with workflow steps and Bake Output" style="width:100%;" loading="lazy" decoding="async">
</div>
</div>

---

## If You Want More Optimization

!!! tip "You can return to Step 1"
    You can go back at any time.

    If you are already in Step 2 or Step 3 and notice that the mesh is still too heavy, return to **Step 1 - Preview / Reduce**, lower **Final Faces** or **Optimize / Reduce**, then click **Create Lowpoly Preview** again.

After recreating the preview, continue forward again:

1. return to **Step 2 - UV / Cage**;
2. click **Generate UVs** again;
3. check the cage;
4. return to **Step 3 - Bake / Output**;
5. click **Bake Textures**.

!!! note "Updated UV mesh"
    The bake should always use the most recent optimized UV mesh.

---

## When to Use the Detailed Step Pages

This page tells you what to press and in which order.

To understand each stage better, use the dedicated pages:

- [Step 1 - Preview / Reduce](step1.md) for Adaptive Reduce, Optimize / Reduce, Final Faces and preview.
- [Step 2 - UV / Cage](step2.md) for Smart UV Project, checker, cage and Auto Cage Extrusion.
- [Step 3 - Bake / Output](step3.md) for texture size, bake materials, bake maps, output and image saving.
