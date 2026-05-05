# Export Tips

After using ScanReady 1.0, you can export the optimized baked asset for VR, AR, videogames, realtime viewers, or other 3D production workflows.

The goal is to keep the model light enough for realtime use while preserving the visual detail of the original scan through baked textures.

---

## Before Exporting

Before exporting, check:

- The final mesh is selected.
- The optimized mesh has UVs.
- The baked material is assigned.
- Texture files were saved if you need external image files.
- The object scale is correct.
- The object origin is placed where you need it.
- The mesh density is suitable for the target platform.

For VR and videogames, performance matters as much as visual quality.

---

## Recommended Export Formats

### glTF / GLB

Use **glTF** or **GLB** for modern realtime workflows.

Good for:

- Web viewers.
- Realtime previews.
- Many game engines.
- AR/VR pipelines.
- Lightweight asset delivery.

`GLB` stores the model and textures in a single file, which is useful for sharing and previewing.

### FBX

Use **FBX** when your target pipeline depends on it.

Good for:

- Unity workflows.
- Unreal Engine workflows.
- DCC-to-engine transfer.
- Teams that already use FBX as a standard.

FBX can work well, but texture connections may need checking after import.

### OBJ

Use **OBJ** for simple static mesh exchange.

Good for:

- Basic geometry transfer.
- Simple archive workflows.
- Compatibility with many tools.

OBJ is simple, but it is less complete than glTF or FBX for modern material workflows.

---

## Texture Maps

Depending on your settings, ScanReady 1.0 can create:

- Base Color texture.
- Normal map.
- Ambient Occlusion map.

When exporting to another application, make sure the external software is using the correct texture files.

### Base Color

Connect this to the main color or albedo input.

### Normal Map

Connect this to the normal input.

In some software, you may need to set the image type as **Non-Color** or **Normal Map**.

### Ambient Occlusion

Connect this to the AO input if your target engine supports it.

Some workflows combine AO with other maps, depending on the engine or material setup.

---

## Texture Resolution

Choose texture size based on the final use.

### 1024

Good for small props, background objects, mobile VR, or lightweight previews.

### 2048

Good general-purpose choice for many assets.

### 4096

Useful for close-up objects or important assets.

### 8192

Use only when very high detail is needed.

Large textures increase memory usage, file size, loading time, and realtime cost.

---

## VR Optimization

For VR, keep assets especially light.

VR needs stable performance because the scene must render smoothly for both eyes.

Before exporting for VR:

- Reduce polygon count as much as possible.
- Use baked textures instead of heavy geometry.
- Avoid unnecessarily large texture sizes.
- Use Normal maps to preserve surface detail.
- Test the asset in the target VR environment.
- Prefer fewer materials when possible.

A model that looks fine on desktop may still be too heavy for standalone VR headsets.

---

## Videogame Optimization

For videogames, balance quality and performance.

Before exporting for a game engine:

- Keep polygon count appropriate for the asset size.
- Use texture detail instead of excessive geometry.
- Use Normal maps for surface detail.
- Use AO maps if useful for the material.
- Keep material count under control.
- Use texture sizes appropriate for the camera distance.
- Test the asset in the real game scene, not only in isolation.

A hero asset can use more detail than a background prop.

---

## Unity Notes

When importing into Unity:

- Check the scale.
- Check material assignments.
- Assign Base Color to Albedo/Base Map.
- Assign Normal map to Normal Map.
- Mark the Normal map texture as a normal map if Unity asks.
- Connect AO if your shader supports it.
- Check texture compression settings.

Use lower texture sizes for mobile or standalone VR projects.

---

## Unreal Engine Notes

When importing into Unreal Engine:

- Check scale and orientation.
- Check material slots.
- Connect Base Color to Base Color.
- Connect Normal map to Normal.
- Connect AO to Ambient Occlusion if used.
- Review texture compression settings.
- Test the asset under realtime lighting.

For Nanite workflows, you may use more geometry, but baked lightweight assets are still useful for VR, mobile, web, and interactive applications.

---

## Web and Realtime Viewers

For web viewers or lightweight realtime presentation:

- Prefer GLB when possible.
- Keep texture sizes moderate.
- Reduce material count.
- Keep mesh density low.
- Test loading time.
- Test performance on the target device.

A smaller asset is easier to share, load, and display interactively.

---

## Keep the Original Scan

Do not delete the original high-poly scan.

Keep it as the source asset for:

- Future re-bakes.
- Higher quality exports.
- Archival preservation.
- Different texture resolutions.
- Different optimization targets.

ScanReady 1.0 creates a practical production version, while the original scan remains your high-detail source.

---

## Final Checklist

Before delivery or export, check:

- Mesh is optimized.
- UVs are present.
- Base Color bake looks correct.
- Normal map looks correct if used.
- AO map looks correct if used.
- Texture files are saved.
- File size is acceptable.
- Asset performs well in the target environment.
