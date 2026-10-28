# Export Tips

After using ScanReady, you can export the optimized, baked asset for VR, AR, video games, realtime viewers or other 3D production workflows.

The goal is to keep the model light enough for realtime use while preserving the original scan's visual detail through baked textures.

---

## Before Exporting

Before export, check that:

- the final mesh is selected;
- the optimized mesh has UVs;
- the baked material is assigned;
- texture files have been saved if you need external images;
- the object's scale is correct;
- the object's origin is positioned where needed;
- mesh density is suitable for the target platform.

!!! tip "Realtime"
    For VR and video games, performance matters as much as visual quality.

---

ScanReady prepares meshes, materials and textures. To export the model, use Blender's **File > Export** and choose the format required by the destination.

## Recommended Export Formats

### glTF / GLB

Use **glTF** or **GLB** for modern realtime workflows.

Suitable for:

- web viewers;
- realtime previews;
- many game engines;
- AR/VR pipelines;
- lightweight asset delivery.

`GLB` stores the model and textures in a single file, useful for sharing and previews.

### FBX

Use **FBX** when the target pipeline requires it.

Suitable for:

- Unity workflows;
- Unreal Engine workflows;
- DCC-to-engine transfers;
- teams already using FBX as a standard.

FBX can work well, but texture connections may need checking after import.

### OBJ

Use **OBJ** for simple exchange of static meshes.

Suitable for:

- basic geometry transfer;
- simple archive workflows;
- compatibility with many tools.

OBJ is simple, but less complete than glTF or FBX for modern material workflows.

---

## Texture Maps

Depending on the settings, ScanReady can create:

- Base Color textures;
- normal maps;
- roughness maps;
- ambient occlusion maps.

When exporting to another application, make sure the external software uses the correct texture files.

### Base Color

Connect this texture to the main color or albedo input.

### Normal Map

Connect this texture to the normal input.

In some software, you may need to set the image type to **Non-Color** or **Normal Map**.

### Roughness Map

Connect this texture to the roughness input when the target material supports it.

Roughness maps must be treated as **Non-Color** data.

### Ambient Occlusion

Connect this texture to the AO input if the target engine supports it.

Some workflows combine AO with other maps, depending on the engine or material setup.

---

## Texture Resolution

Choose texture size based on the final use.

### 1024

Good for small props, background objects, mobile VR or lightweight previews.

### 2048

A good general choice for many assets.

### 4096

Useful for close-up objects or important assets.

### 8192

Use only when very high detail is needed.

!!! warning "Large textures"
    Large textures increase memory usage, file size, loading time and realtime cost.

---

## VR Optimization

For VR, keep assets particularly lightweight.

VR requires stable performance because the scene must render smoothly for both eyes.

Before exporting for VR:

- reduce polygon count as much as possible;
- use baked textures instead of heavy geometry;
- avoid unnecessarily large texture sizes;
- use normal maps to preserve surface detail;
- test the asset in the target VR environment;
- prefer fewer materials when possible.

!!! warning "Standalone VR"
    A model that seems lightweight on desktop may still be too heavy for standalone VR headsets.

---

## Video Game Optimization

For video games, balance quality and performance.

Before exporting to a game engine:

- keep polygon count suitable for the asset's size;
- use texture detail instead of excessive geometry;
- use normal maps for surface detail;
- use an AO map if useful for the material;
- keep material count under control;
- use texture sizes suited to camera distance;
- test the asset in the actual game scene, not only in isolation.

A hero asset can use more detail than a background prop.

---

## Unity Notes

When importing into Unity:

- check scale;
- check material assignments;
- assign Base Color to Albedo/Base Map;
- assign the normal map to Normal Map;
- mark the normal texture as a normal map if Unity asks;
- assign Roughness/Smoothness according to the shader you use;
- connect AO if the shader supports it;
- check texture compression settings.

Use lower texture sizes for mobile or standalone VR projects.

---

## Unreal Engine Notes

When importing into Unreal Engine:

- check scale and orientation;
- check material slots;
- connect Base Color to Base Color;
- connect the normal map to Normal;
- connect Roughness to Roughness;
- connect AO to Ambient Occlusion if used;
- check texture compression settings;
- test the asset under realtime lighting.

For Nanite workflows you can use more geometry, but lightweight baked assets remain useful for VR, mobile, web and interactive applications.

---

## Web and Realtime Viewers

For web viewers or lightweight realtime presentations:

- prefer GLB when possible;
- keep texture sizes moderate;
- reduce the number of materials;
- keep mesh density low;
- test loading time;
- test performance on the target device.

A smaller asset is easier to share, load and display interactively.

---

## Keep the Original Scan

!!! warning "Keep the source"
    Do not delete the original high-poly scan.

Also keep a copy from before ScanReady preparation, because Mesh Settings options can modify the source. You will need it for:

- future bakes;
- higher-quality exports;
- archival preservation;
- different texture resolutions;
- different optimization targets.

ScanReady creates a practical production version, while the original scan remains your high-detail source.

---

## Final Checklist

Before delivery or export, check that:

- the mesh is optimized;
- UVs are present;
- the Base Color bake looks correct;
- the normal map looks correct if used;
- the roughness map looks correct if used;
- the AO map looks correct if used;
- texture files are saved;
- the **Bake Folder** button in Step 3 opens the last saved texture folder;
- file size is acceptable;
- the asset works well in the target environment.
