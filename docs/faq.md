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
- Increasing low-poly density slightly
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

## Why does the low-poly mesh look too smooth?

If the optimized mesh loses too much shape detail:

- Increase **Final Faces**
- Use a higher **Optimize / Reduce** value
- Avoid very aggressive reduction on detailed assets

Some scans require more geometry to preserve important silhouettes correctly.

## I used One Click Bake, but the final model is still too heavy. What should I do?

One Click Bake uses the current Step 1 optimization settings. If the final model is not optimized enough, you can refine it manually without starting from scratch.

This also applies if you are already working in Step 2 or Step 3. You can always go back to Step 1, change the reduction, and continue forward again.

Try this workflow:

- Go back to **Step 1 - Preview / Reduce**
- Lower **Final Faces**, or lower **Optimize / Reduce**
- Click **Create Lowpoly Preview** again
- Inspect the preview with **Show Wireframe** or **Show Adaptive Weights**
- Go to **Step 2 - UV / Cage** and click **Generate UVs** again
- Go to **Step 3 - Bake / Output** and run **Bake Textures** again

If the object is a vehicle, mechanical asset, architectural scan, or another hard-surface object, try the **Hard Surface** Adaptive Reduce preset. For faster tests on very dense scans, enable **Fast Adaptive Reduce** in Advanced before creating the preview again.

Lower values create lighter assets, but very aggressive reduction can damage silhouettes or important details. Use the preview step to find the best balance before baking again.

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



