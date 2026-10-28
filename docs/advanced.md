# <span class="sr-addon-icon sr-icon-settings" title="Advanced"></span>Advanced Settings

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:16px; margin-bottom:30px;">

<div style="flex:1 1 0; min-width:0;">

<p>
Advanced settings provide precise control over mesh cleanup, adaptive reduction, UV generation, bake quality, image output, presets, diagnostics and memory safety.
</p>

<p>
Advanced is the most technical part of ScanReady. Here you can adjust the core workflow to go beyond the automatic result, refine a difficult scan or adapt the process to an asset intended for VR, video games or realtime use.
</p>

<p>
You do not need to change every setting to use ScanReady. For most scans, start with the defaults and make changes only when you need more control over quality, performance, bake accuracy or detail protection.
</p>

<p>
The settings follow the order of the add-on panel. The sections below explain what changes, when to intervene and which stage to regenerate after a change.
</p>

<p>
Work gradually: first create a low-poly preview with default settings, then return to Advanced only to correct something or improve the result.
</p>

<div class="admonition tip">
  <p class="admonition-title">Work step by step</p>
  <p>If you change settings affecting the mesh, Adaptive Reduce or UVs, regenerate the corresponding step before continuing.</p>
</div>

<p>
The main sections follow the workflow. Mesh Settings prepares and cleans the scan before the low-poly preview. Adaptive Reduce controls how ScanReady protects details, edges and normal changes during reduction. UV Settings manages the UV unwrap used for baking.
</p>

<p>
Bake Settings controls samples, margins, normal strength, image format, Occlusion options and memory safety. Base Color, Normal, Roughness and Occlusion maps are selected in Step 3. Presets, Diagnostics and Utilities help with heavy workflows, testing, reusing settings and quickly restoring a clean configuration.
</p>
</div>

<div style="flex:0 0 320px; text-align:center;">
  <p style="margin-top:0;"><strong>Advanced</strong></p>
  <img src="../img/advanced_global.jpg" alt="ScanReady Advanced settings overview" style="width:260px; max-width:100%;" decoding="async" fetchpriority="high">
</div>

</div>

## <span class="sr-addon-icon sr-icon-mesh" title="Mesh Settings"></span>Mesh Settings

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:16px; margin-bottom:30px;">

<div style="flex:1 1 0; min-width:0;">

<p>These settings control scan preparation before the preview. Some affect the high-poly source: save a copy of the project before starting.</p>

</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Mesh Settings</strong></p>
  <img src="../img/advanced_mesh_settings.jpg" alt="ScanReady Mesh Settings screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Pre-Decimate Merge</h3>

<p>
Performs Merge by Distance cleanup on the duplicated preview mesh before adding the Decimate modifier.
</p>

<p>
Merges preview vertices within the specified distance in centimeters. It does not automatically remove every overlapping face: use a small distance to avoid merging details that should remain separate.
</p>

<div class="admonition warning">
  <p class="admonition-title">If holes appear</p>
  <p>If holes appear after optimization or thin details are affected, lower the value and recreate the low-poly preview.</p>
</div>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Pre-Decimate Merge</strong></p>
  <img src="../img/advanced_pre_decimate.jpg" alt="ScanReady Pre-Decimate Merge screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Auto Fix Normals</h3>

<p>
Automatically recalculates high-poly mesh normals before creating the low-poly preview.
</p>

<p>
Enable it when the scan has inverted normals, inconsistent shading or bake artifacts caused by incorrect normal directions.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Auto Fix Normals</strong></p>
  <img src="../img/advanced_autofix_normals.jpg" alt="ScanReady Auto Fix Normals screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<div style="margin:18px 0 30px; text-align:center;">
  <img src="../img/advanced_autofix_normals.gif" alt="ScanReady Auto Fix Normals detail" style="width:760px; max-width:100%;" loading="lazy" decoding="async">
</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Auto Clear Sharp Edges</h3>

<p>
Automatically removes sharp-edge markings from the mesh during preparation.
</p>

<p>
This is useful when an imported scan has unwanted sharp edges that cause hard shading or less clean bakes.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Auto Clear Sharp Edges</strong></p>
  <img src="../img/advanced_autoclear_sharp.jpg" alt="ScanReady Auto Clear Sharp Edges screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<div style="margin:18px 0 30px; text-align:center;">
  <img src="../img/advanced_autoclear_sharp_edge.gif" alt="ScanReady Auto Clear Sharp Edges detail" style="width:760px; max-width:100%;" loading="lazy" decoding="async">
</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Auto Combine Mesh Parts</h3>

<p>
Automatically combines scan mesh parts when working with imports made of many separate objects. It is enabled by default.
</p>

<p>
ScanReady checks whether the selection contains a hierarchy with multiple meshes to combine. If the scan is already one mesh, it does not perform a merge.
</p>

<p>
Leave it enabled in most cases, especially for photogrammetry scans, GLB or FBX files split into multiple elements. Disable it only if automatic merging causes problems or you intentionally want to keep mesh parts separate.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Auto Combine Mesh Parts</strong></p>
  <img src="../img/advanced_autocombine_mesh.jpg" alt="ScanReady Auto Combine Mesh Parts screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<div style="margin:18px 0 30px; text-align:center;">
  <img src="../img/advanced_autocombine_mesh.gif" alt="ScanReady Auto Combine Mesh Parts detail" style="width:760px; max-width:100%;" loading="lazy" decoding="async">
</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Auto Clean Scan Debris</h3>

<p>
Removes common scan debris such as isolated fragments, floating polygons and unnecessary vertices before reduction.
</p>

<p>
It is enabled by default because many raw scans contain small floating parts that can slow optimization, UVs and baking.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Auto Clean Scan Debris</strong></p>
  <img src="../img/advanced_autoclean_scan.jpg" alt="ScanReady Auto Clean Scan Debris screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<div style="margin:18px 0 30px; text-align:center;">
  <img src="../img/advanced_auto_clean_scan.gif" alt="Removing fragments with Auto Clean Scan Debris" style="width:760px; max-width:100%;" loading="lazy" decoding="async">
</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Convert Source Materials</h3>

<p>
Converts the scan's source materials into a cleaner, more predictable configuration for the ScanReady workflow.
</p>

<p>
Some imported models, especially from GLB files, Sketchfab or online libraries, can use complex materials or connections unsuitable for baking. For example, a diffuse texture may be connected to Emission instead of Base Color.
</p>

<p>
When this option is enabled, ScanReady checks the source materials.
</p>

<div class="admonition info">
  <p class="admonition-title">When to convert materials</p>
  <p>If ScanReady finds a standard <strong>Principled BSDF</strong> material, it leaves it unchanged and only protects the material and textures with fake users.</p>
  <p>If it finds complex imported shaders, it rebuilds a cleaner, more predictable material.</p>
</div>

<p>
It is disabled by default. Enable it only if the bake does not turn out well, for example if Base Color is black, incomplete or inconsistent, or imported materials are not read correctly by ScanReady.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Convert Source Materials</strong></p>
  <img src="../img/advanced_convert_source.jpg" alt="ScanReady Convert Source Materials screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>
</div>
<div class="sr-uv-compare" data-uv-compare>
  <div class="sr-uv-compare__image">
    <img src="../img/advanced_convert_source_materials.jpg" alt="Original material with non-standard nodes" class="sr-uv-compare__base" loading="lazy" decoding="async">
    <div class="sr-uv-compare__overlay">
      <img src="../img/advanced_convert_source_materials2.jpg" alt="Converted material with standard Principled BSDF" class="sr-uv-compare__top" loading="lazy" decoding="async">
    </div>
    <span class="sr-uv-compare__label sr-uv-compare__label--left">Original material</span>
    <span class="sr-uv-compare__label sr-uv-compare__label--right">Converted material</span>
    <span class="sr-uv-compare__material sr-uv-compare__material--left"><strong>Non-standard nodes</strong><small>Imported shader</small></span>
    <span class="sr-uv-compare__material sr-uv-compare__material--right"><strong>Principled BSDF</strong><small>Standard material</small></span>
    <button class="sr-uv-compare__handle" type="button" aria-label="Compare the original material and the material converted to Principled BSDF" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50"><span></span></button>
  </div>
</div>

<p align="center"><strong>Move the slider to compare the original and converted materials.</strong></p>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Show Face Orientation</h3>

<p>
Shows Blender's <strong>Face Orientation</strong> overlay to quickly check whether model faces are oriented correctly.
</p>

<p>
In Blender, faces have a direction: one side is considered outside and the other inside. Inverted faces may look correct in the viewport but cause black areas, missing details, incorrect shadows or badly transferred textures during baking.
</p>

<p>
Use <strong>Show Face Orientation</strong> before creating the low-poly preview or baking to check for inverted normals. Faces highlighted in red normally indicate surfaces facing the wrong way and can cause bake problems.
</p>

<p>
When you enable <strong>Show Face Orientation</strong>, ScanReady automatically disables <strong>Backface Culling</strong> to avoid overlapping visual checks.
</p>

<div class="admonition note">
  <p class="admonition-title">Show Face Orientation and Backface Culling</p>
  <p>The two controls are intended for different checks and are mutually exclusive, keeping the viewport readable.</p>
</div>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Show Face Orientation</strong></p>
  <img src="../img/advanced_showface_orientation.jpg" alt="ScanReady Show Face Orientation screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<div style="margin:18px 0 30px; text-align:center;">
  <img src="../img/advanced_showface_orientation2.jpg" alt="ScanReady Show Face Orientation detail" style="width:760px; max-width:100%;" loading="lazy" decoding="async">
</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Backface Culling</h3>

<p>
Enables viewport <strong>Backface Culling</strong> to check how faces behave when viewed from behind.
</p>

<p>
This display mode helps identify scan problems such as inverted faces, single-sided surfaces, holes, open parts or suspiciously oriented areas.
</p>

<p>
This check is important before baking: incorrectly oriented faces or open parts can cause black textures, missing details, incorrect shadows or incorrect transfers from the high-poly mesh to the optimized mesh, even if the model looks correct in the viewport.
</p>

<p>
<strong>Backface Culling</strong> is only a preview mode: it does not modify the mesh or directly change the bake. It helps inspect the scan before proceeding.
</p>

<p>
Backface Culling and Show Face Orientation are linked: enabling one automatically disables the other, so you inspect the scan with one diagnostic mode at a time.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Backface Culling</strong></p>
  <img src="../img/advanced_backface_culling.jpg" alt="ScanReady Backface Culling screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<div style="margin:18px 0 30px; text-align:center;">
  <img src="../img/advanced_backface_culling_2.jpg" alt="ScanReady Backface Culling detail" style="width:760px; max-width:100%;" loading="lazy" decoding="async">
</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Use Texture View</h3>

<p>
Enables Material Preview without scene lights and World. If Backface Culling is active, it instead uses Solid view with textures and flat lighting.
</p>

<p>
It helps inspect baked texture results or previews more clearly.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Use Texture View</strong></p>
  <img src="../img/advanced_usetexture_view.jpg" alt="ScanReady Use Texture View screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<div style="margin:18px 0 30px; text-align:center;">
  <img src="../img/advanced_use_texture_view.gif" alt="ScanReady Use Texture View detail" style="width:760px; max-width:100%;" loading="lazy" decoding="async">
</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Recalculate Outside Normals</h3>

<p>
Recalculates outward-facing normals on the high-poly source associated with the selection.
</p>

<p>
Use it when the scan looks inside out or has inconsistent shading.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Recalculate Outside Normals</strong></p>
  <img src="../img/advanced_recalculate_outside_normals.jpg" alt="ScanReady Recalculate Outside Normals screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<div style="margin:18px 0 30px; text-align:center;">
  <img src="../img/advanced_recaulate_outside.gif" alt="ScanReady Recalculate Outside Normals detail" style="width:760px; max-width:100%;" loading="lazy" decoding="async">
</div>

---

## <span class="sr-addon-icon sr-icon-decim" title="Adaptive Reduce"></span>Adaptive Reduce

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:16px; margin-bottom:30px;">

<div style="flex:1 1 0; min-width:0;">

<p>
Adaptive Reduce controls how ScanReady distributes reduction across the selected scan.
</p>

<p>
It is enabled by default and is designed to protect visually important detail while allowing flat surfaces to be simplified more.
</p>

<p>
Adaptive Reduce weights are calculated when you click <strong>Create Lowpoly Preview</strong>.
</p>

<div class="sr-adaptive-gradient-doc" aria-label="Adaptive weight gradient from minimum to high reduction">
  <div class="sr-adaptive-gradient-doc__bar"></div>
  <div class="sr-adaptive-gradient-doc__labels"><span>Minimum reduction</span><span>Medium reduction</span><span>High reduction</span></div>
</div>

<div class="admonition note">
  <p class="admonition-title">When to recalculate weights</p>
  <p>Changing <strong>Optimize / Reduce</strong> or <strong>Final Faces</strong> afterwards updates the amount of reduction, but does not recalculate adaptive weights.</p>
  <p>To apply a different Adaptive Reduce preset or detailed adaptive values, recreate the low-poly preview.</p>
</div>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Adaptive Reduce</strong></p>
  <img src="../img/adaptive-reduce-best-quality-balanced.png" alt="Adaptive Reduce panel with Best Quality and Balanced" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Adaptive Reduce</h3>

<p>
Enables or disables the adaptive reduction system.
</p>

<p>
When enabled, ScanReady analyzes the mesh and creates weights to protect important details, edges and normal changes while simplifying flat or less important areas more.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Adaptive Reduce</strong></p>
  <img src="../img/advanced_adaptive_reduce_01.jpg" alt="ScanReady Adaptive Reduce screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Adaptive Method</h3>

<p><strong>Best Quality</strong> is the recommended method. It first identifies large planar areas, then recovers persistent curvature, decorations and coherent reliefs. This allows noisy walls, floors and roofs to be reduced without treating real detail as mere scan noise.</p>

<p><strong>Legacy</strong> retains the original Adaptive Reduce calculation. Use it for compatibility with older projects or to compare a particular scan with previous behavior.</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Adaptive Method</strong></p>
  <img src="../img/adaptive-method-menu.png" alt="Adaptive Method menu with Best Quality and Legacy" style="width:230px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Adaptive Preset</h3>

<p>
Choose the preset best suited to the scan and target asset.
</p>

<ul>
<li><strong>Balanced</strong> is the default preset for most scans.</li>
<li><strong>Preserve Details</strong> more strongly protects complex or important surface regions.</li>
<li><strong>Flat Surfaces</strong> reduces broad, simple areas more aggressively.</li>
</ul>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Adaptive Preset</strong></p>
  <img src="../img/adaptive-preset-menu.png" alt="Adaptive Preset menu with Balanced, Preserve Details and Flat Surfaces" style="width:230px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Show Adaptive Weights</h3>

<p>
Shows a color preview of how ScanReady will distribute reduction across the scan.
</p>

<p>
Red areas represent flatter surfaces that can be reduced more. Blue and green areas represent regions protected for detail.
</p>

<p>
The display is only a preview aid. It helps choose the preset and understand reduction behavior; it is not an exported or baked texture.
</p>

<p>When the color map is active, ScanReady temporarily hides the wireframe for readability. Disabling Show Adaptive Weights restores the previous Show Wireframe setting.</p>

<div class="admonition note">
  <p class="admonition-title">Previously calculated weights</p>
  <p>Adaptive Reduce weights are calculated when you click <strong>Create Lowpoly Preview</strong>.</p>
  <p>After the preview exists, changing <strong>Optimize / Reduce</strong> or <strong>Final Faces</strong> updates the amount of reduction using the existing weights.</p>
  <p>If you change a preset or detailed Adaptive Reduce values, click <strong>Create Lowpoly Preview</strong> again to rebuild weights with the new settings.</p>
</div>

<p>
Use this preview for scans with mixed surfaces, such as flat architectural panels alongside sculptural or damaged details.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Show Adaptive Weights</strong></p>
  <img src="../img/advance_show_adaptive.png" alt="ScanReady Show Adaptive Weights screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>
<div style="margin:18px 0 30px; text-align:center;">
  <img src="../img/advance_show_adaptive_01.jpg" alt="ScanReady Show Adaptive Weights detail" style="width:760px; max-width:100%;" loading="lazy" decoding="async">
</div>
<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Adaptive Strength</h3>

<p>
This control appears only with the <strong>Legacy</strong> method and adjusts how strongly the original map affects reduction.
</p>

<p>
Best Quality does not use Adaptive Strength; it uses <strong>Adaptive Decimate Factor</strong> instead.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Adaptive Strength</strong></p>
  <img src="../img/advance_adaptive_reduce_strength.png" alt="ScanReady Adaptive Strength screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Adaptive Reduce Angle</h3>

<p>
Controls sensitivity to normal changes used to distinguish flat areas, curvature and details.
</p>

<p>
Lower values make ScanReady more sensitive to surface variations. Higher values tend to treat more areas as relatively uniform.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Adaptive Reduce Angle</strong></p>
  <img src="../img/advance_adaptive_reduce_angle.png" alt="ScanReady Adaptive Reduce Angle screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Detail Preserve</h3>

<p>
Sets the minimum reduction weight assigned to areas recognized as detail.
</p>

<p>
Lower values protect detected detail more. Higher values allow Decimate to reduce more even in detailed areas.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Detail Preserve</strong></p>
  <img src="../img/advance_adaptive_detail_preserve.png" alt="ScanReady Detail Preserve screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Smooth Weights</h3>

<p>
Smooths Adaptive Reduce weights to make the transition between protected and reduced areas more even.
</p>

<p>
Higher values can produce a less jagged distribution, useful for noisy scans or irregular surfaces.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Smooth Weights</strong></p>
  <img src="../img/advance_smooth_weight.png" alt="ScanReady Smooth Weights screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

### Best Quality Analysis Controls

| Parameter | Balanced | What it controls | Increase / decrease |
|---|---:|---|---|
| **Complexity Sensitivity** | 0.75 | How easily persistent curvature and geometric changes are classified as detail. | Increase for more green/blue and protected geometry; decrease for more aggressive reduction. |
| **Flat / Detail Contrast** | 1.30 | Separation between red planar and protected blue areas. | Increase for a sharper transition; decrease for a softer gradient. |
| **Detail Spread Rings** | 1 | How many neighboring vertex rings receive detected-detail protection. | Increase when reliefs, frames or decorations need surrounding support. High values can protect overly broad areas. |
| **Noise Rejection** | 0.85 | How much isolated variations that do not persist in the surrounding region are attenuated. | Increase to ignore more scan noise; decrease to retain more fine variations, including possible noise. |
| **Analysis Scale** | 4 | Number of connected rings used to distinguish coherent shape from local noise. | Increase for broader, slower analysis; decrease for a more local, noise-sensitive response. |
| **Adaptive Decimate Factor** | 2.0 | How strongly the weight map affects Decimate. It does not change the colors or how the map is calculated. | Normally use 1–5. Very high values accentuate the difference between red and blue but can create long or radial triangles. |

!!! tip "Recommended adjustment"
    Always start with **Balanced** and **Adaptive Decimate Factor 2**. Change one parameter at a time, recreate the preview and check both the color map and resulting wireframe.

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Fast Adaptive Reduce</h3>

<p>
Uses a faster, approximate adaptive calculation mode.
</p>

<p>
It uses fewer neighbors, a smaller analysis scale, no final smoothing and at most one detail-expansion ring. Useful for quick tests on very dense scans; disable it for the final quality check.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Fast Adaptive Reduce</strong></p>
  <img src="../img/advance_fast_adaptive_.png" alt="ScanReady Fast Adaptive Reduce screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Protect Feature Edges</h3>

<p>
Protects important edges and sharp surface breaks during reduction.
</p>

<p>
Recommended for hard-surface scans, vehicles, architecture, objects with visible edges or important silhouettes.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Protect Feature Edges</strong></p>
  <img src="../img/advance_feature_edge.png" alt="ScanReady Protect Feature Edges screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Feature Edge Angle</h3>

<p>
Defines the minimum angle used to consider an edge a feature edge that should be protected.
</p>

<p>
Lower values protect more edges. Higher values protect only sharper direction changes.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Feature Edge Angle</strong></p>
  <img src="../img/advance_edge_angle.png" alt="ScanReady Feature Edge Angle screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Feature Edge Rings</h3>

<p>
Extends feature-edge protection to neighboring geometry rings.
</p>

<p>
This can help keep the shape more stable around sharp edges, frames, panels or prominent scan boundaries.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Feature Edge Rings</strong></p>
  <img src="../img/advance_edge_rings.png" alt="ScanReady Feature Edge Rings screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

---

## <span class="sr-addon-icon sr-icon-uv" title="UV Settings"></span>UV Settings

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:16px; margin-bottom:30px;">

<div style="flex:1 1 0; min-width:0;">

<p>
These settings control how Smart UV Project unwraps the optimized mesh.
</p>

<div class="admonition note">
  <p class="admonition-title">When UV settings are applied</p>
  <p>UV settings are applied when ScanReady generates UVs.</p>
  <p>If you change UV values after creating the layout, click <strong>Generate UVs</strong> again or run <strong>One Click Bake</strong> from the beginning.</p>
  <p><strong>Bake Textures</strong> always uses the UV layout that already exists at bake time.</p>
</div>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>UV Settings</strong></p>
  <img src="../img/advance_uv_settings.png" alt="ScanReady UV Settings screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Smart UV Angle</h3>

<p>
Controls how much Smart UV Project divides the mesh into UV islands.
</p>

<ul>
<li>Lower values create more cuts and more UV islands.</li>
<li>Higher values create larger islands.</li>
</ul>

<p>
You can adjust this value manually for more control over the unwrap used for baking.
</p>

<p>
Adaptive Reduce presets are separate from UV generation: Adaptive Reduce controls mesh simplification, while Smart UV Project controls the UV unwrap.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Smart UV Angle</strong></p>
  <img src="../img/advance_uv_smart_uv.png" alt="ScanReady Smart UV Angle screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>UV Padding</h3>

<p>
Sets the space between UV islands.
</p>

<p>
Increase padding to reduce texture bleeding, especially at lower texture resolutions.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>UV Padding</strong></p>
  <img src="../img/advance_uv_padding.png" alt="ScanReady UV Padding screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

---

## <span class="sr-addon-icon sr-icon-texture" title="Texture Detail"></span>Texture Detail

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:16px; margin-bottom:30px;">

<div style="flex:1 1 0; min-width:0;">

<p>
This section is in <strong>Advanced</strong> after <strong>UV Settings</strong> and before <strong>Bake Settings</strong>.
</p>

<p>
It analyzes the high-poly source and optimized UV mesh to estimate whether the current texture size and number of bake materials can preserve enough scan detail.
</p>

<p>
Use <strong>Analyze Texture Detail</strong> after generating UVs and before baking when you want help deciding whether to increase texture resolution, increase bake materials or improve UV packing.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Texture Detail</strong></p>
  <img src="../img/advance_texture_detail.png" alt="ScanReady Texture Detail screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

---

## <span class="sr-addon-icon sr-icon-render" title="Bake Settings"></span>Bake Settings

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:16px; margin-bottom:30px;">

<div style="flex:1 1 0; min-width:0;">

<p>
These settings control samples, margin, normal strength, image format quality, Occlusion options and memory safety.
</p>

<p>
In the add-on, <strong>Occlusion Settings</strong> and <strong>Memory Safety</strong> are inside <strong>Bake Settings</strong>. Some controls appear only when the corresponding option is enabled.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Bake Settings</strong></p>
  <img src="../img/advance_bake_settings.png" alt="ScanReady Bake Settings screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Bake Samples</h3>

<p>
Sets the number of Cycles samples used for baking.
</p>

<p>
Higher values can reduce noise, especially for Ambient Occlusion, but also increase bake time.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Bake Samples</strong></p>
  <img src="../img/advance_bake_sample.png" alt="ScanReady Bake Samples screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Bake Margin</h3>

<p>
Adds pixel padding around baked UV islands.
</p>

<p>
It helps reduce visible seams and texture bleeding.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Bake Margin</strong></p>
  <img src="../img/advance_bake_margin.png" alt="ScanReady Bake Margin screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Normal Strength</h3>

<p>
Appears when <strong>Bake Normal Map</strong> is enabled.
</p>

<p>
Controls the strength of the Normal Map node in the final material. It changes only the material's appearance, not the baked normal texture.
</p>

<p>
If <strong>Bake Normal Map</strong> is disabled, this control does not appear and the image format control, such as <strong>JPG Quality</strong>, appears directly after <strong>Bake Margin</strong>.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Normal Strength</strong></p>
  <img src="../img/advanced_adaptive_normal_strenght.jpg" alt="ScanReady Normal Strength screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>JPG Quality</h3>

<p>
Controls JPG compression quality when JPG is the selected image format.
</p>

<p>
Higher values preserve more image detail but produce larger files.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>JPG Quality</strong></p>
  <img src="../img/advance_bake_jpg_quality.png" alt="ScanReady JPG Quality screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>TIFF 16-bit</h3>

<p>
Enables higher-precision TIFF output when TIFF is selected.
</p>

<p>
This can be useful for detailed assets, archival workflows or technical texture output.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>TIFF 16-bit</strong></p>
  <img src="../img/advanced_tiff_16bit.jpg" alt="ScanReady TIFF 16-bit screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

---

### <span class="sr-addon-icon sr-icon-step3" title="Occlusion Settings"></span>Occlusion Settings

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:16px; margin-bottom:30px;">

<div style="flex:1 1 0; min-width:0;">

<p>
These options are inside <strong>Bake Settings</strong> and appear when <strong>Bake Occlusion Map</strong> is enabled.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Occlusion Settings</strong></p>
  <img src="../img/advanced_occlusion_settings.jpg" alt="ScanReady Occlusion Settings screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h4>AO Source</h4>

<p>
Controls whether Ambient Occlusion is baked from the high-poly source to the low-poly target or calculated only from the low-poly mesh.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>AO Source</strong></p>
  <img src="../img/advanced_ao_source.png" alt="ScanReady AO Source screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h4>Auto AO Distance</h4>

<p>
Automatically calculates AO distance based on model size.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Auto AO Distance</strong></p>
  <img src="../img/advanced_auto_ao_distance.png" alt="ScanReady Auto AO Distance screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h4>AO Distance</h4>

<p>
Manual AO ray distance when automatic distance is disabled.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>AO Distance</strong></p>
  <img src="../img/advanced_ao_distance.png" alt="ScanReady AO Distance screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h4>AO Samples</h4>

<p>
Controls Ambient Occlusion bake quality.
</p>

<p>
Higher values produce cleaner AO but increase bake time.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>AO Samples</strong></p>
  <img src="../img/advanced_ao_sample.png" alt="ScanReady AO Samples screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h4>AO Mix</h4>

<p>
Controls how much the baked Ambient Occlusion texture darkens the final Base Color material.
</p>

<p>
The default value is <strong>1.0</strong>, which uses the full baked AO texture in the final material. Lower values make the AO effect subtler.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>AO Mix</strong></p>
  <img src="../img/advanced_ao_mix.png" alt="ScanReady AO Mix screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

---

### <span class="sr-addon-icon sr-icon-memory" title="Memory Safety"></span>Memory Safety

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:16px; margin-bottom:30px;">

<div style="flex:1 1 0; min-width:0;">

<p>
These options are inside <strong>Bake Settings</strong> and help reduce memory problems during demanding bake operations.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Memory Safety</strong></p>
  <img src="../img/advanced_memory_safe.png" alt="ScanReady Memory Safety screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h4>Safe Memory Bake</h4>

<p>
Uses a safer baking workflow designed to reduce memory pressure for large scans and heavy Blender scenes.
</p>

<p>
Leave it enabled when working with dense photogrammetry assets or high texture resolutions.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Safe Memory Bake</strong></p>
  <img src="../img/advanced_safe_memory.png" alt="ScanReady Safe Memory Bake screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h4>Force CPU Baking</h4>

<p>
Performs the bake on the CPU when GPU VRAM is insufficient. It still requires enough system RAM.
</p>

<p>
It is usually slower but can be safer on systems with little VRAM.
</p>

<p>
ScanReady can enable it automatically when multi-material baking is used.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Force CPU Baking</strong></p>
  <img src="../img/advanced_force_cpu.png" alt="ScanReady Force CPU Baking screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

---

## Presets

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:16px; margin-bottom:30px;">

<div style="flex:1 1 0; min-width:0;">

<p>
ScanReady can save, reload and delete named presets.
</p>

<p>
Presets save current workflow settings so you can reuse them later.
</p>

<p>
Use presets when working on multiple scans with similar requirements, such as:
</p>

<ul>
<li>VR assets;</li>
<li>game props;</li>
<li>museum objects;</li>
<li>repeated bake settings;</li>
<li>standard studio workflows.</li>
</ul>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Preset</strong></p>
  <img src="../img/advanced_presets.png" alt="ScanReady Preset screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Preset Name</h3>

<p>
Defines the name of the preset to save.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Preset Name</strong></p>
  <img src="../img/advanced_presets_name.png" alt="ScanReady Preset Name screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Save Preset</h3>

<p>
Saves workflow parameters: mesh, reduction, display, UVs, cage, textures, bake, memory and output folder. It does not save scene objects, generated images or update preferences.
</p>
<p>
When reloading a preset, also check <strong>Output Folder</strong> before starting a new bake.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Save Preset</strong></p>
  <img src="../img/advanced_presets_save.png" alt="ScanReady Save Preset screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Preset Selector</h3>

<p>
Lets you choose an existing preset.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Preset Selector</strong></p>
  <img src="../img/advanced_preset_selector.png" alt="ScanReady Preset Selector screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Reload Preset</h3>

<p>
Loads the selected preset.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Reload Preset</strong></p>
  <img src="../img/advanced_reload_presets.png" alt="ScanReady Reload Preset screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<hr>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Delete Preset</h3>

<p>
Deletes the selected preset.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Delete Preset</strong></p>
  <img src="../img/advanced_delete_presets.png" alt="ScanReady Delete Preset screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

---

## <span class="sr-addon-icon sr-icon-diagnostics" title="Diagnostics"></span>Diagnostics

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:16px; margin-bottom:30px;">

<div style="flex:1 1 0; min-width:0;">

<p>
Diagnostic options help you see what ScanReady is doing during testing or performance optimization.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Diagnostics</strong></p>
  <img src="../img/advanced_diagnostic.png" alt="ScanReady Diagnostics screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Show Diagnostic Timing Report</h3>

<p>
Shows a detailed timing report after <strong>ONE CLICK BAKE</strong>.
</p>

<p>
The report can include Preview / Reduce, Generate UVs, Auto Cage, Bake / Finalize, Adaptive / Decimate and individual bake sub-stage times.
</p>

<div class="admonition info">
  <p class="admonition-title">Recommended use</p>
  <p>Keep <strong>Show Diagnostic Timing Report</strong> disabled during videos, demos and normal use. Enable it to compare performance or find out which stage takes the most time.</p>
</div>

<p>
It is disabled by default to keep the panel cleaner during normal use, demos and videos. Enable it only when analyzing performance or comparing settings.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Show Diagnostic Timing Report</strong></p>
  <img src="../img/advanced_diagnostic_02.png" alt="ScanReady Show Diagnostic Timing Report screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

---

## <span class="sr-addon-icon sr-icon-utility" title="Utilities"></span>Utilities

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:16px; margin-bottom:30px;">

<div style="flex:1 1 0; min-width:0;">

<p>
Utility tools help reset or restore the add-on configuration.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Utilities</strong></p>
  <img src="../img/advanced_utilities.png" alt="ScanReady Utilities screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:20px; margin-bottom:28px;">

<div style="flex:1 1 0; min-width:0;">
<h3>Reset Defaults</h3>

<p>
Restores ScanReady settings to their default values.
</p>

<p>
Use it if current settings produce unexpected results or you want to return to a clean configuration.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Reset Defaults</strong></p>
  <img src="../img/advanced_utilities_reset.png" alt="ScanReady Reset Defaults screenshot" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

---

## <span class="sr-addon-icon sr-icon-preferences" title="Addon Preferences / Updates"></span>Addon Preferences / Updates

<p>
ScanReady includes a small support section in Blender Add-on Preferences.
</p>

<p>
Here you can check the installed version, manually check for a newer version, open the documentation, read release notes and reach video tutorials.
</p>

<p>
Official updates are installed through Blender Extensions / Superhive. ScanReady's internal check is informational and only reports that a newer version is available.
</p>

<div style="text-align:center; margin-top:18px; margin-bottom:34px;">
  <p style="margin-top:0;"><strong>Addon Preferences / Updates</strong></p>
  <img src="../img/advanced_addon_preferences.jpg" alt="ScanReady Addon Preferences / Updates screenshot" style="max-width:760px; width:100%;" loading="lazy" decoding="async">
</div>

<h3>Installed version</h3>

<p>
Shows the ScanReady version currently installed in Blender.
</p>

<p>
Use it to quickly check which build you are using before comparing it with a published release.
</p>

<div style="text-align:center; margin-top:16px; margin-bottom:28px;">
  <p style="margin-top:0;"><strong>Installed version</strong></p>
  <img src="../img/advanced_addon_version.jpg" alt="ScanReady Installed version screenshot" style="max-width:760px; width:100%;" loading="lazy" decoding="async">
</div>

<hr>

<h3>Check for Updates</h3>

<p>
Manually checks whether a newer ScanReady version exists.
</p>

<p>
ScanReady reads the public <strong>update-manifest.json</strong> file from the documentation and compares the available version with the installed version.
</p>

<div class="admonition note">
  <p class="admonition-title">Informational check</p>
  <p><strong>Check for Updates</strong> does not install updates and does not replace Blender Extensions / Superhive. It is only a manual notification, also useful when the add-on was installed from ZIP.</p>
</div>

<div style="text-align:center; margin-top:16px; margin-bottom:28px;">
  <p style="margin-top:0;"><strong>Check for Updates</strong></p>
  <img src="../img/advanced_addon_check_update.jpg" alt="ScanReady Check for Updates screenshot" style="max-width:760px; width:100%;" loading="lazy" decoding="async">
</div>

<hr>

<h3>Update Notice</h3>

<div class="sr-doc-row" style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-start; margin-top:16px; margin-bottom:30px;">

<div style="flex:1 1 0; min-width:0;">

<p>
When ScanReady detects a newer version, it can show a notice in the panel with the installed and available versions.
</p>

<p>
The notice appears after a manual check detects a newer version. To update, download the package from the purchase platform or use Update if ScanReady was installed from an extension repository configured in Blender.
</p>
</div>

<div style="flex:0 0 260px; text-align:center;">
  <p style="margin-top:0;"><strong>Update Notice</strong></p>
  <img src="../img/advanced_update_notice_panel.jpg" alt="ScanReady update notice in the main add-on panel" style="width:260px; max-width:100%;" loading="lazy" decoding="async">
</div>

</div>

<div style="text-align:center; margin-top:8px; margin-bottom:30px;">
  <p style="margin-top:0;"><strong>Update check in Preferences</strong></p>
  <img src="../img/preferences_update_notice.jpg" alt="ScanReady update check in Blender add-on preferences" style="max-width:760px; width:100%;" loading="lazy" decoding="async">
</div>

<hr>

<h3>Open Documentation</h3>

<p>
Opens the online ScanReady documentation.
</p>

<p>
Use it to consult the quick guide, manual workflow, FAQ, troubleshooting or settings reference.
</p>

<div style="text-align:center; margin-top:16px; margin-bottom:28px;">
  <p style="margin-top:0;"><strong>Open Documentation</strong></p>
  <img src="../img/advanced_addon_open_documentation.jpg" alt="ScanReady Open Documentation screenshot" style="max-width:760px; width:100%;" loading="lazy" decoding="async">
</div>

<hr>

<h3>Release Notes</h3>

<p>
Opens the ScanReady changelog and release notes page.
</p>

<p>
Use it to see what changed before installing or comparing a new version.
</p>

<div style="text-align:center; margin-top:16px; margin-bottom:28px;">
  <p style="margin-top:0;"><strong>Release Notes</strong></p>
  <img src="../img/advanced_addon_release_note.jpg" alt="ScanReady Release Notes screenshot" style="max-width:760px; width:100%;" loading="lazy" decoding="async">
</div>

<hr>

<h3>Video Tutorials</h3>

<p>
Opens the YouTube channel with ScanReady tutorials.
</p>

<p>
Use it when you prefer following the workflow on video or want practical add-on examples.
</p>

<div style="text-align:center; margin-top:16px; margin-bottom:28px;">
  <p style="margin-top:0;"><strong>Video Tutorials</strong></p>
  <img src="../img/advanced_addon_video_tutorial.jpg" alt="ScanReady Video Tutorials screenshot" style="max-width:760px; width:100%;" loading="lazy" decoding="async">
</div>

---

## Practical Advice

For VR, video games and realtime workflows, always balance quality and performance.

Use advanced settings to find the right compromise between:

- mesh cleanup;
- UV quality;
- bake quality;
- texture resolution;
- file size;
- memory usage;
- realtime performance.

The goal is not to preserve every polygon of the original scan.

The goal is to preserve the scan's visual identity in a lighter asset that is easier to use.



