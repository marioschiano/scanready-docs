# Settings Reference

This page summarizes the main ScanReady 1.0 settings and what they do.

Use it as a quick reference when tuning scans for VR, videogames, realtime visualization, or general Blender optimization.

---

## Mesh and Reduction

| Setting | Description | When to Adjust |
|---|---|---|
| **Final Faces** | Target face count for the optimized lowpoly mesh. | Lower it for lighter VR/game assets. Raise it to preserve silhouette detail. |
| **Optimize / Reduce** | Controls how strongly the mesh is reduced. | Lower values create stronger reduction. Higher values keep more geometry. |
| **Weld Distance** | Merges vertices that are very close together. | Use it to clean small scan artifacts, tiny gaps, or overlapping points. |
| **Auto Fix Normals** | Recalculates high mesh normals before preview creation. | Enable it when the scan has inverted normals or shading artifacts. |
| **Recalculate Outside Normals** | Manually recalculates normals outside. | Use it when the mesh appears inside-out or has broken shading. |

---

## View and Preview

| Setting | Description | When to Adjust |
|---|---|---|
| **Show Wireframe** | Displays the wireframe overlay on the preview object. | Use it to inspect topology density and reduction quality. |
| **Show Checker** | Displays a checker texture for inspection. | Use it to check UV distortion and stretching. |
| **Use Texture View** | Shows the model in a flat texture-oriented view. | Use it to inspect baked or previewed texture results without scene lighting. |
| **Checker Mix** | Controls checker overlay strength. | Lower it when you want to see more of the original texture. |
| **Checker Scale** | Changes checker square size. | Use smaller squares to reveal distortion more clearly. |

---

## UV Settings

| Setting | Description | When to Adjust |
|---|---|---|
| **UV Method** | ScanReady 1.0 uses Smart UV Project for UV generation. | This is the UV method used by the addon workflow. |
| **Smart UV Preset** | Applies a recommended Smart UV angle. | Use it as a quick starting point for common scan types. |
| **Smart UV Angle** | Controls how aggressively Smart UV Project splits islands. | Lower values create more cuts. Higher values create larger islands. |
| **Auto Pack UV** | Packs UV islands automatically after unwrap. | Leave enabled unless you want to arrange UV islands manually. |
| **UV Padding** | Adds spacing between UV islands. | Increase it to reduce texture bleeding and visible seams. |


---

## Cage Settings

| Setting | Description | When to Adjust |
|---|---|---|
| **Show Cage** | Displays the cage preview. | Use it before baking to inspect projection coverage. |
| **Auto Cage Extrusion** | Automatically estimates cage extrusion. | Use it when you want a fast cage setup. |
| **Cage Extrusion** | Manual cage distance. | Increase it if details are missing. Decrease it if wrong areas are captured. |
| **Cage Alpha** | Controls cage preview opacity. | Adjust it only for viewport visibility. It does not affect the bake. |

---

## Texture and Bake

| Setting | Description | When to Adjust |
|---|---|---|
| **Texture Size** | Sets baked texture resolution. | Raise it for close-up assets. Lower it for lightweight VR/game assets. |
| **Bake Materials** | Splits the bake into multiple material groups. | Increase for large scans that need more texture detail. |
| **Bake Samples** | Sets Cycles bake sample count. | Raise it for cleaner bakes, especially AO. Lower it for faster tests. |
| **Bake Margin** | Adds padding around baked UV islands. | Increase it to reduce seams and texture bleeding. |
| **Bake Base Color** | Bakes the main color texture. | Keep enabled when preserving original scan color. |
| **Bake Normal** | Bakes a normal map. | Enable it to preserve surface detail without heavy geometry. |
| **Bake Occlusion** | Bakes an Ambient Occlusion map. | Enable it to add depth and contact shadow detail. |
| **Normal Strength** | Controls the Normal Map node strength. | Adjust it if the normal detail looks too weak or too strong. |

---

## Ambient Occlusion

| Setting | Description | When to Adjust |
|---|---|---|
| **AO Source** | Chooses how AO is baked. | Use high-to-low for scan detail transfer, or low-only for simpler AO. |
| **AO Auto Distance** | Automatically calculates AO distance from model size. | Leave enabled for most assets. |
| **AO Distance** | Manual AO ray distance. | Adjust when automatic distance gives AO that is too strong or too weak. |
| **AO Samples** | Controls AO bake sample count. | Raise it for cleaner AO. Lower it for faster baking. |

---

## Output Settings

| Setting | Description | When to Adjust |
|---|---|---|
| **Save Images** | Saves baked textures to disk. | Enable it when exporting to game engines, archives, or external tools. |
| **Image Format** | Chooses JPG, PNG, or TIFF. | Use JPG for compact color maps, PNG for lossless output, TIFF for high precision. |
| **JPG Quality** | Controls JPG compression quality. | Raise it for better image quality. Lower it for smaller files. |
| **TIFF 16-bit** | Saves TIFF textures with higher precision. | Use it for close-up assets, archival workflows, or detailed maps. |
| **Output Folder** | Folder where baked textures are saved. | Set it before baking if you need files in a specific project folder. |

---

## Memory Safety

| Setting | Description | When to Adjust |
|---|---|---|
| **Safe Memory Bake** | Uses a safer bake workflow for heavy scenes. | Keep enabled for large scans or high texture resolutions. |
| **Force CPU Baking** | Forces baking on CPU instead of GPU. | Enable it when GPU memory is limited or baking crashes. |

---

## Presets

| Control | Description | When to Use |
|---|---|---|
| **Preset Name** | Name used when saving current settings. | Use a clear name for a workflow or asset type. |
| **Save Preset** | Saves the current settings. | Use it before processing similar scans. |
| **Load Preset** | Loads the selected preset. | Use it to repeat a known setup. |
| **Delete Preset** | Deletes the selected preset. | Use it to remove old or unused setups. |

---

## Recommended Starting Points

### Lightweight VR Asset

| Setting | Suggested Direction |
|---|---|
| **Final Faces** | Lower |
| **Texture Size** | 1024 or 2048 |
| **Bake Normal** | Enabled if surface detail matters |
| **Bake Occlusion** | Optional |
| **Safe Memory Bake** | Enabled |
| **Material Count** | Keep low |

### Game Prop

| Setting | Suggested Direction |
|---|---|
| **Final Faces** | Medium |
| **Texture Size** | 2048 |
| **Bake Base Color** | Enabled |
| **Bake Normal** | Enabled |
| **Bake Occlusion** | Optional |
| **Image Format** | PNG or JPG depending on pipeline |

### Close-Up Presentation Asset

| Setting | Suggested Direction |
|---|---|
| **Final Faces** | Higher |
| **Texture Size** | 4096 or higher |
| **Bake Normal** | Enabled |
| **Bake Occlusion** | Enabled |
| **Bake Samples** | Higher |
| **Image Format** | PNG or TIFF |

---

## General Rule

For realtime work, do not keep detail only as geometry.

Use geometry for the main shape, and use baked textures for visual detail.

That balance is what makes scanned assets easier to use in VR, videogames, realtime viewers, and interactive scenes.
