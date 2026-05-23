# FAQ

## How can I contact support?

For support, bug reports, or workflow questions, contact:

<a href="mailto:support.marioschiano3d@gmail.com"><strong>support.marioschiano3d@gmail.com</strong></a>

## Why are the UVs overlapping?

UV overlapping can happen when the mesh is extremely dense or when UV islands do not have enough spacing.

To improve the result:

- Increase **UV Padding**
- Try a different **Smart UV Angle**
- Generate UVs again
- Reduce extremely small mesh fragments before unwrapping

Well-spaced UV islands help prevent texture bleeding and baking artifacts.

## Why does the bake look noisy or dirty?

Noisy baked textures are usually caused by insufficient texture resolution, incorrect cage settings, or overly aggressive optimization.

Try:

- Increasing **Texture Size**
- Increasing **Bake Samples**
- Increasing lowpoly density slightly
- Adjusting **Cage Extrusion**
- Checking the cage preview before baking

Very dense scans may also require multiple bake materials for cleaner texture quality.

## Why is GPU baking still slow?

Large scans and high resolution textures can still require significant processing time even on powerful GPUs.

Bake speed depends on:

- Texture resolution
- Number of bake materials
- Scan complexity
- GPU VRAM
- Enabled bake maps

To improve performance:

- Lower texture resolution
- Disable unnecessary bake maps
- Reduce bake materials when possible
- Use lower bake samples for preview tests

## Why does the lowpoly mesh look too smooth?

If the optimized mesh loses too much shape detail:

- Increase **Final Faces**
- Use a higher **Optimize / Reduce** value
- Avoid very aggressive reduction on detailed assets

Some scans require more geometry to preserve important silhouettes correctly.

## Why are visible seams appearing in the baked texture?

Visible seams can appear when UV islands have insufficient padding or when texture resolution is too low.

Try:

- Increasing **UV Padding**
- Increasing texture resolution
- Checking the checker preview before baking
- Re-generating UVs with different settings

Proper UV packing and padding help reduce visible seams.

## Why does ScanReady recommend multiple bake materials?

Large scans often contain more detail than a single texture can preserve efficiently.

Using multiple bake materials increases available texture space and helps preserve more detail across the asset.

ScanReady can automatically recommend an appropriate number of materials depending on scan complexity and texture detail requirements.

## Why does the optimized mesh look different from the original scan?

Optimization reduces polygon density to improve realtime performance.

Some visual differences are normal because unnecessary geometry is simplified.

However, ScanReady uses adaptive optimization to preserve important surface details while simplifying flatter or less detailed regions more aggressively.



