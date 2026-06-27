# Manual Guide

Use this guide when you want to run ScanReady step by step instead of using **One Click Bake**.

The manual workflow lets you control reduction, UVs, cage setup, and baking separately.

---

## Step 1 - Create the low-poly preview

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin:22px 0 30px;">

<div style="flex:1 1 0; min-width:280px;">
  <ol>
    <li>Select the high-poly scan in Blender.</li>
    <li>Open <strong>STEP 1 Preview / Reduce</strong>.</li>
    <li>Adjust <strong>Optimize / Reduce</strong> or <strong>Final Faces</strong> if needed.</li>
    <li>Click <strong>Create Low-poly Preview</strong>.</li>
  </ol>

  <p>ScanReady cleans the scan, creates an optimized copy, and keeps the original high-poly source intact.</p>
</div>

<div style="flex:0 0 260px; max-width:260px;">
  <img src="../img/step1-preview-reduce.png" alt="STEP 1 Preview Reduce panel with Create Low-poly Preview button" style="width:100%;">
</div>

</div>

---

## Step 2 - Generate UVs and check the cage

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin:22px 0 30px;">

<div style="flex:1 1 0; min-width:280px;">
  <ol>
    <li>Open <strong>STEP 2 UV / Cage</strong>.</li>
    <li>Click <strong>Generate UVs</strong>.</li>
    <li>Enable <strong>Show Cage</strong> and check that the cage covers the high-poly source.</li>
    <li>Use <strong>Auto Cage Extrusion</strong> or adjust <strong>Cage Extrusion</strong> if needed.</li>
  </ol>
</div>

<div style="flex:0 0 320px; max-width:320px;">
  <img src="../img/step2_cage_extrusion.gif" alt="STEP 2 UV Cage interface with Generate UVs and cage controls" style="width:100%;">
</div>

</div>

---

## Step 3 - Bake textures

<div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin:22px 0 30px;">

<div style="flex:1 1 0; min-width:280px;">
  <ol>
    <li>Open <strong>STEP 3 Bake / Output</strong>.</li>
    <li>Choose <strong>Texture Preset / Texture Size</strong> and <strong>Bake Materials</strong>.</li>
    <li>Enable the maps you want to bake.</li>
    <li>Click <strong>Bake Textures</strong>.</li>
  </ol>

  <p>ScanReady bakes the selected maps, links the generated textures, and creates the final realtime-ready asset.</p>
</div>

<div style="flex:0 0 260px; max-width:260px;">
  <img src="../img/quick-start-one-click.png" alt="ScanReady panel with workflow steps and Bake Output section" style="width:100%;">
</div>

</div>

For detailed explanations, see [Step 1](step1.md), [Step 2](step2.md), and [Step 3](step3.md).
