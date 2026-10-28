# Settings Reference

This page summarizes ScanReady's main settings and what they do.

Use it as a quick reference when adjusting scans for VR, video games, realtime visualization or general optimization in Blender.

---

## Panel and Status

| Item | Description | When to use it |
|---|---|---|
| **Mesh Stats** | Shows faces and triangles of the selected object or latest preview. | Quickly check mesh weight before and after reduction. |
| **Refresh Stats** | Manually refreshes mesh statistics shown in the panel. | Use after changing selection or external mesh edits. |
| **ONE CLICK BAKE** | Starts the complete automatic workflow: preview, UVs, cage, bake and final materials. | Use for a quick conversion from high-poly scan to optimized asset. |
| **Workflow Status** | Shows overall progress, completed step, status messages, completed bake maps and timings when diagnostics are enabled. | See where ScanReady is during One Click Bake or manual steps. |
| **Global Progress** | Percentage completion of the current workflow. | Useful during long operations such as preview, UVs, cage and bake. |

---

## View and Preview

| Setting | Description | When to adjust |
|---|---|---|
| **Show Wireframe** | Shows the wireframe overlay on the preview object. | Check topology density and reduction quality. |
| **Show Checker** | Shows a checker texture for inspection. | Check UV distortion and stretching. |
| **Checker Mix** | Controls checker overlay strength. | Lower it to see more of the original texture. |
| **Checker UV Scale** | Changes checker square size. | Use smaller squares to see distortion more clearly. |

!!! info "Where to find Use Texture View"
    **Use Texture View** is available in **Advanced > Mesh Settings**, not in View Options, because it is not usually adjusted during the main workflow.

---

## Main Actions

| Action | Description | When to use it |
|---|---|---|
| **Create Lowpoly Preview** | Creates or updates the optimized preview mesh using Step 1 and Adaptive Reduce settings. | Use whenever you change density, Adaptive Reduce presets or mesh settings that affect reduction. |
| **Generate UVs** | Creates the UV mesh from the preview and generates the Smart UV Project layout. | Use after the preview or when changing Smart UV Preset, Smart UV Angle or UV Padding. |
| **Auto Cage Extrusion** | Calculates a starting cage extrusion by sampling the distance between the optimized mesh and high-poly source. | Use before baking to avoid estimating cage distance manually. |
| **Bake Textures** | Bakes selected maps and builds the final mesh and materials. | Use after generating UVs and checking cage and output. |

---

## Mesh and Reduction

Controls in **Step 1 - Preview / Reduce**. Final Faces and Optimize / Reduce are linked: choose either to adjust density.

| Setting | Description | When to adjust |
|---|---|---|
| **Final Faces** | Target face count for the optimized low-poly mesh. | Lower for lighter VR/game assets; raise to preserve more silhouette detail. |
| **Optimize / Reduce** | Controls how much the mesh is reduced. | Lower values reduce more; higher values retain more geometry. |
| **Reduction** | Reduction percentage derived from the current ratio. | An indicator, not an independent control. |

---

## UV Settings

| Setting | Description | When to adjust |
|---|---|---|
| **Smart UV Preset** | Applies a recommended Smart UV angle. Presets include Detailed, Balanced, Large Islands and Continuous. | Use as a quick starting point for common scan types. |
| **Smart UV Angle** | Controls how aggressively Smart UV Project divides islands. | Lower values create more cuts; higher values create larger islands. |
| **UV Padding** | Adds space between UV islands. | Increase to reduce texture bleeding and visible seams. |

### UV Generation

ScanReady uses **Smart UV Project** to generate UVs.

!!! note "When to regenerate UVs"
    **Adaptive Reduce** presets are separate from UV settings: they control mesh simplification before UV generation and baking.

    If you change **Smart UV Preset**, **Smart UV Angle** or **UV Padding** after UVs have been created, click **Generate UVs** again before baking.

    ScanReady then recreates the UV layout on the optimized mesh using the new values.

---

## Cage Settings

| Setting | Description | When to adjust |
|---|---|---|
| **Show Cage** | Shows the cage preview. | Check projection coverage before baking. |
| **Auto Cage Extrusion** | Automatically estimates cage extrusion. | Use for a quick cage setup. |
| **Cage Extrusion** | Manual cage distance. | Increase if details are missing; decrease if wrong areas are captured. |
| **Cage Opacity** | Controls cage preview opacity. | Adjust only for viewport visibility; it does not affect baking. |

---

## Textures and Baking

This table follows the order of **Step 3 Bake / Output** in the main panel.

| Setting | Description | When to adjust |
|---|---|---|
| **Texture Preset / Texture Size** | Sets baked texture resolution. | Raise for close-up assets; lower for lightweight VR/game assets. |
| **Bake Materials** | Splits the bake into material groups. | Increase for large scans needing more texture detail. Values above `1` automatically enable Force CPU Baking. |
| **Bake Base Color** | Bakes the main color texture. | Keep enabled to preserve the scan's original color. |
| **Bake Normal Map** | Bakes or transfers a normal map. | ScanReady transfers a connected high-poly normal texture; otherwise it performs a geometric high-to-low normal bake. |
| **Bake Roughness Map** | Transfers roughness from the high-poly material when a roughness texture is connected. | Enable to retain roughness variation from the original material. |
| **Bake Occlusion Map** | Bakes an Ambient Occlusion map. | Enable to add depth and contact shadows. |
| **Save Images** | Saves baked textures to disk. | Enable when exporting to game engines, archives or external tools. |
| **Open Folder After Bake** | Automatically opens the bake folder once texture saving is complete. | Enable to see generated files without manually pressing Bake Folder. |
| **Image Format** | Selects JPG, PNG or TIFF. | Use JPG for compact color maps, PNG for lossless output and TIFF for high precision. |
| **Output Folder** | Folder where baked textures are saved. | Set before baking to use a specific project folder. |
| **Bake Folder** | Shows the folder used by the last bake and provides a button to open it. | Use after baking to inspect saved texture files. |

---

## Mesh Settings

Controls in **Advanced > Mesh Settings**, in add-on order. Some modify the source: keep a copy of the original project.

| Setting | Description | When to adjust |
|---|---|---|
| **Pre-Decimate Merge** | Merges preview vertices within the specified distance in centimeters before Decimate. | Use a small distance; lower it if thin details that should remain separate are merged. |
| **Auto Fix Normals** | Recalculates high-poly mesh normals before creating the preview. | Enable for inverted normals or shading artifacts. |
| **Auto Clear Sharp Edges** | Removes unwanted sharp-edge markings during preparation. | Keep enabled when scan edges or shading are incorrectly marked. |
| **Auto Combine Mesh Parts** | Enabled by default. Detects and combines multi-mesh hierarchies when needed; does nothing if the scan is already one mesh. | Keep enabled for GLB, FBX or photogrammetry scans split into parts. Disable only if combining causes problems or parts should remain separate. |
| **Auto Clean Scan Debris** | Removes small fragments, floating polygons and isolated vertices. | Keep enabled for raw photogrammetry scans. |
| **Convert Source Materials** | Disabled by default. Preserves standard source materials and converts only complex imported shaders into a more predictable bake setup. | Enable for a bad bake, such as black/incomplete Base Color, or improperly read imported materials. |
| **Show Face Orientation** | Shows Blender's Face Orientation overlay. | Check inverted normals before preview, UVs or baking. |
| **Backface Culling** | Hides faces seen from behind in the viewport. This preview mode does not modify the mesh or bake. | Find single-sided surfaces, holes, open parts or suspicious orientation. It automatically turns off when Show Face Orientation is enabled, and vice versa. |
| **Use Texture View** | Uses Material Preview without scene lights and World; with Backface Culling enabled, uses Solid with textures. | View materials, checker and cage more clearly. |
| **Recalculate Outside Normals** | Manually recalculates normals outward. | Use for inverted-looking meshes or inconsistent shading. |

---

## Adaptive Reduce

| Setting | Description | When to adjust |
|---|---|---|
| **Adaptive Reduce** | Uses scan-based weights to reduce flat surfaces more and protect important detail. | Keep enabled for most scans; disable for simpler uniform reduction. |
| **Adaptive Method** | Selects Best Quality or the original Legacy calculation. | Normally use Best Quality; use Legacy for compatibility or comparison. |
| **Adaptive Preset** | Selects adaptive reduction behavior. | Balanced for most scans, Preserve Details for complex surfaces, Flat Surfaces for broad simple surfaces. |
| **Show Adaptive Weights** | Displays the weight map: red/orange reduces more, green is transitional and blue protects detail. Temporarily hides wireframe. | Inspect how ScanReady interprets the scan; disabling restores the previous wireframe setting. |
| **Adaptive Strength** | Legacy method strength. | Adjust only when Adaptive Method is Legacy. |
| **Adaptive Reduce Angle** | Reference angle for distinguishing planar areas from significant normal changes. | Lower to recognize smaller variations as detail; raise to include more smooth surfaces in reduction. |
| **Detail Preserve** | Minimum reduction weight in protected areas. | Lower to protect detected detail more; raise to allow more reduction there. |
| **Smooth Weights** | Smooths weight-map transitions. | Raise for less fragmented transitions; avoid excessive values around small details. |
| **Complexity Sensitivity** | Controls how readily Best Quality classifies persistent shape changes as detail. | Raise to protect more geometry; lower for more aggressive reduction. |
| **Flat / Detail Contrast** | Controls separation between flat and detailed areas. | Raise for a sharper red/blue division; lower for a softer gradient. |
| **Detail Spread Rings** | Expands detected detail into neighboring vertex rings. | Raise when reliefs and decorations need more surrounding support. |
| **Noise Rejection** | Dampens isolated variations that do not persist in the surrounding region. | Raise to ignore more scan noise; lower to retain more fine variations. |
| **Analysis Scale** | Sets how many connected rings distinguish coherent forms from local noise. | Raise for broader, slower analysis; lower for a more local response. |
| **Adaptive Decimate Factor** | Controls how strongly Best Quality weights affect Blender Decimate without changing the color map. | Start at 2. The recommended range is 1–5; high values can create long or radial triangles. |
| **Fast Adaptive Reduce** | Uses fewer samples and refinement passes. | Enable for quick dense-scan tests; disable for final quality checking. |
| **Protect Feature Edges** | Protects open boundaries and sufficiently sharp edges. | Keep enabled for silhouettes, arches, bevels, frames and architectural breaks. |
| **Feature Edge Angle** | Minimum angle between face normals for identifying a feature edge. | Lower to protect more edges; raise to protect only sharper breaks. |
| **Feature Edge Rings** | Expands protection into neighboring vertex rings. | Raise if edges lose surrounding support. |

!!! note "When to recreate the preview"
    Adaptive Reduce weights are calculated when you press **Create Lowpoly Preview**. Changing **Optimize / Reduce** or **Final Faces** afterwards updates the amount of reduction, but changing a preset or detailed Adaptive Reduce values requires recreating the low-poly preview to rebuild the weights.

    If you are already in Step 2 or Step 3 and need a lighter or more detailed model, return to Step 1, adjust **Final Faces** or **Optimize / Reduce**, click **Create Lowpoly Preview**, then regenerate UVs and bake.

---

## Texture Detail

This section is in **Advanced**, after **UV Settings** and before **Bake Settings**.

| Setting | Description | When to adjust |
|---|---|---|
| **Texture Detail** | Advanced section for texture detail and UV space analysis. | Use to assess whether texture size and material count are balanced. |
| **Analyze Texture Detail** | Starts high-to-UV analysis and shows texture/material recommendations. | Use after generating UVs and before baking when unsure about resolution or material count. |

---

## Bake Settings

This table follows the order of **Advanced > Bake Settings** in the add-on.

| Setting | Description | When to adjust |
|---|---|---|
| **Bake Samples** | Sets the number of Cycles samples for baking. | Raise for cleaner bakes, especially AO; lower for faster tests. |
| **Bake Margin** | Adds padding around baked UV islands. | Increase to reduce seams and texture bleeding. |
| **Normal Strength** | Appears when **Bake Normal Map** is enabled and controls the Normal Map node strength in the final material. | Adjust weak or strong normal detail. If disabled, the image format control, such as JPG Quality, follows Bake Margin. |
| **JPG Quality** | Controls JPG compression quality when JPG is selected. | Raise for better quality; lower for smaller files. |
| **TIFF 16-bit** | Saves higher-precision TIFF textures when TIFF is selected. | Use for close-up assets, archive workflows or detailed maps. |

---

## Occlusion Settings

This section is in **Advanced > Bake Settings** and appears when **Bake Occlusion Map** is enabled.

| Setting | Description | When to adjust |
|---|---|---|
| **AO Source** | Chooses how AO is baked. | Use high-to-low to transfer scan detail, or low-only for simpler AO. |
| **Auto AO Distance** | Automatically calculates AO distance from model size. | Leave enabled for most assets. |
| **AO Distance** | Manual AO ray distance. | Adjust when automatic distance produces AO that is too strong or weak. |
| **AO Samples** | Controls the AO bake sample count. | Raise for cleaner AO; lower for faster bakes. |
| **AO Mix** | Controls how much baked AO darkens the final Base Color material. | Default is `1.0`; lower if the final material looks too dark or contrasty. |

---

## Memory Safety

This section is in **Advanced > Bake Settings**.

| Setting | Description | When to adjust |
|---|---|---|
| **Safe Memory Bake** | Uses a safer bake workflow for heavy scenes. | Keep enabled for large scans or high texture resolutions. |
| **Force CPU Baking** | Forces CPU rather than GPU baking. | Disabled by default with one material; automatically enabled at `2` or more Bake Materials and can be disabled manually. |

---

## Presets

| Control | Description | When to use it |
|---|---|---|
| **Preset Name** | Name used when saving current settings. | Use a clear name for a workflow or asset type. |
| **Save Preset** | Saves workflow parameters, including Output Folder; does not save meshes, textures or update preferences. | Use before processing similar scans. |
| **Preset Selector** | Menu of available saved presets. | Choose which preset to reload or delete. |
| **Reload Preset** | Reloads the selected preset. | Repeat a known setup or quickly return to a saved preset. |
| **Delete Preset** | Deletes the selected preset. | Remove old or unused setups. |

---

## Diagnostics

| Control | Description | When to use it |
|---|---|---|
| **Show Diagnostic Timing Report** | Shows a detailed timing report after One Click Bake, including Adaptive/Decimate and Bake/Finalize sub-reports. | Keep disabled for videos and normal use; enable to analyze performance or compare tests. |

---

## Utilities

| Control | Description | When to use it |
|---|---|---|
| **Reset Defaults** | Restores default parameter values. | Start again from a known configuration, then regenerate necessary steps. It does not restore an already modified source. |

---

## Addon Preferences / Updates

| Control | Description | When to use it |
|---|---|---|
| **Installed version** | Shows the installed ScanReady version. | Quickly check which build is active in Blender. |
| **Updates are managed by Blender Extensions / Superhive** | Indicates that public updates are managed by the distribution platform. | Find where to obtain the official add-on update. |
| **Check for Updates** | Manually checks the public documentation manifest and compares available and installed versions. | Informational check or fallback, especially for ZIP installations. It does not install updates. |
| **Update Status** | Shows the result of the last update check. | Check whether ScanReady is up to date, a newer version is available or the check failed. |
| **Open Documentation** | Opens ScanReady's online documentation. | Consult the quick guide, workflows, FAQ or troubleshooting. |
| **Release Notes** | Opens the ScanReady changelog and release notes page. | See what changed before updating. |
| **Video Tutorials** | Opens the YouTube channel with ScanReady tutorials. | Watch the workflow on video. |

!!! note "Official update and manual check"
    The **Update** button on the Blender Extensions screen depends on the repository or marketplace from which the extension was installed.

    **Check for Updates** within ScanReady reads the public documentation manifest. It is informational: it does not download or install the update.

---

## Recommended Starting Points

### Lightweight VR Asset

| Setting | Recommended direction |
|---|---|
| **Final Faces** | Lower |
| **Texture Size** | 1024 or 2048 |
| **Bake Normal Map** | Enabled if surface detail matters |
| **Bake Occlusion Map** | Optional |
| **Safe Memory Bake** | Enabled |
| **Bake Materials** | Keep low |

### Game Prop

| Setting | Recommended direction |
|---|---|
| **Final Faces** | Medium |
| **Texture Size** | 2048 |
| **Bake Base Color** | Enabled |
| **Bake Normal Map** | Enabled |
| **Bake Occlusion Map** | Optional |
| **Image Format** | PNG or JPG depending on the pipeline |

### Close-up Presentation Asset

| Setting | Recommended direction |
|---|---|
| **Final Faces** | Higher |
| **Texture Size** | 4096 or higher |
| **Bake Normal Map** | Enabled |
| **Bake Occlusion Map** | Enabled |
| **Bake Samples** | Higher |
| **Image Format** | PNG or TIFF |

---

## General Rule

!!! tip "Recommended balance"
    For realtime, do not retain detail only as geometry.

    Use geometry for the main shape and baked textures for visual detail.

    This balance makes scanned assets easier to use in VR, video games, realtime viewers and interactive scenes.
