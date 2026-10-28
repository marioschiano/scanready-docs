# Changelog

This page contains ScanReady release notes.

Review what's new and the known issues before updating the add-on.

## 1.0.0 - Initial Release

### Added

- Blender Extension package support.
- One Click Bake workflow to create game-ready assets from scans.
- Step 1 Preview / Reduce workflow.
- Adaptive Reduce for scan-aware mesh optimization.
- Adaptive Method selector with Best Quality and Legacy mode for compatibility.
- Best Quality combines large planar-area detection with protection for persistent curvature, reliefs and decorations.
- Adaptive Reduce presets: Balanced, Preserve Details and Flat Surfaces.
- Advanced Best Quality controls for complexity sensitivity, flat/detail contrast, detail expansion, noise rejection, analysis scale and Decimate influence.
- Show Adaptive Weights visualization.
- Auto combine mesh parts for imported scans with a hierarchy.
- Auto clean scan debris option.
- Smart UV Project workflow.
- UV / Cage workflow.
- Base Color, Normal Map, Roughness Map and Occlusion Map baking.
- AO Mix control in Advanced > Bake Settings > Occlusion Settings to adjust how much baked Ambient Occlusion affects the final material.
- Texture Detail analysis to estimate texture/material needs.
- Final mesh setup with Edge Split and Weighted Normal modifiers.
- Safe Memory Bake and Force CPU Baking options.
- Bake Folder shortcut in Step 3 to open the last saved texture folder.
- Documentation and release notes links in add-on preferences.
- Update notification for marketplaces and Blender Extensions.

### Changed

- The update flow now directs users to Blender Extensions or a marketplace instead of installing updates directly within the add-on.
- Adaptive Reduce settings moved to Advanced.
- Show Adaptive Reduce renamed to Show Adaptive Weights.
- The default Adaptive Reduce behavior now uses the Balanced preset.
- Balanced uses the verified Best Quality values and Adaptive Decimate Factor 2.
- Show Adaptive Weights temporarily hides the wireframe and restores the previous preference when disabled.
- Adaptive Strength is shown only with Legacy; Best Quality uses Adaptive Decimate Factor.
- The default Detail Preserve value was changed to better protect detailed scan areas.
- Removed Auto Weld Distance and Weld Distance; Pre-Decimate Merge is now the single explicit weld control.
- Removed the live Weld modifier from the preview stack; vertex welding is now handled by Pre-Decimate Merge applied before Decimate.
- Normal Strength moved to Advanced > Bake Settings.
- Texture Detail / Analyze Texture Detail moved to Advanced.
- Extension manifest cleaned up for Blender Extension validation.

### Fixed

- Fixed Blender Extension manifest validation errors caused by punctuation at the end of manifest strings.
- Improved Adaptive Reduce weight calculation so large flat areas are detected more clearly and coherent decorations remain protected.
- Improved readability of the Adaptive Reduce color preview.
- Reduced continuous mesh stats recalculation to keep the Blender interface more responsive.

### Known Issues

- Very heavy scans can still take time for analysis, reduction, UVs or baking.
- Bake quality depends on scan quality, UV layout, cage/extrusion settings and texture resolution.
- Adaptive Reduce helps distribute polygons more effectively, but is not a perfect substitute for retopology.
