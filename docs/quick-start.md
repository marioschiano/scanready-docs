# Quick Start

This page shows the fastest way to use ScanReady.

<p align="center">
  <img src="../img/hero.jpg" alt="Overview of the ScanReady workflow" style="max-width:620px;width:100%;" decoding="async" fetchpriority="high">
</p>

---

!!! note "Before you start"
    Save a copy of your `.blend` file. Reduction takes place on a separate preview, but preparation options can modify the high-poly source.

## Basic Workflow

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:28px; align-items:flex-start;">

  <div style="flex:1 1 360px; min-width:260px;">

    <p>For a quick first test, let ScanReady handle the workflow automatically with the default settings:</p>

    <ol>
      <li>Select the high-poly scan mesh.</li>
      <li>Click <strong>ONE CLICK BAKE</strong>.</li>
    </ol>

    <p>With the default <strong>Optimize / Reduce 0.10</strong> value, ScanReady keeps approximately 10% of the polygons, reducing the mesh by about 90%, generates UVs and completes the bake with the default settings.</p>

  </div>

  <div style="flex:0 0 260px; text-align:center;">
    <p style="margin-top:0;"><strong>ONE CLICK BAKE</strong></p>
    <img src="../img/quick-start-one-click.png" alt="ScanReady One Click Bake button in Blender" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
  </div>

</div>

---

## What Happens Automatically

When you use **ONE CLICK BAKE**, ScanReady performs the main workflow:

1. Cleans the selected scan.
2. Creates an optimized low-poly preview.
3. Generates UVs.
4. Prepares the cage.
5. Bakes the selected textures.
6. Creates the final material.
7. Saves images if **Save Images** is enabled, as it is by default.

The model is optimized, receives new UVs and can have the selected textures baked in a single workflow.

<p align="center">
  <img src="../img/one-click-bake.gif" alt="ScanReady One Click Bake workflow in Blender" style="max-width:820px;width:100%;" loading="lazy" decoding="async">
</p>

---

## Default Settings

For the first test you do not need to change the settings. If you have not changed the defaults, ScanReady starts with:

- **Optimize / Reduce:** `0.10`
- **Final Faces:** value linked to the reduction ratio
- **Adaptive Reduce:** enabled
- **Adaptive Preset:** `Balanced`
- **Adaptive Method:** `Best Quality`
- **Texture Size:** `2048`
- **Bake Base Color:** enabled
- **Bake Normal Map:** disabled by default; enable it to transfer normal detail
- **Save Images:** enabled to save textures to disk

These values show where the automatic workflow starts. For the first test, leave everything unchanged and press **ONE CLICK BAKE**.

---

## Quick Result

After baking, you should obtain:

- a lighter final mesh;
- automatically generated UVs;
- baked textures connected to the material;
- image files saved in the output folder, if enabled.

Check the result in the viewport and in **Step 3 - Bake / Output**.

!!! tip "You can refine the result after One Click Bake"
    If the result is not sufficient, return to the manual steps and adjust settings only where necessary. If the final model is still too heavy, or has been optimized too much and has lost important shape details, return to **Step 1 - Preview / Reduce**.

    Adjust **Optimize / Reduce** or **Final Faces** and watch the preview update. When you are happy with the result, go to Step 2 and click **Generate UVs** again.

    The workflow is flexible: even if you are already in **Step 2 - UV / Cage** or **Step 3 - Bake / Output**, you can return to Step 1, adjust polygon reduction and then continue through UVs and baking again.

---

## When to Use the Manual Steps

Use the manual workflow if you want more control:

- [Step 1 - Preview / Reduce](step1.md) to adjust mesh density.
- [Step 2 - UV / Cage](step2.md) to check UVs and cage.
- [Step 3 - Bake / Output](step3.md) to manage textures, materials and output.
