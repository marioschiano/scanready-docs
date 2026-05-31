# Changelog

All notable changes to ScanReady will be documented in this file.

Use this page as the public release notes source for Superhive, Blender Extensions, and addon update links.

## 1.0.0 - Initial Release

### Added

- Blender Extension package support.
- One Click Bake workflow for scan-to-game-ready asset creation.
- Step 1 Preview / Reduce workflow.
- Adaptive Reduce for scan-aware mesh optimization.
- Home and Step 1 documentation sections explaining why ScanReady Adaptive Reduce differs from standard Blender Decimate, with placeholders for comparison images.
- Adaptive Reduce presets: Balanced, Preserve Details, Flat Surfaces, and Hard Surface.
- Hard Surface Adaptive Reduce preset for vehicles and hard-surface scans, tuned as a faster approximate pass that protects only stronger normal breaks.
- Show Adaptive Weights visualization.
- Auto combine mesh parts for imported scans with hierarchy.
- Auto clean scan debris option.
- Smart UV Project workflow.
- UV / Cage workflow.
- Base Color, Normal, Roughness, and Ambient Occlusion baking.
- AO Mix control in Advanced > Occlusion Settings for adjusting how strongly baked Ambient Occlusion affects the final material.
- Texture Detail analysis for estimating texture/material needs.
- Final mesh setup with Edge Split and Weighted Normal modifiers.
- Safe Memory Bake and Force CPU Baking options.
- Bake Folder shortcut in Step 3 for opening the latest saved texture folder.
- Documentation and release notes links inside addon preferences.
- Marketplace and Blender Extensions update notification message.

### Changed

- Update flow now points users to Blender Extensions or the marketplace instead of installing updates directly inside the addon.
- Adaptive Reduce settings were moved to Advanced.
- Show Adaptive Reduce was renamed to Show Adaptive Weights.
- Default Adaptive Reduce behavior now uses the Balanced preset.
- Default Detail Preserve value changed to better protect detailed scan areas.
- Removed Auto Weld Distance and Weld Distance; Pre-Decimate Merge is now the single explicit weld control.
- Removed the live Weld modifier from the preview stack; vertex welding is now handled by the applied Pre-Decimate Merge before Decimate.
- Moved Normal Strength to Advanced > Bake Settings.
- Extension manifest cleaned up for Blender Extension validation.

### Fixed

- Fixed Blender Extension manifest validation errors caused by punctuation at the end of manifest strings.
- Improved Adaptive Reduce weight calculation so broad flat areas are detected more clearly.
- Improved Adaptive Reduce color preview readability.
- Reduced continuous mesh stats recalculation so the Blender interface stays more responsive.

### Known Issues

- Very heavy scans can still take time to analyze, reduce, UV, or bake.
- Bake quality depends on scan quality, UV layout, cage/extrusion settings, and texture resolution.
- Adaptive Reduce is a helper for better polygon distribution, not a perfect retopology replacement.
