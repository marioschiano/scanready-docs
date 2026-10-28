# Why ScanReady?

Photogrammetry scans retain a great deal of detail, but often contain millions of polygons, numerous materials and heavy textures. ScanReady brings together the steps needed to create a lighter version in Blender: preparation, reduction, UVs, cage and baking.

<p align="center">
  <img src="../img/hero.jpg" alt="From raw scan to optimized asset" style="max-width:820px;width:100%;" decoding="async" fetchpriority="high">
</p>

## What It Simplifies

- Preparing imported scans as objects or mesh hierarchies.
- Creating and inspecting a low-poly preview.
- Automatically generating UVs with Smart UV Project.
- Estimating the cage to transfer details from the source.
- Baking selected maps and connecting final materials.
- Saving textures for use in other applications.

Start with **One Click Bake** for a first version, or control each stage with the manual steps.

## Adaptive Reduction

**Adaptive Reduce** calculates weights that help protect normal changes, edges and surface details. The Decimate modifier uses these weights to simplify less important areas more aggressively.

<p align="center">
  <img src="../img/why-scanready-adaptive-optimization.jpg" alt="Adaptive Reduce comparison" style="max-width:1000px;width:100%;" loading="lazy" decoding="async">
</p>

The result depends on the scan and the chosen density. Check the silhouette, thin parts and details that must remain visible up close.

## Polygons and Materials in One Workflow

ScanReady does more than optimize geometry. The workflow also prepares UVs, materials and textures to transfer scan detail to a lighter, realtime-ready asset.

<div class="sr-uv-compare" data-uv-compare>
  <div class="sr-uv-compare__image">
    <img src="../img/adaptive-original.png" alt="Original textured scan" class="sr-uv-compare__base" loading="lazy" decoding="async">
    <div class="sr-uv-compare__overlay">
      <img src="../img/adaptive-weights.png" alt="Adaptive Reduce weights displayed in color" class="sr-uv-compare__top" loading="lazy" decoding="async">
    </div>
    <span class="sr-uv-compare__label sr-uv-compare__label--left">Original scan</span>
    <span class="sr-uv-compare__label sr-uv-compare__label--right">Adaptive reduction</span>
    <span class="sr-uv-compare__adaptive-gradient" aria-label="Adaptive weight gradient from minimum to high reduction"><span class="sr-uv-compare__adaptive-gradient-bar"></span><span class="sr-uv-compare__adaptive-gradient-labels"><span>Minimum reduction</span><span>Medium reduction</span><span>High reduction</span></span></span>
    <button class="sr-uv-compare__handle" type="button" aria-label="Compare the original scan and Adaptive Reduce weights" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50"><span></span></button>
  </div>
</div>

<p align="center"><strong>Move the slider to compare the scan and Adaptive Reduce weights.</strong></p>

!!! note "Optimization and retopology"
    ScanReady uses polygon reduction: it does not automatically create quad topology suitable for animation. Models that need to deform may require a dedicated retopology pass.

## Detail in Textures

UVs and baking transfer visual detail from the high-poly scan to the optimized mesh. Geometry retains the main shape, while textures preserve color and surface details.

**Bake Materials** can distribute the result across multiple texture sets. An efficient UV layout helps use the available resolution, but the final choice should also consider memory and material count.

## One Workflow, Two Ways to Work

| Workflow | When to use it |
|---|---|
| **One Click Bake** | To automate the main stages and obtain a first result. |
| **Manual Quick Guide** | To check reduction, UVs, cage and baking separately. |
| **Advanced** | To adapt settings to a difficult scan or specific requirements. |

If the result needs correction, return to the relevant step and regenerate the following stages. You do not need to change every advanced setting to get started.

## Who It's For

ScanReady is designed for photogrammetry artists, environment artists and creators of assets for video games, VR, AR and realtime visualization. It is also useful for interactive versions of artifacts, museum collections and cultural heritage.

Keep an intact copy of the scan for your archive. The optimized version is intended for presentation and production; preparation options can modify the working source.

## From Model to Final Project

1. Import the scan and save a copy of the project.
2. Create and check the low-poly preview.
3. Generate UVs and check the cage.
4. Bake the required textures.
5. Export using Blender's tools and check the asset at its destination.

[Start with the quick start guide](quick-start.md) or explore the [use cases](use-cases.md).

## ScanReady Philosophy

**Fast. Clean. Game-ready.**

Less repetitive setup, more control over the scan's result.
