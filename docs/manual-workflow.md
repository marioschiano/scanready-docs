# Manual Guide

Use this guide when you want to run ScanReady step by step instead of using **One Click Bake**.

The manual workflow lets you control reduction, UVs, cage setup, and baking separately.

---

## Step 1 - Create the low-poly preview

1. Select the high-poly scan in Blender.
2. Open **STEP 1 Preview / Reduce**.
3. Adjust **Optimize / Reduce** or **Final Faces** if needed.
4. Click **Create Low-poly Preview**.

ScanReady cleans the scan, creates an optimized copy, and keeps the original high-poly source intact.

---

## Step 2 - Generate UVs and check the cage

1. Open **STEP 2 UV / Cage**.
2. Click **Generate UVs**.
3. Enable **Show Cage** and check that the cage covers the high-poly source.
4. Use **Auto Cage Extrusion** or adjust **Cage Extrusion** if needed.

---

## Step 3 - Bake textures

1. Open **STEP 3 Bake / Output**.
2. Choose **Texture Preset / Texture Size** and **Bake Materials**.
3. Enable the maps you want to bake.
4. Click **Bake Textures**.

ScanReady bakes the selected maps, links the generated textures, and creates the final realtime-ready asset.

For detailed explanations, see [Step 1](step1.md), [Step 2](step2.md), and [Step 3](step3.md).
