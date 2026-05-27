SCANREADY_VERSION = (1, 0, 0)
SCANREADY_BLENDER_VERSION = (4, 2, 0)

bl_info = {
    "name": "ScanReady",
    "author": "Mario Schiano",
    "version": SCANREADY_VERSION,
    "blender": SCANREADY_BLENDER_VERSION,
    "location": "View3D > Sidebar > Scan Ready",
    "description": "ScanReady v1.0 converts scans into optimized game-ready baked assets.",
    "category": "Object",
}

# ------------------------------------------------------------
# GLOBAL DEFAULTS
# ------------------------------------------------------------
DEFAULTS = {
    "weld_distance_cm": 0.05,
    "pre_decimate_merge_cm": 2.0,
    "auto_fix_normals": False,
    "auto_combine_mesh_parts": True,
    "auto_clean_scan_debris": True,
    "decimate_ratio": 0.1,
    "checker_mix": 1.0,
    "checker_uv_scale": 10.0,
    "smart_uv_angle": 66.0,
    "uv_padding_px": 0.1,
    "cage_extrusion_mm": 0.0,
    "cage_alpha": 1.0,
    "texture_size": 2048,
    "bake_material_count": 1,
    "bake_margin_px": 8,
    "bake_basecolor": True,
    "bake_normal": False,
    "bake_roughness": False,
    "bake_occlusion": False,
    "ao_auto_distance": True,
    "ao_distance": 0.2,
    "ao_samples": 32,
    "ao_source": "HIGH_TO_LOW",
    "save_images": True,
    "image_format": "JPEG",
    "jpeg_quality": 90,
    "tiff_16bit": False,
    "normal_strength": 1.0,
    "fit_low_to_high_before_bake": False,
    "fit_low_to_high_offset_mm": 0.0,
    "low_vram_bake": True,
    "low_vram_force_cpu": False,
}


import bpy
import json
import os
import tempfile
import math
import urllib.request
import urllib.parse
import webbrowser
try:
    import numpy as np
except Exception:
    np = None
try:
    import psutil
except Exception:
    psutil = None
import time
import bmesh
from bpy.props import (
    BoolProperty,
    FloatProperty,
    IntProperty,
    StringProperty,
    PointerProperty,
    EnumProperty,
)
from bpy.types import AddonPreferences, Operator, Panel, PropertyGroup


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

CHECKER_LINK_TAG = "alb_checker_original_link"


def get_version_string():
    version = globals().get("SCANREADY_VERSION", (1, 0, 0))
    return ".".join(map(str, version))


def ensure_object_mode():
    obj = bpy.context.object
    if obj and obj.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')


def ensure_cycles_render_engine(context, operator=None, props=None):
    """Enable Cycles when available and make it the active render engine."""
    scene = context.scene

    def cycles_is_available():
        try:
            enum_items = scene.render.bl_rna.properties["engine"].enum_items
            return "CYCLES" in {item.identifier for item in enum_items}
        except Exception:
            return False

    def force_cycles_cpu_fallback():
        changed = False
        try:
            cycles_addon = bpy.context.preferences.addons.get("cycles")
            cycles_prefs = cycles_addon.preferences if cycles_addon is not None else None
            if cycles_prefs is not None:
                for device_type in ("NONE", "CPU"):
                    try:
                        cycles_prefs.compute_device_type = device_type
                        changed = True
                        break
                    except Exception:
                        pass
        except Exception:
            pass
        try:
            scene.cycles.device = 'CPU'
            changed = True
        except Exception:
            pass
        return changed

    if not cycles_is_available():
        try:
            bpy.ops.preferences.addon_enable(module="cycles")
        except Exception:
            pass

    # A common laptop case is Cycles enabled but CUDA/OptiX selected without a
    # compatible GPU. Bake can still run on CPU, so prefer a CPU fallback.
    force_cycles_cpu_fallback()

    if not cycles_is_available():
        try:
            scene.render.engine = 'CYCLES'
            return True
        except Exception:
            message = "Bake stopped: enable the Cycles add-on in Blender Preferences, then try again."
            if props is not None:
                log_progress(props, 1, message)
            if operator is not None:
                operator.report({'WARNING'}, message)
            return False

    try:
        scene.render.engine = 'CYCLES'
    except Exception as exc:
        force_cycles_cpu_fallback()
        try:
            scene.render.engine = 'CYCLES'
        except Exception:
            message = f"Bake stopped: could not switch to Cycles. Try setting Cycles Compute Device to None/CPU in Preferences."
            if props is not None:
                log_progress(props, 1, message)
            if operator is not None:
                operator.report({'WARNING'}, message)
            return False

    return True

def deselect_all():
    for obj in bpy.context.selected_objects:
        obj.select_set(False)


def make_active(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)


def duplicate_object(obj, suffix):
    new_obj = obj.copy()
    new_obj.data = obj.data.copy()
    new_obj.animation_data_clear()
    new_obj.name = f"{get_base_name(obj)}{suffix}"
    new_obj.data.name = f"{obj.data.name}{suffix}"
    bpy.context.collection.objects.link(new_obj)
    return new_obj


def make_object_materials_unique(obj, suffix="_ALB"):
    """Duplicate material datablocks for this object so source materials are never modified."""
    if obj is None or obj.type != 'MESH':
        return

    mats = obj.data.materials
    if mats is None:
        return

    for i, mat in enumerate(mats):
        if mat is None:
            continue
        try:
            new_mat = mat.copy()
            try:
                new_mat.use_fake_user = False
            except Exception:
                pass
            try:
                if suffix and not new_mat.name.endswith(suffix):
                    source_name = generated_material_source_name(mat.name) or strip_blender_copy_suffix(mat.name)
                    new_mat.name = f"{source_name}{suffix}"
            except Exception:
                pass
            mats[i] = new_mat
        except Exception:
            pass


SCANREADY_GENERATED_MATERIAL_TOKENS = (
    "_PREVIEW",
    "_UV",
    "_FINAL",
    "_Bake_Mat_",
    "ALB_Bake_",
    "ALB_Cage_Preview_Mat",
)


def strip_blender_copy_suffix(name):
    if not name:
        return ""
    clean = str(name)
    while len(clean) > 4 and clean[-4] == "." and clean[-3:].isdigit():
        clean = clean[:-4]
    return clean


def generated_material_source_name(name):
    clean = strip_blender_copy_suffix(name)
    for token in ("_PREVIEW", "_UV", "_FINAL", "_Bake_Mat_"):
        idx = clean.find(token)
        if idx > 0:
            return strip_blender_copy_suffix(clean[:idx])
    return ""


def is_scanready_generated_material_name(name, base_name=None):
    clean = strip_blender_copy_suffix(name)
    if not clean:
        return False
    if clean.startswith("ALB_Bake_") or clean == "ALB_Cage_Preview_Mat":
        return True
    if not any(token in clean for token in SCANREADY_GENERATED_MATERIAL_TOKENS):
        return False
    if not base_name:
        return True
    base = get_clean_source_name(base_name)
    source_name = generated_material_source_name(clean)
    if source_name and get_clean_source_name(source_name) == base:
        return True
    return base in clean


def restore_object_source_materials(obj):
    """Replace ScanReady generated material slots with their original source material."""
    if obj is None or getattr(obj, "type", None) != 'MESH' or getattr(obj, "data", None) is None:
        return False
    changed = False
    mats = obj.data.materials
    for i, mat in enumerate(list(mats)):
        if mat is None:
            continue
        mat_name = str(getattr(mat, "name", "") or "")
        if not is_scanready_generated_material_name(mat_name):
            continue
        source_name = generated_material_source_name(mat_name)
        if not source_name:
            continue
        source_mat = bpy.data.materials.get(source_name)
        if source_mat is not None and source_mat != mat and not is_scanready_generated_material_name(source_mat.name):
            try:
                mats[i] = source_mat
                changed = True
            except Exception:
                pass
    return changed


def collapse_duplicate_material_slots(obj):
    """Remove duplicate material slots while preserving face material assignments."""
    if obj is None or getattr(obj, "type", None) != 'MESH' or getattr(obj, "data", None) is None:
        return False
    mats = obj.data.materials
    if mats is None or len(mats) < 2:
        return False

    slot_map = {}
    new_mats = []
    old_to_new = {}
    changed = False
    for i, mat in enumerate(list(mats)):
        key = mat.name if mat is not None else f"__none_{i}"
        if key in slot_map:
            old_to_new[i] = slot_map[key]
            changed = True
        else:
            slot_map[key] = len(new_mats)
            old_to_new[i] = len(new_mats)
            new_mats.append(mat)

    if not changed:
        return False

    for poly in obj.data.polygons:
        try:
            poly.material_index = old_to_new.get(poly.material_index, 0)
        except Exception:
            pass
    mats.clear()
    for mat in new_mats:
        try:
            mats.append(mat)
        except Exception:
            pass
    return True


def get_clean_source_name(name):
    if not name:
        return "Object"
    for prefix in ("1_", "2_", "3_"):
        if name.startswith(prefix):
            name = name[len(prefix):]
            break
    for suffix in ("_high", "_optimize", "_UV", "_Cage", "_final", "_preview", "_uv", "_bake"):
        if name.endswith(suffix):
            name = name[:-len(suffix)]
            break
    return name


def get_base_name(obj):
    if obj is None:
        return "Object"
    if obj.get("alb_source_object"):
        return get_clean_source_name(obj["alb_source_object"])
    return get_clean_source_name(obj.name)


def build_role_name(base, role):
    base = get_clean_source_name(base)
    if role == "preview":
        return f"1_{base}_preview"
    if role == "uv":
        return f"2_{base}_UV"
    if role == "cage":
        return f"2_{base}_Cage"
    if role == "final":
        return f"3_{base}_final"
    return base


def get_high_object_from_any(obj):
    if obj is None:
        return None
    if obj.get("alb_role") == "high":
        return obj
    if obj.get("alb_source_object"):
        return bpy.data.objects.get(obj["alb_source_object"])
    return obj


def is_high_mesh_name(name):
    clean = str(name or "").strip().lower()
    if clean.endswith(")"):
        clean = clean
    # Blender duplicates add suffixes like .001; ignore them for role detection.
    parts = clean.rsplit(".", 1)
    if len(parts) == 2 and parts[1].isdigit():
        clean = parts[0]
    normalized = clean.replace("-", "_").replace(" ", "_")
    return (
        normalized.endswith("_high")
        or normalized.endswith("high")
        or "mesh_high" in normalized
    )


def find_existing_high_mesh_in_scene(context):
    scene = context.scene if context and getattr(context, "scene", None) else bpy.context.scene
    objects = list(scene.objects) if scene else list(bpy.data.objects)
    candidates = []
    for obj in objects:
        if getattr(obj, "type", None) != 'MESH':
            continue
        if obj.get("alb_role") == "high" or is_high_mesh_name(getattr(obj, "name", "")):
            candidates.append(obj)
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]
    candidates.sort(key=lambda item: len(getattr(item.data, "polygons", [])), reverse=True)
    return candidates[0]


def get_preview_object_from_any(obj):
    if obj is None:
        return None
    if obj.get("alb_role") == "preview":
        return obj
    base = get_base_name(obj)
    return bpy.data.objects.get(build_role_name(base, "preview"))


def get_uv_object_from_any(obj):
    if obj is None:
        return None
    if obj.get("alb_role") == "uv":
        return obj
    if obj.get("alb_role") == "final" and obj.get("alb_uv_object"):
        return bpy.data.objects.get(obj["alb_uv_object"])
    base = get_base_name(obj)
    return bpy.data.objects.get(build_role_name(base, "uv"))


def delete_object_if_exists(name):
    obj = bpy.data.objects.get(name)
    if obj:
        bpy.data.objects.remove(obj, do_unlink=True)


def face_count(obj):
    return len(obj.data.polygons) if obj and obj.type == 'MESH' else 0


def triangle_count(obj):
    if obj is None or obj.type != 'MESH':
        return 0
    return sum(max(1, len(poly.vertices) - 2) for poly in obj.data.polygons)


def update_cached_ui_mesh_stats(context, stats_obj=None):
    props = context.scene.alb_props

    if stats_obj is None:
        obj = context.active_object
        if obj is not None and obj.type == 'MESH':
            stats_obj = obj
        else:
            stats_obj = get_high_object_from_any(obj)

    if stats_obj is not None and getattr(stats_obj, "type", None) == 'MESH':
        props.ui_faces_cached = face_count(stats_obj)
        props.ui_tris_cached = triangle_count(stats_obj)
        preview = get_preview_object_from_any(stats_obj)
        if preview is not None and preview.get("alb_role") == "preview":
            update_preview_info_from_preview(context, preview)
    else:
        props.ui_faces_cached = 0
        props.ui_tris_cached = 0

class ALB_OT_refresh_stats(Operator):
    bl_idname = "object.alb_refresh_stats"
    bl_label = "Refresh Stats"
    bl_description = "Refresh cached mesh statistics shown in the panel"

    def execute(self, context):
        update_cached_ui_mesh_stats(context)
        self.report({'INFO'}, "Stats updated")
        return {'FINISHED'}



def estimated_face_count(original_faces, decimate_ratio):
    return max(1, int(original_faces * decimate_ratio)) if original_faces > 0 else 0


def format_preview_info(original_faces, preview_faces):
    if original_faces > 0:
        reduction = (1.0 - (preview_faces / original_faces)) * 100.0
    else:
        reduction = 0.0
    return f"Faces: {original_faces:,} -> {preview_faces:,} ({reduction:.1f}%)"


def update_preview_info_from_preview(context, preview, source=None):
    if context is None or preview is None or getattr(preview, "type", None) != 'MESH':
        return False
    if source is None:
        source = get_high_object_from_any(preview)
    input_faces = preview_decimate_input_face_count(preview, source)
    preview_faces = evaluated_preview_face_count(preview)
    if input_faces <= 0 or preview_faces <= 0:
        return False
    try:
        context.scene.alb_props.preview_info = format_preview_info(input_faces, preview_faces)
        return True
    except Exception:
        return False


def get_first_view3d_area_and_region(context):
    screen = context.screen
    if not screen:
        return None, None
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    return area, region
    return None, None


def is_in_local_view(context):
    area, region = get_first_view3d_area_and_region(context)
    if area is None:
        return False
    space = area.spaces.active
    return getattr(space, "local_view", None) is not None


def toggle_local_view(context):
    area, region = get_first_view3d_area_and_region(context)
    if area is None or region is None:
        return False
    space = area.spaces.active
    try:
        with context.temp_override(area=area, region=region, space_data=space):
            bpy.ops.view3d.localview(frame_selected=False)
        return True
    except Exception:
        return False


def enter_local_view_for_selection(context):
    if not is_in_local_view(context):
        toggle_local_view(context)



def isolate_in_local_view(context, target_obj):
    if target_obj is None:
        return

    for area in context.screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces.active
            for region in area.regions:
                if region.type == 'WINDOW':
                    try:
                        with context.temp_override(area=area, region=region, space_data=space):
                            # If already in local view, first exit it
                            if getattr(space, "local_view", None):
                                bpy.ops.view3d.localview(frame_selected=False)

                            deselect_all()
                            target_obj.hide_set(False)
                            make_active(target_obj)

                            # Enter local view with only the target selected
                            bpy.ops.view3d.localview(frame_selected=False)
                    except Exception:
                        pass
                    return


def isolate_objects_in_local_view(context, objects):
    valid_objects = [obj for obj in objects if obj is not None]
    if not valid_objects:
        return

    for area in context.screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces.active
            for region in area.regions:
                if region.type == 'WINDOW':
                    try:
                        with context.temp_override(area=area, region=region, space_data=space):
                            if getattr(space, "local_view", None):
                                bpy.ops.view3d.localview(frame_selected=False)

                            deselect_all()
                            for obj in valid_objects:
                                obj.hide_set(False)
                                obj.select_set(True)
                            context.view_layer.objects.active = valid_objects[0]

                            bpy.ops.view3d.localview(frame_selected=False)
                    except Exception:
                        pass
                    return

def exit_local_view_if_needed(context):
    if is_in_local_view(context):
        toggle_local_view(context)


def set_object_workflow_visibility(obj, visible, render_visible=None):
    if obj is None:
        return
    hidden = not bool(visible)
    try:
        obj.hide_set(hidden)
    except Exception:
        pass
    try:
        # Keep the viewport monitor enabled so users can recover high/UV/cage
        # objects by simply clicking the eye icon in the Outliner.
        obj.hide_viewport = False
    except Exception:
        pass
    try:
        obj.hide_render = (not bool(render_visible)) if render_visible is not None else hidden
    except Exception:
        pass


def get_workflow_objects_for_base(base):
    if not base:
        return []
    names = {
        build_role_name(base, "preview"),
        build_role_name(base, "uv"),
        build_role_name(base, "cage"),
        build_role_name(base, "final"),
        f"{get_clean_source_name(base)}_high",
    }
    objects = []
    for obj in bpy.data.objects:
        if getattr(obj, "type", None) != 'MESH':
            continue
        try:
            role = obj.get("alb_role")
        except Exception:
            role = None
        if obj.name in names or (role in {"high", "preview", "uv", "cage", "final"} and get_base_name(obj) == base):
            objects.append(obj)
    return objects


def set_workflow_visibility(context, visible_objects, active_obj=None, hide_related=True, render_visible_objects=True):
    visible = [obj for obj in (visible_objects or []) if obj is not None]
    visible_names = {obj.name for obj in visible}
    try:
        exit_local_view_if_needed(context)
    except Exception:
        pass

    related_by_name = {}
    if hide_related:
        for obj in visible:
            try:
                for related in get_workflow_objects_for_base(get_base_name(obj)):
                    related_by_name[related.name] = related
            except Exception:
                pass

    for obj in related_by_name.values():
        should_show = obj.name in visible_names
        set_object_workflow_visibility(obj, should_show, render_visible=(should_show and render_visible_objects))

    for obj in visible:
        set_object_workflow_visibility(obj, True, render_visible=render_visible_objects)

    try:
        deselect_all()
    except Exception:
        pass
    if active_obj is None and visible:
        active_obj = visible[0]
    if active_obj is not None:
        try:
            make_active(active_obj)
        except Exception:
            pass

def set_wireframe_overlay(context, state):
    screen = context.screen
    if not screen:
        return
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces.active
            try:
                space.overlay.show_wireframes = state
                space.overlay.wireframe_threshold = 1.0
            except Exception:
                pass



def set_face_orientation_overlay(context, state):
    screen = getattr(context, "screen", None) if context else None
    if not screen:
        return
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces.active
            try:
                space.overlay.show_face_orientation = bool(state)
            except Exception:
                pass
def texture_size_from_preset(preset_str):
    try:
        return int(preset_str)
    except Exception:
        return 2048


def get_bake_material_count(props):
    try:
        return max(1, int(props.bake_material_count))
    except Exception:
        return 1


def sanitize_bake_material_count(props):
    try:
        value = max(1, min(16, int(props.bake_material_count)))
        if int(props.bake_material_count) != value:
            props.bake_material_count = value
        sync_force_cpu_from_bake_materials(props, value)
        return value
    except Exception:
        try:
            props.bake_material_count = DEFAULTS['bake_material_count']
            sync_force_cpu_from_bake_materials(props, DEFAULTS['bake_material_count'])
        except Exception:
            pass
        return DEFAULTS['bake_material_count']


def sync_force_cpu_from_bake_materials(props, material_count=None):
    if props is None:
        return
    try:
        if getattr(props, "is_resetting_defaults", False):
            return
    except Exception:
        pass
    try:
        count = int(material_count if material_count is not None else props.bake_material_count)
    except Exception:
        count = 1
    if count > 1 and hasattr(props, "low_vram_force_cpu"):
        try:
            props.low_vram_force_cpu = True
        except Exception:
            pass


def find_preview_for_source(source, fallback_obj=None):
    if fallback_obj is not None and getattr(fallback_obj, "type", None) == 'MESH':
        preview = get_preview_object_from_any(fallback_obj)
        if preview is not None and preview.get("alb_role") == "preview":
            return preview
    if source is None or getattr(source, "type", None) != 'MESH':
        return None
    for obj in bpy.data.objects:
        if getattr(obj, "type", None) != 'MESH':
            continue
        if obj.get("alb_role") == "preview" and obj.get("alb_source_object") == source.name:
            return obj
    preview = bpy.data.objects.get(build_role_name(get_base_name(source), "preview"))
    if preview is not None and preview.get("alb_role") == "preview":
        return preview
    return None


def evaluated_face_count_with_modifier_disabled(obj, modifier_name):
    if obj is None or getattr(obj, "type", None) != 'MESH':
        return 0
    mod = obj.modifiers.get(modifier_name)
    old_show = None
    if mod is not None:
        old_show = mod.show_viewport
        mod.show_viewport = False
    mesh = None
    obj_eval = None
    try:
        depsgraph = bpy.context.evaluated_depsgraph_get()
        depsgraph.update()
        obj_eval = obj.evaluated_get(depsgraph)
        mesh = obj_eval.to_mesh()
        return len(mesh.polygons) if mesh is not None else face_count(obj)
    except Exception:
        return face_count(obj)
    finally:
        try:
            if obj_eval is not None and mesh is not None:
                obj_eval.to_mesh_clear()
        except Exception:
            pass
        if mod is not None and old_show is not None:
            try:
                mod.show_viewport = old_show
                bpy.context.view_layer.update()
            except Exception:
                pass


def preview_decimate_input_face_count(preview, source=None):
    if preview is not None and getattr(preview, "type", None) == 'MESH':
        count = evaluated_face_count_with_modifier_disabled(preview, "ALB_Decimate")
        if count > 0:
            return count
    return face_count(source)


def evaluated_preview_face_count(preview):
    if preview is None or getattr(preview, "type", None) != 'MESH':
        return 0
    mesh = None
    obj_eval = None
    try:
        depsgraph = bpy.context.evaluated_depsgraph_get()
        depsgraph.update()
        obj_eval = preview.evaluated_get(depsgraph)
        mesh = obj_eval.to_mesh()
        return len(mesh.polygons) if mesh is not None else face_count(preview)
    except Exception:
        return face_count(preview)
    finally:
        try:
            if obj_eval is not None and mesh is not None:
                obj_eval.to_mesh_clear()
        except Exception:
            pass


def evaluated_preview_face_count_for_ratio(preview, ratio):
    if preview is None or getattr(preview, "type", None) != 'MESH':
        return 0
    dec = preview.modifiers.get("ALB_Decimate")
    if dec is None:
        return face_count(preview)
    old_ratio = dec.ratio
    old_show = dec.show_viewport
    try:
        dec.show_viewport = True
        dec.ratio = max(0.0001, min(1.0, ratio))
        bpy.context.view_layer.update()
        return evaluated_preview_face_count(preview)
    except Exception:
        return 0
    finally:
        try:
            dec.ratio = old_ratio
            dec.show_viewport = old_show
            bpy.context.view_layer.update()
        except Exception:
            pass


def decimate_ratio_for_target_faces(preview, target_faces, input_faces):
    if preview is None or preview.modifiers.get("ALB_Decimate") is None:
        return max(0.0001, min(1.0, target_faces / max(1, input_faces)))
    target_faces = max(1, min(int(target_faces), max(1, int(input_faces))))
    best_ratio = max(0.0001, min(1.0, target_faces / max(1, input_faces)))
    best_count = evaluated_preview_face_count_for_ratio(preview, best_ratio)
    best_diff = abs(best_count - target_faces) if best_count > 0 else input_faces
    low = 0.0001
    high = 1.0
    for _ in range(18):
        mid = (low + high) * 0.5
        count = evaluated_preview_face_count_for_ratio(preview, mid)
        if count <= 0:
            break
        diff = abs(count - target_faces)
        if diff < best_diff:
            best_ratio = mid
            best_count = count
            best_diff = diff
        if count > target_faces:
            high = mid
        elif count < target_faces:
            low = mid
        else:
            best_ratio = mid
            best_count = count
            break
    return max(0.0001, min(1.0, best_ratio))


def update_preview_modifiers_from_props(obj, props, source=None):
    if props is None:
        return
    if source is None and obj is not None and getattr(obj, "type", None) == 'MESH':
        source = get_high_object_from_any(obj)
    preview = find_preview_for_source(source, obj)
    if preview is None or preview.get("alb_role") != "preview":
        return
    weld = preview.modifiers.get("ALB_Weld")
    dec = preview.modifiers.get("ALB_Decimate")
    if weld:
        weld.merge_threshold = props.weld_distance_cm / 100.0
    if dec:
        dec.ratio = props.decimate_ratio
        dec.show_viewport = True
    try:
        preview.update_tag()
        bpy.context.view_layer.update()
    except Exception:
        pass


def recalculate_normals_outside(obj):
    if obj is None or getattr(obj, "type", None) != 'MESH' or obj.data is None:
        return 0
    mesh = obj.data
    bm = bmesh.new()
    try:
        bm.from_mesh(mesh)
        bm.faces.ensure_lookup_table()
        face_count_value = len(bm.faces)
        if face_count_value <= 0:
            return 0
        bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
        bm.to_mesh(mesh)
        mesh.update()
        try:
            mesh.validate(clean_customdata=False)
        except Exception:
            pass
        return face_count_value
    finally:
        bm.free()


def maybe_auto_fix_source_normals(context, props, source):
    if props is None or source is None or not getattr(props, "auto_fix_normals", False):
        return False
    count = recalculate_normals_outside(source)
    if count > 0:
        props.normals_status = f"Normals recalculated outside on {count:,} faces."
        try:
            log_progress(props, max(float(getattr(props, "progress_percent", 0.0)), 10.0), "Normals recalculated outside...")
        except Exception:
            pass
        return True
    props.normals_status = "No mesh faces found for normal recalculation."
    return False


def get_hierarchy_root(obj):
    if obj is None:
        return None
    root = obj
    visited = set()
    while getattr(root, "parent", None) is not None and root.name not in visited:
        visited.add(root.name)
        root = root.parent
    return root


def get_mesh_descendants(root):
    meshes = []
    if root is None:
        return meshes
    for child in getattr(root, "children_recursive", []):
        if getattr(child, "type", None) == 'MESH':
            meshes.append(child)
    if getattr(root, "type", None) == 'MESH' and root not in meshes:
        meshes.insert(0, root)
    return meshes


def get_empty_descendants(root):
    empties = []
    if root is None:
        return empties
    for child in getattr(root, "children_recursive", []):
        if getattr(child, "type", None) == 'EMPTY':
            empties.append(child)
    if getattr(root, "type", None) == 'EMPTY':
        empties.insert(0, root)
    return empties


def clear_parent_keep_world_transform(obj):
    if obj is None:
        return
    try:
        world = obj.matrix_world.copy()
        obj.parent = None
        obj.matrix_parent_inverse.identity()
        obj.matrix_world = world
    except Exception:
        pass


def remove_empty_hierarchy_objects(empties):
    # Remove only locator/empty helpers captured from the selected hierarchy.
    for empty in sorted([e for e in (empties or []) if e is not None], key=lambda e: len(getattr(e, "children_recursive", [])), reverse=True):
        try:
            if getattr(empty, "type", None) == 'EMPTY':
                bpy.data.objects.remove(empty, do_unlink=True)
        except Exception:
            pass


def auto_combine_mesh_parts_if_needed(context, props, source, operator=None):
    if source is None or props is None or not getattr(props, "auto_combine_mesh_parts", True):
        return source

    selected_meshes = [obj for obj in context.selected_objects if getattr(obj, "type", None) == 'MESH']
    combine_meshes = []
    hierarchy_root = None
    empty_cleanup = []

    if len(selected_meshes) > 1:
        combine_meshes = selected_meshes
        hierarchy_root = get_hierarchy_root(source)
    else:
        hierarchy_root = get_hierarchy_root(source)
        if hierarchy_root is not None and hierarchy_root != source:
            combine_meshes = get_mesh_descendants(hierarchy_root)
            empty_cleanup = get_empty_descendants(hierarchy_root)
        elif getattr(source, "type", None) == 'EMPTY':
            combine_meshes = get_mesh_descendants(source)
            empty_cleanup = get_empty_descendants(source)

    combine_meshes = [obj for obj in combine_meshes if obj is not None and getattr(obj, "type", None) == 'MESH']
    # Conservative rule: if there is no hierarchy/multi-selection, keep current behavior.
    if len(combine_meshes) <= 1:
        return source

    active_mesh = source if source in combine_meshes else combine_meshes[0]
    base_name = get_clean_source_name(hierarchy_root.name if hierarchy_root is not None else active_mesh.name)

    try:
        log_progress(props, 5, f"Combining {len(combine_meshes)} mesh parts from selected hierarchy...")
    except Exception:
        pass

    ensure_object_mode()
    for obj in combine_meshes:
        try:
            clear_parent_keep_world_transform(obj)
            obj.hide_viewport = False
            obj.hide_set(False)
            obj.select_set(True)
        except Exception:
            pass

    try:
        context.view_layer.objects.active = active_mesh
        bpy.ops.object.join()
    except Exception as exc:
        if operator is not None:
            operator.report({'WARNING'}, f"Could not auto combine mesh parts: {exc}")
        return source

    combined = context.active_object
    if combined is None or getattr(combined, "type", None) != 'MESH':
        return source

    try:
        combined.name = base_name
        combined.data.name = f"{base_name}_Mesh"
        combined["alb_auto_combined_parts"] = len(combine_meshes)
    except Exception:
        pass
    try:
        combined.parent = None
        combined.matrix_parent_inverse.identity()
    except Exception:
        pass

    try:
        removed_vertices = apply_mesh_weld_by_distance(combined, props.weld_distance_cm / 100.0)
        combined["alb_auto_weld_removed"] = int(removed_vertices)
        log_progress(props, 6, f"Combined mesh welded. Merged vertices: {removed_vertices:,}")
    except Exception:
        combined["alb_auto_weld_removed"] = 0

    remove_empty_hierarchy_objects(empty_cleanup)
    ensure_object_visible_and_active(combined)
    try:
        log_progress(props, 7, f"Combined mesh parts into {combined.name}")
    except Exception:
        pass
    return combined

def switch_properties_from_material_to_object(context):
    try:
        screen = context.screen
        if not screen:
            return
        for area in screen.areas:
            if area.type == 'PROPERTIES':
                space = area.spaces.active
                if getattr(space, "context", None) == 'MATERIAL':
                    try:
                        space.context = 'OBJECT'
                    except Exception:
                        pass
    except Exception:
        pass




def enter_local_view_with_objects(context, objects, active_obj=None):
    try:
        objs = [o for o in objects if o is not None]
        if not objs:
            return

        view3d_areas = [a for a in context.screen.areas if a.type == 'VIEW_3D']
        if not view3d_areas:
            return

        deselect_all()
        for obj in objs:
            try:
                obj.hide_set(False)
            except Exception:
                pass
            try:
                obj.select_set(True)
            except Exception:
                pass

        if active_obj is None or active_obj not in objs:
            active_obj = objs[0]

        try:
            make_active(active_obj)
        except Exception:
            pass

        # Try to enter local view from a 3D viewport override
        for area in view3d_areas:
            region = next((r for r in area.regions if r.type == 'WINDOW'), None)
            if region is None:
                continue
            space = area.spaces.active
            override = context.copy()
            override["area"] = area
            override["region"] = region
            override["space_data"] = space
            try:
                # Ensure local view is toggled on with the selected objects
                if getattr(space, "local_view", None) is None:
                    bpy.ops.view3d.localview(override, frame_selected=False)
                return
            except Exception:
                pass

        # Fallback
        try:
            bpy.ops.view3d.localview(frame_selected=False)
        except Exception:
            pass
    except Exception:
        pass


def switch_viewport_to_material_preview(context):
    try:
        screen = context.screen
        if not screen:
            return
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        try:
                            space.shading.type = 'MATERIAL'
                        except Exception:
                            pass
    except Exception:
        pass


def switch_to_material_preview(context):
    for area in context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    try:
                        if space.shading.type != 'MATERIAL':
                            space.shading.type = 'MATERIAL'
                    except Exception:
                        pass
                    try:
                        space.shading.render_pass = 'COMBINED'
                    except Exception:
                        pass


def switch_to_solid_preview(context):
    try:
        screen = context.screen
    except Exception:
        screen = None
    if not screen:
        return
    for area in screen.areas:
        if area.type != 'VIEW_3D':
            continue
        for space in area.spaces:
            if space.type != 'VIEW_3D':
                continue
            try:
                # Material Preview is safer for imported GLB materials. Solid +
                # texture color can show black when the material uses node setups
                # or vertex/image data Blender does not expose as a solid texture.
                space.shading.type = 'MATERIAL'
            except Exception:
                pass
            try:
                space.shading.render_pass = 'COMBINED'
            except Exception:
                pass
            try:
                space.shading.use_scene_lights = False
            except Exception:
                pass
            try:
                space.shading.use_scene_world = False
            except Exception:
                pass

def enable_viewport_statistics(context):
    """Enable Viewport Overlays > Statistics in every visible 3D view."""
    try:
        screen = context.screen
    except Exception:
        screen = None
    if screen is None:
        return

    for area in screen.areas:
        if area.type != 'VIEW_3D':
            continue
        for space in area.spaces:
            if space.type != 'VIEW_3D':
                continue
            try:
                if not space.overlay.show_stats:
                    space.overlay.show_stats = True
            except Exception:
                pass


ONE_CLICK_PROGRESS_RANGES = {
    "PREVIEW": (0.0, 25.0, "Preview", 1, 4),
    "UV": (25.0, 45.0, "UV Mapping", 2, 4),
    "CAGE": (45.0, 55.0, "Auto Cage", 3, 4),
    "BAKE": (55.0, 100.0, "Texture Bake", 4, 4),
}


def get_one_click_global_progress(props, local_percent):
    phase = str(getattr(props, "one_click_phase", "") or "").upper()
    start, end, label, phase_index, phase_total = ONE_CLICK_PROGRESS_RANGES.get(phase, (0.0, 100.0, "Workflow", 1, 1))
    local = max(0.0, min(100.0, float(local_percent)))
    global_percent = start + ((end - start) * (local / 100.0))
    return global_percent, label, phase_index, phase_total, local


def log_progress(props, percent, message):
    local_percent = max(0.0, min(100.0, float(percent)))
    display_percent = local_percent
    display_message = message
    display_detail = ""
    status_bar_message = message

    if getattr(props, "one_click_active", False):
        display_percent, phase_label, phase_index, phase_total, phase_percent = get_one_click_global_progress(props, local_percent)
        display_message = f"Phase {phase_index}/{phase_total}: {phase_label}"
        display_detail = f"{phase_percent:.0f}% of phase - {message}"
        status_bar_message = (
            f"ScanReady {display_percent:.0f}% | "
            f"Phase {phase_index}/{phase_total} {phase_label} {phase_percent:.0f}% | {message}"
        )

    props.progress_percent = max(0.0, min(100.0, float(display_percent)))
    props.progress_status = display_message
    try:
        props.progress_detail = display_detail
    except Exception:
        pass
    print(f"[ScanReady] {status_bar_message}")

    # Also show status in Blender's bottom status bar when possible.
    try:
        bpy.context.workspace.status_text_set(text=f"ScanReady: {status_bar_message}")
    except Exception:
        pass

    # Force UI redraw so Process Progress updates during long operations
    try:
        wm = bpy.context.window_manager
        for window in wm.windows:
            for area in window.screen.areas:
                area.tag_redraw()
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
    except Exception:
        pass


def get_bake_task_explanation(bake_type, phase):
    explanations = {
        'DIFFUSE': {
            'prepare': "Preparing Base Color bake from the high mesh material color.",
            'bake': "Baking Base Color from the high mesh to the new UV layout.",
            'save': "Saving the baked Base Color texture.",
            'complete': "Base Color bake completed and stored for the final material.",
        },
        'NORMAL': {
            'prepare': "Preparing geometric normal map bake from high mesh surface detail.",
            'bake': "Baking geometric normal map because no linked high-poly normal texture was found for this material.",
            'save': "Saving the baked geometric normal map as a Non-Color data texture.",
            'complete': "Geometric normal map bake completed and stored for the final material.",
        },
        'NORMAL_TEXTURE': {
            'prepare': "Preparing linked high-poly normal map texture transfer.",
            'bake': "Baking the linked high-poly normal map texture to the new UV layout.",
            'save': "Saving the transferred normal map as a Non-Color data texture.",
            'complete': "Normal map texture bake completed and stored for the final material.",
        },
        'ROUGHNESS': {
            'prepare': "Preparing roughness data bake.",
            'bake': "Baking roughness data to the new UV layout.",
            'save': "Saving the baked roughness map as a Non-Color data texture.",
            'complete': "Roughness bake completed and stored for the final material.",
        },
        'ROUGHNESS_TEXTURE': {
            'prepare': "Preparing linked high-poly roughness texture transfer.",
            'bake': "Baking the linked high-poly roughness texture to the new UV layout.",
            'save': "Saving the transferred roughness map as a Non-Color data texture.",
            'complete': "Roughness texture bake completed and stored for the final material.",
        },
        'AO': {
            'prepare': "Preparing ambient occlusion bake.",
            'bake': "Baking ambient occlusion to the new UV layout.",
            'save': "Saving the baked ambient occlusion texture.",
            'complete': "Ambient occlusion bake completed and stored for the final material.",
        },
    }
    return explanations.get(bake_type, {}).get(phase, str(bake_type))


def build_bake_completion_summary(props, basecolor_imgs, normal_imgs, roughness_imgs, occlusion_imgs, slot_count):
    total = max(1, int(slot_count or 1))
    lines = []

    def count_done(items):
        return sum(1 for item in (items or []) if item is not None)

    if getattr(props, "bake_basecolor", False):
        lines.append(f"Base Color baked: {count_done(basecolor_imgs)}/{total}")
    if getattr(props, "bake_normal", False):
        lines.append(f"Normal Map baked: {count_done(normal_imgs)}/{total}")
    if getattr(props, "bake_roughness", False):
        lines.append(f"Roughness baked: {count_done(roughness_imgs)}/{total}")
    if getattr(props, "bake_occlusion", False):
        lines.append(f"Occlusion baked: {count_done(occlusion_imgs)}/{total}")

    if not lines:
        return ""
    return "Bake maps completed:\n" + "\n".join(lines)


def is_progress_active(props):
    status = str(getattr(props, "progress_status", "") or "").strip().lower()
    percent = float(getattr(props, "progress_percent", 0.0) or 0.0)

    if not status:
        return False
    if "process completed" in status or "completed" in status or "completato" in status:
        return False
    if "not baked yet" in status:
        return False
    return percent < 100.0


def format_seconds_hms(seconds):
    try:
        seconds = max(0, int(round(float(seconds))))
    except Exception:
        seconds = 0
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h > 0:
        return f"{h}h {m:02d}m {s:02d}s"
    if m > 0:
        return f"{m}m {s:02d}s"
    return f"{s}s"


def format_seconds_readable(seconds):
    try:
        seconds = max(0, int(round(float(seconds))))
    except Exception:
        seconds = 0

    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    parts = []
    if h > 0:
        parts.append(f"{h} hour" + ("" if h == 1 else "s"))
    if m > 0:
        parts.append(f"{m} minute" + ("" if m == 1 else "s"))
    if s > 0 or not parts:
        parts.append(f"{s} second" + ("" if s == 1 else "s"))
    return " ".join(parts)


def now_precise_seconds():
    try:
        return time.perf_counter()
    except Exception:
        return time.time()


def set_precise_timer_prop(props, prop_name):
    try:
        setattr(props, prop_name, repr(now_precise_seconds()))
    except Exception:
        pass


def get_precise_elapsed_from_prop(props, prop_name):
    try:
        start = float(getattr(props, prop_name, "") or "0")
        if start > 0.0:
            return max(0.0, now_precise_seconds() - start)
    except Exception:
        pass
    return 0.0


def clear_precise_timer_prop(props, prop_name):
    try:
        setattr(props, prop_name, "")
    except Exception:
        pass


def build_time_estimate_suffix(start_time, completed_items, total_items):
    try:
        now = time.time()
        elapsed = max(0.0, now - float(start_time))
    except Exception:
        return ""

    if completed_items <= 0 or total_items <= 0:
        return f"\nElapsed: {format_seconds_hms(elapsed)}"

    avg = elapsed / max(1, int(completed_items))
    remaining_items = max(0, int(total_items) - int(completed_items))
    remaining = avg * remaining_items
    return f"\nElapsed: {format_seconds_hms(elapsed)} | ETA: {format_seconds_hms(remaining)}"



def estimate_bake_memory_usage_gb(props):
    try:
        size = int(get_effective_texture_size(props))
    except Exception:
        try:
            size = int(props.texture_size)
        except Exception:
            size = 2048

    try:
        materials = max(1, int(get_bake_material_count(props)))
    except Exception:
        materials = 1

    passes = 0
    try:
        if props.bake_basecolor:
            passes += 1
    except Exception:
        pass
    try:
        if props.bake_normal:
            passes += 1
    except Exception:
        pass
    try:
        if props.bake_roughness:
            passes += 1
    except Exception:
        pass

    if passes <= 0:
        return 0.0

    mem_bytes = size * size * 4 * materials * passes
    return float(mem_bytes) / float(1024 ** 3)


def get_available_system_ram_gb():
    try:
        if psutil is not None:
            return float(psutil.virtual_memory().available) / float(1024 ** 3)
    except Exception:
        pass
    return 0.0


def validate_bake_memory_or_warn(operator, props):
    estimated = estimate_bake_memory_usage_gb(props)
    available = get_available_system_ram_gb()

    if available <= 0.0:
        return True, estimated, available, ""

    ratio = estimated / max(0.001, available)

    if ratio > 0.80:
        msg = f"Estimated RAM usage too high: ~{estimated:.2f} GB required, ~{available:.2f} GB available."
        try:
            operator.report({'ERROR'}, msg)
        except Exception:
            pass
        return False, estimated, available, msg

    if ratio > 0.50:
        msg = f"High RAM usage expected: ~{estimated:.2f} GB required, ~{available:.2f} GB available."
        try:
            operator.report({'WARNING'}, msg)
        except Exception:
            pass
        return True, estimated, available, msg

    return True, estimated, available, ""

def get_uv_margin(props):
    return max(0.0, float(props.uv_padding_px) / max(1, int(props.texture_size)))




def ensure_output_folder_exists(path_str):
    try:
        abs_path = bpy.path.abspath(path_str)
    except Exception:
        abs_path = path_str
    if abs_path:
        os.makedirs(abs_path, exist_ok=True)
    return abs_path


def get_safe_output_folder(props):
    # Custom folder set by user
    try:
        raw = str(getattr(props, "output_folder", "")).strip()
    except Exception:
        raw = ""

    if raw and raw not in {"//", "//bake/"}:
        folder = bpy.path.abspath(raw)
        os.makedirs(folder, exist_ok=True)
        return folder, False

    # Saved blend file -> project-relative bake folder
    if bpy.data.is_saved:
        folder = bpy.path.abspath("//bake/")
        os.makedirs(folder, exist_ok=True)
        return folder, False

    # Unsaved blend file -> temp folder fallback
    temp_dir = os.path.join(tempfile.gettempdir(), "AutoLowpolyBaker")
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir, True


def save_image_to_folder(image, folder, filename_no_ext, image_format='JPEG'):
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    ext_map = {
        'JPEG': '.jpg',
        'PNG': '.png',
        'TIFF': '.tif',
    }
    file_ext = ext_map.get(image_format, '.jpg')

    try:
        image.update()
    except Exception:
        pass

    file_path = os.path.join(folder, filename_no_ext + file_ext)
    image.filepath_raw = file_path
    image.file_format = image_format

    try:
        settings = bpy.context.scene.render.image_settings
        settings.file_format = image_format
        if image_format == 'TIFF':
            use_16bit = bool(getattr(bpy.context.scene.alb_props, "tiff_16bit", False))
            settings.color_depth = '16' if use_16bit else '8'
    except Exception:
        pass

    if image_format == 'JPEG':
        try:
            quality = int(bpy.context.scene.alb_props.jpeg_quality)
        except Exception:
            quality = 90

        try:
            bpy.context.scene.render.image_settings.quality = quality
        except Exception:
            pass

        try:
            image.save_quality = quality
        except Exception:
            pass

    image.save()
    return file_path


def is_addon_temp_bake_image(img):
    if img is None:
        return False
    name = str(getattr(img, "name", "") or "")
    return (
        bool(img.get("alb_scanready_bake_image", False))
        or bool(img.get("alb_pending_temp_cleanup", False))
        or "_BaseColor_Mat" in name
        or "_Normal_Mat" in name
        or "_Roughness_Mat" in name
        or "_Occlusion_Mat" in name
        or name.startswith("ALB_Bake_")
    )


def unlink_image_from_bake_nodes(image):
    if image is None:
        return
    for mat in list(bpy.data.materials):
        if mat is None or not getattr(mat, "use_nodes", False):
            continue
        try:
            nodes = mat.node_tree.nodes
        except Exception:
            continue
        for node in nodes:
            try:
                if getattr(node, "type", "") == 'TEX_IMAGE' and getattr(node, "image", None) == image:
                    node.image = None
            except Exception:
                pass


def collect_material_node_images(obj):
    images = set()
    if obj is None or getattr(obj, "type", None) != 'MESH':
        return images
    for mat in list(getattr(obj.data, "materials", []) or []):
        if mat is None or not getattr(mat, "use_nodes", False) or mat.node_tree is None:
            continue
        for node in mat.node_tree.nodes:
            try:
                if getattr(node, "type", "") == 'TEX_IMAGE':
                    img = getattr(node, "image", None)
                    if img is not None:
                        images.add(img)
            except Exception:
                pass
    return images


def remove_temp_bake_image_datablock(image, force=False):
    if image is None:
        return False
    if not is_addon_temp_bake_image(image):
        return False
    try:
        unlink_image_from_bake_nodes(image)
        if force or getattr(image, "users", 0) == 0:
            bpy.data.images.remove(image)
            return True
    except Exception:
        pass
    return False


def defer_temp_bake_image_cleanup(image, delay_seconds=10.0):
    if image is None or not is_addon_temp_bake_image(image):
        return False
    try:
        unlink_image_from_bake_nodes(image)
        image["alb_pending_temp_cleanup"] = True
        image["alb_cleanup_after"] = time.time() + max(1.0, float(delay_seconds))
        image.use_fake_user = False
        return True
    except Exception:
        return False


def purge_unlinked_temp_bake_images():
    removed = 0
    now = time.time()
    for img in list(bpy.data.images):
        try:
            cleanup_after = float(img.get("alb_cleanup_after", 0.0)) if hasattr(img, "get") else 0.0
            cleanup_ready = bool(img.get("alb_pending_temp_cleanup", False)) and now >= cleanup_after
            if is_addon_temp_bake_image(img) and cleanup_ready and getattr(img, "users", 0) == 0:
                bpy.data.images.remove(img)
                removed += 1
        except Exception:
            pass
    try:
        bpy.context.view_layer.update()
    except Exception:
        pass
    return removed


def has_pending_temp_bake_images():
    now = time.time()
    for img in list(bpy.data.images):
        try:
            if not is_addon_temp_bake_image(img):
                continue
            if not bool(img.get("alb_pending_temp_cleanup", False)):
                continue
            if getattr(img, "users", 0) == 0 or now < float(img.get("alb_cleanup_after", 0.0)):
                return True
        except Exception:
            pass
    return False


def safe_post_bake_preview_cleanup():
    """Reduce Blender preview/depsgraph pressure after repeated material rebuilds.

    Conservative cleanup only:
    - clear workspace status text
    - avoid immediate image datablock deletion while Blender preview jobs may still read materials
    - avoid aggressive UI redraw or node preview touching here
    """
    try:
        bpy.context.workspace.status_text_set(text=None)
    except Exception:
        pass


def cleanup_scanready_bake_resources_for_base(base_name):
    """Remove old ScanReady bake resources for a model before rebuilding the workflow."""
    base = get_clean_source_name(base_name)
    if not base:
        return

    legacy_preview_name = f"1_{base}_optimize"
    current_preview_name = build_role_name(base, "preview")
    if legacy_preview_name != current_preview_name:
        delete_object_if_exists(legacy_preview_name)

    image_tokens = (
        f"{base}_BaseColor_Mat",
        f"{base}_Normal_Mat",
        f"{base}_Roughness_Mat",
        f"{base}_Occlusion_Mat",
        f"2_{base}_UV_BaseColor_Mat",
        f"2_{base}_UV_Normal_Mat",
        f"2_{base}_UV_Roughness_Mat",
        f"2_{base}_UV_Occlusion_Mat",
    )
    source_images = set()
    try:
        high_obj = bpy.data.objects.get(build_role_name(base, "high"))
        source_images = collect_material_node_images(high_obj)
    except Exception:
        source_images = set()
    for img in list(bpy.data.images):
        try:
            name = str(getattr(img, "name", "") or "")
            if is_addon_temp_bake_image(img) or any(token in name for token in image_tokens):
                if img in source_images and not bool(img.get("alb_scanready_bake_image", False)):
                    continue
                unlink_image_from_bake_nodes(img)
                try:
                    img.use_fake_user = False
                except Exception:
                    pass
                if getattr(img, "users", 0) == 0:
                    bpy.data.images.remove(img)
        except Exception:
            pass

    material_tokens = (
        f"{base}_Final_Mat",
        f"3_{base}_final_Final_Mat",
        "_Bake_Mat_",
        "_FINAL",
        "_PREVIEW",
        "_UV",
        "ALB_Bake_",
        "ALB_Cage_Preview_Mat",
    )
    for mat in list(bpy.data.materials):
        try:
            name = str(getattr(mat, "name", "") or "")
            if (
                any(token in name for token in material_tokens)
                and is_scanready_generated_material_name(name)
                and (
                    getattr(mat, "users", 0) == 0
                    or bool(getattr(mat, "use_fake_user", False))
                    or is_scanready_generated_material_name(name, base)
                )
            ):
                try:
                    mat.use_fake_user = False
                except Exception:
                    pass
                if getattr(mat, "users", 0) == 0:
                    bpy.data.materials.remove(mat)
        except Exception:
            pass

    try:
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
    except Exception:
        pass

    try:
        purge_unlinked_temp_bake_images()
    except Exception:
        pass


def protect_source_material_images(obj):
    if obj is None or getattr(obj, "type", None) != 'MESH':
        return
    for mat in list(getattr(obj.data, "materials", []) or []):
        if mat is None or not getattr(mat, "use_nodes", False) or mat.node_tree is None:
            continue
        for node in mat.node_tree.nodes:
            try:
                if getattr(node, "type", "") == 'TEX_IMAGE':
                    img = getattr(node, "image", None)
                    if img is not None:
                        img.use_fake_user = True
            except Exception:
                pass




# ------------------------------------------------------------
# Checker overlay
# ------------------------------------------------------------

def create_checker_image(name="ALB_Checker_Image", size=1024, cells=16):
    img = bpy.data.images.get(name)
    if img:
        return img

    img = bpy.data.images.new(name=name, width=size, height=size, alpha=False)
    pixels = []
    for y in range(size):
        for x in range(size):
            cx = int((x / size) * cells)
            cy = int((y / size) * cells)
            v = 0.18 if (cx + cy) % 2 == 0 else 0.82
            pixels.extend((v, v, v, 1.0))
    img.pixels = pixels
    img.pack()
    return img


def get_material_output(material):
    if not material or not material.use_nodes or not material.node_tree:
        return None
    for node in material.node_tree.nodes:
        if node.type == 'OUTPUT_MATERIAL' and getattr(node, "is_active_output", True):
            return node
    return None


def remove_checker_from_material(material):
    if not material or not material.use_nodes or not material.node_tree:
        return False

    nt = material.node_tree
    nodes = nt.nodes
    links = nt.links

    output = get_material_output(material)
    if output is None:
        output = nodes.new("ShaderNodeOutputMaterial")
        output.location = (300, 0)

    mix_node = nodes.get("ALB_Checker_Mix")
    checker_tex = nodes.get("ALB_Checker_Tex")
    checker_bsdf = nodes.get("ALB_Checker_BSDF")
    texcoord = nodes.get("ALB_Checker_TexCoord")
    mapping = nodes.get("ALB_Checker_Mapping")
    value_node = nodes.get("ALB_Checker_Factor")

    if mix_node is None:
        return False

    for l in list(links):
        if l.to_node == output and l.to_socket.name == "Surface":
            links.remove(l)

    if CHECKER_LINK_TAG in material:
        stored = material[CHECKER_LINK_TAG]
        parts = stored.split("|")
        if len(parts) == 2:
            original_node = nodes.get(parts[0])
            if original_node:
                original_socket = original_node.outputs.get(parts[1])
                if original_socket:
                    links.new(original_socket, output.inputs["Surface"])
        del material[CHECKER_LINK_TAG]

    for n in [mix_node, checker_tex, checker_bsdf, texcoord, mapping, value_node]:
        if n and n.name in nodes:
            nodes.remove(n)

    return True


def apply_checker_to_material(material, factor=1.0, scale=10.0):
    if not material:
        return False

    if not material.use_nodes:
        material.use_nodes = True

    nt = material.node_tree
    nodes = nt.nodes
    links = nt.links
    output = get_material_output(material)
    if output is None:
        return False

    mix_node = nodes.get("ALB_Checker_Mix")
    checker_tex = nodes.get("ALB_Checker_Tex")
    mapping = nodes.get("ALB_Checker_Mapping")
    value_node = nodes.get("ALB_Checker_Factor")

    if mix_node and checker_tex and mapping and value_node:
        value_node.outputs[0].default_value = factor
        mapping.inputs["Scale"].default_value[0] = scale
        mapping.inputs["Scale"].default_value[1] = scale
        mapping.inputs["Scale"].default_value[2] = scale
        return True

    remove_checker_from_material(material)

    original_link = None
    for l in links:
        if l.to_node == output and l.to_socket.name == "Surface":
            original_link = l
            break

    original_from_socket = None
    if original_link is not None:
        original_from_node = original_link.from_node
        original_from_socket = original_link.from_socket
        material[CHECKER_LINK_TAG] = f"{original_from_node.name}|{original_from_socket.name}"

    mix_node = nodes.new("ShaderNodeMixShader")
    mix_node.name = "ALB_Checker_Mix"
    mix_node.label = "ALB_Checker_Mix"

    checker_bsdf = nodes.new("ShaderNodeBsdfDiffuse")
    checker_bsdf.name = "ALB_Checker_BSDF"
    checker_bsdf.label = "ALB_Checker_BSDF"

    checker_tex = nodes.new("ShaderNodeTexImage")
    checker_tex.name = "ALB_Checker_Tex"
    checker_tex.label = "ALB_Checker_Tex"
    checker_tex.image = create_checker_image()
    checker_tex.interpolation = 'Closest'
    checker_tex.extension = 'REPEAT'
    checker_tex.image.colorspace_settings.name = 'sRGB'

    texcoord = nodes.new("ShaderNodeTexCoord")
    texcoord.name = "ALB_Checker_TexCoord"
    texcoord.label = "ALB_Checker_TexCoord"

    mapping = nodes.new("ShaderNodeMapping")
    mapping.name = "ALB_Checker_Mapping"
    mapping.label = "ALB_Checker_Mapping"
    mapping.inputs["Scale"].default_value[0] = scale
    mapping.inputs["Scale"].default_value[1] = scale
    mapping.inputs["Scale"].default_value[2] = scale

    value_node = nodes.new("ShaderNodeValue")
    value_node.name = "ALB_Checker_Factor"
    value_node.label = "ALB_Checker_Factor"
    value_node.outputs[0].default_value = factor

    mix_node.location = (output.location.x - 220, output.location.y)
    checker_bsdf.location = (mix_node.location.x - 250, mix_node.location.y - 180)
    value_node.location = (mix_node.location.x - 250, mix_node.location.y + 120)
    checker_tex.location = (checker_bsdf.location.x - 500, checker_bsdf.location.y)
    mapping.location = (checker_tex.location.x - 250, checker_tex.location.y)
    texcoord.location = (mapping.location.x - 250, mapping.location.y)

    if original_link is not None:
        links.remove(original_link)
        links.new(original_from_socket, mix_node.inputs[1])
    links.new(checker_bsdf.outputs["BSDF"], mix_node.inputs[2])
    links.new(value_node.outputs[0], mix_node.inputs["Fac"])
    links.new(texcoord.outputs["UV"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], checker_tex.inputs["Vector"])
    links.new(checker_tex.outputs["Color"], checker_bsdf.inputs["Color"])
    links.new(mix_node.outputs["Shader"], output.inputs["Surface"])

    return True


def apply_checker_to_object(obj, factor=1.0, scale=10.0):
    if obj is None or obj.type != 'MESH':
        return False

    ok = False

    if not obj.data.materials:
        mat = bpy.data.materials.new(name="ALB_Default_Mat")
        mat.use_nodes = True
        obj.data.materials.append(mat)

    for i, mat in enumerate(obj.data.materials):
        if mat is None:
            mat = bpy.data.materials.new(name=f"ALB_Auto_Mat_{i}")
            mat.use_nodes = True
            obj.data.materials[i] = mat

        if not mat.use_nodes:
            mat.use_nodes = True

        applied = apply_checker_to_material(mat, factor=factor, scale=scale)
        ok = ok or applied

    return ok


def remove_checker_from_object(obj):
    if obj is None or obj.type != 'MESH':
        return False
    ok = False
    for mat in obj.data.materials:
        if mat:
            removed = remove_checker_from_material(mat)
            ok = ok or removed
    return ok


def get_checker_target_object(context):
    obj = context.active_object if context is not None else None
    props = context.scene.alb_props if context and getattr(context, "scene", None) and hasattr(context.scene, "alb_props") else None
    if obj is None or getattr(obj, "type", None) != 'MESH':
        return None

    try:
        anchor = str(getattr(props, "workflow_status_anchor", "") or "").upper()
    except Exception:
        anchor = ""

    if anchor == "STEP2":
        high_obj = get_high_object_from_any(obj)
        cage_obj = get_cage_object_from_any(obj)
        if high_obj is not None and cage_obj is not None:
            return high_obj

    return obj


def remove_checker_from_related_objects(obj):
    targets = set()
    if obj is not None and getattr(obj, "type", None) == 'MESH':
        targets.add(obj)
    for getter in (get_high_object_from_any, get_preview_object_from_any, get_uv_object_from_any, get_cage_object_from_any):
        try:
            target = getter(obj)
            if target is not None and getattr(target, "type", None) == 'MESH':
                targets.add(target)
        except Exception:
            pass
    for target in targets:
        try:
            remove_checker_from_object(target)
        except Exception:
            pass


def update_checker_overlay(self, context):
    props = context.scene.alb_props if context and getattr(context, "scene", None) and hasattr(context.scene, "alb_props") else None
    if props is not None and getattr(props, "is_resetting_defaults", False):
        return
    props = context.scene.alb_props
    obj = get_checker_target_object(context)

    if obj is None or obj.type != 'MESH':
        return

    if props.show_checker:
        # Checker stays independent from "Use Texture View".
        # Only switch viewport shading type to Material Preview so the checker is visible.
        switch_to_material_preview(context)
        apply_checker_to_object(obj, factor=props.checker_mix, scale=props.checker_uv_scale)
    else:
        remove_checker_from_related_objects(obj)
        # Keep Material Preview after disabling checker. It is the most predictable
        # view for preview, cage inspection, and final material checks.
        props.use_texture_view = True
        switch_viewport_to_material_preview(context)



def disable_checker_for_bake_on_high(high_obj):
    """Checker is preview-only and must never affect bake results.

    This does not auto-enable checker anywhere. It only removes the checker overlay
    from the HIGH object right before baking if the user had enabled preview checker.
    """
    if high_obj is None or getattr(high_obj, "type", None) != 'MESH':
        return False
    try:
        return remove_checker_from_object(high_obj)
    except Exception:
        return False


def ensure_uv_map(obj):
    if not obj.data.uv_layers:
        obj.data.uv_layers.new(name="UVMap")


def enter_edit_and_select_all(obj):
    ensure_object_mode()
    deselect_all()
    ensure_object_visible_and_active(obj)
    bpy.ops.object.mode_set(mode='EDIT')
    try:
        bpy.ops.mesh.reveal()
    except Exception:
        pass
    try:
        bpy.ops.mesh.select_mode(type='FACE')
    except Exception:
        pass
    bpy.ops.mesh.select_all(action='SELECT')
    try:
        bpy.ops.uv.select_all(action='SELECT')
    except Exception:
        pass


def clear_all_seams_and_sharp(obj):
    ensure_object_mode()
    deselect_all()
    ensure_object_visible_and_active(obj)
    for e in obj.data.edges:
        e.use_seam = False
        e.use_edge_sharp = False
    obj.data.update()


def prepare_mesh_for_uv_unwrap(obj, weld_distance_m=0.0):
    if obj is None or obj.type != 'MESH' or obj.data is None:
        return 0

    ensure_object_mode()
    deselect_all()
    ensure_object_visible_and_active(obj)
    clear_all_seams_and_sharp(obj)

    bm = bmesh.new()
    removed_estimate = 0
    try:
        bm.from_mesh(obj.data)
        before = len(bm.verts)
        verts = list(bm.verts)
        dist = max(0.0, float(weld_distance_m or 0.0))
        if dist > 0.0:
            bmesh.ops.remove_doubles(bm, verts=verts, dist=dist)
        try:
            bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
        except Exception:
            pass
        after = len(bm.verts)
        removed_estimate = max(0, before - after)
        bm.to_mesh(obj.data)
        obj.data.update()
        try:
            obj.data.validate(clean_customdata=False)
        except Exception:
            pass
    except Exception:
        removed_estimate = 0
    finally:
        bm.free()

    clear_all_seams_and_sharp(obj)
    return removed_estimate


def merge_preview_geometry_before_decimate(obj, merge_distance_m=0.0):
    if obj is None or obj.type != 'MESH' or obj.data is None:
        return 0

    ensure_object_mode()
    deselect_all()
    ensure_object_visible_and_active(obj)
    clear_all_seams_and_sharp(obj)

    merged_vertices = 0
    before_verts = len(obj.data.vertices)

    try:
        merge_dist = max(0.0, float(merge_distance_m or 0.0))
        if merge_dist <= 0.0:
            return 0

        bpy.ops.object.mode_set(mode='EDIT')
        try:
            bpy.ops.mesh.reveal()
        except Exception:
            pass
        try:
            bpy.ops.mesh.select_mode(type='VERT')
        except Exception:
            pass
        try:
            bpy.ops.mesh.select_all(action='SELECT')
        except Exception:
            pass

        try:
            bpy.ops.mesh.remove_doubles(threshold=merge_dist)
        except Exception:
            try:
                bpy.ops.mesh.merge_by_distance(distance=merge_dist)
            except Exception:
                pass

        try:
            bpy.ops.mesh.normals_make_consistent(inside=False)
        except Exception:
            pass

        bpy.ops.object.mode_set(mode='OBJECT')

        obj.data.update()
        try:
            obj.data.validate(clean_customdata=False)
        except Exception:
            pass

        after_verts = len(obj.data.vertices)
        merged_vertices = max(0, before_verts - after_verts)
    except Exception:
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except Exception:
            pass
        merged_vertices = 0

    clear_all_seams_and_sharp(obj)
    return merged_vertices




def minimize_uv_stretch_selected(iterations=25):
    """Reduce UV stretch on current selection before average scale + pack."""
    try:
        bpy.ops.uv.select_all(action='SELECT')
    except Exception:
        pass

    # Blender signatures vary a bit; keep this conservative.
    try:
        bpy.ops.uv.minimize_stretch(fill_holes=True, blend=0.0, iterations=iterations)
        return
    except Exception:
        pass
    try:
        bpy.ops.uv.minimize_stretch(iterations=iterations)
    except Exception:
        pass



def selected_uv_bounds_outside_01(obj, epsilon=1e-6):
    """Check if currently selected visible UVs are outside the 0-1 tile."""
    if obj is None or obj.type != 'MESH':
        return False, (0.0, 1.0, 0.0, 1.0)

    try:
        import bmesh
        bm = bmesh.from_edit_mesh(obj.data)
    except Exception:
        return False, (0.0, 1.0, 0.0, 1.0)

    uv_layer = bm.loops.layers.uv.active
    if uv_layer is None:
        return False, (0.0, 1.0, 0.0, 1.0)

    uvs = []
    for f in bm.faces:
        if f.hide or not f.select:
            continue
        for l in f.loops:
            luv = l[uv_layer]
            if getattr(luv, "select", True):
                uvs.append((float(luv.uv.x), float(luv.uv.y)))

    if not uvs:
        return False, (0.0, 1.0, 0.0, 1.0)

    min_u = min(u for u, _ in uvs)
    max_u = max(u for u, _ in uvs)
    min_v = min(v for _, v in uvs)
    max_v = max(v for _, v in uvs)

    outside = (min_u < -epsilon) or (max_u > 1.0 + epsilon) or (min_v < -epsilon) or (max_v > 1.0 + epsilon)
    return outside, (min_u, max_u, min_v, max_v)


def normalize_selected_uvs_to_01(obj, padding=0.0, preserve_aspect=True):
    """Force currently selected visible UVs into the 0-1 tile."""
    if obj is None or obj.type != 'MESH':
        return False

    try:
        import bmesh
        bm = bmesh.from_edit_mesh(obj.data)
    except Exception:
        return False

    uv_layer = bm.loops.layers.uv.active
    if uv_layer is None:
        return False

    selected_loops = []
    for f in bm.faces:
        if f.hide or not f.select:
            continue
        for l in f.loops:
            luv = l[uv_layer]
            if getattr(luv, "select", True):
                selected_loops.append(l)

    if not selected_loops:
        return False

    us = [l[uv_layer].uv.x for l in selected_loops]
    vs = [l[uv_layer].uv.y for l in selected_loops]

    min_u, max_u = min(us), max(us)
    min_v, max_v = min(vs), max(vs)

    width = max(max_u - min_u, 1e-12)
    height = max(max_v - min_v, 1e-12)

    try:
        pad = float(padding)
    except Exception:
        pad = 0.0
    pad = max(0.0, min(0.49, pad))
    available = max(1e-6, 1.0 - (2.0 * pad))

    if preserve_aspect:
        scale = available / max(width, height)
        out_w = width * scale
        out_h = height * scale
        offset_u = pad + ((available - out_w) * 0.5) - (min_u * scale)
        offset_v = pad + ((available - out_h) * 0.5) - (min_v * scale)

        for l in selected_loops:
            uv = l[uv_layer].uv
            uv.x = uv.x * scale + offset_u
            uv.y = uv.y * scale + offset_v
    else:
        scale_u = available / width
        scale_v = available / height
        offset_u = pad - (min_u * scale_u)
        offset_v = pad - (min_v * scale_v)

        for l in selected_loops:
            uv = l[uv_layer].uv
            uv.x = uv.x * scale_u + offset_u
            uv.y = uv.y * scale_v + offset_v

    try:
        bmesh.update_edit_mesh(obj.data)
    except Exception:
        pass
    return True


def enforce_selected_uvs_inside_01(obj, padding=0.0):
    """Safety net after pack: check UV bounds and force-fit into 0-1 if needed."""
    outside, bounds = selected_uv_bounds_outside_01(obj)
    if not outside:
        return False, bounds

    normalize_selected_uvs_to_01(obj, padding=padding, preserve_aspect=True)
    outside_after, bounds_after = selected_uv_bounds_outside_01(obj)
    return True, bounds_after if outside_after else bounds_after


def pack_islands_alb(island_margin=0.01):
    # Target settings:
    # Shape Method: Exact Shape (Concave)
    # Scale: ON
    # Rotate: ON
    # Rotation Method: Any
    # Margin Method: Scaled
    # Pack to: Closest UDIM
    try:
        bpy.ops.uv.pack_islands(
            shape_method='CONCAVE',
            scale=True,
            rotate=True,
            rotate_method='ANY',
            margin_method='SCALED',
            margin=island_margin,
            merge_overlap=False,
            udim_source='CLOSEST_UDIM',
        )
        return
    except TypeError:
        pass

    try:
        bpy.ops.uv.pack_islands(
            shape_method='CONCAVE',
            rotate=True,
            rotate_method='ANY',
            margin_method='SCALED',
            margin=island_margin,
            udim_source='CLOSEST_UDIM',
        )
        return
    except TypeError:
        pass

    try:
        bpy.ops.uv.pack_islands(
            rotate=True,
            rotate_method='ANY',
            margin_method='SCALED',
            margin=island_margin,
        )
        return
    except TypeError:
        pass

    try:
        bpy.ops.uv.pack_islands(
            rotate=True,
            margin=island_margin,
        )
        return
    except TypeError:
        bpy.ops.uv.pack_islands(margin=island_margin)

def finalize_uv_pack(island_margin=0.01):
    bpy.ops.object.mode_set(mode='EDIT')
    try:
        bpy.ops.mesh.select_mode(type='FACE')
    except Exception:
        pass
    bpy.ops.mesh.select_all(action='SELECT')
    try:
        bpy.ops.uv.select_all(action='SELECT')
    except Exception:
        pass
    pack_islands_alb(island_margin)
    bpy.ops.object.mode_set(mode='OBJECT')



def mark_seams_from_current_uv_islands(obj, clear_existing=True):
    """Convert current UV island borders into real mesh seams.

    Robust version:
    for each manifold edge, compare the UV pair on the exact loop that uses that edge
    in each adjacent face. If the UV edge differs across the two faces, mark a seam.
    """
    if obj is None or obj.type != 'MESH':
        return

    ensure_object_mode()
    ensure_uv_map(obj)

    me = obj.data
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.faces.ensure_lookup_table()
    bm.edges.ensure_lookup_table()

    uv_layer = bm.loops.layers.uv.active
    if uv_layer is None:
        bm.free()
        return

    if clear_existing:
        for e in bm.edges:
            e.seam = False

    eps = 1e-5

    def uv_equal(a, b):
        return (a - b).length <= eps

    def get_face_edge_uv_pair(edge, face):
        for loop in face.loops:
            if loop.edge == edge:
                a = loop[uv_layer].uv.copy()
                b = loop.link_loop_next[uv_layer].uv.copy()
                return a, b
        return None, None

    for e in bm.edges:
        if e.is_boundary or (not e.is_manifold) or len(e.link_faces) != 2:
            e.seam = True
            continue

        f1 = e.link_faces[0]
        f2 = e.link_faces[1]

        a1, b1 = get_face_edge_uv_pair(e, f1)
        a2, b2 = get_face_edge_uv_pair(e, f2)

        if a1 is None or b1 is None or a2 is None or b2 is None:
            e.seam = True
            continue

        same_dir = uv_equal(a1, a2) and uv_equal(b1, b2)
        opp_dir = uv_equal(a1, b2) and uv_equal(b1, a2)

        if not (same_dir or opp_dir):
            e.seam = True

    bm.to_mesh(me)
    bm.free()
    me.update()


def seams_from_islands_context_safe(context):
    """Run uv.seams_from_islands with a real UV Editor context.
    Returns True only if the operator actually runs successfully.
    """
    screen = context.screen
    if screen is None:
        return False

    for area in screen.areas:
        if area.type == 'IMAGE_EDITOR':
            for region in area.regions:
                if region.type != 'WINDOW':
                    continue

                space = area.spaces.active
                old_mode = getattr(space, "ui_mode", None)

                try:
                    if hasattr(space, "ui_mode"):
                        space.ui_mode = 'UV'
                except Exception:
                    pass

                try:
                    with context.temp_override(
                        window=context.window,
                        screen=screen,
                        area=area,
                        region=region,
                        space_data=space,
                        scene=context.scene,
                        active_object=context.active_object,
                        object=context.active_object,
                        edit_object=context.edit_object,
                    ):
                        try:
                            bpy.ops.uv.select_all(action='SELECT')
                        except Exception:
                            pass

                        result = bpy.ops.uv.seams_from_islands(
                            mark_seams=True,
                            mark_sharp=False
                        )
                        if 'FINISHED' in result:
                            return True

                except Exception:
                    pass
                finally:
                    try:
                        if old_mode is not None and hasattr(space, "ui_mode"):
                            space.ui_mode = old_mode
                    except Exception:
                        pass

    return False


def smart_uv_and_pack(obj, island_margin=0.01, angle_limit=66.0, do_pack=True):
    """Simple and stable Smart UV flow:
    Smart UV Project -> Average Islands Scale -> Pack Islands
    """
    ensure_uv_map(obj)
    clear_all_seams_and_sharp(obj)
    ensure_object_mode()
    deselect_all()
    ensure_object_visible_and_active(obj)

    bpy.ops.object.mode_set(mode='EDIT')
    try:
        bpy.ops.mesh.reveal()
    except Exception:
        pass
    try:
        bpy.ops.mesh.select_mode(type='FACE')
    except Exception:
        pass
    bpy.ops.mesh.select_all(action='SELECT')

    # 1) Smart UV Project
    bpy.ops.uv.smart_project(
        angle_limit=math.radians(angle_limit),
        island_margin=island_margin,
        area_weight=0.0,
        correct_aspect=True,
        scale_to_bounds=False
    )

    if do_pack:
        # 2) Pack Islands only (keep Smart UV proportions intact for scans/organic assets)
        try:
            bpy.ops.uv.select_all(action='SELECT')
        except Exception:
            pass
        pack_islands_alb(island_margin)


    bpy.ops.object.mode_set(mode='OBJECT')

def smart_uv_per_material_and_pack(obj, target_material_count, island_margin=0.01, angle_limit=66.0):
    if obj is None or obj.type != 'MESH':
        return

    target_material_count = max(1, int(target_material_count))

    ensure_uv_map(obj)
    clear_all_seams_and_sharp(obj)
    ensure_object_mode()
    deselect_all()
    ensure_object_visible_and_active(obj)

    # First split faces into material groups
    split_mesh_into_material_groups_by_axis(obj, target_material_count, axis='X')

    old_sync = None
    try:
        old_sync = bpy.context.scene.tool_settings.use_uv_select_sync
        bpy.context.scene.tool_settings.use_uv_select_sync = True
    except Exception:
        pass

    # Then unwrap each material group independently.
    # Do not use scale_to_bounds: it can stretch scan UVs. Pack Islands handles the layout.
    for mat_index in range(target_material_count):
        bpy.ops.object.mode_set(mode='OBJECT')

        has_faces = False
        for poly in obj.data.polygons:
            sel = (poly.material_index == mat_index)
            poly.select = sel
            has_faces = has_faces or sel

        if not has_faces:
            continue

        bpy.ops.object.mode_set(mode='EDIT')
        try:
            bpy.ops.mesh.reveal()
        except Exception:
            pass
        try:
            bpy.ops.mesh.select_mode(type='FACE')
        except Exception:
            pass

        # 1) Smart UV only on currently selected faces for this material
        bpy.ops.uv.smart_project(
            angle_limit=math.radians(angle_limit),
            island_margin=island_margin,
            area_weight=0.0,
            correct_aspect=True,
            scale_to_bounds=False
        )

        # 2) Pack Islands last, only for the selected material faces
        pack_islands_alb(island_margin)

    bpy.ops.object.mode_set(mode='OBJECT')

    try:
        if old_sync is not None:
            bpy.context.scene.tool_settings.use_uv_select_sync = old_sync
    except Exception:
        pass



# ------------------------------------------------------------
# Materials / bake
# ------------------------------------------------------------

def create_image(name, size, alpha=False, color=(0.0, 0.0, 0.0, 1.0)):
    image_name = name
    if bpy.data.images.get(image_name):
        suffix = int(time.time() * 1000) % 100000
        image_name = f"{name}_{suffix}"
        counter = 1
        while bpy.data.images.get(image_name):
            image_name = f"{name}_{suffix}_{counter:02d}"
            counter += 1
    img = bpy.data.images.new(name=image_name, width=size, height=size, alpha=alpha)
    img.generated_color = color
    try:
        img["alb_scanready_bake_image"] = True
        img.use_fake_user = False
    except Exception:
        pass
    return img


def build_final_material(low_obj, basecolor_img=None, normal_img=None):
    final_mat_name = f"{get_base_name(low_obj)}_Final_Mat"
    final_mat = bpy.data.materials.get(final_mat_name)
    if final_mat is None:
        final_mat = bpy.data.materials.new(final_mat_name)
        final_mat.use_nodes = True
    try:
        final_mat.use_fake_user = False
    except Exception:
        pass

    nt = final_mat.node_tree
    nodes = nt.nodes
    links = nt.links
    nodes.clear()

    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (400, 0)

    principled = nodes.new("ShaderNodeBsdfPrincipled")
    principled.location = (100, 0)
    links.new(principled.outputs["BSDF"], out.inputs["Surface"])

    if basecolor_img:
        base_node = nodes.new("ShaderNodeTexImage")
        base_node.location = (-500, 150)
        base_node.image = basecolor_img
        base_node.image.colorspace_settings.name = 'sRGB'
        links.new(base_node.outputs["Color"], principled.inputs["Base Color"])

    if normal_img:
        ntex = nodes.new("ShaderNodeTexImage")
        ntex.location = (-500, -150)
        ntex.image = normal_img
        ntex.image.colorspace_settings.name = 'Non-Color'

        nmap = nodes.new("ShaderNodeNormalMap")
        nmap.location = (-200, -150)

        links.new(ntex.outputs["Color"], nmap.inputs["Color"])
        links.new(nmap.outputs["Normal"], principled.inputs["Normal"])

    low_obj.data.materials.clear()
    low_obj.data.materials.append(final_mat)
    return final_mat



def ensure_target_material_slots(obj, target_material_count):
    target_material_count = max(1, int(target_material_count))

    while len(obj.data.materials) > target_material_count:
        obj.data.materials.pop(index=len(obj.data.materials) - 1)

    while len(obj.data.materials) < target_material_count:
        mat = bpy.data.materials.new(
            name=f"{get_base_name(obj)}_Bake_Mat_{len(obj.data.materials):02d}"
        )
        mat.use_nodes = True
        obj.data.materials.append(mat)


def split_mesh_into_material_groups_by_axis(obj, target_material_count, axis='X'):
    if obj is None or obj.type != 'MESH':
        return

    target_material_count = max(1, int(target_material_count))
    axis_map = {'X': 0, 'Y': 1, 'Z': 2}
    axis_index = axis_map.get(axis.upper(), 0)

    ensure_target_material_slots(obj, target_material_count)

    coords = [v.co[axis_index] for v in obj.data.vertices]
    if not coords:
        return

    min_c = min(coords)
    max_c = max(coords)
    span = max(max_c - min_c, 1e-8)

    for poly in obj.data.polygons:
        center = poly.center[axis_index]
        normalized = (center - min_c) / span
        mat_index = int(normalized * target_material_count)
        mat_index = min(mat_index, target_material_count - 1)
        poly.material_index = mat_index

    obj.data.update()


def repack_uvs_per_material(obj, target_material_count, uv_margin=0.01):
    if obj is None or obj.type != 'MESH':
        return

    target_material_count = max(1, int(target_material_count))
    ensure_object_mode()
    deselect_all()
    ensure_object_visible_and_active(obj)

    # Repack each material group independently so each baked texture uses the full 0-1 UV space
    for mat_index in range(target_material_count):
        bpy.ops.object.mode_set(mode='OBJECT')

        has_faces = False
        for poly in obj.data.polygons:
            sel = (poly.material_index == mat_index)
            poly.select = sel
            has_faces = has_faces or sel

        if not has_faces:
            continue

        bpy.ops.object.mode_set(mode='EDIT')
        try:
            bpy.ops.mesh.select_mode(type='FACE')
        except Exception:
            pass

        # Make sure UV selection follows selected faces
        try:
            bpy.context.scene.tool_settings.use_uv_select_sync = True
        except Exception:
            pass

        try:
            bpy.ops.uv.select_all(action='SELECT')
        except Exception:
            pass

        try:
            pack_islands_alb(uv_margin)
        except Exception:
            pass

    bpy.ops.object.mode_set(mode='OBJECT')

def prepare_uv_material_slots_for_bake(uv_obj, slot_count, uv_margin=0.01):
    if uv_obj is None or uv_obj.type != 'MESH':
        return

    slot_count = max(1, int(slot_count))
    props = bpy.context.scene.alb_props if getattr(bpy.context, "scene", None) and hasattr(bpy.context.scene, "alb_props") else None

    ensure_object_mode()
    deselect_all()
    try:
        uv_obj.hide_set(False)
    except Exception:
        pass
    try:
        uv_obj.hide_viewport = False
    except Exception:
        pass
    ensure_object_visible_and_active(uv_obj)

    # STEP 1 - assign material groups
    ensure_target_material_slots(uv_obj, slot_count)

    if slot_count == 1:
        for poly in uv_obj.data.polygons:
            poly.material_index = 0
        try:
            uv_obj.data.update()
        except Exception:
            pass

        # Important:
        # if the user previously baked with multiple materials, the UV layout may still
        # be split/packed as separate groups. When going back to 1 material, rebuild
        # the UV layout for the whole object so everything is packed together in 0-1.
        try:
            smart_uv_and_pack(
                uv_obj,
                island_margin=uv_margin,
                angle_limit=float(getattr(props, "smart_uv_angle", 66.0)) if props is not None else 66.0,
                do_pack=True
            )
        except Exception:
            # Fallback        except Exception:
            # Fallback: at least repack the whole existing UV layout
            try:
                finalize_uv_pack(uv_margin)
            except Exception:
                pass
        return

    split_mesh_into_material_groups_by_axis(uv_obj, slot_count, axis='X')

    old_sync = None
    try:
        old_sync = bpy.context.scene.tool_settings.use_uv_select_sync
        bpy.context.scene.tool_settings.use_uv_select_sync = True
    except Exception:
        pass

    try:
        # STEP 2 - unwrap + pack each material independently
        for mat_index in range(slot_count):
            bpy.ops.object.mode_set(mode='OBJECT')

            has_faces = False
            for poly in uv_obj.data.polygons:
                sel = (poly.material_index == mat_index)
                poly.select = sel
                has_faces = has_faces or sel

            try:
                uv_obj.data.update()
            except Exception:
                pass

            if not has_faces:
                continue

            bpy.ops.object.mode_set(mode='EDIT')

            try:
                bpy.ops.mesh.reveal()
            except Exception:
                pass
            try:
                bpy.ops.mesh.select_mode(type='FACE')
            except Exception:
                pass

            # Work only on the current material group
            try:
                bpy.ops.mesh.hide(unselected=True)
            except Exception:
                pass

            try:
                bpy.ops.mesh.select_all(action='SELECT')
            except Exception:
                pass
            try:
                bpy.ops.uv.select_all(action='SELECT')
            except Exception:
                pass

            bpy.ops.uv.smart_project(
                angle_limit=math.radians(float(getattr(props, "smart_uv_angle", 66.0)) if props is not None else 66.0),
                island_margin=uv_margin,
                area_weight=0.0,
                correct_aspect=True,
                scale_to_bounds=False
            )

            try:
                bpy.ops.uv.select_all(action='SELECT')
            except Exception:
                pass
            try:
                pack_islands_alb(uv_margin)
            except Exception:
                pass


            try:
                bpy.ops.mesh.reveal()
            except Exception:
                pass
            try:
                bpy.ops.mesh.select_all(action='DESELECT')
            except Exception:
                pass

        bpy.ops.object.mode_set(mode='OBJECT')

    finally:
        try:
            if old_sync is not None:
                bpy.context.scene.tool_settings.use_uv_select_sync = old_sync
        except Exception:
            pass


def find_first_image_from_socket(socket, visited=None, depth=0):
    if socket is None or depth > 8:
        return None
    if visited is None:
        visited = set()

    try:
        links = list(socket.links)
    except Exception:
        links = []

    for link in links:
        node = getattr(link, "from_node", None)
        if node is None:
            continue
        node_key = getattr(node, "name", str(id(node)))
        if node_key in visited:
            continue
        visited.add(node_key)

        if getattr(node, "type", "") == 'TEX_IMAGE':
            image = getattr(node, "image", None)
            if image is not None:
                return image

        for input_socket in getattr(node, "inputs", []):
            image = find_first_image_from_socket(input_socket, visited, depth + 1)
            if image is not None:
                return image

    return None


def find_first_image_color_socket_from_socket(socket, visited=None, depth=0):
    if socket is None or depth > 8:
        return None, None
    if visited is None:
        visited = set()

    try:
        links = list(socket.links)
    except Exception:
        links = []

    for link in links:
        node = getattr(link, "from_node", None)
        if node is None:
            continue
        try:
            node_key = node.as_pointer()
        except Exception:
            node_key = getattr(node, "name", str(id(node)))
        if node_key in visited:
            continue
        visited.add(node_key)

        if getattr(node, "type", "") == 'TEX_IMAGE':
            image = getattr(node, "image", None)
            color_socket = node.outputs.get("Color") if hasattr(node.outputs, "get") else None
            if image is not None and color_socket is not None:
                return color_socket, image

        for input_socket in getattr(node, "inputs", []):
            color_socket, image = find_first_image_color_socket_from_socket(input_socket, visited, depth + 1)
            if color_socket is not None and image is not None:
                return color_socket, image

    return None, None


def find_normal_map_image_from_socket(socket, visited=None, depth=0):
    if socket is None or depth > 8:
        return None
    if visited is None:
        visited = set()

    try:
        links = list(socket.links)
    except Exception:
        links = []

    for link in links:
        node = getattr(link, "from_node", None)
        if node is None:
            continue
        try:
            node_key = node.as_pointer()
        except Exception:
            node_key = getattr(node, "name", str(id(node)))
        if node_key in visited:
            continue
        visited.add(node_key)

        node_type = getattr(node, "type", "")
        if node_type == 'NORMAL_MAP':
            color_socket = node.inputs.get("Color")
            image = find_first_image_from_socket(color_socket, visited, depth + 1)
            if image is not None:
                return image
        elif node_type == 'TEX_IMAGE':
            image = getattr(node, "image", None)
            if image is not None:
                return image

        normal_socket = node.inputs.get("Normal") if hasattr(node.inputs, "get") else None
        image = find_normal_map_image_from_socket(normal_socket, visited, depth + 1)
        if image is not None:
            return image

    return None


def get_principled_bsdf_node(mat):
    if mat is None or not getattr(mat, "use_nodes", False):
        return None
    nt = getattr(mat, "node_tree", None)
    if nt is None:
        return None
    for node in nt.nodes:
        if getattr(node, "type", "") == 'BSDF_PRINCIPLED':
            return node
    return None


def get_linked_material_image(mat, principled_input_name):
    bsdf = get_principled_bsdf_node(mat)
    if bsdf is None:
        return None
    socket = bsdf.inputs.get(principled_input_name)
    if principled_input_name == "Normal":
        return find_normal_map_image_from_socket(socket)
    return find_first_image_from_socket(socket)


def get_material_surface_output(mat):
    if mat is None or not getattr(mat, "use_nodes", False):
        return None
    nt = getattr(mat, "node_tree", None)
    if nt is None:
        return None
    for node in nt.nodes:
        if getattr(node, "type", "") == 'OUTPUT_MATERIAL':
            return node
    return None


def find_first_image_in_material(mat):
    if mat is None or not getattr(mat, "use_nodes", False):
        return None
    nt = getattr(mat, "node_tree", None)
    if nt is None:
        return None
    preferred_names = ("base", "albedo", "diffuse", "color", "col")
    candidates = []
    for node in nt.nodes:
        if getattr(node, "type", "") != 'TEX_IMAGE':
            continue
        image = getattr(node, "image", None)
        if image is None:
            continue
        name = f"{getattr(node, 'name', '')} {getattr(node, 'label', '')} {getattr(image, 'name', '')}".lower()
        score = 1
        if any(token in name for token in preferred_names):
            score += 10
        if any(token in name for token in ("normal", "rough", "metal", "ao", "occlusion", "height", "disp")):
            score -= 5
        candidates.append((score, image))
    if not candidates:
        return None
    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1]


def get_source_base_color_image(mat):
    image = get_linked_material_image(mat, "Base Color")
    if image is not None:
        return image

    output = get_material_surface_output(mat)
    if output is not None:
        image = find_first_image_from_socket(output.inputs.get("Surface"))
        if image is not None:
            return image

    return find_first_image_in_material(mat)


def get_source_base_color_socket(mat):
    bsdf = get_principled_bsdf_node(mat)
    if bsdf is not None:
        socket = bsdf.inputs.get("Base Color")
        color_socket, image = find_first_image_color_socket_from_socket(socket)
        if color_socket is not None and image is not None:
            return color_socket, image

    output = get_material_surface_output(mat)
    if output is not None:
        color_socket, image = find_first_image_color_socket_from_socket(output.inputs.get("Surface"))
        if color_socket is not None and image is not None:
            return color_socket, image

    image = find_first_image_in_material(mat)
    if image is None:
        return None, None

    nt = getattr(mat, "node_tree", None)
    if nt is None:
        return None, None
    for node in nt.nodes:
        if getattr(node, "type", "") == 'TEX_IMAGE' and getattr(node, "image", None) == image:
            color_socket = node.outputs.get("Color") if hasattr(node.outputs, "get") else None
            if color_socket is not None:
                return color_socket, image
    return None, None


def force_linked_image_non_color(mat, principled_input_name, states=None):
    image = get_linked_material_image(mat, principled_input_name)
    if image is None:
        return False

    color_settings = getattr(image, "colorspace_settings", None)
    if color_settings is None:
        return False

    try:
        old_name = color_settings.name
    except Exception:
        old_name = None

    try:
        color_settings.name = 'Non-Color'
        if states is not None and old_name != 'Non-Color':
            states.append((image, old_name))
        return True
    except Exception:
        return False


def enforce_high_source_data_images_non_color(high_obj):
    if high_obj is None or getattr(high_obj, "type", None) != 'MESH':
        return 0

    changed = 0
    seen_images = set()
    for mat in high_obj.data.materials:
        if mat is None or not getattr(mat, "use_nodes", False):
            continue
        for input_name in ("Normal", "Roughness"):
            image = get_linked_material_image(mat, input_name)
            if image is None:
                continue
            try:
                key = image.as_pointer()
            except Exception:
                key = id(image)
            if key in seen_images:
                continue
            seen_images.add(key)
            if force_linked_image_non_color(mat, input_name):
                changed += 1
    return changed


def restore_image_color_spaces(states):
    for image, old_name in states:
        if image is None or old_name is None:
            continue
        try:
            image.colorspace_settings.name = old_name
        except Exception:
            pass


def collect_linked_source_images(high_obj, slot_count, principled_input_name):
    images = [None] * max(1, int(slot_count))
    if high_obj is None or getattr(high_obj, "type", None) != 'MESH':
        return images

    materials = [mat for mat in high_obj.data.materials if mat is not None]
    if not materials:
        return images

    for idx in range(len(images)):
        mat = None
        if idx < len(materials):
            mat = materials[idx]
        elif len(materials) == 1:
            mat = materials[0]

        image = get_linked_material_image(mat, principled_input_name)
        if image is not None:
            images[idx] = image

    return images


def get_source_socket_for_texture_transfer(mat, principled_input_name):
    bsdf = get_principled_bsdf_node(mat)
    if bsdf is None:
        return None

    socket = bsdf.inputs.get(principled_input_name)
    if socket is None:
        return None

    if principled_input_name == "Normal":
        image = get_linked_material_image(mat, principled_input_name)
        if image is None:
            return None
        nt = mat.node_tree
        for node in nt.nodes:
            if getattr(node, "type", "") == 'TEX_IMAGE' and getattr(node, "image", None) == image:
                return node.outputs.get("Color")
        return None

    try:
        links = list(socket.links)
    except Exception:
        links = []
    if links:
        return getattr(links[0], "from_socket", None)

    return None


def setup_high_materials_for_texture_transfer(high_obj, principled_input_name, default_color):
    states = []
    color_space_states = []
    if high_obj is None or getattr(high_obj, "type", None) != 'MESH':
        return states, color_space_states

    for mat in high_obj.data.materials:
        if mat is None or not getattr(mat, "use_nodes", False):
            continue
        nt = getattr(mat, "node_tree", None)
        if nt is None:
            continue

        nodes = nt.nodes
        links = nt.links
        output = None
        for node in nodes:
            if getattr(node, "type", "") == 'OUTPUT_MATERIAL':
                output = node
                break
        if output is None:
            continue

        linked_image = get_linked_material_image(mat, principled_input_name)
        if linked_image is None:
            continue

        if principled_input_name == "Normal":
            # Normal maps are data textures. Keep them Non-Color permanently on
            # the high source so transfer bakes and later viewport evaluation match.
            force_linked_image_non_color(mat, principled_input_name)
        elif principled_input_name == "Roughness":
            # Roughness is data, not color. Keep source roughness images as Non-Color
            # so the high mesh and baked final mesh are interpreted the same way.
            force_linked_image_non_color(mat, principled_input_name)

        surface_socket = output.inputs.get("Surface")
        original_sources = []
        try:
            for link in list(surface_socket.links):
                original_sources.append(link.from_socket)
                links.remove(link)
        except Exception:
            pass

        emission = nodes.new("ShaderNodeEmission")
        emission.name = "ALB_TextureTransfer_Emission"
        emission.location = (120, -360)
        source_socket = get_source_socket_for_texture_transfer(mat, principled_input_name)
        try:
            if source_socket is not None:
                links.new(source_socket, emission.inputs["Color"])
            else:
                emission.inputs["Color"].default_value = default_color
            emission.inputs["Strength"].default_value = 1.0
            links.new(emission.outputs["Emission"], surface_socket)
        except Exception:
            pass

        states.append((mat, output, original_sources, emission))

    return states, color_space_states


def setup_high_materials_for_standard_texture_bake(high_obj, bake_input_name):
    """Temporarily replace complex source shaders with simple texture materials."""
    states = []
    color_space_states = []
    if high_obj is None or getattr(high_obj, "type", None) != 'MESH':
        return states, color_space_states

    for mat in high_obj.data.materials:
        if mat is None:
            continue
        if not getattr(mat, "use_nodes", False):
            mat.use_nodes = True
        nt = getattr(mat, "node_tree", None)
        if nt is None:
            continue

        base_color_socket, base_image = get_source_base_color_socket(mat)
        normal_image = get_linked_material_image(mat, "Normal")
        roughness_image = get_linked_material_image(mat, "Roughness")

        if bake_input_name == "Base Color" and base_image is None:
            continue
        if bake_input_name == "Normal" and normal_image is None:
            continue
        if bake_input_name == "Roughness" and roughness_image is None:
            continue

        nodes = nt.nodes
        links = nt.links
        output = get_material_surface_output(mat)
        if output is None:
            output = nodes.new("ShaderNodeOutputMaterial")
            output.location = (420, 0)

        surface_socket = output.inputs.get("Surface")
        original_sources = []
        try:
            for link in list(surface_socket.links):
                original_sources.append(link.from_socket)
                links.remove(link)
        except Exception:
            pass

        created_nodes = []

        def add_image_node(image, name, location):
            node = nodes.new("ShaderNodeTexImage")
            node.name = name
            node.label = name
            node.image = image
            node.location = location
            created_nodes.append(node)
            return node

        try:
            if bake_input_name == "Base Color":
                shader = nodes.new("ShaderNodeEmission")
                shader.name = "ALB_StandardBake_Emission"
                shader.location = (120, -360)
                created_nodes.append(shader)
                links.new(base_color_socket, shader.inputs["Color"])
                shader.inputs["Strength"].default_value = 1.0
                links.new(shader.outputs["Emission"], surface_socket)
            else:
                shader = nodes.new("ShaderNodeEmission")
                shader.name = "ALB_StandardBake_DataEmission"
                shader.location = (120, -360)
                created_nodes.append(shader)
                data_image = normal_image if bake_input_name == "Normal" else roughness_image
                node_name = "ALB_StandardBake_Normal" if bake_input_name == "Normal" else "ALB_StandardBake_Roughness"
                data_node = add_image_node(data_image, node_name, (-420, -300))
                force_image_non_color(data_image, color_space_states)
                links.new(data_node.outputs["Color"], shader.inputs["Color"])
                shader.inputs["Strength"].default_value = 1.0
                links.new(shader.outputs["Emission"], surface_socket)
        except Exception:
            pass

        states.append((mat, output, original_sources, created_nodes))

    return states, color_space_states


def force_image_non_color(image, states=None):
    if image is None:
        return False
    color_settings = getattr(image, "colorspace_settings", None)
    if color_settings is None:
        return False
    try:
        old_name = color_settings.name
    except Exception:
        old_name = None
    try:
        color_settings.name = 'Non-Color'
        if states is not None and old_name != 'Non-Color':
            states.append((image, old_name))
        return True
    except Exception:
        return False


def restore_high_materials_after_standard_texture_bake(states):
    for mat, output, original_sources, created_nodes in states:
        try:
            nt = mat.node_tree
            nodes = nt.nodes
            links = nt.links
            surface_socket = output.inputs.get("Surface")
            for link in list(surface_socket.links):
                links.remove(link)
            for source_socket in original_sources:
                try:
                    links.new(source_socket, surface_socket)
                except Exception:
                    pass
            for node in created_nodes:
                try:
                    nodes.remove(node)
                except Exception:
                    pass
        except Exception:
            pass


def restore_high_materials_after_texture_transfer(states):
    for mat, output, original_sources, emission in states:
        try:
            nt = mat.node_tree
            nodes = nt.nodes
            links = nt.links
            surface_socket = output.inputs.get("Surface")
            for link in list(surface_socket.links):
                links.remove(link)
            for source_socket in original_sources:
                try:
                    links.new(source_socket, surface_socket)
                except Exception:
                    pass
            if emission is not None:
                nodes.remove(emission)
        except Exception:
            pass


def build_final_materials_for_slots(low_obj, basecolor_imgs, normal_imgs, slot_count, occlusion_imgs=None, roughness_imgs=None):
    while len(low_obj.data.materials) < slot_count:
        low_obj.data.materials.append(None)

    for idx in range(slot_count):
        final_mat_name = f"{get_base_name(low_obj)}_Final_Mat_{idx:02d}"
        final_mat = bpy.data.materials.get(final_mat_name)
        if final_mat is None:
            final_mat = bpy.data.materials.new(final_mat_name)
            final_mat.use_nodes = True
        elif not final_mat.use_nodes:
            final_mat.use_nodes = True
        try:
            final_mat.use_fake_user = False
        except Exception:
            pass

        nt = final_mat.node_tree
        nodes = nt.nodes
        links = nt.links

        # Conservative rebuild: clear the existing node tree, but do not recreate the material datablock.
        # Reusing the same datablock is safer for Blender preview jobs than destroying/recreating materials often.
        try:
            nodes.clear()
        except Exception:
            for n in list(nodes):
                try:
                    nodes.remove(n)
                except Exception:
                    pass

        out = nodes.new("ShaderNodeOutputMaterial")
        out.location = (450, 0)
        principled = nodes.new("ShaderNodeBsdfPrincipled")
        principled.location = (150, 0)
        links.new(principled.outputs["BSDF"], out.inputs["Surface"])

        base_img = basecolor_imgs[idx] if idx < len(basecolor_imgs) else None
        normal_img = normal_imgs[idx] if idx < len(normal_imgs) else None
        ao_img = occlusion_imgs[idx] if occlusion_imgs and idx < len(occlusion_imgs) else None
        roughness_img = roughness_imgs[idx] if roughness_imgs and idx < len(roughness_imgs) else None

        if isinstance(base_img, str):
            base_img = load_saved_image_if_exists(base_img)
        if isinstance(normal_img, str):
            normal_img = load_saved_image_if_exists(normal_img)
        if isinstance(ao_img, str):
            ao_img = load_saved_image_if_exists(ao_img)
        if isinstance(roughness_img, str):
            roughness_img = load_saved_image_if_exists(roughness_img)

        base_node = None
        if base_img:
            base_node = nodes.new("ShaderNodeTexImage")
            base_node.location = (-700, 180)
            base_node.image = base_img
            base_node.image.colorspace_settings.name = 'sRGB'

        ao_node = None
        if ao_img:
            ao_node = nodes.new("ShaderNodeTexImage")
            ao_node.location = (-700, -40)
            ao_node.image = ao_img
            ao_node.image.colorspace_settings.name = 'Non-Color'

        if base_node and ao_node:
            mix_node = nodes.new("ShaderNodeMix")
            mix_node.location = (-340, 110)
            try:
                mix_node.data_type = 'RGBA'
                mix_node.blend_type = 'MULTIPLY'
                mix_node.factor_mode = 'UNIFORM'
                mix_node.inputs["Factor"].default_value = 1.0
                links.new(base_node.outputs["Color"], mix_node.inputs["A"])
                links.new(ao_node.outputs["Color"], mix_node.inputs["B"])
                links.new(mix_node.outputs["Result"], principled.inputs["Base Color"])
            except Exception:
                try:
                    mix_node.blend_type = 'MULTIPLY'
                    mix_node.inputs[0].default_value = 1.0
                    links.new(base_node.outputs["Color"], mix_node.inputs[6])
                    links.new(ao_node.outputs["Color"], mix_node.inputs[7])
                    links.new(mix_node.outputs[2], principled.inputs["Base Color"])
                except Exception:
                    links.new(base_node.outputs["Color"], principled.inputs["Base Color"])
        elif base_node:
            links.new(base_node.outputs["Color"], principled.inputs["Base Color"])
        elif ao_node:
            links.new(ao_node.outputs["Color"], principled.inputs["Base Color"])

        if normal_img:
            ntex = nodes.new("ShaderNodeTexImage")
            ntex.location = (-700, -240)
            ntex.image = normal_img
            ntex.image.colorspace_settings.name = 'Non-Color'
            nmap = nodes.new("ShaderNodeNormalMap")
            nmap.location = (-340, -240)
            try:
                nmap.inputs["Strength"].default_value = bpy.context.scene.alb_props.normal_strength
            except Exception:
                try:
                    nmap.inputs["Strength"].default_value = DEFAULTS['normal_strength']
                except Exception:
                    pass
            links.new(ntex.outputs["Color"], nmap.inputs["Color"])
            links.new(nmap.outputs["Normal"], principled.inputs["Normal"])

        if roughness_img:
            rtex = nodes.new("ShaderNodeTexImage")
            rtex.location = (-700, -430)
            rtex.image = roughness_img
            rtex.image.colorspace_settings.name = 'Non-Color'
            try:
                links.new(rtex.outputs["Color"], principled.inputs["Roughness"])
            except Exception:
                pass

        low_obj.data.materials[idx] = final_mat

    while len(low_obj.data.materials) > slot_count:
        low_obj.data.materials.pop(index=len(low_obj.data.materials)-1)



# ------------------------------------------------------------
# Cage preview helpers
# ------------------------------------------------------------

CAGE_SAFETY_COLOR_ATTR = "ALB_Cage_Safety"
CAGE_SAFETY_DISTANCE_ATTR = "ALB_Cage_Safety_Distance"


def get_cage_color_from_extrusion(extrusion_mm):
    try:
        val = float(extrusion_mm)
    except Exception:
        val = 0.0

    # Use millimeter thresholds for clearer visual feedback:
    # 0 mm = red, 0-2 mm = orange/yellow, >= 2 mm = green
    if val <= 0.0:
        return (1.0, 0.0, 0.0, 1.0)
    elif val < 2.0:
        return (1.0, 0.75, 0.15, 1.0)
    else:
        return (0.0, 1.0, 0.2, 1.0)


def get_cage_color_from_target_progress(current_mm, target_mm, alpha=1.0):
    try:
        current = max(0.0, float(current_mm))
        target = max(0.0001, float(target_mm))
    except Exception:
        return (1.0, 0.0, 0.0, alpha)

    ratio = max(0.0, min(1.0, current / target))
    if ratio < 0.5:
        k = ratio / 0.5
        return (1.0, 0.75 * k, 0.0, alpha)

    k = (ratio - 0.5) / 0.5
    return (1.0 - k, 0.75 + (0.25 * k), 0.0, alpha)


def ensure_cage_material():
    mat_name = "ALB_Cage_Preview_Mat"
    mat = bpy.data.materials.get(mat_name)
    if mat is None:
        mat = bpy.data.materials.new(mat_name)
    mat.use_nodes = True
    nt = mat.node_tree
    nodes = nt.nodes
    links = nt.links
    nodes.clear()

    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (250, 0)

    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (0, 0)

    try:
        bsdf.inputs["Roughness"].default_value = 0.2
    except Exception:
        pass

    try:
        if "Specular IOR Level" in bsdf.inputs:
            bsdf.inputs["Specular IOR Level"].default_value = 0.0
        elif "Specular" in bsdf.inputs:
            bsdf.inputs["Specular"].default_value = 0.0
    except Exception:
        pass

    try:
        props = bpy.context.scene.alb_props
        current_mm = float(getattr(props, "cage_extrusion_mm", 0.0))
        target_mm = float(getattr(props, "auto_cage_target_mm", 0.0))
        alpha = float(getattr(props, "cage_alpha", 1.0))
        if target_mm > 0.0:
            color = get_cage_color_from_target_progress(current_mm, target_mm, alpha)
        else:
            color = get_cage_color_from_extrusion(current_mm)
            color = (color[0], color[1], color[2], alpha)
        bsdf.inputs["Base Color"].default_value = color
    except Exception:
        bsdf.inputs["Base Color"].default_value = (1.0, 0.0, 0.0, 1.0)

    try:
        if "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = bpy.context.scene.alb_props.cage_alpha
    except Exception:
        pass

    try:
        mat.blend_method = 'BLEND'
        mat.shadow_method = 'NONE'
    except Exception:
        pass

    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def get_cage_heat_color(ratio, alpha=1.0):
    t = max(0.0, min(1.0, float(ratio)))
    if t < 0.5:
        k = t / 0.5
        return (1.0, 0.85 * k, 0.0, alpha)
    k = (t - 0.5) / 0.5
    return (1.0 - k, 0.85 + (0.15 * k), 0.0, alpha)


def ensure_color_attribute(mesh, name):
    try:
        attr = mesh.color_attributes.get(name)
        if attr is None:
            attr = mesh.color_attributes.new(name=name, type='BYTE_COLOR', domain='CORNER')
        return attr
    except Exception:
        return None


def ensure_distance_attribute(mesh, name):
    try:
        attr = mesh.attributes.get(name)
        if attr is None:
            attr = mesh.attributes.new(name=name, type='FLOAT', domain='POINT')
        return attr
    except Exception:
        return None


def write_cage_safety_colors_from_distances(cage_obj, max_distance_m, alpha=1.0):
    if cage_obj is None or cage_obj.type != 'MESH' or cage_obj.data is None:
        return False
    mesh = cage_obj.data
    color_attr = ensure_color_attribute(mesh, CAGE_SAFETY_COLOR_ATTR)
    try:
        distance_attr = mesh.attributes.get(CAGE_SAFETY_DISTANCE_ATTR)
    except Exception:
        distance_attr = None
    if color_attr is None or distance_attr is None:
        return False

    safe_max = max(float(max_distance_m), 0.000001)
    try:
        vertex_distances = [max(0.0, float(item.value)) for item in distance_attr.data]
    except Exception:
        return False

    try:
        for poly in mesh.polygons:
            for loop_index in poly.loop_indices:
                vertex_index = mesh.loops[loop_index].vertex_index
                local_distance = vertex_distances[vertex_index] if vertex_index < len(vertex_distances) else 0.0
                color_attr.data[loop_index].color = get_cage_heat_color(local_distance / safe_max, alpha)
        mesh.update()
        return True
    except Exception:
        return False


def update_cage_safety_colors(context, cage_obj, uv_obj=None, high_obj=None):
    if context is None or cage_obj is None or cage_obj.type != 'MESH':
        return False
    try:
        props = context.scene.alb_props
        target_mm = float(getattr(props, "auto_cage_target_mm", 0.0))
        current_mm = float(props.cage_extrusion_mm)
        alpha = float(props.cage_alpha)
    except Exception:
        target_mm = 0.0
        current_mm = 0.0
        alpha = 1.0

    try:
        cage_mat = ensure_cage_material()
        if cage_obj.data.materials:
            cage_obj.data.materials[0] = cage_mat
        else:
            cage_obj.data.materials.append(cage_mat)

        color = get_cage_color_from_target_progress(current_mm, target_mm, alpha) if target_mm > 0.0 else get_cage_color_from_extrusion(current_mm)
        color = (color[0], color[1], color[2], alpha)
        for node in cage_mat.node_tree.nodes:
            if getattr(node, "type", "") == 'BSDF_PRINCIPLED':
                if "Base Color" in node.inputs:
                    node.inputs["Base Color"].default_value = color
                if "Alpha" in node.inputs:
                    node.inputs["Alpha"].default_value = alpha
                break
        cage_obj.data.update()
        return True
    except Exception:
        return False

    max_distance_m = max(0.000001, current_mm * 0.001)

    if uv_obj is None:
        try:
            uv_obj = bpy.data.objects.get(cage_obj.get("alb_uv_object", ""))
        except Exception:
            uv_obj = None
    if high_obj is None and uv_obj is not None:
        high_obj = get_high_object_from_any(uv_obj)
    if high_obj is None or high_obj.type != 'MESH':
        return False

    depsgraph = context.evaluated_depsgraph_get()
    try:
        depsgraph.update()
    except Exception:
        pass

    high_eval = None
    high_mesh = None
    try:
        high_eval = high_obj.evaluated_get(depsgraph)
        high_mesh = high_eval.to_mesh()
        if high_mesh is None or len(high_mesh.vertices) == 0 or len(high_mesh.polygons) == 0:
            return False

        from mathutils.bvhtree import BVHTree
        cage_inv = cage_obj.matrix_world.inverted()
        high_world = high_eval.matrix_world if high_eval is not None else high_obj.matrix_world
        high_to_cage = cage_inv @ high_world
        high_vertices = [high_to_cage @ v.co for v in high_mesh.vertices]
        high_polygons = [list(poly.vertices) for poly in high_mesh.polygons]
        high_bvh = BVHTree.FromPolygons(high_vertices, high_polygons, all_triangles=False)
        distance_attr = ensure_distance_attribute(cage_obj.data, CAGE_SAFETY_DISTANCE_ATTR)
        if high_bvh is None or distance_attr is None:
            return False

        cage_mesh = cage_obj.data
        for vertex in cage_mesh.vertices:
            local_distance = 0.0
            try:
                loc, normal, face_index, distance = high_bvh.find_nearest(vertex.co)
                if loc is not None:
                    local_distance = max(0.0, (loc - vertex.co).dot(vertex.normal))
            except Exception:
                local_distance = 0.0
            try:
                distance_attr.data[vertex.index].value = local_distance
            except Exception:
                pass

        return write_cage_safety_colors_from_distances(cage_obj, max_distance_m, alpha)
    except Exception:
        return False
    finally:
        try:
            if high_eval is not None and high_mesh is not None:
                high_eval.to_mesh_clear()
        except Exception:
            pass


def get_cage_object_from_any(obj):
    if obj is None:
        return None
    if obj.get("alb_role") == "cage":
        return obj
    base = get_base_name(obj)
    return bpy.data.objects.get(build_role_name(base, "cage"))


def update_cage_preview_from_props(context):
    obj = context.active_object
    if obj is None:
        return

    props = context.scene.alb_props if context and getattr(context, "scene", None) and hasattr(context.scene, "alb_props") else None
    if props is None:
        return

    cage = get_cage_object_from_any(obj)
    if cage is None:
        return

    strength_mm = float(props.cage_extrusion_mm)
    strength_m = strength_mm * 0.001

    mod = cage.modifiers.get("ALB_Cage_Displace")
    if mod is not None:
        try:
            mod.direction = 'NORMAL'
        except Exception:
            pass
        try:
            mod.strength = strength_m
        except Exception:
            pass

    # Update cage material color and alpha live
    try:
        cage_mat = ensure_cage_material()
        if cage.data.materials:
            cage.data.materials[0] = cage_mat
        else:
            cage.data.materials.append(cage_mat)

        nt = cage_mat.node_tree
        bsdf = None
        for node in nt.nodes:
            if getattr(node, "type", "") == 'BSDF_PRINCIPLED':
                bsdf = node
                break
        if bsdf is not None:
            if "Alpha" in bsdf.inputs:
                bsdf.inputs["Alpha"].default_value = props.cage_alpha
        update_cage_safety_colors(context, cage)
    except Exception:
        pass

    try:
        cage.data.update()
    except Exception:
        pass


def set_mesh_polygons_smooth(obj, smooth=True):
    if obj is None or obj.type != 'MESH' or obj.data is None:
        return
    try:
        for poly in obj.data.polygons:
            poly.use_smooth = bool(smooth)
        obj.data.update()
    except Exception:
        pass

def capture_mesh_smooth_state(obj):
    if obj is None or obj.type != 'MESH' or obj.data is None:
        return None
    try:
        return (obj.name, [bool(poly.use_smooth) for poly in obj.data.polygons])
    except Exception:
        return None


def restore_mesh_smooth_state(state):
    if not state:
        return
    try:
        obj_name, smooth_values = state
        obj = bpy.data.objects.get(obj_name)
        if obj is None or obj.type != 'MESH' or obj.data is None:
            return
        for poly, smooth in zip(obj.data.polygons, smooth_values):
            poly.use_smooth = bool(smooth)
        obj.data.update()
    except Exception:
        pass


def restore_mesh_smooth_states(states):
    for state in states or []:
        restore_mesh_smooth_state(state)


def apply_temporary_bake_smooth(objects):
    states = []
    for obj in objects or []:
        state = capture_mesh_smooth_state(obj)
        if state is not None:
            states.append(state)
            set_mesh_polygons_smooth(obj, True)
    return states

def ensure_edge_split_modifier(obj, split_angle_degrees=79.0):
    if obj is None or obj.type != 'MESH':
        return

    split_angle = math.radians(float(split_angle_degrees))
    for mod in obj.modifiers:
        if mod.type == 'EDGE_SPLIT':
            try:
                mod.split_angle = split_angle
            except Exception:
                pass
            try:
                mod.use_edge_angle = True
            except Exception:
                pass
            return

    try:
        mod = obj.modifiers.new(name="ALB_EdgeSplit", type='EDGE_SPLIT')
        mod.split_angle = split_angle
        mod.use_edge_angle = True
    except Exception:
        pass

def ensure_weighted_normal_modifier(obj):
    if obj is None or obj.type != 'MESH':
        return

    try:
        obj.data.use_auto_smooth = True
    except Exception:
        pass

    for mod in obj.modifiers:
        if mod.type == 'WEIGHTED_NORMAL':
            try:
                mod.keep_sharp = True
            except Exception:
                pass
            try:
                mod.weight = 50
            except Exception:
                pass
            try:
                mod.mode = 'FACE_AREA'
            except Exception:
                pass
            return

    try:
        mod = obj.modifiers.new(name="ALB_WeightedNormal", type='WEIGHTED_NORMAL')
        mod.keep_sharp = True
        mod.weight = 50
        mod.mode = 'FACE_AREA'
    except Exception:
        pass


def ensure_final_shading_modifiers(obj):
    set_mesh_polygons_smooth(obj, True)
    ensure_edge_split_modifier(obj, 79.0)
    ensure_weighted_normal_modifier(obj)

def create_or_update_cage_preview(context, uv_obj):
    if uv_obj is None or uv_obj.type != 'MESH':
        return None

    base = get_base_name(uv_obj)
    cage_name = build_role_name(base, "cage")
    delete_object_if_exists(cage_name)

    cage_obj = duplicate_object(uv_obj, "")
    cage_obj.name = cage_name
    try:
        cage_obj.data.name = f"{cage_name}_Mesh"
    except Exception:
        pass

    cage_obj["alb_role"] = "cage"
    cage_obj["alb_source_object"] = uv_obj.get("alb_source_object", "")
    cage_obj["alb_uv_object"] = uv_obj.name
    cage_obj.location = uv_obj.location.copy()
    cage_obj.rotation_euler = uv_obj.rotation_euler.copy()
    cage_obj.scale = uv_obj.scale.copy()

    for mod in list(cage_obj.modifiers):
        try:
            cage_obj.modifiers.remove(mod)
        except Exception:
            pass

    disp = cage_obj.modifiers.new(name="ALB_Cage_Displace", type='DISPLACE')
    try:
        disp.direction = 'NORMAL'
    except Exception:
        pass
    disp.strength = float(context.scene.alb_props.cage_extrusion_mm) * 0.001

    cage_mat = ensure_cage_material()
    cage_obj.data.materials.clear()
    cage_obj.data.materials.append(cage_mat)
    try:
        update_cage_safety_colors(context, cage_obj, uv_obj, get_high_object_from_any(uv_obj))
    except Exception:
        pass

    try:
        cage_obj.display_type = 'SOLID'
        cage_obj.show_in_front = True
        cage_obj.hide_set(not context.scene.alb_props.show_cage)
    except Exception:
        pass

    return cage_obj


def remove_cage_preview_for_base(base_name):
        delete_object_if_exists(build_role_name(base_name, "cage"))


def update_cage_alpha(self, context):
    update_cage_preview_from_props(context)


def update_cage_extrusion(self, context):
    try:
        context.scene.alb_props.auto_cage_status = ""
        context.scene.alb_props.auto_cage_coverage = 0.0
    except Exception:
        pass
    update_cage_preview_from_props(context)


def estimate_auto_cage_extrusion_mm(context, uv_obj, high_obj, sample_limit=6000):
    if uv_obj is None or high_obj is None:
        return None, "UV or high object not found."
    if uv_obj.type != 'MESH' or high_obj.type != 'MESH':
        return None, "Auto cage needs mesh objects."

    depsgraph = context.evaluated_depsgraph_get()
    try:
        depsgraph.update()
    except Exception:
        pass

    high_eval = None
    high_mesh = None
    low_eval = None
    low_mesh = None
    try:
        high_eval = high_obj.evaluated_get(depsgraph)
        high_mesh = high_eval.to_mesh()
    except Exception:
        high_eval = None
        high_mesh = None
    try:
        low_eval = uv_obj.evaluated_get(depsgraph)
        low_mesh = low_eval.to_mesh()
    except Exception:
        low_eval = None
        low_mesh = None

    try:
        if high_mesh is None or len(high_mesh.vertices) == 0:
            return None, "High mesh has no vertices."
        if low_mesh is None or len(low_mesh.vertices) == 0 or len(low_mesh.polygons) == 0:
            return None, "Lowpoly mesh has no faces."

        try:
            from mathutils.bvhtree import BVHTree
            low_vertices = [v.co.copy() for v in low_mesh.vertices]
            low_polygons = [list(poly.vertices) for poly in low_mesh.polygons]
            low_bvh = BVHTree.FromPolygons(low_vertices, low_polygons, all_triangles=False)
        except Exception:
            low_bvh = None

        if low_bvh is None:
            return None, "Could not build lowpoly distance tree."

        uv_world = uv_obj.matrix_world
        high_world = high_eval.matrix_world if high_eval is not None else high_obj.matrix_world
        high_to_uv = uv_world.inverted() @ high_world
        uv_normal_matrix = uv_world.to_3x3()

        try:
            diag = max(uv_obj.dimensions.length, high_obj.dimensions.length, 0.001)
        except Exception:
            diag = 10.0

        step = max(1, int(math.ceil(len(high_mesh.vertices) / float(sample_limit))))
        sample_indices = range(0, len(high_mesh.vertices), step)
        sampled_count = len(range(0, len(high_mesh.vertices), step))
        distances = []

        for vert_index in sample_indices:
            vert = high_mesh.vertices[vert_index]
            try:
                high_co_uv = high_to_uv @ vert.co
                loc, normal, face_index, distance = low_bvh.find_nearest(high_co_uv)
            except Exception:
                continue
            if loc is None or normal is None:
                continue

            try:
                high_world_co = high_world @ vert.co
                low_world_co = uv_world @ loc
                normal_world = (uv_normal_matrix @ normal).normalized()
                projected = (high_world_co - low_world_co).dot(normal_world)
            except Exception:
                continue

            if projected > 0.0:
                distances.append(projected)

        if not distances:
            return None, "Could not measure high mesh outside the lowpoly mesh."

        distances.sort()

        def percentile_value(values, percentile):
            if not values:
                return 0.0
            index = int(round((len(values) - 1) * percentile))
            index = max(0, min(len(values) - 1, index))
            return values[index]

        raw_max_m = distances[-1]
        p95_m = percentile_value(distances, 0.95)
        p99_m = percentile_value(distances, 0.99)

        # Very large isolated distances usually come from borders, holes, or mismatched scan areas.
        # Keep the maximum for normal objects, but ignore it when it is clearly far from the rest.
        precise_m = raw_max_m
        used_outlier_filter = False
        if len(distances) >= 50 and p99_m > 0.0 and raw_max_m > (p99_m * 3.0):
            precise_m = p99_m
            used_outlier_filter = True
        elif len(distances) >= 50 and p95_m > 0.0 and raw_max_m > (p95_m * 6.0):
            precise_m = p95_m
            used_outlier_filter = True

        estimated_m = precise_m * 3.50
        scale_limit_m = max(0.001, diag * 0.04)
        used_scale_limit = False
        if estimated_m > scale_limit_m:
            estimated_m = scale_limit_m
            used_scale_limit = True

        estimated_mm = max(0.01, estimated_m * 1000.0)
        coverage = 100.0 * (len(distances) / max(1, sampled_count))
        filter_note = ", outliers filtered" if used_outlier_filter else ""
        scale_note = ", scale limit" if used_scale_limit else ""
        status = f"Auto cage: {estimated_mm:.3f} mm (+250% margin{filter_note}{scale_note}) from {len(distances)} samples ({coverage:.0f}% hit coverage)."
        return estimated_mm, status
    finally:
        try:
            if high_eval is not None and high_mesh is not None:
                high_eval.to_mesh_clear()
        except Exception:
            pass
        try:
            if low_eval is not None and low_mesh is not None:
                low_eval.to_mesh_clear()
        except Exception:
            pass

def return_to_cage_edit_view(context, obj):
    if obj is None:
        return

    uv_obj = get_uv_object_from_any(obj)
    if uv_obj is None:
        if obj.get("alb_role") == "uv":
            uv_obj = obj
        elif obj.get("alb_role") == "final" and obj.get("alb_uv_object"):
            uv_obj = bpy.data.objects.get(obj["alb_uv_object"])

    if uv_obj is None:
        return

    cage_obj = get_cage_object_from_any(uv_obj)
    if cage_obj is None:
        cage_obj = create_or_update_cage_preview(context, uv_obj)

    base = get_base_name(uv_obj)
    final_obj = bpy.data.objects.get(build_role_name(base, "final"))
    if final_obj is not None:
        try:
            bpy.data.objects.remove(final_obj, do_unlink=True)
        except Exception:
            pass

    try:
        uv_obj.hide_set(False)
    except Exception:
        pass

    if cage_obj is not None:
        try:
            cage_obj.hide_set(False)
        except Exception:
            pass

    ensure_object_mode()
    visible_for_cage = [uv_obj, cage_obj] if cage_obj is not None else [uv_obj]
    set_workflow_visibility(context, visible_for_cage, active_obj=uv_obj, hide_related=True, render_visible_objects=False)

    if cage_obj is not None:
        try:
            cage_obj.select_set(True)
        except Exception:
            pass

    props = context.scene.alb_props
    props.show_step1 = False
    props.show_step2 = True
    props.show_step3 = True
    try:
        switch_viewport_to_material_preview(context)
    except Exception:
        pass
    log_progress(props, 100, "Returned to cage edit view")



def ensure_cage_from_preview(context, obj):
    if obj is None or obj.type != 'MESH':
        return None, None

    preview = get_preview_object_from_any(obj)
    if preview is None and obj.get("alb_role") == "preview":
        preview = obj
    if preview is None:
        return None, None

    cage_obj = get_cage_object_from_any(preview)
    if cage_obj is None:
        cage_obj = duplicate_object(preview, "")
        cage_obj.name = build_role_name(get_base_name(preview), "cage")
        try:
            cage_obj.data.name = f"{cage_obj.name}_Mesh"
        except Exception:
            pass

        cage_obj["alb_role"] = "cage"
        cage_obj["alb_source_object"] = preview.get("alb_source_object", "")
        cage_obj["alb_preview_object"] = preview.name
        cage_obj.location = preview.location.copy()
        cage_obj.rotation_euler = preview.rotation_euler.copy()
        cage_obj.scale = preview.scale.copy()

        for mod in list(cage_obj.modifiers):
            try:
                cage_obj.modifiers.remove(mod)
            except Exception:
                pass

        disp = cage_obj.modifiers.new(name="ALB_Cage_Displace", type='DISPLACE')
        try:
            disp.direction = 'NORMAL'
        except Exception:
            pass
        disp.strength = props.cage_extrusion_mm * 0.001

        cage_mat = ensure_cage_material()
        cage_obj.data.materials.clear()
        cage_obj.data.materials.append(cage_mat)

    try:
        cage_obj.hide_set(False)
        cage_obj.show_in_front = True
    except Exception:
        pass

    return preview, cage_obj

def update_show_cage(self, context):
    props = context.scene.alb_props if context and getattr(context, "scene", None) and hasattr(context.scene, "alb_props") else None
    if props is not None and getattr(props, "is_resetting_defaults", False):
        return
    obj = context.active_object

    if context.scene.alb_props.show_cage:
        # Cage alpha needs Material Preview; keep this limited to cage views.
        switch_viewport_to_material_preview(context)
        preview_obj, cage_obj = ensure_cage_from_preview(context, obj)
        high_obj = get_high_object_from_any(preview_obj) if preview_obj is not None else None

        target_obj = high_obj if high_obj is not None else preview_obj

        if target_obj is not None:
            try:
                target_obj.hide_set(False)
            except Exception:
                pass
            if cage_obj is not None:
                try:
                    cage_obj.hide_set(False)
                except Exception:
                    pass

            visible_for_cage = [target_obj, cage_obj] if cage_obj is not None else [target_obj]
            set_workflow_visibility(context, visible_for_cage, active_obj=target_obj, hide_related=True, render_visible_objects=False)

            # Keep cage visible, but not selected, to avoid visual clutter
            if cage_obj is not None:
                try:
                    cage_obj.hide_set(False)
                    cage_obj.select_set(False)
                except Exception:
                    pass

            props = context.scene.alb_props
            if not getattr(props, "one_click_active", False):
                props.show_step1 = False
                props.show_step2 = True
                props.show_step3 = True
            log_progress(props, 100, "Cage preview ready")
    else:
        cage_obj = get_cage_object_from_any(obj)
        if cage_obj is None:
            preview_obj = get_preview_object_from_any(obj)
            if preview_obj is not None:
                cage_obj = get_cage_object_from_any(preview_obj)
        if cage_obj is not None:
            try:
                cage_obj.hide_set(True)
            except Exception:
                pass

def get_auto_bake_margin(texture_size, base_margin=4):
    try:
        size = max(1, int(texture_size))
    except Exception:
        size = 1024
    try:
        base = max(1, int(base_margin))
    except Exception:
        base = 4
    return max(1, int(round(base * (size / 1024.0))))


def ensure_bake_margin_props(props):
    if not hasattr(props, "use_auto_bake_margin"):
        return False
    if not hasattr(props, "base_bake_margin_px"):
        return False
    if not hasattr(props, "bake_margin_px"):
        return False
    return True



def get_or_create_bake_cage(context, uv_obj):
    props = context.scene.alb_props
    cage_obj = get_cage_object_from_any(uv_obj)
    if cage_obj is None:
        cage_obj = create_or_update_cage_preview(context, uv_obj)

    if cage_obj is None:
        return None

    try:
        mod = cage_obj.modifiers.get("ALB_Cage_Displace")
        if mod is not None:
            try:
                mod.direction = 'NORMAL'
            except Exception:
                pass
            mod.strength = props.cage_extrusion_mm * 0.001
    except Exception:
        pass

    try:
        cage_obj.hide_render = True
    except Exception:
        pass

    return cage_obj


def prepare_bake_selection(context, high_obj, uv_obj):
    if high_obj is None or uv_obj is None:
        return False

    ensure_object_mode()
    exit_local_view_if_needed(context)

    cage_obj = get_cage_object_from_any(uv_obj)
    cage_was_hidden = None
    if cage_obj is not None:
        try:
            cage_was_hidden = cage_obj.hide_get()
        except Exception:
            cage_was_hidden = False
        try:
            cage_obj.hide_set(True)
        except Exception:
            pass

    deselect_all()

    try:
        high_obj.hide_set(False)
    except Exception:
        pass
    try:
        uv_obj.hide_set(False)
    except Exception:
        pass

    high_obj.select_set(True)
    uv_obj.select_set(True)
    context.view_layer.objects.active = uv_obj

    return cage_obj, cage_was_hidden


def restore_cage_visibility(cage_obj, cage_was_hidden):
    if cage_obj is None:
        return
    try:
        if cage_was_hidden is None:
            cage_obj.hide_set(False)
        else:
            cage_obj.hide_set(cage_was_hidden)
    except Exception:
        pass


def get_effective_base_margin(props):
    try:
        return max(1, int(props.base_bake_margin_px))
    except Exception:
        return 4


def sync_texture_and_margin(props):
    size = get_effective_texture_size(props)
    try:
        props.texture_size = size
    except Exception:
        pass
    try:
        if hasattr(props, "use_auto_bake_margin"):
            if props.use_auto_bake_margin:
                props.bake_margin_px = get_effective_bake_margin(props)
        else:
            props.bake_margin_px = get_effective_bake_margin(props)
    except Exception:
        pass




def get_effective_texture_size(props):
    try:
        return int(props.texture_size_preset)
    except Exception:
        try:
            return int(props.texture_size)
        except Exception:
            return 2048


def get_margin_from_texture_preset(props):
    size = get_effective_texture_size(props)
    mapping = {
        512: 2,
        1024: 4,
        2048: 8,
        4096: 16,
        8192: 32,
    }
    return mapping.get(size, max(1, int(round(size / 256.0))))


def update_texture_size_preset(self, context):
    props = context.scene.alb_props
    try:
        props.texture_size = int(props.texture_size_preset)
    except Exception:
        pass

    # Update visible bake margin immediately when preset changes
    try:
        props.bake_margin_px = get_margin_from_texture_preset(props)
    except Exception:
        pass


def update_texture_size(self, context):
    props = context.scene.alb_props
    try:
        props.bake_margin_px = get_margin_from_texture_preset(props)
    except Exception:
        pass


def update_bake_margin_display(self, context):
    props = context.scene.alb_props
    try:
        props.bake_margin_px = get_margin_from_texture_preset(props)
    except Exception:
        pass



PRESET_FIELDS = [
    "weld_distance_cm",
    "target_poly",
    "decimate_ratio",
    "show_wireframe",
    "show_checker",
    "use_texture_view",
    "checker_mix",
    "checker_uv_scale",
    "uv_method",
    "smart_uv_angle",
    "auto_pack_uv",
    "show_cage",
    "uv_padding_px",
    "texture_size_preset",
    "bake_material_count",
    "bake_samples",
    "bake_margin_px",
    "cage_extrusion_mm",
    "cage_alpha",
    "bake_basecolor",
    "bake_normal",
    "bake_roughness",
    "bake_occlusion",
    "ao_auto_distance",
    "ao_distance",
    "ao_samples",
    "ao_source",
    "normal_strength",
    "fit_low_to_high_before_bake",
    "fit_low_to_high_offset_mm",
    "low_vram_bake",
    "low_vram_force_cpu",
    "save_images",
    "image_format",
    "jpeg_quality",
    "tiff_16bit",
    "output_folder",
]

def get_preset_json_path():
    try:
        cfg_dir = bpy.utils.user_resource('CONFIG')
    except Exception:
        cfg_dir = None
    if not cfg_dir:
        cfg_dir = os.path.expanduser("~")
    return os.path.join(cfg_dir, "auto_baker_presets.json")

def load_presets_dict():
    path = get_preset_json_path()
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}

def save_presets_dict(data):
    path = get_preset_json_path()
    folder = os.path.dirname(path)
    try:
        os.makedirs(folder, exist_ok=True)
    except Exception:
        pass
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_preset_enum_items(self, context):
    presets = load_presets_dict()
    items = [("__NONE__", "None", "No preset selected")]
    for name in sorted(presets.keys(), key=lambda s: s.lower()):
        items.append((name, name, f"Load preset: {name}"))
    return items


def update_preset_selector(self, context):
    """Auto-load preset when the dropdown changes."""
    try:
        name = getattr(self, "preset_selector", "__NONE__")
        if not name or name == "__NONE__":
            return

        data = load_presets_dict()
        preset = data.get(name)
        if not isinstance(preset, dict):
            return

        apply_preset_values(self, preset)
    except Exception:
        pass


def collect_current_preset_values(props):
    data = {}
    for field in PRESET_FIELDS:
        if hasattr(props, field):
            try:
                data[field] = getattr(props, field)
            except Exception:
                pass
    return data

def apply_preset_values(props, data):
    props.internal_update_lock = True
    try:
        for field, value in data.items():
            if hasattr(props, field):
                try:
                    if field == "bake_material_count":
                        value = max(1, min(16, int(value)))
                    setattr(props, field, value)
                except Exception:
                    pass
        sanitize_bake_material_count(props)
    finally:
        props.internal_update_lock = False


def update_smart_uv_preset(self, context):
    """Sync preset -> smart_uv_angle."""
    if getattr(self, "internal_update_lock", False):
        return
    preset = getattr(self, "smart_uv_preset", "BALANCED")
    angle_map = {
        'DETAILED': 30.0,
        'BALANCED': 66.0,
        'LARGE': 75.0,
        'CONTINUOUS': 88.0,
    }
    if preset in angle_map:
        self.internal_update_lock = True
        try:
            self.smart_uv_angle = angle_map[preset]
        finally:
            self.internal_update_lock = False

# ------------------------------------------------------------
# PropertyGroup
# ------------------------------------------------------------

def update_wireframe(self, context):
    props = context.scene.alb_props if context and getattr(context, "scene", None) and hasattr(context.scene, "alb_props") else None
    if props is not None and getattr(props, "is_resetting_defaults", False):
        return
    set_wireframe_overlay(context, self.show_wireframe)



def update_face_orientation_overlay(self, context):
    props = context.scene.alb_props if context and getattr(context, "scene", None) and hasattr(context.scene, "alb_props") else None
    if props is not None and getattr(props, "is_resetting_defaults", False):
        return
    set_face_orientation_overlay(context, self.show_face_orientation)
def update_target_poly(self, context):
    if getattr(self, "internal_update_lock", False) or getattr(self, "is_resetting_defaults", False):
        return
    obj = context.active_object
    source = get_high_object_from_any(obj)
    if source is None:
        return
    preview = find_preview_for_source(source, obj)
    input_faces = preview_decimate_input_face_count(preview, source)
    if input_faces <= 0:
        return
    target = max(1, min(self.target_poly, input_faces))
    ratio = decimate_ratio_for_target_faces(preview, target, input_faces)
    self.internal_update_lock = True
    self.target_poly = target
    self.decimate_ratio = ratio
    self.internal_update_lock = False
    update_preview_modifiers_from_props(obj, context.scene.alb_props, source=source)
    actual_faces = evaluated_preview_face_count(preview) if preview is not None else estimated_face_count(input_faces, ratio)
    self.internal_update_lock = True
    self.target_poly = max(1, actual_faces)
    self.internal_update_lock = False
    context.scene.alb_props.preview_info = format_preview_info(input_faces, actual_faces)


def update_decimate_ratio(self, context):
    if getattr(self, "internal_update_lock", False) or getattr(self, "is_resetting_defaults", False):
        return
    obj = context.active_object
    source = get_high_object_from_any(obj)
    if source is None:
        return
    preview = find_preview_for_source(source, obj)
    input_faces = preview_decimate_input_face_count(preview, source)
    if input_faces <= 0:
        return
    ratio = max(0.0001, min(1.0, self.decimate_ratio))
    self.internal_update_lock = True
    self.decimate_ratio = ratio
    self.internal_update_lock = False
    update_preview_modifiers_from_props(obj, context.scene.alb_props, source=source)
    preview_faces = evaluated_preview_face_count(preview) if preview is not None else estimated_face_count(input_faces, ratio)
    self.internal_update_lock = True
    self.target_poly = max(1, preview_faces)
    self.internal_update_lock = False
    context.scene.alb_props.preview_info = format_preview_info(input_faces, preview_faces)


def update_weld_distance(self, context):
    if getattr(self, "internal_update_lock", False):
        return
    obj = context.active_object if context is not None else None
    source = get_high_object_from_any(obj)
    if source is None:
        return
    update_preview_modifiers_from_props(obj, context.scene.alb_props, source=source)


def update_bake_material_count(self, context):
    if getattr(self, "internal_update_lock", False) or getattr(self, "is_resetting_defaults", False):
        return
    try:
        value = max(1, min(16, int(self.bake_material_count)))
        if int(self.bake_material_count) != value:
            self.bake_material_count = value
        if value > 1:
            sync_force_cpu_from_bake_materials(self, value)
        elif hasattr(self, "low_vram_force_cpu"):
            self.low_vram_force_cpu = False
    except Exception:
        pass


# ------------------------------------------------------------
# UV Texture Efficiency Analysis
# ------------------------------------------------------------


def format_pixel_count(value):
    try:
        value = float(value)
    except Exception:
        return "0 px"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f} Mpx"
    if value >= 1_000:
        return f"{value / 1_000:.1f} Kpx"
    return f"{value:.0f} px"


def describe_texture_detail_match(linear_percent):
    try:
        percent = max(0.0, float(linear_percent))
    except Exception:
        percent = 0.0

    if percent < 95.0:
        loss = max(0.0, 100.0 - percent)
        return f"Detail match: {percent:.0f}% - about {loss:.0f}% lower"
    if percent <= 110.0:
        return f"Detail match: {percent:.0f}% - similar quality"
    extra = percent - 100.0
    return f"Detail match: {percent:.0f}% - {extra:.0f}% above source"


def describe_texture_budget_match(budget_percent, linear_percent):
    try:
        budget = max(0.0, float(budget_percent))
    except Exception:
        budget = 0.0
    try:
        linear = max(0.0, float(linear_percent))
    except Exception:
        linear = 0.0
    return f"Texture match: {budget:.0f}% | Detail estimate: {linear:.0f}%"


def describe_texture_detail_advice(linear_percent, requested_materials, recommended_materials, texture_size):
    try:
        percent = max(0.0, float(linear_percent))
    except Exception:
        percent = 0.0

    if percent < 95.0:
        return f"Use {recommended_materials} material(s), or raise texture size."
    if percent <= 110.0:
        return f"Balanced: {requested_materials} material(s) at {texture_size}px."
    return f"You can reduce materials or texture size."

def polygon_uv_area_from_loops(poly, uv_layer):
    coords = []
    for loop_index in poly.loop_indices:
        try:
            uv = uv_layer.data[loop_index].uv
            coords.append((float(uv.x), float(uv.y)))
        except Exception:
            pass
    if len(coords) < 3:
        return 0.0
    total = 0.0
    count = len(coords)
    for i in range(count):
        x1, y1 = coords[i]
        x2, y2 = coords[(i + 1) % count]
        total += (x1 * y2) - (x2 * y1)
    return abs(total) * 0.5


def analyze_uv_texture_efficiency(obj, texture_size, max_sampled_polygons=80000):
    if obj is None or getattr(obj, "type", None) != 'MESH':
        return None, "Select a mesh object with UVs first."
    mesh = obj.data
    if not mesh.uv_layers or mesh.uv_layers.active is None:
        return None, "The selected mesh has no active UV map."

    uv_layer = mesh.uv_layers.active
    material_count = max(1, len(mesh.materials))
    uv_area_by_material = {i: 0.0 for i in range(material_count)}
    total_uv_area = 0.0

    try:
        mesh.calc_loop_triangles()
    except Exception:
        pass

    triangles = mesh.loop_triangles
    tri_count = len(triangles)
    poly_count = len(mesh.polygons)
    max_sampled_polygons = max(1, int(max_sampled_polygons or 1))
    sample_stride = max(1, int(math.ceil(tri_count / max_sampled_polygons))) if tri_count > max_sampled_polygons else 1
    sampled_polygons = 0

    uv_count = len(uv_layer.data)
    if np is not None:
        uv_values = np.empty(uv_count * 2, dtype=np.float32)
        uv_layer.data.foreach_get("uv", uv_values)
    else:
        uv_values = [0.0] * (uv_count * 2)
        uv_layer.data.foreach_get("uv", uv_values)

    for tri_index in range(0, tri_count, sample_stride):
        tri = triangles[tri_index]
        loops = tri.loops
        if len(loops) < 3:
            continue
        li0, li1, li2 = int(loops[0]) * 2, int(loops[1]) * 2, int(loops[2]) * 2
        u0, v0 = float(uv_values[li0]), float(uv_values[li0 + 1])
        u1, v1 = float(uv_values[li1]), float(uv_values[li1 + 1])
        u2, v2 = float(uv_values[li2]), float(uv_values[li2 + 1])
        area = abs(((u1 - u0) * (v2 - v0)) - ((v1 - v0) * (u2 - u0))) * 0.5
        try:
            poly = mesh.polygons[tri.polygon_index]
            mat_index = max(0, min(int(poly.material_index), material_count - 1))
        except Exception:
            mat_index = 0
        uv_area_by_material[mat_index] = uv_area_by_material.get(mat_index, 0.0) + area
        total_uv_area += area
        sampled_polygons += 1

    if sample_stride > 1 and sampled_polygons > 0:
        estimate_scale = float(tri_count) / float(sampled_polygons)
        total_uv_area *= estimate_scale
        for mat_index in range(material_count):
            uv_area_by_material[mat_index] = uv_area_by_material.get(mat_index, 0.0) * estimate_scale

    size = max(1, int(texture_size))
    pixels_per_texture = float(size * size)
    total_texture_pixels = pixels_per_texture * material_count
    effective_pixels = 0.0
    active_materials = 0

    per_material = []
    for mat_index in range(material_count):
        uv_area = float(uv_area_by_material.get(mat_index, 0.0))
        if uv_area > 0.000001:
            active_materials += 1
        coverage_for_pixels = max(0.0, min(uv_area, 1.0))
        material_effective_pixels = pixels_per_texture * coverage_for_pixels
        effective_pixels += material_effective_pixels
        mat = mesh.materials[mat_index] if mat_index < len(mesh.materials) else None
        mat_name = mat.name if mat else f"Material {mat_index + 1}"
        per_material.append((mat_index, mat_name, uv_area, material_effective_pixels))

    used_ratio = effective_pixels / total_texture_pixels if total_texture_pixels > 0 else 0.0
    wasted_ratio = max(0.0, 1.0 - used_ratio)
    linear_ratio = (used_ratio ** 0.5) if used_ratio > 0.0 else 0.0

    result = {
        "object_name": obj.name,
        "texture_size": size,
        "material_count": material_count,
        "active_materials": active_materials,
        "total_uv_area": total_uv_area,
        "total_texture_pixels": total_texture_pixels,
        "effective_pixels": effective_pixels,
        "used_ratio": used_ratio,
        "wasted_ratio": wasted_ratio,
        "linear_ratio": linear_ratio,
        "per_material": per_material,
        "sampled": sample_stride > 1,
        "sample_stride": sample_stride,
        "sampled_polygons": sampled_polygons,
        "polygon_count": poly_count,
        "triangle_count": tri_count,
    }
    return result, ""


def strip_blender_copy_suffix(name):
    if not name:
        return ""
    if len(name) > 4 and name[-4] == "." and name[-3:].isdigit():
        return name[:-4]
    return name


def normalized_object_name(obj):
    return strip_blender_copy_suffix(getattr(obj, "name", "")).lower()


def is_uv_analysis_high_candidate(obj):
    if obj is None or getattr(obj, "type", None) != 'MESH':
        return False
    role = obj.get("alb_role")
    name = normalized_object_name(obj)
    if role == "high":
        return True
    return is_high_mesh_name(name)


def is_uv_analysis_uv_candidate(obj):
    if obj is None or getattr(obj, "type", None) != 'MESH':
        return False
    role = obj.get("alb_role")
    name = normalized_object_name(obj)
    if role == "uv":
        return True
    return name.endswith("_uv") or name.startswith("2_") and "_uv" in name or "mesh_uv" in name


def uv_analysis_pair_score(high_obj, uv_obj, active_obj=None):
    if high_obj is None or uv_obj is None or high_obj is uv_obj:
        return -1

    score = 0
    high_base = get_base_name(high_obj).lower()
    uv_base = get_base_name(uv_obj).lower()
    high_name = normalized_object_name(high_obj)
    uv_name = normalized_object_name(uv_obj)
    expected_uv_name = build_role_name(high_base, "uv").lower()

    if high_obj.get("alb_role") == "high":
        score += 40
    if uv_obj.get("alb_role") == "uv":
        score += 40
    if uv_obj.get("alb_source_object") == high_obj.name:
        score += 100
    if high_base == uv_base:
        score += 70
    if uv_name == expected_uv_name:
        score += 45
    if high_name.endswith("_high"):
        score += 20
    if uv_name.endswith("_uv") or uv_name.startswith("2_"):
        score += 20

    if active_obj is not None:
        active_base = get_base_name(active_obj).lower()
        if active_base and active_base == high_base:
            score += 10

    try:
        score += min(10, int(len(high_obj.data.polygons) / 100000))
    except Exception:
        pass
    return score


def get_material_image_texture_pixels(mat):
    if mat is None or not getattr(mat, "use_nodes", False) or mat.node_tree is None:
        return 0.0
    best_pixels = 0.0
    for node in mat.node_tree.nodes:
        if getattr(node, "type", "") != 'TEX_IMAGE':
            continue
        img = getattr(node, "image", None)
        if img is None:
            continue
        try:
            width, height = img.size[0], img.size[1]
            pixels = float(max(1, int(width)) * max(1, int(height)))
            best_pixels = max(best_pixels, pixels)
        except Exception:
            pass
    return best_pixels


def estimate_original_texture_detail_pixels(obj, uv_result, fallback_texture_size):
    if obj is None or getattr(obj, "type", None) != 'MESH' or not uv_result:
        return 0.0, False

    fallback_pixels = float(max(1, int(fallback_texture_size)) ** 2)
    total_pixels = 0.0
    found_source_images = False

    for mat_index, _mat_name, uv_area, _effective_pixels in uv_result.get("per_material", []):
        mat = obj.data.materials[mat_index] if mat_index < len(obj.data.materials) else None
        source_pixels = get_material_image_texture_pixels(mat)
        if source_pixels > 0.0:
            found_source_images = True
        else:
            source_pixels = fallback_pixels
        coverage = max(0.0, min(float(uv_area), 1.0))
        total_pixels += source_pixels * coverage

    return max(1.0, total_pixels), found_source_images


def estimate_original_texture_detail_pixels_fast(obj, fallback_texture_size, uv_result=None):
    if obj is None or getattr(obj, "type", None) != 'MESH':
        return float(max(1, int(fallback_texture_size)) ** 2), False

    fallback_pixels = float(max(1, int(fallback_texture_size)) ** 2)
    materials = list(getattr(obj.data, "materials", []) or [])
    if not materials:
        return fallback_pixels, False

    uv_area_by_material = {}
    if uv_result:
        for mat_index, _mat_name, uv_area, _effective_pixels in uv_result.get("per_material", []):
            uv_area_by_material[int(mat_index)] = max(0.0, min(float(uv_area), 1.0))

    total_pixels = 0.0
    found_source_images = False
    for mat_index, mat in enumerate(materials):
        source_pixels = get_material_image_texture_pixels(mat)
        if source_pixels > 0.0:
            found_source_images = True
        else:
            source_pixels = fallback_pixels
        coverage = uv_area_by_material.get(mat_index, 1.0)
        total_pixels += source_pixels * coverage

    return max(1.0, total_pixels), found_source_images


def get_source_material_texture_count(obj):
    if obj is None or getattr(obj, "type", None) != 'MESH':
        return 1
    materials = list(getattr(obj.data, "materials", []) or [])
    if not materials:
        return 1

    textured_count = 0
    for mat in materials:
        if get_material_image_texture_pixels(mat) > 0.0:
            textured_count += 1
    return max(1, textured_count or len(materials))


def get_source_texture_summary(obj, fallback_texture_size):
    fallback_size = max(1, int(fallback_texture_size))
    fallback_pixels = float(fallback_size * fallback_size)
    if obj is None or getattr(obj, "type", None) != 'MESH':
        return 1, fallback_size, fallback_pixels, False

    materials = list(getattr(obj.data, "materials", []) or [])
    if not materials:
        return 1, fallback_size, fallback_pixels, False

    total_pixels = 0.0
    found_source_images = False
    source_count = 0
    largest_size = fallback_size

    for mat in materials:
        source_pixels = get_material_image_texture_pixels(mat)
        if source_pixels > 0.0:
            found_source_images = True
            source_count += 1
            total_pixels += source_pixels
            try:
                largest_size = max(largest_size, int(round(math.sqrt(source_pixels))))
            except Exception:
                pass
        else:
            source_count += 1
            total_pixels += fallback_pixels

    return max(1, source_count), largest_size, max(1.0, total_pixels), found_source_images


def build_texture_detail_status(context, high_obj=None, uv_obj=None):
    try:
        props = context.scene.alb_props
        active_obj = context.active_object
        texture_size = get_effective_texture_size(props)
        requested_materials = max(1, min(16, get_bake_material_count(props)))

        if high_obj is None or uv_obj is None:
            high_obj, uv_obj = find_uv_analysis_pair(active_obj)
        if high_obj is None or uv_obj is None:
            return ""

        source_material_count, source_texture_size, _source_pixels, _uses_images = get_source_texture_summary(
            high_obj,
            texture_size,
        )
        uv_result, uv_error = analyze_uv_texture_efficiency(uv_obj, texture_size, max_sampled_polygons=250000)
        if uv_error or not uv_result:
            return ""

        uv_space_percent = max(0.0, float(uv_result["total_uv_area"]) * 100.0)
        source_linear_budget = float(source_material_count * source_texture_size)
        recommended_raw = int(math.ceil(source_linear_budget / max(1.0, float(texture_size))))
        recommended_materials = max(1, min(16, recommended_raw))
        return (
            "UV analysis complete\n"
            f"Compared {high_obj.name} with\n"
            f"{uv_obj.name} | UV Space: {uv_space_percent:.2f}%\n"
            f"Recommended: {recommended_materials} material(s) at {texture_size}px"
        )
    except Exception:
        return ""


def build_recommended_materials_status(context, high_obj=None, uv_obj=None):
    try:
        props = context.scene.alb_props
        active_obj = context.active_object
        texture_size = get_effective_texture_size(props)

        if high_obj is None or uv_obj is None:
            high_obj, uv_obj = find_uv_analysis_pair(active_obj)
        if high_obj is None or uv_obj is None:
            return ""

        source_material_count, source_texture_size, _source_pixels, _uses_images = get_source_texture_summary(
            high_obj,
            texture_size,
        )
        source_linear_budget = float(source_material_count * source_texture_size)
        recommended_raw = int(math.ceil(source_linear_budget / max(1.0, float(texture_size))))
        recommended_materials = max(1, min(16, recommended_raw))
        return f"Recommended: {recommended_materials} material(s) at {texture_size}px"
    except Exception:
        return ""


def find_uv_analysis_pair(active_obj=None):
    scene = bpy.context.scene if bpy.context else None
    objects = list(scene.objects) if scene else list(bpy.data.objects)
    mesh_objects = [obj for obj in objects if getattr(obj, "type", None) == 'MESH']

    high_candidates = [obj for obj in mesh_objects if is_uv_analysis_high_candidate(obj)]
    uv_candidates = [obj for obj in mesh_objects if is_uv_analysis_uv_candidate(obj)]

    active_high = get_high_object_from_any(active_obj) if active_obj is not None else None
    active_uv = get_uv_object_from_any(active_obj) if active_obj is not None else None
    if active_high is not None and getattr(active_high, "type", None) == 'MESH' and active_high not in high_candidates:
        high_candidates.append(active_high)
    if active_uv is not None and getattr(active_uv, "type", None) == 'MESH' and active_uv not in uv_candidates:
        uv_candidates.append(active_uv)

    best_high = None
    best_uv = None
    best_score = -1
    for high_obj in high_candidates:
        for uv_obj in uv_candidates:
            score = uv_analysis_pair_score(high_obj, uv_obj, active_obj)
            if score > best_score:
                best_score = score
                best_high = high_obj
                best_uv = uv_obj

    if best_score >= 50:
        return best_high, best_uv

    if active_high is not None and active_uv is not None and active_high is not active_uv:
        if getattr(active_high, "type", None) == 'MESH' and getattr(active_uv, "type", None) == 'MESH':
            return active_high, active_uv

    return None, None

class ALB_Properties(PropertyGroup):
    internal_update_lock: BoolProperty(name="Internal Update Lock", default=False, options={'HIDDEN'})
    is_resetting_defaults: BoolProperty(name="Is Resetting Defaults", default=False, options={'HIDDEN'})
    show_step1: BoolProperty(name="Show Step 1", default=False)
    show_step2: BoolProperty(name="Show Step 2", default=False)
    show_step3: BoolProperty(name="Show Step 3", default=False)
    show_step4: BoolProperty(name="Show Step 4", default=False)
    show_advanced_presets: BoolProperty(name="Show Advanced Presets", default=False)
    smart_uv_preset: EnumProperty(
        name="Smart UV Preset",
        description="Quick preset for Smart UV Project. Selecting one of these sets a recommended Smart UV Angle automatically.",
        items=[
            ('DETAILED', "Detailed", "30 deg - more cuts, more precision, less stretching"),
            ('BALANCED', "Balanced", "66 deg - recommended default balance"),
            ('LARGE', "Large Islands", "75 deg - fewer cuts, larger islands"),
            ('CONTINUOUS', "Continuous", "88 deg - fewer UV cuts, keeps connected scan surfaces together"),
        ],
        default='BALANCED',
        update=update_smart_uv_preset
    )
    preset_name_input: StringProperty(
        name="Preset Name",
        description="Name used when saving the current settings as a preset.",
        default=""
    )
    preset_selector: EnumProperty(
        name="Preset",
        description="Select a saved preset. Changing this dropdown auto-loads all saved values.",
        items=get_preset_enum_items,
        update=update_preset_selector
    )

    weld_distance_cm: FloatProperty(
        name="Weld Distance (cm)",
        description="Merge distance in centimeters, matching Blender modifier display. For example 1.0 merges vertices within 1 cm.",
        default=DEFAULTS['weld_distance_cm'],
        min=0.0,
        max=100.0,
        precision=3,
        update=update_weld_distance,
    )
    pre_decimate_merge_cm: FloatProperty(
        name="Pre-Decimate Merge (cm)",
        description="Merge by Distance on the duplicated preview mesh before Decimate. Use it to reduce overlapping scan polygons before optimization.",
        default=DEFAULTS['pre_decimate_merge_cm'],
        min=0.0,
        max=100.0,
        precision=3,
    )
    auto_fix_normals: BoolProperty(
        name="Auto Fix Normals",
        description="Recalculate the high mesh normals outside before creating the lowpoly preview. Useful when inverted normals cause bake artifacts.",
        default=DEFAULTS['auto_fix_normals'],
    )
    auto_combine_mesh_parts: BoolProperty(
        name="Auto Combine Mesh Parts",
        description="Automatically combines mesh parts from the selected hierarchy before optimization. Useful for GLB/FBX scans imported as many child meshes.",
        default=DEFAULTS['auto_combine_mesh_parts'],
    )
    auto_clean_scan_debris: BoolProperty(
        name="Auto Clean Scan Debris",
        description="Automatically removes loose geometry and small detached scan fragments before optimization. Disable this if important small parts are being removed.",
        default=DEFAULTS['auto_clean_scan_debris'],
    )
    show_face_orientation: BoolProperty(
        name="Show Face Orientation",
        description="Show Blender face orientation overlay to detect flipped normals before UVs and baking.",
        default=False,
        update=update_face_orientation_overlay,
    )
    normals_status: StringProperty(
        name="Normals Status",
        default="",
        options={'HIDDEN'},
    )
    uv_analysis_summary: StringProperty(
        name="UV Analysis Summary",
        default="",
        options={'HIDDEN'},
    )
    uv_analysis_detail: StringProperty(
        name="UV Analysis Detail",
        default="",
        options={'HIDDEN'},
    )
    uv_analysis_warning: StringProperty(
        name="UV Analysis Warning",
        default="",
        options={'HIDDEN'},
    )
    uv_analysis_uv_space: StringProperty(
        name="UV Analysis UV Space",
        default="",
        options={'HIDDEN'},
    )
    uv_analysis_recommendation: StringProperty(
        name="UV Analysis Recommendation",
        default="",
        options={'HIDDEN'},
    )

    target_poly: IntProperty(
        name="Final Faces",
        description="Final number of faces for the optimized lowpoly mesh. Lower values make it lighter; higher values keep more detail.",
        default=4000,
        min=1,
        update=update_target_poly,
    )

    decimate_ratio: FloatProperty(
        name="Optimize / Reduce",
        description="Controls mesh reduction. 0.10 keeps 10% of faces, meaning about 90% reduction.",
        default=0.1,
        min=0.0001,
        max=1.0,
        update=update_decimate_ratio,
    )


    show_wireframe: BoolProperty(
        name="Show Wireframe",
        description="Displays the wireframe overlay on the preview object to inspect topology density and decimation quality.",
        default=False,
        update=update_wireframe
    )
    show_checker: BoolProperty(
        name="Show Checker",
        description="Displays a checker texture to inspect UV distortion and stretching. Preview only: it should not affect the baked result.",
        default=False,
        update=update_checker_overlay
    )
    use_texture_view: BoolProperty(
        name="Use Texture View",
        description="Shows the model in flat texture view, without scene lighting. Useful for inspecting the baked diffuse result.",
        default=True,
        update=lambda self, context: update_texture_view(context)
    )
    checker_mix: FloatProperty(
        name="Checker Mix",
        description="Blends the checker texture over the model. 0 = original texture, 1 = full checker overlay.",
        default=1.0,
        min=0.0,
        max=1.0,
        update=update_checker_overlay
    )
    checker_uv_scale: FloatProperty(
        name="Checker UV Scale",
        description="Changes the size of the checker squares. Smaller squares reveal distortion more clearly.",
        default=10.0,
        min=0.001,
        max=1000.0,
        update=update_checker_overlay
    )

    uv_method: EnumProperty(
        name="UV Method",
        items=[
            ('SMART', "Smart UV Project", "Fast automatic unwrap, useful for scans and general-purpose use"),
        ],
        default='SMART',
    )

    smart_uv_angle: FloatProperty(
        name="Smart UV Angle",
        description="Angle threshold used by Smart UV Project. Lower values create more cuts; higher values create larger islands.",
        default=66.0,
        min=1.0,
        max=89.0
    )
    auto_pack_uv: BoolProperty(
        name="Auto Pack UV",
        description="Automatically packs UV islands after unwrap. Turn this off only if you want to arrange islands manually.",
        default=True
    )
    show_cage: BoolProperty(
        name="Show Cage",
        description="Use it before baking to check that the scan details will be captured correctly, without covering the wrong parts.",
        default=False,
        update=update_show_cage
    )
    uv_padding_px: FloatProperty(
        name="UV Padding",
        description="Padding between UV islands. Higher values reduce texture bleeding, especially at lower resolutions.",
        default=0.1,
        min=0.0,
        max=64.0,
    )

    texture_size_preset: EnumProperty(
        name="Texture Preset",
        description="Output texture resolution for baked maps. Higher resolutions preserve more detail but increase bake time and memory usage.",
        items=[
            ('512', "512", ""),
            ('1024', "1024", ""),
            ('2048', "2048", ""),
            ('4096', "4096", ""),
            ('8192', "8192", ""),
        ],
        default='2048',
        update=update_texture_size_preset,
    )

    texture_size: IntProperty(name="Texture Size", default=2048, min=512, max=8192, update=update_texture_size)
    bake_material_count: IntProperty(
        name="Bake Materials",
        description="Splits the bake into multiple material groups. Higher values can improve texture detail on large scans, but increase bake time and the number of output materials.",
        default=1,
        min=1,
        max=16,
        update=update_bake_material_count,
    )
    bake_samples: IntProperty(
        name="Bake Samples",
        description="Number of Cycles samples used for baking. Higher values can reduce noise, but increase bake time.",
        default=8,
        min=1,
        max=4096
    )
    bake_margin_px: IntProperty(
        name="Bake Margin",
        description="Extra pixel padding around baked islands to reduce seams and bleeding in the final texture.",
        default=8,
        min=0,
        max=128
    )
    cage_extrusion_mm: FloatProperty(
        name="Cage Extrusion",
        description="Increase this if the baked texture is missing scan details or shows gaps. Use the smallest value that captures the details cleanly.",
        default=0.0,
        min=0.0,
        max=1000.0,
        update=update_cage_extrusion
    )
    cage_alpha: FloatProperty(
        name="Cage Opacity",
        description="Controls the transparency of the cage preview. 0 = invisible, 1 = fully visible. Preview only, it does not change the bake result.",
        default=1.0,
        min=0.0,
        max=1.0,
        update=update_cage_alpha
    )
    auto_cage_status: StringProperty(name="Auto Cage Status", default="")
    auto_cage_coverage: FloatProperty(name="Auto Cage Coverage", default=0.0, min=0.0, max=100.0)
    auto_cage_target_mm: FloatProperty(name="Auto Cage Target", default=0.0, min=0.0, options={'HIDDEN'})

    bake_basecolor: BoolProperty(
        name="Bake Base Color",
        description="Bakes the diffuse/base color texture from the high object to the final mesh.",
        default=True
    )
    bake_normal: BoolProperty(
        name="Bake Normal",
        description="Bakes a normal map to preserve surface detail from the high object.",
        default=False
    )
    bake_roughness: BoolProperty(
        name="Bake Roughness",
        description="Bakes the high-poly roughness material input to the final low-poly material. Use when the high material has a roughness texture or bakeable roughness signal.",
        default=False
    )
    bake_occlusion: BoolProperty(
        name="Bake Occlusion",
        description="Bakes an ambient occlusion map. This map is always saved as PNG to avoid JPG compression artifacts.",
        default=False
    )
    ao_source: EnumProperty(
        name="AO Source",
        description="Choose whether AO is baked from the original high poly mesh to the low poly mesh, or from the low poly mesh only.",
        items=[
            ('HIGH_TO_LOW', "High -> Low", "Bake AO from the high poly source onto the low poly target"),
            ('LOW_ONLY', "Low Only", "Bake AO using only the low poly target; faster but less detailed"),
        ],
        default='HIGH_TO_LOW'
    )
    ao_auto_distance: BoolProperty(
        name="Auto AO Distance",
        description="Automatically calculates AO distance from the size of the model.",
        default=True
    )
    ao_distance: FloatProperty(
        name="AO Distance",
        description="Maximum distance used by ambient occlusion rays. Used when Auto AO Distance is disabled.",
        default=0.2,
        min=0.001,
        max=100.0
    )
    ao_samples: IntProperty(
        name="AO Samples",
        description="Samples used for the ambient occlusion bake. Higher values are cleaner but slower.",
        default=32,
        min=1,
        max=512
    )
    normal_strength: FloatProperty(
        name="Normal Strength",
        description="Strength used by the Normal Map node on the final material. Changes only the viewport/material appearance, not the baked image.",
        default=1.0,
        min=0.0,
        max=5.0
    )
    fit_low_to_high_before_bake: BoolProperty(
        name="Fit Low to High Before Bake",
        description="Projects the UV low-poly mesh onto the high-poly source before baking. Useful when height mismatch causes black gaps or missed projection details.",
        default=DEFAULTS['fit_low_to_high_before_bake'],
    )
    fit_low_to_high_offset_mm: FloatProperty(
        name="Fit Offset",
        description="Small offset in millimeters after fitting the low mesh to the high mesh. Use positive values if the fitted low mesh sinks into the high surface.",
        default=DEFAULTS['fit_low_to_high_offset_mm'],
        min=-100.0,
        max=100.0,
        precision=3,
    )
    low_vram_bake: BoolProperty(
        name="Safe Memory Bake",
        description="Uses a safer bake workflow designed to reduce memory pressure on heavy scenes and large scans.",
        default=DEFAULTS['low_vram_bake']
    )
    low_vram_force_cpu: BoolProperty(
        name="Force CPU Baking",
        description="Forces baking on CPU to avoid GPU memory issues. Safer on heavy projects, but usually slower.",
        default=DEFAULTS['low_vram_force_cpu']
    )

    save_images: BoolProperty(
        name="Save Images",
        description="Saves baked textures to disk in the selected output folder.",
        default=True
    )
    image_format: EnumProperty(
        name="Image Format",
        description="File format used when saving baked textures to disk.",
        items=[
            ('JPEG', "JPG", "Save images as JPG"),
            ('PNG', "PNG", "Save images as PNG"),
            ('TIFF', "TIFF", "Save images as TIFF"),
        ],
        default='JPEG',
    )
    jpeg_quality: IntProperty(
        name="JPG Quality",
        description="Compression quality used when saving JPG textures. Higher values keep more quality; lower values create smaller files.",
        default=90,
        min=10,
        max=100
    )
    tiff_16bit: BoolProperty(
        name="16-bit TIFF",
        description="Save TIFF textures with higher precision. Useful for detailed normal maps, displacement, or close-up renders. Creates larger files.",
        default=False
    )

    output_folder: StringProperty(
        name="Output Folder",
        description="Folder where baked textures will be saved. Relative paths like //bake/ are saved next to the current Blender file.",
        subtype='DIR_PATH',
        default="//bake/",
    )

    progress_percent: FloatProperty(name="Progress", default=0.0, min=0.0, max=100.0)
    progress_status: StringProperty(name="Status", default="")
    progress_detail: StringProperty(name="Progress Detail", default="")
    workflow_status_anchor: StringProperty(name="Workflow Status Anchor", default="STEP1", options={'HIDDEN'})
    one_click_active: BoolProperty(name="One Click Active", default=False, options={'HIDDEN'})
    one_click_phase: StringProperty(name="One Click Phase", default="", options={'HIDDEN'})
    one_click_start_time: StringProperty(name="One Click Start Time", default="", options={'HIDDEN'})
    preview_info: StringProperty(name="Preview Info", default="No preview created")
    wireframe_was_enabled_before_uv: BoolProperty(name="Wireframe Was Enabled Before UV", default=False)
    checker_was_enabled_before_bake: BoolProperty(name="Checker Was Enabled Before Bake", default=False)
    last_saved_texture_path: StringProperty(name="Last Saved Texture Path", default="")
    ui_faces_cached: IntProperty(name="UI Faces Cached", default=0)
    ui_tris_cached: IntProperty(name="UI Tris Cached", default=0)



def find_first_image_texture_node(nodes):
    for node in nodes:
        if getattr(node, "type", "") == 'TEX_IMAGE' and getattr(node, "image", None) is not None:
            return node
    return None


def get_material_output_node(nodes):
    for node in nodes:
        if getattr(node, "type", "") == 'OUTPUT_MATERIAL':
            return node
    return None


def convert_material_to_preview_emission(mat):
    if mat is None:
        return

    if not mat.use_nodes:
        mat.use_nodes = True

    # Work on a copy to avoid modifying shared/original materials globally
    nt = mat.node_tree
    if nt is None:
        return

    nodes = nt.nodes
    links = nt.links

    output = get_material_output_node(nodes)
    if output is None:
        return

    tex_node = find_first_image_texture_node(nodes)

    emission = nodes.get("ALB_Preview_Emission")
    if emission is None:
        emission = nodes.new(type='ShaderNodeEmission')
        emission.name = "ALB_Preview_Emission"
        emission.label = "ALB_Preview_Emission"
        emission.location = (output.location.x - 220, output.location.y)

    # Remove existing links to output surface
    for link in list(output.inputs['Surface'].links):
        links.remove(link)

    # Remove existing links to emission color
    for link in list(emission.inputs['Color'].links):
        links.remove(link)

    if tex_node is not None:
        try:
            links.new(tex_node.outputs['Color'], emission.inputs['Color'])
        except Exception:
            emission.inputs['Color'].default_value = (0.8, 0.8, 0.8, 1.0)
    else:
        emission.inputs['Color'].default_value = (0.8, 0.8, 0.8, 1.0)

    emission.inputs['Strength'].default_value = 1.0

    try:
        links.new(emission.outputs['Emission'], output.inputs['Surface'])
    except Exception:
        pass


def apply_preview_materials(obj):
    if obj is None or obj.type != 'MESH':
        return

    for i, mat in enumerate(obj.data.materials):
        if mat is None:
            continue
        local_mat = mat.copy()
        local_mat.name = f"{mat.name}_Preview"
        obj.data.materials[i] = local_mat
        convert_material_to_preview_emission(local_mat)


def smart_uv_project_exact(obj):
    if obj is None or obj.type != 'MESH':
        return

    ensure_object_mode()
    deselect_all()
    ensure_object_visible_and_active(obj)

    bpy.ops.object.mode_set(mode='EDIT')
    try:
        bpy.ops.mesh.select_mode(type='FACE')
    except Exception:
        pass
    bpy.ops.mesh.select_all(action='SELECT')

    bpy.ops.uv.smart_project(
        angle_limit=66.0,
        island_margin=0.0,
        area_weight=0.0,
        correct_aspect=True,
        scale_to_bounds=False
    )

    bpy.ops.object.mode_set(mode='OBJECT')



def enforce_roughness_one(obj):
    if obj is None or getattr(obj, "type", None) != 'MESH':
        return

    for mat in obj.data.materials:
        if mat is None:
            continue

        if not mat.use_nodes:
            mat.use_nodes = True

        nt = mat.node_tree
        if nt is None:
            continue

        nodes = nt.nodes
        bsdf = nodes.get("Principled BSDF")
        if bsdf is None:
            continue

        try:
            force_linked_image_non_color(mat, "Roughness")
        except Exception:
            pass

        try:
            roughness_input = bsdf.inputs["Roughness"]
            if not getattr(roughness_input, "is_linked", False):
                roughness_input.default_value = 1.0
        except Exception:
            pass

        try:
            if "Specular IOR Level" in bsdf.inputs:
                bsdf.inputs["Specular IOR Level"].default_value = 0.0
            elif "Specular" in bsdf.inputs:
                bsdf.inputs["Specular"].default_value = 0.0
        except Exception:
            pass


# ------------------------------------------------------------
# Operators
# ------------------------------------------------------------

def ensure_object_visible_and_active(obj):
    if obj is None:
        return
    try:
        obj.hide_set(False)
    except Exception:
        pass
    try:
        obj.hide_viewport = False
    except Exception:
        pass
    try:
        obj.hide_render = False
    except Exception:
        pass
    try:
        make_active(obj)
    except Exception:
        pass


def fit_low_mesh_to_high_before_bake(context, low_obj, high_obj, offset_mm=0.0):
    if low_obj is None or high_obj is None:
        return False
    if getattr(low_obj, "type", None) != 'MESH' or getattr(high_obj, "type", None) != 'MESH':
        return False

    ensure_object_mode()
    exit_local_view_if_needed(context)
    ensure_object_visible_and_active(low_obj)
    ensure_object_visible_for_bake(high_obj)

    mod_name = "ALB_Fit_Low_To_High"
    try:
        old = low_obj.modifiers.get(mod_name)
        if old is not None:
            low_obj.modifiers.remove(old)
    except Exception:
        pass

    try:
        shrink = low_obj.modifiers.new(name=mod_name, type='SHRINKWRAP')
        shrink.target = high_obj
        shrink.wrap_method = 'NEAREST_SURFACEPOINT'
        shrink.offset = float(offset_mm or 0.0) * 0.001
    except Exception:
        return False

    try:
        context.view_layer.objects.active = low_obj
        low_obj.select_set(True)
        bpy.ops.object.modifier_apply(modifier=mod_name)
        try:
            low_obj.data.update()
        except Exception:
            pass
        return True
    except Exception:
        try:
            if low_obj.modifiers.get(mod_name) is not None:
                low_obj.modifiers.remove(low_obj.modifiers.get(mod_name))
        except Exception:
            pass
        return False


def apply_mesh_weld_by_distance(obj, distance_m):
    if obj is None or obj.type != 'MESH' or obj.data is None:
        return 0
    distance_m = max(0.0, float(distance_m or 0.0))
    if distance_m <= 0.0:
        return 0
    ensure_object_mode()
    bm = bmesh.new()
    removed_estimate = 0
    try:
        bm.from_mesh(obj.data)
        before = len(bm.verts)
        bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=distance_m)
        after = len(bm.verts)
        removed_estimate = max(0, before - after)
        bm.to_mesh(obj.data)
        obj.data.update()
        try:
            obj.data.validate(clean_customdata=False)
        except Exception:
            pass
    except Exception:
        removed_estimate = 0
    finally:
        bm.free()
    return removed_estimate

def clean_high_scan_mesh(obj, keep_largest_island=True, remove_small_islands=True, small_island_ratio=0.002, small_island_min_faces=24):
    if obj is None or obj.type != 'MESH':
        return

    ensure_object_mode()
    deselect_all()
    ensure_object_visible_and_active(obj)

    bpy.ops.object.mode_set(mode='EDIT')
    try:
        bpy.ops.mesh.reveal()
    except Exception:
        pass

    # First pass: remove loose verts/edges
    try:
        bpy.ops.mesh.select_all(action='SELECT')
    except Exception:
        pass

    try:
        bpy.ops.mesh.delete_loose(use_verts=True, use_edges=True, use_faces=False)
    except TypeError:
        try:
            bpy.ops.mesh.delete_loose()
        except Exception:
            pass
    except Exception:
        pass

    # Connected island cleanup:
    # - single-piece scans can keep only the largest island;
    # - auto-combined GLB/FBX hierarchies keep valid separate parts, but remove
    #   very small detached fragments that come from scan noise.
    if keep_largest_island or remove_small_islands:
        try:
            import bmesh

            bm = bmesh.from_edit_mesh(obj.data)
            bm.faces.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            bm.verts.ensure_lookup_table()

            visited = set()
            islands = []

            for face in bm.faces:
                if face in visited or not face.is_valid:
                    continue

                stack = [face]
                island_faces = []

                while stack:
                    f = stack.pop()
                    if f in visited or not f.is_valid:
                        continue
                    visited.add(f)
                    island_faces.append(f)

                    for e in f.edges:
                        for linked in e.link_faces:
                            if linked not in visited and linked.is_valid:
                                stack.append(linked)

                if island_faces:
                    islands.append(island_faces)

            if islands:
                faces_to_delete = set()
                if keep_largest_island:
                    largest_island = max(islands, key=len)
                    largest_face_set = set(largest_island)
                    faces_to_delete.update(face for face in bm.faces if face.is_valid and face not in largest_face_set)
                elif remove_small_islands:
                    largest_count = max(len(island) for island in islands)
                    total_faces = max(1, sum(len(island) for island in islands))
                    min_keep_faces = max(int(small_island_min_faces), int(total_faces * float(small_island_ratio)))
                    min_keep_faces = min(min_keep_faces, max(1, int(largest_count * 0.25)))
                    for island in islands:
                        if len(island) < min_keep_faces:
                            faces_to_delete.update(face for face in island if face.is_valid)

                if faces_to_delete:
                    verts_to_delete = set()
                    for face in faces_to_delete:
                        verts_to_delete.update(v for v in face.verts if v.is_valid)
                    if verts_to_delete:
                        bmesh.ops.delete(bm, geom=list(verts_to_delete), context='VERTS')
                        bmesh.update_edit_mesh(obj.data)
        except Exception:
            pass
    # Final pass: clean any loose leftovers generated by island deletion
    try:
        bpy.ops.mesh.select_all(action='SELECT')
    except Exception:
        pass

    try:
        bpy.ops.mesh.delete_loose(use_verts=True, use_edges=True, use_faces=False)
    except TypeError:
        try:
            bpy.ops.mesh.delete_loose()
        except Exception:
            pass
    except Exception:
        pass

    bpy.ops.object.mode_set(mode='OBJECT')


def set_viewport_diffuse_color_mode(context):
    screen = context.screen
    if screen is None:
        return

    for area in screen.areas:
        if area.type != 'VIEW_3D':
            continue
        for space in area.spaces:
            if space.type != 'VIEW_3D':
                continue
            try:
                shading = space.shading
                shading.type = 'MATERIAL'
                try:
                    shading.render_pass = 'COMBINED'
                except Exception:
                    pass
                try:
                    shading.use_scene_lights = False
                except Exception:
                    pass
                try:
                    shading.use_scene_world = False
                except Exception:
                    pass
            except Exception:
                pass

def update_texture_view(context):
    props = context.scene.alb_props
    screen = context.screen
    if screen is None:
        return

    for area in screen.areas:
        if area.type != 'VIEW_3D':
            continue
        for space in area.spaces:
            if space.type != 'VIEW_3D':
                continue
            try:
                shading = space.shading
                if props.use_texture_view:
                    shading.type = 'MATERIAL'
                    try:
                        shading.render_pass = 'COMBINED'
                    except Exception:
                        pass
                    try:
                        shading.use_scene_lights = False
                    except Exception:
                        pass
                    try:
                        shading.use_scene_world = False
                    except Exception:
                        pass
            except Exception:
                pass



class ALB_OT_analyze_uv_usage(Operator):
    bl_idname = "object.alb_analyze_uv_usage"
    bl_label = "Analyze Texture Detail"
    bl_description = "Compare the original high mesh and the ScanReady UV mesh to estimate bake texel detail"

    def execute(self, context):
        props = context.scene.alb_props
        log_progress(props, 1, "Starting UV texture efficiency analysis...")
        props.progress_detail = "Searching the scene for ScanReady high and UV meshes"

        active_obj = context.active_object
        texture_size = get_effective_texture_size(props)
        requested_materials = max(1, min(16, get_bake_material_count(props)))

        log_progress(props, 12, "Finding high and UV mesh pair...")
        high_obj, uv_obj = find_uv_analysis_pair(active_obj)

        if high_obj is not None and uv_obj is not None:
            log_progress(props, 28, f"Reading original high material textures: {high_obj.name}")
            source_material_count, source_texture_size, original_effective_pixels, original_uses_source_images = get_source_texture_summary(
                high_obj,
                texture_size,
            )

            log_progress(props, 55, f"Estimating optimized UV mesh layout: {uv_obj.name}")
            uv_result, uv_error = analyze_uv_texture_efficiency(uv_obj, texture_size, max_sampled_polygons=250000)
            if uv_error:
                error = uv_error
                props.uv_analysis_summary = error
                props.uv_analysis_detail = ""
                props.uv_analysis_recommendation = ""
                props.uv_analysis_uv_space = ""
                props.uv_analysis_warning = ""
                log_progress(props, 100, "UV analysis failed")
                props.progress_detail = error
                self.report({'WARNING'}, error)
                return {'CANCELLED'}

            log_progress(props, 76, "Calculating texel detail and material recommendation...")
            pixels_per_texture = float(texture_size * texture_size)
            uv_efficiency = max(0.01, min(1.0, float(uv_result["total_uv_area"])))
            uv_space_percent = max(0.0, float(uv_result["total_uv_area"]) * 100.0)
            source_linear_budget = float(source_material_count * source_texture_size)
            target_linear_budget_per_material = max(1.0, float(texture_size))
            target_linear_budget = float(requested_materials) * target_linear_budget_per_material
            linear_detail_percent = max(0.0, (target_linear_budget / max(1.0, source_linear_budget)) * 100.0)
            budget_percent = linear_detail_percent
            recommended_raw = int(math.ceil(source_linear_budget / target_linear_budget_per_material))
            recommended_materials = max(1, min(16, recommended_raw))

            props.uv_analysis_summary = (
                f"Source: {source_material_count} x {source_texture_size}px | "
                f"Target: {requested_materials} x {texture_size}px"
            )
            props.uv_analysis_detail = (
                f"{describe_texture_budget_match(budget_percent, linear_detail_percent)}"
            )
            props.uv_analysis_uv_space = f"UV Space: {uv_space_percent:.2f}%"
            can_raise_texture_size = int(texture_size) < 8192
            if linear_detail_percent < 95.0 and recommended_raw > 16:
                tail = "ScanReady max is 16, or raise texture size." if can_raise_texture_size else "ScanReady max is 16; accept lower detail or use fewer source maps."
                props.uv_analysis_recommendation = (
                    f"Needs ~{recommended_raw} material(s); {tail}"
                )
            elif linear_detail_percent < 95.0 and requested_materials < recommended_materials:
                tail = "or raise texture size." if can_raise_texture_size else "at this texture size."
                props.uv_analysis_recommendation = (
                    f"Use up to {recommended_materials} material(s) {tail}"
                )
            elif linear_detail_percent < 95.0:
                tail = "Raise texture size or improve UV packing." if can_raise_texture_size else "Use more materials or improve UV packing."
                props.uv_analysis_recommendation = (
                    tail
                )
            elif linear_detail_percent <= 110.0:
                props.uv_analysis_recommendation = (
                    "Balanced for this estimate."
                )
            else:
                props.uv_analysis_recommendation = (
                    "Reduce materials or texture size."
                )

            log_progress(props, 90, "Building UV analysis report...")
            if uv_result["total_uv_area"] > uv_result["material_count"] + 0.01:
                props.uv_analysis_warning = "UVs may overlap or go outside the 0-1 area. Check the UV layout."
            elif uv_efficiency < 0.45:
                props.uv_analysis_warning = "UVs use little texture space. Improve packing before adding more materials."
            elif linear_detail_percent < 95.0:
                props.uv_analysis_warning = "Bake result may look softer than the original scan."
            elif linear_detail_percent > 110.0:
                props.uv_analysis_warning = "Extra texture cost may not be useful."
            else:
                props.uv_analysis_warning = "Good match for this high-to-UV comparison."

            log_progress(props, 100, "UV analysis complete")
            props.progress_detail = (
                f"Compared {high_obj.name} with\n"
                f"{uv_obj.name} | UV Space: {uv_space_percent:.2f}%\n"
                f"Recommended: {recommended_materials} material(s) at {texture_size}px"
            )
            self.report({'INFO'}, "High and UV texture usage analyzed")
            return {'FINISHED'}

        log_progress(props, 25, "No automatic high + UV pair found")
        props.progress_detail = "Falling back to the active mesh, if one is available"
        obj = active_obj
        result, error = analyze_uv_texture_efficiency(obj, texture_size, max_sampled_polygons=250000)
        if error:
            props.uv_analysis_summary = error
            props.uv_analysis_detail = ""
            props.uv_analysis_recommendation = ""
            props.uv_analysis_uv_space = ""
            props.uv_analysis_warning = ""
            log_progress(props, 100, "UV analysis failed")
            props.progress_detail = error
            self.report({'WARNING'}, error)
            return {'CANCELLED'}

        log_progress(props, 55, f"Reading UVs from active mesh: {obj.name}")
        coverage_percent = result["total_uv_area"] * 100.0
        used_percent = result["used_ratio"] * 100.0
        wasted_percent = result["wasted_ratio"] * 100.0
        linear_percent = result["linear_ratio"] * 100.0

        props.uv_analysis_summary = (
            f"{result['object_name']}: {result['material_count']} material(s), "
            f"UV Space: {coverage_percent:.2f}%"
        )
        props.uv_analysis_detail = describe_texture_detail_match(linear_percent)

        log_progress(props, 76, "Calculating single-mesh UV estimate...")
        target_uv_efficiency = 0.85
        pixels_per_texture = float(result["texture_size"] * result["texture_size"])
        effective_pixels = max(1.0, float(result["effective_pixels"]))
        per_material_capacity = max(1.0, pixels_per_texture * target_uv_efficiency)
        recommended_materials = max(1, min(16, int(math.ceil(effective_pixels / per_material_capacity))))
        requested_capacity = per_material_capacity * requested_materials
        requested_ratio = requested_capacity / effective_pixels
        requested_linear_ratio = math.sqrt(max(0.0, requested_ratio))
        props.uv_analysis_recommendation = describe_texture_detail_advice(
            requested_linear_ratio * 100.0,
            requested_materials,
            recommended_materials,
            result["texture_size"],
        )

        log_progress(props, 90, "Building UV analysis report...")
        if result["total_uv_area"] > result["material_count"] + 0.01:
            props.uv_analysis_warning = "UV area is above the available 0-1 space. Check for overlapping or out-of-tile UVs."
        elif requested_materials < recommended_materials:
            props.uv_analysis_warning = "Current Bake Materials may lose texel detail. Increase materials or texture size for close-up assets."
        elif requested_materials > recommended_materials + 1:
            props.uv_analysis_warning = "Current Bake Materials may be more than needed. Try fewer materials to keep the asset lighter."
        elif wasted_percent > 45.0 and result["material_count"] > 1:
            props.uv_analysis_warning = "Large unused texture space detected. Fewer materials or better UV packing may be enough."
        elif used_percent > 75.0:
            props.uv_analysis_warning = "Good texture usage. Extra materials may not be necessary unless you need more close-up detail."
        else:
            props.uv_analysis_warning = "Only one mesh was found. Create or select the ScanReady UV mesh for a high-to-UV comparison."

        log_progress(props, 100, "UV analysis complete")
        props.progress_detail = f"Analyzed {result['object_name']} | Recommended materials: {recommended_materials}"
        self.report({'INFO'}, "UV texture usage analyzed")
        return {'FINISHED'}

class ALB_OT_create_preview(Operator):
    bl_idname = "object.alb_create_preview"
    bl_label = "Create Lowpoly Preview"
    bl_description = "Duplicate the high poly object and create an interactive lowpoly preview"

    def execute(self, context):
        step_start_time = now_precise_seconds()
        props = context.scene.alb_props
        props.workflow_status_anchor = "STEP1"
        enable_viewport_statistics(context)
        log_progress(props, 1, "Starting lowpoly preview...")
        try:
            props.use_texture_view = True
            switch_viewport_to_material_preview(context)
        except Exception:
            pass

        # Preview starts in Material Preview so texture/material feedback stays consistent.
        # Texture View remains enabled as the workflow display state.
        # Keep default preview toggles unchanged: no automatic wireframe/checker enable.

        source = context.active_object
        source_is_selected = False
        try:
            source_is_selected = bool(source is not None and source.select_get())
        except Exception:
            source_is_selected = False
        source_can_prepare = bool(
            source is not None and source_is_selected and (
                source.type == 'MESH' or (source.type == 'EMPTY' and getattr(props, "auto_combine_mesh_parts", True))
            )
        )
        if not source_can_prepare:
            source = find_existing_high_mesh_in_scene(context)
            source_is_selected = source is not None
            source_can_prepare = bool(source is not None and source.type == 'MESH' and source_is_selected)

        if not source_can_prepare:
            log_progress(props, 0, "Select the high mesh or a scan hierarchy parent.")
            try:
                props.progress_detail = ""
            except Exception:
                pass
            self.report({'WARNING'}, "Select the high poly mesh or its imported hierarchy parent.")
            return {'CANCELLED'}

        log_progress(props, 8, "Preparing source mesh...")

        # If preview/uv/final is selected, always resolve back to the real source object first
        if source.get("alb_source_object"):
            resolved = bpy.data.objects.get(source["alb_source_object"])
            if resolved is not None:
                source = resolved
        elif source.get("alb_role") in {"preview", "uv", "final"}:
            resolved = get_high_object_from_any(source)
            if resolved is not None:
                source = resolved

        source = auto_combine_mesh_parts_if_needed(context, props, source, operator=self)
        if source is None or source.type != 'MESH':
            log_progress(props, 0, "No mesh parts found in selected hierarchy.")
            self.report({'WARNING'}, "No mesh parts found in selected hierarchy.")
            return {'CANCELLED'}

        source_was_auto_combined = bool(source.get("alb_auto_combined_parts", 0))
        if source_was_auto_combined:
            removed_vertices = int(source.get("alb_auto_weld_removed", 0))
            log_progress(props, 9, f"Auto-combined mesh welded. Merged vertices: {removed_vertices:,}")

        ensure_object_visible_and_active(source)

        if object_has_non_unit_scale(source):
            log_progress(props, 12, "Applying scale...")
            apply_scale_only(source)

        ensure_object_visible_and_active(source)
        maybe_auto_fix_source_normals(context, props, source)

        # Take base name BEFORE renaming
        base = get_base_name(source)

        # Rename original object to _high immediately and explicitly
        if not source.name.endswith("_high"):
            source.name = f"{base}_high"
        try:
            source.data.name = f"{source.name}_Mesh"
        except Exception:
            pass
        source["alb_role"] = "high"

        # Enforce clean viewport shading on the renamed high object immediately
        protect_source_material_images(source)
        enforce_roughness_one(source)

        log_progress(props, 18, "Cleaning source scan...")

        # Clean the original high mesh before creating the preview, so both HIGH and LOW stay clean
        if getattr(props, "auto_clean_scan_debris", True):
            clean_high_scan_mesh(source, keep_largest_island=not bool(source.get("alb_auto_combined_parts", 0)), remove_small_islands=True)
        else:
            log_progress(props, 18, "Auto clean disabled. Keeping scan debris and detached parts.")


        preview_name = build_role_name(base, "preview")
        uv_name = build_role_name(base, "uv")
        final_name = build_role_name(base, "final")

        delete_object_if_exists(preview_name)
        delete_object_if_exists(uv_name)
        delete_object_if_exists(final_name)
        cleanup_scanready_bake_resources_for_base(base)

        ensure_object_mode()
        
        # --- CLEAN OLD UV & CAGE ---
        base_name = get_base_name(source)
        delete_object_if_exists(build_role_name(base_name, "uv"))
        delete_object_if_exists(build_role_name(base_name, "cage"))
        cleanup_scanready_bake_resources_for_base(base_name)
        log_progress(props, 35, "Creating preview mesh...")
        preview = duplicate_object(source, "_preview")
        make_object_materials_unique(preview, suffix="_PREVIEW")
        preview.name = build_role_name(base, "preview")
        try:
            preview.data.name = f"{preview.name}_Mesh"
        except Exception:
            pass
        preview["alb_role"] = "preview"
        preview["alb_source_object"] = source.name
        source["alb_role"] = "high"

        # Keep preview on top of high poly
        preview.location = source.location.copy()
        preview.rotation_euler = source.rotation_euler.copy()
        preview.scale = source.scale.copy()

        log_progress(props, 48, "Merging close preview vertices before decimate...")
        try:
            merged_vertices = merge_preview_geometry_before_decimate(
                preview,
                props.pre_decimate_merge_cm / 100.0
            )
            if merged_vertices > 0:
                log_progress(
                    props,
                    52,
                    f"Preview cleanup: merged {merged_vertices:,} close vertices."
                )
        except Exception:
            pass

        log_progress(props, 55, "Applying preview optimization settings...")
        weld = preview.modifiers.new(name="ALB_Weld", type='WELD')
        weld.merge_threshold = props.weld_distance_cm / 100.0

        dec = preview.modifiers.new(name="ALB_Decimate", type='DECIMATE')
        dec.ratio = props.decimate_ratio
        dec.use_collapse_triangulate = False

        set_workflow_visibility(context, [preview], active_obj=preview, hide_related=True, render_visible_objects=False)
        set_wireframe_overlay(context, props.show_wireframe)

        # Do not auto-restore checker after bake during preview creation. Keeping
        # Create Preview in Solid Texture mode avoids forcing Material Preview on heavy scans.
        try:
            props.checker_was_enabled_before_bake = False
        except Exception:
            pass

        if props.show_checker:
            apply_checker_to_object(preview, factor=props.checker_mix, scale=props.checker_uv_scale)
            switch_to_material_preview(context)
        else:
            try:
                props.use_texture_view = True
            except Exception:
                pass
            switch_to_material_preview(context)

        log_progress(props, 80, "Updating viewport visibility...")
        set_workflow_visibility(context, [preview], active_obj=preview, hide_related=True, render_visible_objects=False)

        log_progress(props, 92, "Updating mesh stats...")
        update_cached_ui_mesh_stats(context, preview)
        update_preview_info_from_preview(context, preview, source)
        if not getattr(props, "one_click_active", False):
            props.show_step1 = False
            props.show_step2 = True
            props.show_step3 = False
        if getattr(props, "one_click_active", False):
            log_progress(props, 100, "Preview ready")
        else:
            log_progress(props, 100, "STEP 1 completed")
            try:
                step_time = format_seconds_readable(now_precise_seconds() - step_start_time)
                props.progress_detail = (
                    "Lowpoly preview created.\n"
                    f"Step time: {step_time}\n"
                    "Ready for STEP 2: Generate UVs."
                )
            except Exception:
                pass
        self.report({'INFO'}, "Preview created.")
        return {'FINISHED'}


class ALB_OT_generate_uvs(Operator):
    bl_idname = "object.alb_generate_uvs"
    bl_label = "Generate UVs"
    bl_description = "Create a new UV object from the preview, apply modifiers and unwrap"

    def execute(self, context):
        step_start_time = now_precise_seconds()
        props = context.scene.alb_props
        props.workflow_status_anchor = "STEP2"
        log_progress(props, 1, "Starting UV generation...")

        # Remember current wireframe state, then disable wireframe clutter for UV + cage step
        props.wireframe_was_enabled_before_uv = props.show_wireframe
        props.show_wireframe = False

        # Show Checker must remain a manual user choice.
        # Generate UVs must not enable or disable checker automatically.

        # After Generate UVs, automatically enable Show Cage for bake setup.

        active = context.active_object
        preview = get_preview_object_from_any(active)

        if preview is None or preview.get("alb_role") != "preview":
            self.report({'WARNING'}, "Select a preview created by the add-on.")
            return {'CANCELLED'}

        log_progress(props, 8, "Preparing preview for UVs...")

        high = get_high_object_from_any(preview)
        if high is None:
            self.report({'WARNING'}, "Original high poly object not found.")
            return {'CANCELLED'}

        base = get_base_name(preview)
        uv_name = build_role_name(base, "uv")
        final_name = build_role_name(base, "final")
        cage_name = build_role_name(base, "cage")
        delete_object_if_exists(uv_name)
        delete_object_if_exists(final_name)
        delete_object_if_exists(cage_name)
        cleanup_scanready_bake_resources_for_base(base)

        log_progress(props, 18, "Creating UV mesh...")
        ensure_object_mode()
        uv_obj = duplicate_object(preview, "_uv")
        make_object_materials_unique(uv_obj, suffix="_UV")
        uv_obj.name = build_role_name(base, "uv")
        try:
            uv_obj.data.name = f"{uv_obj.name}_Mesh"
        except Exception:
            pass
        uv_obj["alb_role"] = "uv"
        uv_obj["alb_source_object"] = high.name
        uv_obj["alb_preview_object"] = preview.name
        uv_obj.location = preview.location.copy()
        uv_obj.rotation_euler = preview.rotation_euler.copy()
        uv_obj.scale = preview.scale.copy()
        enforce_roughness_one(uv_obj)

        exit_local_view_if_needed(context)
        deselect_all()
        ensure_object_visible_and_active(uv_obj)

        log_progress(props, 30, "Applying preview modifiers...")
        ensure_object_visible_and_active(uv_obj)
        # Apply modifiers on the UV object only
        for mod_name in [m.name for m in uv_obj.modifiers]:
            try:
                bpy.ops.object.modifier_apply(modifier=mod_name)
            except Exception:
                pass

        ensure_weighted_normal_modifier(uv_obj)

        log_progress(props, 10, "Generating UVs...")
        ensure_object_visible_and_active(uv_obj)
        uv_margin = get_uv_margin(props)

        # Reset and normalize the UV mesh before unwrapping. This avoids Smart UV
        # splitting welded scan triangles because of stale sharp flags, tiny
        # degenerate geometry, or inconsistent normals left by decimation.
        try:
            fixed_vertices = prepare_mesh_for_uv_unwrap(uv_obj, props.weld_distance_cm / 100.0)
            if fixed_vertices > 0:
                log_progress(props, 35, f"UV mesh prepared. Merged vertices: {fixed_vertices:,}")
        except Exception:
            clear_all_seams_and_sharp(uv_obj)

        try:
            log_progress(props, 55, "Smart UV Project...")
            requested = get_bake_material_count(props)
            if requested > 1:
                smart_uv_per_material_and_pack(
                    uv_obj,
                    target_material_count=requested,
                    island_margin=uv_margin,
                    angle_limit=props.smart_uv_angle
                )
            else:
                smart_uv_and_pack(
                    uv_obj,
                    island_margin=uv_margin,
                    angle_limit=props.smart_uv_angle,
                    do_pack=True
                )
        except Exception as e:
            self.report({'ERROR'}, f"Error while generating UVs: {e}")
            return {'CANCELLED'}

        # Every new UV generation must reset cage preview controls        # Every new UV generation must reset cage preview controls
        # to a clean, predictable bake setup.
        props.cage_extrusion_mm = DEFAULTS['cage_extrusion_mm']
        props.cage_alpha = DEFAULTS['cage_alpha']
        props.auto_cage_target_mm = 0.0

        cage_obj = create_or_update_cage_preview(context, uv_obj)
        try:
            cage_obj.hide_set(not props.show_cage)
        except Exception:
            pass
        if props.show_checker:
            apply_checker_to_object(uv_obj, factor=props.checker_mix, scale=props.checker_uv_scale)

        log_progress(props, 92, "Updating UV stats and viewport...")
        try:
            high_obj = get_high_object_from_any(uv_obj)
        except Exception:
            high_obj = None
        try:
            cage_obj = get_cage_object_from_any(uv_obj)
        except Exception:
            cage_obj = None

        if high_obj is not None and cage_obj is not None:
            try:
                log_progress(props, 88, "Calculating cage color target...")
                estimated_mm, status = estimate_auto_cage_extrusion_mm(context, uv_obj, high_obj)
                if estimated_mm is not None:
                    props.auto_cage_target_mm = estimated_mm
                    props.auto_cage_status = f"Cage target: {estimated_mm:.2f} mm"
                    update_cage_safety_colors(context, cage_obj, uv_obj, high_obj)
                else:
                    props.auto_cage_status = status
            except Exception:
                pass

        # Hide UV object from the bake-prep local view.
        try:
            uv_obj.hide_set(True)
        except Exception:
            pass

        # Enable Show Cage here because this is the view/setup the user expects
        # right after Generate UVs.
        try:
            props.show_cage = True
        except Exception:
            pass

        try:
            visible_for_uv = []
            if high_obj is not None:
                visible_for_uv.append(high_obj)
            if cage_obj is not None:
                visible_for_uv.append(cage_obj)
            set_workflow_visibility(
                context,
                visible_for_uv,
                active_obj=high_obj if high_obj is not None else (visible_for_uv[0] if visible_for_uv else None),
                hide_related=True,
                render_visible_objects=False
            )
        except Exception:
            pass

        # Bake preparation view: show HIGH + CAGE explicitly, without Local View.
        # Cage alpha needs Material Preview here so the green cage stays transparent.
        try:
            props.use_texture_view = True
            switch_viewport_to_material_preview(context)
        except Exception:
            pass

        try:
            deselect_all()
        except Exception:
            pass

        try:
            if high_obj is not None:
                high_obj.select_set(True)
                make_active(high_obj)
        except Exception:
            pass

        if props.show_checker and high_obj is not None:
            try:
                apply_checker_to_object(high_obj, factor=props.checker_mix, scale=props.checker_uv_scale)
            except Exception:
                pass

        try:
            if cage_obj is not None:
                cage_obj.select_set(False)
                cage_obj.show_in_front = True
        except Exception:
            pass

        update_cached_ui_mesh_stats(context, uv_obj)
        if not getattr(props, "one_click_active", False):
            props.show_step1 = False
            props.show_step2 = True
            props.show_step3 = True
        if getattr(props, "one_click_active", False):
            log_progress(props, 100, "UVs generated")
        else:
            log_progress(props, 100, "STEP 2 completed")
            try:
                step_time = format_seconds_readable(now_precise_seconds() - step_start_time)
                recommended_status = build_recommended_materials_status(context, high_obj, uv_obj)
                if recommended_status:
                    props.progress_detail = (
                        "UVs generated and cage ready.\n"
                        f"{recommended_status}\n"
                        "Increase Cage Extrusion, or press Auto Cage Extrusion, until the cage preview becomes green.\n"
                        f"Step time: {step_time}\n"
                        "Ready for STEP 3: Bake Textures."
                    )
                else:
                    props.progress_detail = (
                        "UVs generated and cage ready.\n"
                        "Increase Cage Extrusion, or press Auto Cage Extrusion, until the cage preview becomes green.\n"
                        f"Step time: {step_time}\n"
                        "Ready for STEP 3: Bake Textures."
                    )
            except Exception:
                pass
        self.report({'INFO'}, "UVs generated.")
        return {'FINISHED'}


def cleanup_bake_image_resources():
    try:
        bpy.context.view_layer.update()
    except Exception:
        pass


def cleanup_temp_bake_images_delayed():
    try:
        purge_unlinked_temp_bake_images()
        if has_pending_temp_bake_images():
            return 5.0
    except Exception:
        pass
    return None


def schedule_delayed_bake_cleanup(delay_seconds=10.0):
    try:
        bpy.app.timers.register(cleanup_temp_bake_images_delayed, first_interval=max(5.0, float(delay_seconds)))
    except Exception:
        pass


def load_saved_image_if_exists(path_str):
    try:
        if path_str and os.path.exists(path_str):
            abs_path = os.path.abspath(path_str)
            for img in bpy.data.images:
                try:
                    img_path = bpy.path.abspath(getattr(img, "filepath", "") or getattr(img, "filepath_raw", ""))
                    if os.path.abspath(img_path) == abs_path:
                        try:
                            img.reload()
                        except Exception:
                            pass
                        return img
                except Exception:
                    pass

            img = bpy.data.images.load(abs_path, check_existing=False)
            try:
                img.reload()
            except Exception:
                pass
            return img
    except Exception:
        pass
    return None



def object_has_non_unit_scale(obj, eps=1e-6):
    if obj is None:
        return False
    try:
        sx, sy, sz = obj.scale
        return abs(sx - 1.0) > eps or abs(sy - 1.0) > eps or abs(sz - 1.0) > eps
    except Exception:
        return False


def apply_scale_only(obj):
    if obj is None or obj.type != 'MESH':
        return
    if not object_has_non_unit_scale(obj):
        return

    ensure_object_mode()
    deselect_all()
    try:
        obj.hide_set(False)
    except Exception:
        pass
    ensure_object_visible_and_active(obj)
    try:
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    except Exception:
        pass


def isolate_material_faces_for_bake(obj, mat_index, uv_margin=0.01):
    """Isolate only the requested material faces for baking without modifying UV layout.

    Important: this function must NOT repack or rescale UVs, otherwise later bake
    passes will no longer match textures baked in earlier passes.
    """
    if obj is None or obj.type != 'MESH':
        return False

    ensure_object_mode()
    deselect_all()
    try:
        obj.hide_set(False)
    except Exception:
        pass
    try:
        obj.hide_viewport = False
    except Exception:
        pass
    ensure_object_visible_and_active(obj)

    has_faces = False
    for poly in obj.data.polygons:
        sel = (poly.material_index == mat_index)
        poly.select = sel
        has_faces = has_faces or sel
    try:
        obj.data.update()
    except Exception:
        pass

    if not has_faces:
        return False

    try:
        bpy.ops.object.mode_set(mode='EDIT')
    except Exception:
        return False

    try:
        bpy.ops.mesh.reveal()
    except Exception:
        pass
    try:
        bpy.ops.mesh.select_mode(type='FACE')
    except Exception:
        pass

    # Only isolate current material faces. Do not change UV packing here.
    try:
        bpy.ops.mesh.hide(unselected=True)
    except Exception:
        pass

    try:
        bpy.ops.object.mode_set(mode='OBJECT')
    except Exception:
        return False

    return True


def reveal_all_material_faces(obj):
    if obj is None or obj.type != 'MESH':
        return

    ensure_object_mode()
    deselect_all()
    ensure_object_visible_and_active(obj)
    try:
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.reveal()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
    except Exception:
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except Exception:
            pass


def make_material_subset_object(source_obj, mat_index, name_suffix="_bake_tmp"):
    if source_obj is None or source_obj.type != 'MESH':
        return None

    tmp = source_obj.copy()
    tmp.data = source_obj.data.copy()
    tmp.animation_data_clear()
    tmp.name = f"{source_obj.name}{name_suffix}_{mat_index:02d}"
    try:
        tmp.data.name = f"{tmp.name}_Mesh"
    except Exception:
        pass
    bpy.context.collection.objects.link(tmp)

    try:
        import bmesh
        bm = bmesh.new()
        bm.from_mesh(tmp.data)
        bm.faces.ensure_lookup_table()
        faces_to_delete = [f for f in bm.faces if f.material_index != mat_index]
        if faces_to_delete:
            bmesh.ops.delete(bm, geom=faces_to_delete, context='FACES')
        bm.to_mesh(tmp.data)
        bm.free()
        tmp.data.update()
    except Exception:
        pass

    # keep only one material slot if possible
    try:
        keep_mat = source_obj.data.materials[mat_index] if mat_index < len(source_obj.data.materials) else None
        while len(tmp.data.materials) > 0:
            tmp.data.materials.pop(index=len(tmp.data.materials)-1)
        if keep_mat is not None:
            tmp.data.materials.append(keep_mat)
        for poly in tmp.data.polygons:
            poly.material_index = 0
        tmp.data.update()
    except Exception:
        pass

    return tmp


def remove_object_and_data(obj):
    if obj is None:
        return
    try:
        mesh = obj.data
    except Exception:
        mesh = None
    try:
        bpy.data.objects.remove(obj, do_unlink=True)
    except Exception:
        pass
    try:
        if mesh is not None and mesh.users == 0:
            bpy.data.meshes.remove(mesh)
    except Exception:
        pass





def hard_reset_bake_system_state(context, uv_obj, high_obj=None):
    """Reset viewport, selection, mesh visibility and basic bake flags between whole bake phases."""
    try:
        ensure_object_mode()
    except Exception:
        pass
    try:
        exit_local_view_if_needed(context)
    except Exception:
        pass
    try:
        deselect_all()
    except Exception:
        pass

    ensure_object_visible_for_bake(uv_obj)
    if high_obj is not None:
        ensure_object_visible_for_bake(high_obj)

    if uv_obj is not None and getattr(uv_obj, "type", None) == 'MESH':
        try:
            ensure_object_visible_and_active(uv_obj)
        except Exception:
            pass
        try:
            bpy.ops.object.mode_set(mode='EDIT')
            try:
                bpy.ops.mesh.reveal()
            except Exception:
                pass
            try:
                bpy.ops.mesh.select_mode(type='FACE')
            except Exception:
                pass
            try:
                bpy.ops.mesh.select_all(action='DESELECT')
            except Exception:
                pass
            bpy.ops.object.mode_set(mode='OBJECT')
        except Exception:
            try:
                bpy.ops.object.mode_set(mode='OBJECT')
            except Exception:
                pass
        try:
            for poly in uv_obj.data.polygons:
                poly.select = False
            uv_obj.data.update()
        except Exception:
            pass

    try:
        scene = context.scene
        scene.render.bake.use_selected_to_active = True
        scene.render.bake.use_cage = False
        scene.render.bake.use_pass_direct = False
        scene.render.bake.use_pass_indirect = False
        scene.render.bake.use_pass_color = False
    except Exception:
        pass



def capture_object_visibility_state(obj):
    state = {"obj": obj}
    try:
        state["hide_render"] = bool(obj.hide_render)
    except Exception:
        state["hide_render"] = None
    try:
        state["hide_viewport"] = bool(obj.hide_viewport)
    except Exception:
        state["hide_viewport"] = None
    try:
        state["hide_get"] = bool(obj.hide_get())
    except Exception:
        state["hide_get"] = None
    try:
        state["selected"] = bool(obj.select_get())
    except Exception:
        state["selected"] = None
    return state


def restore_object_visibility_state(state):
    obj = state.get("obj")
    if obj is None:
        return
    try:
        if state.get("hide_render") is not None:
            obj.hide_render = state["hide_render"]
    except Exception:
        pass
    try:
        if state.get("hide_viewport") is not None:
            obj.hide_viewport = state["hide_viewport"]
    except Exception:
        pass
    try:
        if state.get("hide_get") is not None:
            if state["hide_get"]:
                obj.hide_set(True)
            else:
                obj.hide_set(False)
    except Exception:
        pass
    try:
        if state.get("selected") is not None:
            obj.select_set(state["selected"])
    except Exception:
        pass


def isolate_scene_for_bake(high_obj, uv_obj):
    """Hide every other mesh object from render/viewport so bake only sees high and uv."""
    kept = {o for o in (high_obj, uv_obj) if o is not None}
    states = []
    try:
        for obj in bpy.data.objects:
            if getattr(obj, "type", None) != 'MESH':
                continue
            states.append(capture_object_visibility_state(obj))
            if obj in kept:
                try:
                    obj.hide_render = False
                except Exception:
                    pass
                try:
                    obj.hide_viewport = False
                except Exception:
                    pass
                try:
                    obj.hide_set(False)
                except Exception:
                    pass
            else:
                try:
                    obj.hide_render = True
                except Exception:
                    pass
                try:
                    obj.hide_viewport = True
                except Exception:
                    pass
                try:
                    obj.hide_set(True)
                except Exception:
                    pass
    except Exception:
        pass
    return states


def restore_scene_after_bake(states):
    try:
        for state in states or []:
            restore_object_visibility_state(state)
    except Exception:
        pass


def ensure_object_visible_for_bake(obj):
    if obj is None:
        return
    try:
        obj.hide_set(False)
    except Exception:
        pass
    try:
        obj.hide_viewport = False
    except Exception:
        pass
    try:
        obj.hide_render = False
    except Exception:
        pass
    try:
        for collection in getattr(obj, "users_collection", []) or []:
            collection.hide_viewport = False
            collection.hide_render = False
    except Exception:
        pass


def reveal_source_mesh_for_bake(obj):
    """Reveal hidden high-poly geometry before selected-to-active baking."""
    if obj is None or getattr(obj, "type", None) != 'MESH':
        return
    try:
        ensure_object_mode()
        deselect_all()
        ensure_object_visible_and_active(obj)
        bpy.ops.object.mode_set(mode='EDIT')
        try:
            bpy.ops.mesh.reveal()
        except Exception:
            pass
        try:
            bpy.ops.mesh.select_all(action='DESELECT')
        except Exception:
            pass
        bpy.ops.object.mode_set(mode='OBJECT')
    except Exception:
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except Exception:
            pass


def configure_bake_cage_or_extrusion(context, scene, props, uv_obj):
    """Use ScanReady cage when available; otherwise fall back to extrusion."""
    bake_cage = get_or_create_bake_cage(context, uv_obj)
    if bake_cage is not None:
        try:
            bake_cage.hide_set(False)
        except Exception:
            pass
        try:
            bake_cage.hide_viewport = False
        except Exception:
            pass
        try:
            bake_cage.hide_render = False
        except Exception:
            pass
        try:
            scene.render.bake.use_cage = True
            scene.render.bake.cage_object = bake_cage
            scene.render.bake.cage_extrusion = 0.0
            return
        except Exception:
            pass

    try:
        scene.render.bake.use_cage = False
    except Exception:
        pass
    try:
        extrusion = float(props.cage_extrusion_mm) * 0.001
    except Exception:
        extrusion = 0.0
    if extrusion <= 0.0:
        try:
            size = max(float(uv_obj.dimensions.x), float(uv_obj.dimensions.y), float(uv_obj.dimensions.z))
            extrusion = max(0.001, size * 0.002)
        except Exception:
            extrusion = 0.001
    try:
        scene.render.bake.cage_extrusion = extrusion
    except Exception:
        pass


def force_selected_to_active_bake_visibility(context, high_obj, uv_obj):
    """Make high and UV render-visible immediately before selected-to-active bake."""
    if high_obj is None or uv_obj is None:
        return

    ensure_object_mode()
    exit_local_view_if_needed(context)
    ensure_object_visible_for_bake(high_obj)
    ensure_object_visible_for_bake(uv_obj)
    reveal_source_mesh_for_bake(high_obj)

    cage_obj = get_cage_object_from_any(uv_obj)
    if cage_obj is not None:
        try:
            cage_obj.hide_render = True
        except Exception:
            pass

    try:
        context.scene.render.bake.use_selected_to_active = True
    except Exception:
        pass

    deselect_all()
    try:
        high_obj.select_set(True)
        uv_obj.select_set(True)
        context.view_layer.objects.active = uv_obj
    except Exception:
        pass

    try:
        context.view_layer.update()
    except Exception:
        pass


def hard_reset_bake_phase_state(context, uv_obj, high_obj=None):
    """Hard reset between diffuse phase and normal phase."""
    if uv_obj is None or uv_obj.type != 'MESH':
        return

    ensure_object_mode()
    exit_local_view_if_needed(context)
    deselect_all()

    ensure_object_visible_for_bake(uv_obj)

    if high_obj is not None:
        ensure_object_visible_for_bake(high_obj)

    try:
        ensure_object_visible_and_active(uv_obj)
    except Exception:
        pass

    try:
        bpy.ops.object.mode_set(mode='EDIT')
        try:
            bpy.ops.mesh.reveal()
        except Exception:
            pass
        try:
            bpy.ops.mesh.select_mode(type='FACE')
        except Exception:
            pass
        try:
            bpy.ops.mesh.select_all(action='DESELECT')
        except Exception:
            pass
        bpy.ops.object.mode_set(mode='OBJECT')
    except Exception:
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except Exception:
            pass

    try:
        for poly in uv_obj.data.polygons:
            poly.select = False
    except Exception:
        pass

    try:
        uv_obj.data.update()
    except Exception:
        pass

def ensure_bake_image_node_for_material(mat, node_name="ALB_Bake_Image"):
    if mat is None:
        return None, None
    if not mat.use_nodes:
        mat.use_nodes = True
    nt = mat.node_tree
    nodes = nt.nodes
    links = nt.links

    out = None
    bsdf = None
    for n in nodes:
        if n.type == 'OUTPUT_MATERIAL' and out is None:
            out = n
        elif n.type == 'BSDF_PRINCIPLED' and bsdf is None:
            bsdf = n
    if out is None:
        out = nodes.new("ShaderNodeOutputMaterial")
        out.location = (400, 0)
    if bsdf is None:
        bsdf = nodes.new("ShaderNodeBsdfPrincipled")
        bsdf.location = (100, 0)
        try:
            links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
        except Exception:
            pass

    img_node = nodes.get(node_name)
    if img_node is None:
        img_node = nodes.new("ShaderNodeTexImage")
        img_node.name = node_name
        img_node.location = (-500, 150)
    return nodes, img_node



def calculate_auto_ao_distance(uv_obj, high_obj=None):
    """Return an AO distance in scene units based on object size."""
    obj = high_obj if high_obj is not None else uv_obj
    try:
        dims = obj.dimensions
        size = max(float(dims.x), float(dims.y), float(dims.z))
    except Exception:
        size = 1.0
    return max(0.001, min(size * 0.10, 100.0))


def apply_ao_bake_settings(scene, props, uv_obj, high_obj=None):
    """Apply AO-specific settings before bpy.ops.object.bake(type='AO')."""
    try:
        scene.cycles.samples = int(props.ao_samples)
    except Exception:
        pass

    try:
        distance = calculate_auto_ao_distance(uv_obj, high_obj) if props.ao_auto_distance else float(props.ao_distance)
    except Exception:
        distance = 0.2

    try:
        scene.world.light_settings.distance = distance
    except Exception:
        pass

    try:
        scene.eevee.gtao_distance = distance
    except Exception:
        pass

    try:
        scene.render.bake.cage_extrusion = float(props.cage_extrusion_mm) * 0.001
    except Exception:
        pass

    return distance


class ALB_OT_bake_textures_modal(Operator):
    bl_idname = "object.alb_bake_textures_modal"
    bl_label = "Bake Textures Modal"
    bl_description = "Low VRAM modal bake with real step-by-step progress"

    _timer = None
    _task_index = 0
    _tasks = None
    _basecolor_imgs = None
    _normal_imgs = None
    _roughness_imgs = None
    _occlusion_imgs = None
    _folder = ""
    _used_temp_folder = False
    _uv_name = ""
    _high_name = ""
    _slot_count = 1
    _finalized = False
    _start_time = 0.0
    _completed_tasks = 0
    _last_bake_type = ""
    _bake_smooth_states = None

    def _finish(self, context, cancelled=False, message=""):
        props = context.scene.alb_props
        try:
            restore_mesh_smooth_states(getattr(self, "_bake_smooth_states", None))
            self._bake_smooth_states = None
        except Exception:
            pass
        if self._timer is not None:
            try:
                context.window_manager.event_timer_remove(self._timer)
            except Exception:
                pass
            self._timer = None

        if cancelled:
            try:
                props.one_click_active = False
                props.one_click_phase = ""
            except Exception:
                pass
            log_progress(props, 0, message or "Bake cancelled")
            if message:
                self.report({'WARNING'}, message)
            return {'CANCELLED'}

        uv_obj = bpy.data.objects.get(self._uv_name)
        high_obj = bpy.data.objects.get(self._high_name)
        if uv_obj is None or high_obj is None:
            log_progress(props, 0, "Bake finished, but final mesh could not be built")
            self.report({'WARNING'}, "Bake finished, but final mesh could not be built.")
            return {'CANCELLED'}

        # Stable finalization path:
        # create final object and link the saved baked textures,
        # but do not force Material Preview or immediate cleanup.
        switch_properties_from_material_to_object(context)

        bake_name = build_role_name(get_base_name(uv_obj), "final")
        delete_object_if_exists(bake_name)

        bake_obj = duplicate_object(uv_obj, "")
        bake_obj.name = build_role_name(get_base_name(uv_obj), "final")
        bake_obj["alb_role"] = "final"
        bake_obj["alb_source_object"] = high_obj.name
        bake_obj["alb_uv_object"] = uv_obj.name
        bake_obj.location = uv_obj.location.copy()
        bake_obj.rotation_euler = uv_obj.rotation_euler.copy()
        bake_obj.scale = uv_obj.scale.copy()

        for mod in list(bake_obj.modifiers):
            try:
                bake_obj.modifiers.remove(mod)
            except Exception:
                pass

        log_progress(props, 95, "Creating final mesh and linking baked textures...")
        build_final_materials_for_slots(
            bake_obj,
            self._basecolor_imgs,
            self._normal_imgs,
            self._slot_count,
            self._occlusion_imgs,
            self._roughness_imgs
        )
        enforce_roughness_one(bake_obj)
        ensure_final_shading_modifiers(bake_obj)

        try:
            safe_post_bake_preview_cleanup()
        except Exception:
            pass

        set_workflow_visibility(context, [bake_obj], active_obj=bake_obj, hide_related=True, render_visible_objects=True)

        # After bake, enable Texture View automatically so the final mesh is shown
        # in Material Preview with textures visible.
        try:
            props.use_texture_view = True
            switch_viewport_to_material_preview(context)
        except Exception:
            pass

        props.show_step1 = True
        props.show_step2 = True
        props.show_step3 = True
        one_click_elapsed = get_precise_elapsed_from_prop(props, "one_click_start_time") if getattr(props, "one_click_active", False) else 0.0
        try:
            props.one_click_active = False
            props.one_click_phase = ""
        except Exception:
            pass
        try:
            if one_click_elapsed > 0.0:
                elapsed_label = format_seconds_readable(one_click_elapsed)
                elapsed_label = f"Total workflow time: {elapsed_label}"
            else:
                elapsed_label = format_seconds_readable(time.time() - float(self._start_time))
                elapsed_label = f"Step time: {elapsed_label}"
        except Exception:
            elapsed_label = "Step time: 0 seconds"
        log_progress(props, 100, "STEP 3 completed")
        try:
            bake_summary = build_bake_completion_summary(
                props,
                self._basecolor_imgs,
                self._normal_imgs,
                self._roughness_imgs,
                self._occlusion_imgs,
                self._slot_count
            )
            recommended_status = build_recommended_materials_status(context, high_obj, uv_obj)
            detail_parts = ["Bake completed.", "Final mesh created and textures linked"]
            if bake_summary:
                detail_parts.append(bake_summary)
            if recommended_status:
                detail_parts.append(recommended_status)
            detail_parts.append(elapsed_label)
            props.progress_detail = "\n".join(detail_parts)
        except Exception:
            pass
        try:
            clear_precise_timer_prop(props, "one_click_start_time")
        except Exception:
            pass
        try:
            bpy.context.workspace.status_text_set(text=None)
        except Exception:
            pass

        if self._folder:
            self.report({'INFO'}, f"Textures saved in {self._folder}")
        self.report({'INFO'}, f"Bake completed on {self._slot_count} material slot(s). Final mesh created and textures linked.")
        schedule_delayed_bake_cleanup(12.0)
        return {'FINISHED'}

    def _run_single_bake(self, context, bake_type, mat_idx):
        props = context.scene.alb_props
        scene = context.scene
        uv_obj = bpy.data.objects.get(self._uv_name)
        high_obj = bpy.data.objects.get(self._high_name)
        if uv_obj is None or high_obj is None:
            raise RuntimeError("Bake source objects not found")

        scene_visibility_states = isolate_scene_for_bake(high_obj, uv_obj)

        hard_reset_bake_system_state(context, uv_obj, high_obj)
        ensure_object_visible_for_bake(uv_obj)
        ensure_object_visible_for_bake(high_obj)

        ok = isolate_material_faces_for_bake(uv_obj, mat_idx, uv_margin=get_uv_margin(props))
        if not ok:
            raise RuntimeError(f"Could not isolate material {mat_idx}")

        map_label = {
            'DIFFUSE': 'BaseColor',
            'NORMAL': 'Normal',
            'NORMAL_TEXTURE': 'Normal',
            'ROUGHNESS': 'Roughness',
            'ROUGHNESS_TEXTURE': 'Roughness',
            'AO': 'Occlusion',
        }.get(bake_type, bake_type)

        img_name = f"{get_base_name(uv_obj)}_{map_label}_Mat{mat_idx:02d}"
        img = create_image(img_name, props.texture_size)
        if bake_type in {'NORMAL', 'NORMAL_TEXTURE', 'DISPLACEMENT', 'ROUGHNESS', 'ROUGHNESS_TEXTURE', 'AO'}:
            try:
                img.colorspace_settings.name = 'Non-Color'
            except Exception:
                pass

        mat = uv_obj.data.materials[mat_idx] if mat_idx < len(uv_obj.data.materials) else None
        nodes, img_node = ensure_bake_image_node_for_material(mat, node_name="ALB_Bake_Image")
        if img_node is not None:
            img_node.image = img
            for n in nodes:
                n.select = False
            img_node.select = True
            nodes.active = img_node

        try:
            disable_checker_for_bake_on_high(high_obj)
        except Exception:
            pass

        deselect_all()
        high_obj.hide_set(False)
        uv_obj.hide_set(False)
        high_obj.hide_viewport = False
        uv_obj.hide_viewport = False

        if bake_type == 'AO' and getattr(props, "ao_source", "HIGH_TO_LOW") == 'LOW_ONLY':
            scene.render.bake.use_selected_to_active = False
            uv_obj.select_set(True)
        else:
            scene.render.bake.use_selected_to_active = True
            high_obj.select_set(True)
            uv_obj.select_set(True)

        context.view_layer.objects.active = uv_obj

        if bake_type == 'AO':
            ao_distance_used = apply_ao_bake_settings(scene, props, uv_obj, high_obj)
            try:
                log_progress(props, 0, f"AO distance: {ao_distance_used:.4f} | AO samples: {int(props.ao_samples)}")
            except Exception:
                pass
        elif bake_type != 'AO':
            force_selected_to_active_bake_visibility(context, high_obj, uv_obj)
            configure_bake_cage_or_extrusion(context, scene, props, uv_obj)

        if bake_type == 'DIFFUSE':
            scene.render.bake.use_pass_direct = False
            scene.render.bake.use_pass_indirect = False
            scene.render.bake.use_pass_color = True

        label = {
            'DIFFUSE': 'Base Color',
            'NORMAL': 'Normal',
            'NORMAL_TEXTURE': 'Normal Texture',
            'ROUGHNESS': 'Roughness',
            'ROUGHNESS_TEXTURE': 'Roughness Texture',
            'AO': 'Occlusion',
        }.get(bake_type, bake_type)
        total = max(1, self._slot_count)
        progress_value = 10 + ((self._completed_tasks + 1) / max(1, len(self._tasks))) * 80.0
        eta_suffix = build_time_estimate_suffix(self._start_time, self._completed_tasks, len(self._tasks))
        log_progress(
            props,
            progress_value,
            f"{label}: material {mat_idx + 1}/{total} - {get_bake_task_explanation(bake_type, 'prepare')}{eta_suffix}"
        )

        print(f"[ScanReady] {label}: material {mat_idx + 1}/{total}")
        log_progress(
            props,
            progress_value,
            f"{label}: material {mat_idx + 1}/{total} - {get_bake_task_explanation(bake_type, 'bake')}{eta_suffix}"
        )

        transfer_states = []
        standard_material_states = []
        color_space_states = []
        actual_bake_type = bake_type
        if bake_type == 'DIFFUSE':
            standard_material_states, color_space_states = setup_high_materials_for_standard_texture_bake(
                high_obj,
                "Base Color"
            )
            if standard_material_states:
                actual_bake_type = 'EMIT'
        elif bake_type == 'NORMAL_TEXTURE':
            standard_material_states, color_space_states = setup_high_materials_for_standard_texture_bake(
                high_obj,
                "Normal"
            )
            if standard_material_states:
                actual_bake_type = 'EMIT'
            else:
                transfer_states, color_space_states = setup_high_materials_for_texture_transfer(
                    high_obj,
                    "Normal",
                    (0.5, 0.5, 1.0, 1.0)
                )
                actual_bake_type = 'EMIT' if transfer_states else 'NORMAL'
        elif bake_type == 'ROUGHNESS_TEXTURE':
            standard_material_states, color_space_states = setup_high_materials_for_standard_texture_bake(
                high_obj,
                "Roughness"
            )
            if standard_material_states:
                actual_bake_type = 'EMIT'
            else:
                transfer_states, color_space_states = setup_high_materials_for_texture_transfer(
                    high_obj,
                    "Roughness",
                    (1.0, 1.0, 1.0, 1.0)
                )
                actual_bake_type = 'EMIT'

        try:
            bpy.ops.object.bake(type=actual_bake_type)
        finally:
            if standard_material_states:
                restore_high_materials_after_standard_texture_bake(standard_material_states)
            if transfer_states:
                restore_high_materials_after_texture_transfer(transfer_states)
            if color_space_states:
                restore_image_color_spaces(color_space_states)

        try:
            img.update()
        except Exception:
            pass
        finally:
            try:
                restore_scene_after_bake(scene_visibility_states)
            except Exception:
                pass

        eta_suffix = build_time_estimate_suffix(self._start_time, self._completed_tasks, len(self._tasks))
        log_progress(
            props,
            progress_value,
            f"{label}: material {mat_idx + 1}/{total} - {get_bake_task_explanation(bake_type, 'save')}{eta_suffix}"
        )

        saved_path = None
        if self._folder:
            # Base Color follows the user image format. Technical/data maps are always PNG.
            save_format = props.image_format if bake_type == 'DIFFUSE' else 'PNG'
            saved_path = save_image_to_folder(img, self._folder, img_name, save_format)

        # Streaming bake policy:
        # save the current texture, store only its file path for final linking,
        # then defer removal of the temporary image datablock. Blender 4.5 can
        # still have shader/material preview jobs reading it right after bake.
        try:
            if img_node is not None and getattr(img_node, "image", None) == img:
                img_node.image = None
        except Exception:
            pass
        defer_temp_bake_image_cleanup(img, delay_seconds=12.0)

        eta_suffix = build_time_estimate_suffix(self._start_time, self._completed_tasks, len(self._tasks))
        log_progress(
            props,
            progress_value,
            f"{label}: material {mat_idx + 1}/{total} - cleaning up...{eta_suffix}"
        )

        reveal_all_material_faces(uv_obj)

        if bake_type == 'DIFFUSE':
            self._basecolor_imgs[mat_idx] = saved_path
        elif bake_type in {'NORMAL', 'NORMAL_TEXTURE'}:
            self._normal_imgs[mat_idx] = saved_path
        elif bake_type in {'ROUGHNESS', 'ROUGHNESS_TEXTURE'}:
            self._roughness_imgs[mat_idx] = saved_path
        elif bake_type == 'AO':
            self._occlusion_imgs[mat_idx] = saved_path

        self._completed_tasks += 1
        eta_suffix = build_time_estimate_suffix(self._start_time, self._completed_tasks, len(self._tasks))
        if mat_idx + 1 < total:
            next_msg = f"{get_bake_task_explanation(bake_type, 'complete')} Preparing next material {mat_idx + 2}/{total}.{eta_suffix}"
        else:
            next_msg = f"{label}: material {mat_idx + 1}/{total} - {get_bake_task_explanation(bake_type, 'complete')}{eta_suffix}"

        log_progress(
            props,
            progress_value,
            next_msg
        )

        print(f"[ScanReady] {label} saved: material {mat_idx + 1}/{total}")

    def _run_full_map_bake(self, context, bake_type):
        props = context.scene.alb_props
        scene = context.scene
        uv_obj = bpy.data.objects.get(self._uv_name)
        high_obj = bpy.data.objects.get(self._high_name)
        if uv_obj is None or high_obj is None:
            raise RuntimeError("Bake source objects not found")

        slot_count = max(1, self._slot_count)
        material_nodes = []
        for idx in range(slot_count):
            mat = uv_obj.data.materials[idx]
            if mat is None:
                mat = bpy.data.materials.new(name=f"{get_base_name(uv_obj)}_Bake_Mat_{idx:02d}")
                mat.use_nodes = True
                uv_obj.data.materials[idx] = mat
            if not mat.use_nodes:
                mat.use_nodes = True
            nt = mat.node_tree
            nodes = nt.nodes
            diffuse_node = nodes.get(f"ALB_Bake_Diffuse_{idx:02d}")
            if diffuse_node is None:
                diffuse_node = nodes.new("ShaderNodeTexImage")
                diffuse_node.name = f"ALB_Bake_Diffuse_{idx:02d}"
                diffuse_node.location = (-500, 150)

            normal_node = nodes.get(f"ALB_Bake_Normal_{idx:02d}")
            if normal_node is None:
                normal_node = nodes.new("ShaderNodeTexImage")
                normal_node.name = f"ALB_Bake_Normal_{idx:02d}"
                normal_node.location = (-500, -150)
            material_nodes.append((idx, nodes, diffuse_node, normal_node))

        if bake_type == 'DIFFUSE':
            label = "Base Color"
            log_progress(props, 25, f"{label}: step 1/2")
            scene.render.bake.use_pass_direct = False
            scene.render.bake.use_pass_indirect = False
            scene.render.bake.use_pass_color = True
            imgs = []
            for idx, nodes, diffuse_node, normal_node in material_nodes:
                img = create_image(f"{get_base_name(uv_obj)}_BaseColor_Mat{idx:02d}", props.texture_size)
                diffuse_node.image = img
                imgs.append((idx, img, diffuse_node))
                for n in nodes:
                    n.select = False
                diffuse_node.select = True
                nodes.active = diffuse_node
        else:
            label = "Normal"
            log_progress(props, 70, f"{label}: step 2/2")
            imgs = []
            for idx, nodes, diffuse_node, normal_node in material_nodes:
                img = create_image(f"{get_base_name(uv_obj)}_Normal_Mat{idx:02d}", props.texture_size)
                normal_node.image = img
                imgs.append((idx, img, normal_node))
                for n in nodes:
                    n.select = False
                normal_node.select = True
                nodes.active = normal_node

        deselect_all()
        high_obj.hide_set(False)
        uv_obj.hide_set(False)
        high_obj.hide_viewport = False
        uv_obj.hide_viewport = False
        high_obj.select_set(True)
        uv_obj.select_set(True)
        context.view_layer.objects.active = uv_obj

        bake_cage = get_or_create_bake_cage(context, uv_obj)
        if bake_cage is not None:
            scene.render.bake.use_cage = True
            scene.render.bake.cage_object = bake_cage
            scene.render.bake.cage_extrusion = 0.0
        else:
            scene.render.bake.use_cage = False
            scene.render.bake.cage_extrusion = (props.cage_extrusion_mm * 0.001)

        print(f"[ScanReady] {label}: baking...")
        bpy.ops.object.bake(type=bake_type)

        for idx, img, node in imgs:
            try:
                img.update()
            except Exception:
                pass
            saved_path = None
            if self._folder:
                saved_path = save_image_to_folder(img, self._folder, f"{get_base_name(uv_obj)}_{'BaseColor' if bake_type == 'DIFFUSE' else 'Normal'}_Mat{idx:02d}", props.image_format)
            else:
                try:
                    img.pack()
                except Exception:
                    pass

            if bake_type == 'DIFFUSE':
                self._basecolor_imgs[idx] = saved_path if saved_path else img
            else:
                self._normal_imgs[idx] = saved_path if saved_path else img

        print(f"[ScanReady] {label}: saved")

    def invoke(self, context, event):
        props = context.scene.alb_props
        uv_obj = get_uv_object_from_any(context.active_object)

        if uv_obj is None or uv_obj.get("alb_role") != "uv":
            self.report({'WARNING'}, "Select a UV object created by the add-on.")
            return {'CANCELLED'}

        high_obj = get_high_object_from_any(uv_obj)
        if high_obj is None or high_obj.type != 'MESH':
            self.report({'WARNING'}, "Original high poly object not found.")
            return {'CANCELLED'}

        # Use smoothed source/target normals during bake to avoid transferring
        # faceted high-poly shading into normal and occlusion maps.
        self._bake_smooth_states = apply_temporary_bake_smooth([high_obj, uv_obj])

        base = get_base_name(uv_obj)
        delete_object_if_exists(build_role_name(base, "final"))
        cleanup_scanready_bake_resources_for_base(base)
        protect_source_material_images(high_obj)

        texture_detail_status = build_texture_detail_status(context, high_obj, uv_obj)
        if texture_detail_status:
            log_progress(props, 100, "UV analysis complete")
            props.progress_detail = texture_detail_status

        ensure_object_mode()
        exit_local_view_if_needed(context)

        props.checker_was_enabled_before_bake = props.show_checker
        if props.show_checker:
            preview_obj = get_preview_object_from_any(uv_obj)
            if preview_obj is not None:
                remove_checker_from_object(preview_obj)
            remove_checker_from_object(uv_obj)
            remove_checker_from_object(high_obj)

        # Cage must not stay visible during baking.
        if getattr(props, "show_cage", False):
            props.show_cage = False

        props.use_texture_view = False

        try:
            set_workflow_visibility(context, [high_obj, uv_obj], active_obj=uv_obj, hide_related=True, render_visible_objects=True)
        except Exception:
            pass

        try:
            safe_post_bake_preview_cleanup()
        except Exception:
            pass

        uv_obj.location = high_obj.location.copy()
        uv_obj.rotation_euler = high_obj.rotation_euler.copy()
        uv_obj.scale = high_obj.scale.copy()

        self._used_temp_folder = False
        self._folder = ""
        props.last_saved_texture_path = ""

        if props.save_images:
            self._folder, self._used_temp_folder = get_safe_output_folder(props)
        else:
            self._folder = tempfile.mkdtemp(prefix="scanready_bake_")
            self._used_temp_folder = True
        try:
            ensure_output_folder_exists(self._folder)
        except Exception:
            pass
        props.last_saved_texture_path = self._folder

        scene = context.scene
        if not ensure_cycles_render_engine(context, operator=self, props=props):
            return {'CANCELLED'}
        if props.low_vram_force_cpu:
            try:
                scene.cycles.device = 'CPU'
            except Exception:
                pass
        scene.cycles.samples = props.bake_samples
        scene.render.bake.use_selected_to_active = True
        sync_texture_and_margin(props)
        scene.render.bake.margin = get_margin_from_texture_preset(props)

        data_image_count = enforce_high_source_data_images_non_color(high_obj)
        if data_image_count:
            log_progress(props, 4, f"High source data texture color space set to Non-Color: {data_image_count}")

        if getattr(props, "fit_low_to_high_before_bake", False):
            log_progress(props, 4, "Fitting low mesh to high before bake...")
            fitted = fit_low_mesh_to_high_before_bake(
                context,
                uv_obj,
                high_obj,
                getattr(props, "fit_low_to_high_offset_mm", 0.0)
            )
            if fitted:
                log_progress(props, 5, "Low mesh fitted to high source.")
            else:
                log_progress(props, 5, "Fit Low to High skipped.")

        requested = get_bake_material_count(props)
        self._slot_count = max(1, requested)
        log_progress(props, 4, f"Preparing {self._slot_count} bake material slot(s)...")
        prepare_uv_material_slots_for_bake(uv_obj, self._slot_count, uv_margin=get_uv_margin(props))

        self._uv_name = uv_obj.name
        self._high_name = high_obj.name
        self._basecolor_imgs = [None] * self._slot_count
        linked_normal_imgs = collect_linked_source_images(high_obj, self._slot_count, "Normal") if props.bake_normal else [None] * self._slot_count
        linked_roughness_imgs = collect_linked_source_images(high_obj, self._slot_count, "Roughness") if getattr(props, "bake_roughness", False) else [None] * self._slot_count
        self._normal_imgs = [None] * self._slot_count
        self._roughness_imgs = [None] * self._slot_count
        self._occlusion_imgs = [None] * self._slot_count
        self._tasks = []

        linked_normal_count = sum(1 for img in linked_normal_imgs if img is not None)
        linked_roughness_count = sum(1 for img in linked_roughness_imgs if img is not None)
        if linked_normal_count:
            log_progress(props, 5, f"Found linked high-poly normal texture(s): {linked_normal_count}/{self._slot_count}. ScanReady will bake them to the new UV layout.")
        elif props.bake_normal:
            log_progress(props, 5, "No linked high-poly normal texture found. ScanReady will bake a geometric normal map from the high mesh.")
        if linked_roughness_count:
            log_progress(props, 5, f"Found linked high-poly roughness texture(s): {linked_roughness_count}/{self._slot_count}. ScanReady will bake roughness to the final material.")
        elif getattr(props, "bake_roughness", False):
            log_progress(props, 5, "Bake Roughness is enabled, but no linked high-poly roughness texture was found. Roughness bake will be skipped.")

        # Always bake per material so progress feedback is detailed in every mode.
        if props.bake_basecolor:
            for i in range(self._slot_count):
                self._tasks.append(("DIFFUSE", i))
        if props.bake_normal:
            for i in range(self._slot_count):
                if linked_normal_imgs[i] is not None:
                    self._tasks.append(("NORMAL_TEXTURE", i))
                else:
                    self._tasks.append(("NORMAL", i))
        if getattr(props, "bake_roughness", False):
            if linked_roughness_count:
                for i in range(self._slot_count):
                    if linked_roughness_imgs[i] is not None:
                        self._tasks.append(("ROUGHNESS_TEXTURE", i))
            else:
                self.report({'WARNING'}, "Bake Roughness enabled, but no linked high-poly roughness texture was found.")
        if getattr(props, "bake_occlusion", False):
            for i in range(self._slot_count):
                self._tasks.append(("AO", i))

        self._task_index = 0
        self._finalized = False
        self._start_time = time.time()
        self._completed_tasks = 0
        self._last_bake_type = ""

        try:
            hard_reset_bake_system_state(context, uv_obj, high_obj)
        except Exception:
            pass

        if not self._tasks:
            restore_mesh_smooth_states(getattr(self, "_bake_smooth_states", None))
            self._bake_smooth_states = None
            self.report({'WARNING'}, "No bake maps enabled.")
            return {'CANCELLED'}

        log_progress(props, 5, "Preparing per-material bake... | Elapsed: 0s")
        log_progress(props, 6, "Process Progress active - bake starting...")
        print("[ScanReady] Modal bake started")

        self._timer = context.window_manager.event_timer_add(0.1, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type == 'ESC':
            return self._finish(context, cancelled=True, message="Bake cancelled by user")

        if event.type != 'TIMER':
            return {'PASS_THROUGH'}

        try:
            if self._task_index < len(self._tasks):
                bake_type, mat_idx = self._tasks[self._task_index]

                # Hard phase boundary between DIFFUSE and NORMAL:
                # Diffuse is fully saved first, then the UV/high state is reset
                # before starting normal maps.
                if self._last_bake_type and bake_type != self._last_bake_type:
                    props = context.scene.alb_props
                    uv_obj = bpy.data.objects.get(self._uv_name)
                    high_obj = bpy.data.objects.get(self._high_name)
                    log_progress(
                        props,
                        50 if bake_type == 'NORMAL' else 10,
                        f"Completed {self._last_bake_type} phase. Resetting system state before {bake_type} phase..."
                    )
                    hard_reset_bake_system_state(context, uv_obj, high_obj)

                self._run_single_bake(context, bake_type, mat_idx)
                self._last_bake_type = bake_type

                self._task_index += 1

                if self._task_index == len(self._tasks):
                    props = context.scene.alb_props
                    log_progress(props, 92, f"Bake maps completed. Building final materials...{build_time_estimate_suffix(self._start_time, self._completed_tasks, len(self._tasks))}")
                return {'RUNNING_MODAL'}

            return self._finish(context)

        except Exception as e:
            return self._finish(context, cancelled=True, message=f"Modal bake failed: {e}")



class ALB_OT_bake_textures(Operator):
    bl_idname = "object.alb_bake_textures"
    bl_label = "Bake Textures"
    bl_description = "Bake from the original high poly object to the UV object"

    def execute(self, context):
        props = context.scene.alb_props
        props.workflow_status_anchor = "STEP3"
        log_progress(props, 1, "Starting bake...")

        ok, estimated_ram_gb, available_ram_gb, ram_message = validate_bake_memory_or_warn(self, props)
        if available_ram_gb > 0.0:
            log_progress(props, 1, f"Estimated RAM: ~{estimated_ram_gb:.2f} GB | Available: ~{available_ram_gb:.2f} GB")
        else:
            log_progress(props, 1, f"Estimated RAM: ~{estimated_ram_gb:.2f} GB")

        if not ok:
            return {'CANCELLED'}

        # Cycles is required for Blender baking. Check before starting the nested modal
        # operator so Blender shows a clean warning instead of a Python traceback.
        if not ensure_cycles_render_engine(context, operator=self, props=props):
            return {'CANCELLED'}

        # Always use the modal bake operator so progress feedback works in every bake mode.
        try:
            bpy.ops.object.alb_bake_textures_modal('INVOKE_DEFAULT')
        except RuntimeError as exc:
            message = str(exc).replace("Error: ", "").strip() or "Bake could not start."
            log_progress(props, 0, message)
            self.report({'WARNING'}, message)
            return {'CANCELLED'}
        return {'FINISHED'}

        uv_obj = get_uv_object_from_any(context.active_object)

        if uv_obj is None or uv_obj.get("alb_role") != "uv":
            self.report({'WARNING'}, "Select a UV object created by the add-on.")
            return {'CANCELLED'}

        high_obj = get_high_object_from_any(uv_obj)
        if high_obj is None or high_obj.type != 'MESH':
            self.report({'WARNING'}, "Original high poly object not found.")
            return {'CANCELLED'}

        ensure_object_mode()
        exit_local_view_if_needed(context)

        props.checker_was_enabled_before_bake = props.show_checker
        if props.show_checker:
            preview_obj = get_preview_object_from_any(uv_obj)
            if preview_obj is not None:
                remove_checker_from_object(preview_obj)
            remove_checker_from_object(uv_obj)
            props.show_checker = False

        if getattr(props, "show_cage", False):
            props.show_cage = False

        props.use_texture_view = False

        uv_obj.location = high_obj.location.copy()
        uv_obj.rotation_euler = high_obj.rotation_euler.copy()
        uv_obj.scale = high_obj.scale.copy()

        used_temp_folder = False
        folder = None
        props.last_saved_texture_path = ""

        # Low VRAM mode must save sequential bakes to disk to free memory safely.
        if props.low_vram_bake:
            if props.save_images:
                folder, used_temp_folder = get_safe_output_folder(props)
            else:
                folder = tempfile.mkdtemp(prefix="scanready_bake_")
                used_temp_folder = True
            try:
                ensure_output_folder_exists(folder)
            except Exception:
                pass
            props.last_saved_texture_path = folder
        elif props.save_images:
            folder, used_temp_folder = get_safe_output_folder(props)
            try:
                ensure_output_folder_exists(folder)
            except Exception:
                pass
            props.last_saved_texture_path = folder
        scene = context.scene
        if props.low_vram_bake and used_temp_folder:
            log_progress(props, 2, "Low VRAM mode: using temporary bake folder...")
        if not ensure_cycles_render_engine(context, operator=self, props=props):
            return {'CANCELLED'}
        if props.low_vram_bake and props.low_vram_force_cpu:
            try:
                scene.cycles.device = 'CPU'
            except Exception:
                pass
            log_progress(props, 3, "Low VRAM mode: forcing CPU bake...")
        scene.cycles.samples = props.bake_samples
        scene.render.bake.use_selected_to_active = True
        sync_texture_and_margin(props)
        scene.render.bake.margin = get_margin_from_texture_preset(props)

        bake_cage = get_or_create_bake_cage(context, uv_obj)
        if bake_cage is not None:
            scene.render.bake.use_cage = True
            scene.render.bake.cage_object = bake_cage
            scene.render.bake.cage_extrusion = 0.0
        else:
            scene.render.bake.use_cage = False
            scene.render.bake.cage_extrusion = (props.cage_extrusion_mm * 0.001)

        requested = get_bake_material_count(props)
        slot_count = max(1, requested)

        # Step 3 decides the final material count.
        # 1 = single material bake
        # >1 = group current UV material slots into the requested number of final materials
        prepare_uv_material_slots_for_bake(uv_obj, slot_count, uv_margin=get_uv_margin(props))

        basecolor_imgs = []
        normal_imgs = []
        material_nodes = []

        for idx in range(slot_count):
            mat = uv_obj.data.materials[idx]
            if mat is None:
                mat = bpy.data.materials.new(name=f"{get_base_name(uv_obj)}_Bake_Mat_{idx:02d}")
                mat.use_nodes = True
                uv_obj.data.materials[idx] = mat
            if not mat.use_nodes:
                mat.use_nodes = True
            nt = mat.node_tree
            nodes = nt.nodes
            links = nt.links
            out = None
            bsdf = None
            for n in nodes:
                if n.type == 'OUTPUT_MATERIAL' and out is None:
                    out = n
                elif n.type == 'BSDF_PRINCIPLED' and bsdf is None:
                    bsdf = n
            if out is None:
                out = nodes.new("ShaderNodeOutputMaterial")
                out.location = (400, 0)
            if bsdf is None:
                bsdf = nodes.new("ShaderNodeBsdfPrincipled")
                try:
                    bsdf.inputs["Roughness"].default_value = 1.0
                except Exception:
                    pass
                try:
                    if "Specular IOR Level" in bsdf.inputs:
                        bsdf.inputs["Specular IOR Level"].default_value = 0.0
                    elif "Specular" in bsdf.inputs:
                        bsdf.inputs["Specular"].default_value = 0.0
                except Exception:
                    pass
                bsdf.location = (100, 0)
            if not any(l.from_node == bsdf and l.to_node == out for l in links):
                links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

            diffuse_node = nodes.get(f"ALB_Bake_Diffuse_{idx:02d}")
            if diffuse_node is None:
                diffuse_node = nodes.new("ShaderNodeTexImage")
                diffuse_node.name = f"ALB_Bake_Diffuse_{idx:02d}"
                diffuse_node.location = (-500, 150)

            normal_node = nodes.get(f"ALB_Bake_Normal_{idx:02d}")
            if normal_node is None:
                normal_node = nodes.new("ShaderNodeTexImage")
                normal_node.name = f"ALB_Bake_Normal_{idx:02d}"
                normal_node.location = (-500, -150)

            material_nodes.append((idx, nodes, diffuse_node, normal_node))

        def prepare_selection():
            deselect_all()
            high_obj.hide_set(False)
            uv_obj.hide_set(False)
            high_obj.hide_viewport = False
            uv_obj.hide_viewport = False
            high_obj.select_set(True)
            uv_obj.select_set(True)
            context.view_layer.objects.active = uv_obj

        low_vram_mode = bool(props.low_vram_bake and folder and slot_count > 1)

        if props.bake_basecolor:
            scene.render.bake.use_pass_direct = False
            scene.render.bake.use_pass_indirect = False
            scene.render.bake.use_pass_color = True

            if low_vram_mode:
                # Bake one temporary material-subset object at a time for maximum stability.
                for mat_idx in range(slot_count):
                    log_progress(props, 10 + ((mat_idx + 1) / max(1, slot_count)) * 40.0, f"Base Color bake {mat_idx + 1}/{slot_count}...")
                    tmp_uv = make_material_subset_object(uv_obj, mat_idx, name_suffix="_alb_tmp_uv")
                    if tmp_uv is None:
                        continue

                    img = create_image(f"{get_base_name(uv_obj)}_BaseColor_Mat{mat_idx:02d}", props.texture_size)

                    mat = tmp_uv.data.materials[0] if tmp_uv.data.materials else None
                    nodes, img_node = ensure_bake_image_node_for_material(mat, node_name="ALB_Bake_Image")
                    if img_node is not None:
                        img_node.image = img
                        for n in nodes:
                            n.select = False
                        img_node.select = True
                        nodes.active = img_node

                    deselect_all()
                    high_obj.hide_set(False)
                    tmp_uv.hide_set(False)
                    high_obj.hide_viewport = False
                    tmp_uv.hide_viewport = False
                    high_obj.select_set(True)
                    tmp_uv.select_set(True)
                    context.view_layer.objects.active = tmp_uv

                    # Use extrusion only in low VRAM mode to avoid extra cage object memory.
                    scene.render.bake.use_cage = False
                    scene.render.bake.cage_extrusion = (props.cage_extrusion_mm * 0.001)

                    bpy.ops.object.bake(type='DIFFUSE')

                    try:
                        img.update()
                    except Exception:
                        pass

                    saved_path = None
                    if folder:
                        saved_path = save_image_to_folder(img, folder, f"{get_base_name(uv_obj)}_BaseColor_Mat{mat_idx:02d}", props.image_format)

                    if img_node is not None:
                        img_node.image = None
                    defer_temp_bake_image_cleanup(img, delay_seconds=12.0)
                    remove_object_and_data(tmp_uv)
                    cleanup_bake_image_resources()

                    if saved_path:
                        basecolor_imgs.append(saved_path)
            else:
                for idx, nodes, diffuse_node, normal_node in material_nodes:
                    base_img = create_image(f"{get_base_name(uv_obj)}_BaseColor_Mat{idx:02d}", props.texture_size)
                    diffuse_node.image = base_img
                    basecolor_imgs.append(base_img)

                log_progress(props, 35, "Base Color bake in progress...")
                for idx, nodes, diffuse_node, normal_node in material_nodes:
                    for n in nodes:
                        n.select = False
                    diffuse_node.select = True
                    nodes.active = diffuse_node
                prepare_selection()
                bpy.ops.object.bake(type='DIFFUSE')
                for idx, img in enumerate(basecolor_imgs):
                    try:
                        img.update()
                    except Exception:
                        pass
                    if props.save_images and folder:
                        save_image_to_folder(img, folder, f"{get_base_name(uv_obj)}_BaseColor_Mat{idx:02d}", props.image_format)
                    else:
                        try:
                            img.pack()
                        except Exception:
                            pass

        if props.bake_normal:
            if low_vram_mode:
                for mat_idx in range(slot_count):
                    log_progress(props, 55 + ((mat_idx + 1) / max(1, slot_count)) * 40.0, f"Normal bake {mat_idx + 1}/{slot_count}...")
                    tmp_uv = make_material_subset_object(uv_obj, mat_idx, name_suffix="_alb_tmp_uv")
                    if tmp_uv is None:
                        continue

                    img = create_image(f"{get_base_name(uv_obj)}_Normal_Mat{mat_idx:02d}", props.texture_size)

                    mat = tmp_uv.data.materials[0] if tmp_uv.data.materials else None
                    nodes, img_node = ensure_bake_image_node_for_material(mat, node_name="ALB_Bake_Image")
                    if img_node is not None:
                        img_node.image = img
                        for n in nodes:
                            n.select = False
                        img_node.select = True
                        nodes.active = img_node

                    deselect_all()
                    high_obj.hide_set(False)
                    tmp_uv.hide_set(False)
                    high_obj.hide_viewport = False
                    tmp_uv.hide_viewport = False
                    high_obj.select_set(True)
                    tmp_uv.select_set(True)
                    context.view_layer.objects.active = tmp_uv

                    scene.render.bake.use_cage = False
                    scene.render.bake.cage_extrusion = (props.cage_extrusion_mm * 0.001)

                    bpy.ops.object.bake(type='NORMAL')

                    try:
                        img.update()
                    except Exception:
                        pass

                    saved_path = None
                    if folder:
                        saved_path = save_image_to_folder(img, folder, f"{get_base_name(uv_obj)}_Normal_Mat{mat_idx:02d}", props.image_format)

                    if img_node is not None:
                        img_node.image = None
                    defer_temp_bake_image_cleanup(img, delay_seconds=12.0)
                    remove_object_and_data(tmp_uv)
                    cleanup_bake_image_resources()

                    if saved_path:
                        normal_imgs.append(saved_path)
            else:
                for idx, nodes, diffuse_node, normal_node in material_nodes:
                    norm_img = create_image(f"{get_base_name(uv_obj)}_Normal_Mat{idx:02d}", props.texture_size)
                    normal_node.image = norm_img
                    normal_imgs.append(norm_img)

                log_progress(props, 70, "Normal bake in progress...")
                for idx, nodes, diffuse_node, normal_node in material_nodes:
                    for n in nodes:
                        n.select = False
                    normal_node.select = True
                    nodes.active = normal_node
                prepare_selection()
                bpy.ops.object.bake(type='NORMAL')
                for idx, img in enumerate(normal_imgs):
                    try:
                        img.update()
                    except Exception:
                        pass
                    if props.save_images and folder:
                        save_image_to_folder(img, folder, f"{get_base_name(uv_obj)}_Normal_Mat{idx:02d}", props.image_format)
                    else:
                        try:
                            img.pack()
                        except Exception:
                            pass

        bake_name = build_role_name(get_base_name(uv_obj), "final")
        delete_object_if_exists(bake_name)

        bake_obj = duplicate_object(uv_obj, "")
        bake_obj.name = build_role_name(get_base_name(uv_obj), "final")
        bake_obj["alb_role"] = "final"
        bake_obj["alb_source_object"] = high_obj.name
        bake_obj["alb_uv_object"] = uv_obj.name
        bake_obj.location = uv_obj.location.copy()
        bake_obj.rotation_euler = uv_obj.rotation_euler.copy()
        bake_obj.scale = uv_obj.scale.copy()

        for mod in list(bake_obj.modifiers):
            try:
                bake_obj.modifiers.remove(mod)
            except Exception:
                pass

        build_final_materials_for_slots(bake_obj, basecolor_imgs, normal_imgs, slot_count)
        enforce_roughness_one(bake_obj)
        ensure_final_shading_modifiers(bake_obj)

        set_workflow_visibility(context, [bake_obj], active_obj=bake_obj, hide_related=True, render_visible_objects=True)
        if not low_vram_mode:
            props.use_texture_view = True
            switch_to_material_preview(context)

        props.show_step1 = True
        props.show_step2 = True
        props.show_step3 = True
        log_progress(props, 100, "STEP 3 completed")
        try:
            bpy.context.workspace.status_text_set(text=None)
        except Exception:
            pass
        if props.save_images and folder:
            self.report({'INFO'}, f"Texture salvate in {folder}")
        self.report({'INFO'}, f"Bake completed on {slot_count} material slot(s).")
        return {'FINISHED'}


class ALB_OT_one_click_bake(Operator):
    bl_idname = "object.alb_one_click_bake"
    bl_label = "ONE CLICK BAKE"
    bl_description = "Automatically clean, reduce, unwrap, create the cage, and bake the scan into a game-ready asset"

    def execute(self, context):
        props = context.scene.alb_props
        source = context.active_object
        if source is None or (source.type != 'MESH' and not (source.type == 'EMPTY' and getattr(props, "auto_combine_mesh_parts", True))):
            self.report({'WARNING'}, "Select the scan/high poly mesh first, or select its imported hierarchy parent.")
            return {'CANCELLED'}

        enable_viewport_statistics(context)
        props.one_click_active = True
        props.one_click_phase = "PREVIEW"
        props.workflow_status_anchor = "STEP1"
        set_precise_timer_prop(props, "one_click_start_time")
        props.show_step1 = False
        props.show_step2 = False
        props.show_step3 = False
        props.show_step4 = False
        try:
            props.use_texture_view = True
            switch_viewport_to_material_preview(context)
        except Exception:
            pass
        log_progress(props, 1, "ScanReady: converting scan to game-ready asset...")

        result = bpy.ops.object.alb_create_preview()
        if 'CANCELLED' in result:
            props.one_click_active = False
            props.one_click_phase = ""
            clear_precise_timer_prop(props, "one_click_start_time")
            self.report({'WARNING'}, "ScanReady stopped while creating the lowpoly preview.")
            return {'CANCELLED'}

        props.one_click_phase = "UV"
        props.workflow_status_anchor = "STEP2"
        result = bpy.ops.object.alb_generate_uvs()
        if 'CANCELLED' in result:
            props.one_click_active = False
            props.one_click_phase = ""
            clear_precise_timer_prop(props, "one_click_start_time")
            self.report({'WARNING'}, "ScanReady stopped while generating UVs.")
            return {'CANCELLED'}

        props.one_click_phase = "CAGE"
        props.workflow_status_anchor = "STEP2"
        result = bpy.ops.object.alb_auto_cage_extrusion()
        if 'CANCELLED' in result:
            props.one_click_active = False
            props.one_click_phase = ""
            clear_precise_timer_prop(props, "one_click_start_time")
            self.report({'WARNING'}, "ScanReady stopped while estimating cage extrusion.")
            return {'CANCELLED'}

        # Auto cage leaves the user in a visual check state, but the one-click
        # path should continue directly into the existing modal bake workflow.
        props.show_cage = False

        texture_detail_status = build_texture_detail_status(context)
        if texture_detail_status:
            log_progress(props, 100, "UV analysis complete")
            props.progress_detail = texture_detail_status

        props.one_click_phase = "BAKE"
        props.workflow_status_anchor = "STEP3"
        result = bpy.ops.object.alb_bake_textures()
        if 'CANCELLED' in result:
            props.one_click_active = False
            props.one_click_phase = ""
            clear_precise_timer_prop(props, "one_click_start_time")
            self.report({'WARNING'}, "ScanReady stopped while starting the bake.")
            return {'CANCELLED'}

        self.report({'INFO'}, "ScanReady started. Baking continues in the progress panel.")
        return {'FINISHED'}



class ALB_OT_refresh_cage_preview(Operator):
    bl_idname = "object.alb_refresh_cage_preview"
    bl_label = "Refresh Cage"
    bl_description = "Create or refresh the cage preview from the UV mesh"

    def execute(self, context):
        active = context.active_object
        uv_obj = get_uv_object_from_any(active)
        if uv_obj is None or uv_obj.get("alb_role") != "uv":
            self.report({'WARNING'}, "Select a UV object created by the add-on.")
            return {'CANCELLED'}

        cage_obj = create_or_update_cage_preview(context, uv_obj)
        if cage_obj is None:
            self.report({'WARNING'}, "Could not create cage preview.")
            return {'CANCELLED'}

        deselect_all()
        uv_obj.hide_set(False)
        try:
            cage_obj.hide_set(False)
        except Exception:
            pass
        ensure_object_visible_and_active(uv_obj)
        try:
            visible_for_cage = [uv_obj, cage_obj] if context.scene.alb_props.show_cage else [uv_obj]
            set_workflow_visibility(context, visible_for_cage, active_obj=uv_obj, hide_related=True, render_visible_objects=False)
            cage_obj.hide_set(not context.scene.alb_props.show_cage)
            if context.scene.alb_props.show_cage:
                switch_viewport_to_material_preview(context)
        except Exception:
            pass
        self.report({'INFO'}, "Cage preview updated.")
        return {'FINISHED'}


class ALB_OT_auto_cage_extrusion(Operator):
    bl_idname = "object.alb_auto_cage_extrusion"
    bl_label = "Auto Cage Extrusion"
    bl_description = "Estimate cage extrusion by sampling the distance from the UV mesh to the original high poly mesh"

    def execute(self, context):
        props = context.scene.alb_props
        active = context.active_object
        uv_obj = get_uv_object_from_any(active)
        if uv_obj is None or uv_obj.get("alb_role") != "uv":
            self.report({'WARNING'}, "Select a UV object created by the add-on.")
            return {'CANCELLED'}

        high_obj = get_high_object_from_any(uv_obj)
        if high_obj is None or high_obj.type != 'MESH':
            self.report({'WARNING'}, "Original high poly object not found.")
            return {'CANCELLED'}

        log_progress(props, 15, "Preparing cage for bake...")
        estimated_mm, status = estimate_auto_cage_extrusion_mm(context, uv_obj, high_obj)
        if estimated_mm is None:
            props.auto_cage_status = "Auto Cage could not estimate a safe value."
            self.report({'WARNING'}, status)
            log_progress(props, 100, "Auto cage estimation failed")
            return {'CANCELLED'}

        props.cage_extrusion_mm = estimated_mm
        props.auto_cage_target_mm = estimated_mm
        props.auto_cage_status = "Cage ready for bake."
        props.auto_cage_coverage = 100.0
        props.show_cage = True

        cage_obj = create_or_update_cage_preview(context, uv_obj)
        if cage_obj is not None:
            try:
                cage_obj.hide_set(False)
            except Exception:
                pass
            try:
                set_workflow_visibility(context, [high_obj, cage_obj], active_obj=high_obj, hide_related=True, render_visible_objects=False)
                switch_viewport_to_material_preview(context)
            except Exception:
                pass

        log_progress(props, 100, "Cage ready. Continue to STEP 3: Bake Textures.")
        try:
            props.progress_detail = "Cage ready for bake.\nReady for STEP 3: Bake Textures."
        except Exception:
            pass
        self.report({'INFO'}, "Cage ready for bake.")
        return {'FINISHED'}


class ALB_OT_remove_cage_preview(Operator):
    bl_idname = "object.alb_remove_cage_preview"
    bl_label = "Remove Cage"
    bl_description = "Remove the cage preview object"

    def execute(self, context):
        active = context.active_object
        base = get_base_name(active)
        remove_cage_preview_for_base(base)
        self.report({'INFO'}, "Cage preview removed.")
        return {'FINISHED'}


def draw_compact_prop(layout, obj, prop_name, label, factor=0.48, value_scale=1.15):
    row = layout.row(align=True)
    split = row.split(factor=factor, align=True)
    split.label(text=label)

    right = split.row(align=True)
    right.alignment = 'RIGHT'
    right.scale_x = value_scale
    right.prop(obj, prop_name, text="")



class ALB_OT_save_preset(Operator):
    bl_idname = "object.alb_save_preset"
    bl_label = "Save Preset"
    bl_description = "Save all current settings as a named preset"

    def execute(self, context):
        props = context.scene.alb_props
        name = (props.preset_name_input or "").strip()
        if not name:
            self.report({'WARNING'}, "Enter a preset name first")
            return {'CANCELLED'}

        data = load_presets_dict()
        data[name] = collect_current_preset_values(props)
        save_presets_dict(data)
        props.preset_selector = name
        self.report({'INFO'}, f"Preset saved: {name}")
        return {'FINISHED'}


class ALB_OT_load_preset(Operator):
    bl_idname = "object.alb_load_preset"
    bl_label = "Load Preset"
    bl_description = "Load the selected preset and apply all saved settings"

    def execute(self, context):
        props = context.scene.alb_props
        name = props.preset_selector
        if not name or name == "__NONE__":
            self.report({'WARNING'}, "Select a preset first")
            return {'CANCELLED'}

        data = load_presets_dict()
        preset = data.get(name)
        if not isinstance(preset, dict):
            self.report({'WARNING'}, f"Preset not found: {name}")
            return {'CANCELLED'}

        apply_preset_values(props, preset)
        self.report({'INFO'}, f"Preset loaded: {name}")
        return {'FINISHED'}


class ALB_OT_delete_preset(Operator):
    bl_idname = "object.alb_delete_preset"
    bl_label = "Delete Preset"
    bl_description = "Delete the selected preset"

    def execute(self, context):
        props = context.scene.alb_props
        name = props.preset_selector
        if not name or name == "__NONE__":
            self.report({'WARNING'}, "Select a preset first")
            return {'CANCELLED'}

        data = load_presets_dict()
        if name in data:
            del data[name]
            save_presets_dict(data)
            props.preset_selector = "__NONE__"
            self.report({'INFO'}, f"Preset deleted: {name}")
            return {'FINISHED'}

        self.report({'WARNING'}, f"Preset not found: {name}")
        return {'CANCELLED'}


class ALB_OT_recalculate_normals_outside(Operator):
    bl_idname = "object.alb_recalculate_normals_outside"
    bl_label = "Recalculate Outside Normals"
    bl_description = "Recalculate the high mesh normals outside to help prevent bake artifacts from inverted normals"

    def execute(self, context):
        props = context.scene.alb_props
        obj = context.active_object
        source = get_high_object_from_any(obj)
        if source is None and obj is not None and obj.type == 'MESH':
            source = obj
        if source is None or source.type != 'MESH':
            self.report({'WARNING'}, "Select the high poly mesh first.")
            return {'CANCELLED'}
        count = recalculate_normals_outside(source)
        if count <= 0:
            props.normals_status = "No mesh faces found for normal recalculation."
            self.report({'WARNING'}, props.normals_status)
            return {'CANCELLED'}
        props.normals_status = f"Normals recalculated outside on {count:,} faces."
        self.report({'INFO'}, props.normals_status)
        try:
            bpy.context.workspace.status_text_set(text=f"ScanReady: {props.normals_status}")
        except Exception:
            pass
        return {'FINISHED'}


class ALB_OT_reset_defaults(Operator):
    bl_idname = "object.alb_reset_defaults"
    bl_label = "Reset Defaults"
    bl_description = "Restore all default settings"

    def execute(self, context):
        props = context.scene.alb_props

        # Fast reset: lock live updates so Blender does not rebuild checker/cage/preview
        # repeatedly while defaults are being restored.
        props.is_resetting_defaults = True
        props.internal_update_lock = True
        try:
            # STEP 1
            props.weld_distance_cm = DEFAULTS['weld_distance_cm']
            if hasattr(props, "pre_decimate_merge_cm"):
                props.pre_decimate_merge_cm = DEFAULTS['pre_decimate_merge_cm']
            if hasattr(props, "auto_fix_normals"):
                props.auto_fix_normals = DEFAULTS['auto_fix_normals']
            if hasattr(props, "auto_combine_mesh_parts"):
                props.auto_combine_mesh_parts = DEFAULTS['auto_combine_mesh_parts']
            if hasattr(props, "auto_clean_scan_debris"):
                props.auto_clean_scan_debris = DEFAULTS['auto_clean_scan_debris']
            if hasattr(props, "normals_status"):
                props.normals_status = ""
            props.show_wireframe = False
            props.show_checker = False
            props.checker_was_enabled_before_bake = False
            props.ui_faces_cached = 0
            props.ui_tris_cached = 0
            props.checker_mix = DEFAULTS['checker_mix']
            props.checker_uv_scale = DEFAULTS['checker_uv_scale']

            # Keep target/ratio in sync without firing preview updates
            props.target_poly = 4000
            props.decimate_ratio = DEFAULTS['decimate_ratio']


            # STEP 2
            props.uv_method = 'SMART'
            if hasattr(props, "smart_uv_preset"):
                props.smart_uv_preset = 'BALANCED'
            if hasattr(props, "smart_uv_angle"):
                props.smart_uv_angle = DEFAULTS['smart_uv_angle']
            props.auto_pack_uv = True
            props.show_cage = False
            props.uv_padding_px = DEFAULTS['uv_padding_px']

            # STEP 3
            if hasattr(props, "texture_size_preset"):
                props.texture_size_preset = '2048'
            if hasattr(props, "texture_size"):
                props.texture_size = DEFAULTS['texture_size']
            if hasattr(props, "use_auto_bake_margin"):
                props.use_auto_bake_margin = True
            if hasattr(props, "base_bake_margin_px"):
                props.base_bake_margin_px = 4
            if hasattr(props, "bake_margin_px"):
                props.bake_margin_px = DEFAULTS['bake_margin_px']
            if hasattr(props, "bake_material_count"):
                props.bake_material_count = DEFAULTS['bake_material_count']
            props.cage_extrusion_mm = DEFAULTS['cage_extrusion_mm']
            props.cage_alpha = DEFAULTS['cage_alpha']
            if hasattr(props, "auto_cage_status"):
                props.auto_cage_status = ""
            if hasattr(props, "auto_cage_coverage"):
                props.auto_cage_coverage = 0.0
            if hasattr(props, "auto_cage_target_mm"):
                props.auto_cage_target_mm = 0.0
            props.bake_basecolor = DEFAULTS['bake_basecolor']
            props.bake_normal = DEFAULTS['bake_normal']
            if hasattr(props, "bake_roughness"):
                props.bake_roughness = DEFAULTS['bake_roughness']
            if hasattr(props, "bake_occlusion"):
                props.bake_occlusion = DEFAULTS['bake_occlusion']
            if hasattr(props, "ao_auto_distance"):
                props.ao_auto_distance = DEFAULTS['ao_auto_distance']
            if hasattr(props, "ao_distance"):
                props.ao_distance = DEFAULTS['ao_distance']
            if hasattr(props, "ao_samples"):
                props.ao_samples = DEFAULTS['ao_samples']
            if hasattr(props, "ao_source"):
                props.ao_source = DEFAULTS['ao_source']
            props.save_images = DEFAULTS['save_images']
            if hasattr(props, "image_format"):
                props.image_format = DEFAULTS['image_format']
            if hasattr(props, "jpeg_quality"):
                props.jpeg_quality = DEFAULTS['jpeg_quality']
            if hasattr(props, "tiff_16bit"):
                props.tiff_16bit = DEFAULTS['tiff_16bit']
            props.normal_strength = DEFAULTS['normal_strength']
            if hasattr(props, "low_vram_bake"):
                props.low_vram_bake = DEFAULTS['low_vram_bake']
            if hasattr(props, "low_vram_force_cpu"):
                props.low_vram_force_cpu = DEFAULTS['low_vram_force_cpu']
            if hasattr(props, "fit_low_to_high_before_bake"):
                props.fit_low_to_high_before_bake = DEFAULTS['fit_low_to_high_before_bake']
            if hasattr(props, "fit_low_to_high_offset_mm"):
                props.fit_low_to_high_offset_mm = DEFAULTS['fit_low_to_high_offset_mm']

            try:
                if hasattr(props, "last_saved_texture_path"):
                    props.last_saved_texture_path = ""
            except Exception:
                pass

            for attr in (
                "uv_analysis_summary",
                "uv_analysis_detail",
                "uv_analysis_warning",
                "uv_analysis_uv_space",
                "uv_analysis_recommendation",
            ):
                try:
                    if hasattr(props, attr):
                        setattr(props, attr, "")
                except Exception:
                    pass

            # Reset progress box to neutral
            try:
                props.progress_percent = 0.0
                props.progress_status = ""
                props.progress_detail = ""
                props.workflow_status_anchor = "STEP1"
                props.one_click_active = False
                props.one_click_phase = ""
                clear_precise_timer_prop(props, "one_click_start_time")
            except Exception:
                pass
        finally:
            props.internal_update_lock = False
            props.is_resetting_defaults = False

        # Do a single lightweight cleanup at the end instead of many live updates
        try:
            obj = context.active_object
            target = obj
            if target is not None:
                try:
                    remove_checker_from_object(target)
                except Exception:
                    pass
            preview_obj = get_preview_object_from_any(obj) if obj is not None else None
            if preview_obj is not None:
                try:
                    remove_checker_from_object(preview_obj)
                except Exception:
                    pass
            cage_obj = get_cage_object_from_any(obj) if obj is not None else None
            if cage_obj is not None:
                try:
                    cage_obj.hide_set(True)
                except Exception:
                    pass
        except Exception:
            pass

        self.report({'INFO'}, "Default values restored.")
        return {'FINISHED'}


# ------------------------------------------------------------
# UI
# ------------------------------------------------------------

def draw_wrapped_label(layout, text, max_chars=54, icon='NONE'):
    text = str(text or "")
    if not text:
        return

    lines = []
    for paragraph in text.splitlines():
        words = paragraph.split()
        current = ""
        for word in words:
            if not current:
                current = word
            elif len(current) + 1 + len(word) <= max_chars:
                current += " " + word
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        elif paragraph == "":
            lines.append("")

    for i, line in enumerate(lines):
        if i == 0 and icon != 'NONE':
            layout.label(text=line, icon=icon)
        else:
            layout.label(text=line)


def draw_progress_bar(layout, value, text="", detail=""):
    value = max(0.0, min(100.0, value))
    box = layout.box()
    box.label(text=f"Global Progress: {value:.0f}%")
    if text:
        draw_wrapped_label(box, text, max_chars=48)
    if detail:
        draw_wrapped_label(box, detail, max_chars=48)


def draw_workflow_status(layout, props):
    progress_box = layout.box()
    header = progress_box.row()
    try:
        active = is_progress_active(props)
    except Exception:
        active = False
    header.alert = active
    header.scale_y = 1.15 if active else 1.0
    header.label(text="Workflow Status", icon='INFO')
    draw_progress_bar(
        progress_box,
        props.progress_percent,
        props.progress_status,
        getattr(props, "progress_detail", "")
    )


def shorten_ui_path(path, max_chars=46):
    path = str(path or "")
    if len(path) <= max_chars:
        return path

    normalized = path.replace("\\", "/")
    parts = [p for p in normalized.split("/") if p]
    if len(parts) >= 2:
        shortened = f".../{parts[-2]}/{parts[-1]}"
        if len(shortened) <= max_chars:
            return shortened

    return "..." + path[-max(8, max_chars - 3):]


class ALB_PT_panel(Panel):
    bl_label = f"Scan Ready v{get_version_string()}"
    bl_idname = "ALB_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Scan Ready'

    def draw(self, context):
        layout = self.layout
        props = context.scene.alb_props
        obj = context.active_object
        sanitize_bake_material_count(props)

        source_obj = get_high_object_from_any(obj)
        stats_obj = obj if obj and obj.type == 'MESH' else source_obj
        preview_obj = get_preview_object_from_any(obj) if obj is not None else None
        uv_obj = get_uv_object_from_any(obj) if obj is not None else None
        has_preview = preview_obj is not None and getattr(preview_obj, "type", None) == 'MESH'
        has_uv = uv_obj is not None and getattr(uv_obj, "type", None) == 'MESH'

        prefs = get_scanready_addon_preferences(context)
        if is_scanready_update_available(prefs):
            draw_scanready_update_notice(layout, prefs, include_actions=False)

        stats_box = layout.box()
        stats_header = stats_box.row(align=True)
        stats_header.label(text="Mesh Stats", icon='MESH_DATA')
        stats_header.operator("object.alb_refresh_stats", text="", icon='FILE_REFRESH')
        if props.preview_info:
            stats_box.label(text=props.preview_info)


        one_click_box = layout.box()
        one_click_row = one_click_box.row()
        one_click_row.scale_y = 1.6
        one_click_row.operator("object.alb_one_click_bake", text="ONE CLICK BAKE", icon='RENDER_STILL', depress=True)
        one_click_box.label(text="One-click scan optimization", icon='INFO')

        view_box = layout.box()
        view_box.label(text="View Options", icon='HIDE_OFF')
        view_col = view_box.column(align=True)
        view_col.prop(props, "show_wireframe")
        view_col.prop(props, "show_checker")
        if props.show_checker:
            view_col.prop(props, "checker_mix")
            view_col.prop(props, "checker_uv_scale")

        workflow_status_anchor = str(getattr(props, "workflow_status_anchor", "STEP1") or "STEP1").upper()
        if props.show_step4 and workflow_status_anchor not in {"STEP1", "STEP2", "STEP3"}:
            workflow_status_anchor = "STEP4"
        if workflow_status_anchor not in {"STEP1", "STEP2", "STEP3", "STEP4"}:
            workflow_status_anchor = "STEP1"

        # STEP 1
        if workflow_status_anchor == "STEP1":
            draw_workflow_status(layout, props)

        header1 = layout.row(align=True)
        header1.label(text="", icon='MOD_DECIM')
        header1.prop(
            props, "show_step1",
            text="STEP 1 Preview / Reduce",
            emboss=False,
            icon='DOWNARROW_HLT' if props.show_step1 else 'RIGHTARROW'
        )

        if props.show_step1:
            box1 = layout.box()
            col1 = box1.column(align=True)
            col1.prop(props, "target_poly")
            col1.prop(props, "decimate_ratio")
            reduction_percent = max(0.0, min(99.99, (1.0 - float(props.decimate_ratio)) * 100.0))
            col1.label(text=f"Reduction: {reduction_percent:.1f}%", icon='MOD_DECIM')

            row = box1.row()
            row.scale_y = 1.35
            row.operator("object.alb_create_preview", text="Create Lowpoly Preview", icon='RESTRICT_VIEW_OFF', depress=True)

        if workflow_status_anchor == "STEP2":
            draw_workflow_status(layout, props)

        # STEP 2
        header2 = layout.row(align=True)
        header2.label(text="", icon='TEXTURE')
        header2.prop(
            props, "show_step2",
            text="STEP 2 UV / Cage",
            emboss=False,
            icon='DOWNARROW_HLT' if props.show_step2 else 'RIGHTARROW'
        )

        if props.show_step2:
            box2 = layout.box()
            col2 = box2.column(align=True)
            col2.prop(props, "smart_uv_preset")
            col2.separator()
            col2.prop(props, "show_cage")
            if props.show_cage:
                col2.prop(props, "cage_extrusion_mm")
                col2.prop(props, "cage_alpha")
            auto_cage_row = box2.row()
            auto_cage_row.enabled = has_uv
            auto_cage_row.operator("object.alb_auto_cage_extrusion", text="Auto Cage Extrusion", icon='MOD_DISPLACE')
            if getattr(props, "auto_cage_status", ""):
                box2.label(text=props.auto_cage_status, icon='INFO')

            row = box2.row()
            row.enabled = has_preview
            row.scale_y = 1.35
            row.operator("object.alb_generate_uvs", text="Generate UVs", icon='GROUP_UVS', depress=has_preview)
            if not has_preview:
                box2.label(text="Create a lowpoly preview first.", icon='INFO')

        # STEP 3
        if workflow_status_anchor == "STEP3" and not props.show_step4:
            draw_workflow_status(layout, props)

        header3 = layout.row(align=True)
        header3.label(text="", icon='RENDER_RESULT')
        header3.prop(
            props, "show_step3",
            text="STEP 3 Bake / Output",
            emboss=False,
            icon='DOWNARROW_HLT' if props.show_step3 else 'RIGHTARROW'
        )

        if props.show_step3:
            box3 = layout.box()
            col3 = box3.column(align=True)
            draw_compact_prop(col3, props, "texture_size_preset", "Texture Preset:")
            draw_compact_prop(col3, props, "bake_material_count", "Bake Materials:")

            uv_eff_box = col3.box()
            uv_eff_box.label(text="Texture Detail", icon='TEXTURE')
            uv_eff_box.operator("object.alb_analyze_uv_usage", text="Analyze Texture Detail", icon='VIEWZOOM')
            if getattr(props, "uv_analysis_summary", ""):
                draw_wrapped_label(uv_eff_box, props.uv_analysis_summary, max_chars=58)
            if getattr(props, "uv_analysis_recommendation", ""):
                draw_wrapped_label(uv_eff_box, props.uv_analysis_recommendation, max_chars=58, icon='CHECKMARK')
            if getattr(props, "uv_analysis_detail", ""):
                draw_wrapped_label(uv_eff_box, props.uv_analysis_detail, max_chars=58)
            if getattr(props, "uv_analysis_warning", ""):
                warning_icon = 'CHECKMARK' if props.uv_analysis_warning.startswith("Good match") else 'ERROR'
                draw_wrapped_label(uv_eff_box, props.uv_analysis_warning, max_chars=58, icon=warning_icon)
            if getattr(props, "uv_analysis_uv_space", ""):
                draw_wrapped_label(uv_eff_box, props.uv_analysis_uv_space, max_chars=58)
            col3.separator()
            col3.prop(props, "bake_basecolor")
            col3.prop(props, "bake_normal")
            if props.bake_normal:
                col3.prop(props, "normal_strength")
            col3.prop(props, "bake_roughness")
            col3.prop(props, "bake_occlusion")
            col3.separator()
            col3.prop(props, "save_images")

            if props.save_images:
                draw_compact_prop(col3, props, "image_format", "Image Format:")
                draw_compact_prop(col3, props, "output_folder", "Output Folder:", factor=0.34)

            row = box3.row()
            row.enabled = has_uv
            row.scale_y = 1.55
            row.operator("object.alb_bake_textures", text="Bake Textures", icon='RENDER_STILL', depress=has_uv)
            if not has_uv:
                box3.label(text="Generate UVs before baking.", icon='INFO')

            path_box = box3.box()
            path_box.label(text="Output", icon='FILE_FOLDER')
            if getattr(props, "last_saved_texture_path", ""):
                path_box.label(text=shorten_ui_path(props.last_saved_texture_path))
            else:
                path_box.label(text="No textures saved yet")

        if workflow_status_anchor in {"STEP3", "STEP4"} and props.show_step4:
            draw_workflow_status(layout, props)

        # STEP 4
        header4 = layout.row(align=True)
        header4.label(text="", icon='TOOL_SETTINGS')
        header4.prop(
            props, "show_step4",
            text="Advanced",
            emboss=False,
            icon='DOWNARROW_HLT' if props.show_step4 else 'RIGHTARROW'
        )

        if props.show_step4:
            box4 = layout.box()

            mesh_box = box4.box()
            mesh_box.label(text="Mesh Settings", icon='MESH_DATA')
            mesh_col = mesh_box.column(align=True)
            mesh_col.prop(props, "weld_distance_cm")
            mesh_col.prop(props, "pre_decimate_merge_cm")
            mesh_col.prop(props, "auto_fix_normals")
            mesh_col.prop(props, "auto_combine_mesh_parts")
            mesh_col.prop(props, "auto_clean_scan_debris")
            mesh_col.prop(props, "show_face_orientation")
            mesh_col.prop(props, "use_texture_view")
            normals_row = mesh_col.row()
            normals_row.operator("object.alb_recalculate_normals_outside", text="Recalculate Outside Normals", icon='NORMALS_FACE')
            if getattr(props, "normals_status", ""):
                status = props.normals_status
                if len(status) > 44:
                    status = status[:41] + "..."
                mesh_col.label(text=status, icon='INFO')


            uv_box = box4.box()
            uv_box.label(text="UV Settings", icon='UV')
            uv_col = uv_box.column(align=True)
            uv_col.prop(props, "smart_uv_angle")
            uv_col.prop(props, "uv_padding_px")

            bake_box = box4.box()
            bake_box.label(text="Bake Settings", icon='RENDER_STILL')
            bake_col = bake_box.column(align=True)
            bake_col.prop(props, "bake_samples")
            bake_col.prop(props, "bake_margin_px")
            bake_col.prop(props, "fit_low_to_high_before_bake")
            if props.fit_low_to_high_before_bake:
                bake_col.prop(props, "fit_low_to_high_offset_mm")
            if getattr(props, "image_format", "JPEG") == 'JPEG':
                bake_col.prop(props, "jpeg_quality")
            if getattr(props, "image_format", "JPEG") == 'TIFF':
                bake_col.prop(props, "tiff_16bit")
            if props.bake_occlusion:
                ao_box = bake_col.box()
                ao_box.label(text="Occlusion Settings", icon='SHADING_RENDERED')
                ao_col = ao_box.column(align=True)
                ao_col.prop(props, "ao_source")
                ao_col.prop(props, "ao_auto_distance")
                if not props.ao_auto_distance:
                    ao_col.prop(props, "ao_distance")
                ao_col.prop(props, "ao_samples")
            memory_box = bake_col.box()
            memory_box.label(text="Memory Safety", icon='TOOL_SETTINGS')
            memory_col = memory_box.column(align=True)
            memory_col.prop(props, "low_vram_bake")
            memory_col.prop(props, "low_vram_force_cpu")

            preset_box = box4.box()
            preset_header = preset_box.row(align=True)
            preset_header.prop(
                props,
                "show_advanced_presets",
                text="Presets",
                emboss=False,
                icon='DOWNARROW_HLT' if props.show_advanced_presets else 'RIGHTARROW'
            )
            if props.show_advanced_presets:
                preset_col = preset_box.column(align=True)
                preset_col.prop(props, "preset_name_input")
                row_preset_top = preset_col.row(align=True)
                row_preset_top.operator("object.alb_save_preset", text="Save Preset", icon='ADD')
                row_preset_select = preset_col.row(align=True)
                row_preset_select.prop(props, "preset_selector", text="")
                row_preset_actions = preset_col.row(align=True)
                row_preset_actions.operator("object.alb_load_preset", text="Reload Preset", icon='IMPORT')
                row_preset_actions.operator("object.alb_delete_preset", text="Delete Preset", icon='TRASH')

            util_box = box4.box()
            util_box.label(text="Utilities", icon='TOOL_SETTINGS')
            row_reset = util_box.row()
            row_reset.scale_y = 1.15
            row_reset.operator("object.alb_reset_defaults", text="Reset Defaults", icon='FILE_REFRESH')



# ------------------------------------------------------------
# Addon Preferences / Updates
# ------------------------------------------------------------

SCANREADY_DOCUMENTATION_URL = "https://marioschiano.github.io/scanready-docs/"
SCANREADY_RELEASE_NOTES_URL = SCANREADY_DOCUMENTATION_URL
SCANREADY_UPDATE_MANIFEST_URL = "https://marioschiano.github.io/scanready-docs/update-manifest.json"


def version_tuple_from_string(value):
    parts = []
    for token in str(value).replace("v", "").split("."):
        try:
            parts.append(int(token))
        except Exception:
            parts.append(0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts[:3])


def get_scanready_addon_preferences(context):
    try:
        return context.preferences.addons[__name__].preferences
    except Exception:
        return None


def is_scanready_update_available(prefs):
    if prefs is None:
        return False
    try:
        if not getattr(prefs, "latest_version", ""):
            return False
        return version_tuple_from_string(prefs.latest_version) > version_tuple_from_string(get_version_string())
    except Exception:
        return False


def draw_scanready_update_notice(layout, prefs, include_actions=True):
    box = layout.box()
    notice_col = box.column(align=True)

    icon_row = notice_col.row()
    icon_row.alert = True
    icon_row.alignment = 'CENTER'
    icon_row.label(text="", icon='FILE_REFRESH')

    title_row = notice_col.row()
    title_row.alert = True
    title_row.alignment = 'CENTER'
    title_row.label(text="Newer version of ScanReady available")

    hint_row = notice_col.row()
    hint_row.alert = True
    hint_row.alignment = 'CENTER'
    hint_row.label(text="Update from Blender Extensions or your marketplace")

    installed_row = notice_col.row()
    installed_row.alignment = 'CENTER'
    installed_row.label(text=f"Installed version: {get_version_string()}")

    available_row = notice_col.row()
    available_row.alignment = 'CENTER'
    available_row.label(text=f"Available Version: {prefs.latest_version}")

    if include_actions:
        action_row = box.row(align=True)
        action_row.operator("scanready.open_release_notes", text="Release Notes", icon='HELP')

    return box


class ALB_OT_check_for_updates(Operator):
    bl_idname = "scanready.check_for_updates"
    bl_label = "Check for Updates"
    bl_description = "Check whether a newer ScanReady version is available"

    def execute(self, context):
        prefs = get_scanready_addon_preferences(context)
        if prefs is None:
            self.report({'WARNING'}, "ScanReady preferences not found")
            return {'CANCELLED'}
        current_version = get_version_string()
        manifest_url = prefs.update_manifest_url.strip()

        if not manifest_url:
            prefs.update_status = "Update source not configured yet. Add the Superhive or Gumroad manifest URL after publishing."
            self.report({'INFO'}, "ScanReady update source is not configured yet")
            return {'FINISHED'}

        try:
            request = urllib.request.Request(manifest_url, headers={"User-Agent": "ScanReady"})
            with urllib.request.urlopen(request, timeout=8) as response:
                data = json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            prefs.update_status = f"Could not check for updates: {exc}"
            self.report({'WARNING'}, "Could not check for ScanReady updates")
            return {'CANCELLED'}

        latest_version = str(data.get("latest_version", current_version)).strip()
        release_notes_url = str(data.get("release_notes_url", "")).strip()

        prefs.latest_version = latest_version
        if release_notes_url:
            prefs.release_notes_url = release_notes_url

        if version_tuple_from_string(latest_version) > version_tuple_from_string(current_version):
            prefs.update_available = True
            prefs.update_status = f"Version {latest_version} is available. Update from Blender Extensions or your marketplace."
        else:
            prefs.update_available = False
            prefs.update_status = f"ScanReady is up to date. Installed version: {current_version}."

        self.report({'INFO'}, prefs.update_status)
        return {'FINISHED'}


class ALB_OT_open_documentation(Operator):
    bl_idname = "scanready.open_documentation"
    bl_label = "Open ScanReady Documentation"
    bl_description = "Open the ScanReady online documentation"

    def execute(self, context):
        webbrowser.open(SCANREADY_DOCUMENTATION_URL)
        return {'FINISHED'}

class ALB_OT_open_release_notes(Operator):
    bl_idname = "scanready.open_release_notes"
    bl_label = "View ScanReady Release Notes"
    bl_description = "Open the ScanReady release notes page"

    def execute(self, context):
        prefs = get_scanready_addon_preferences(context)
        url = prefs.release_notes_url.strip() if prefs is not None else ""
        url = url or SCANREADY_RELEASE_NOTES_URL
        webbrowser.open(url)
        return {'FINISHED'}


class ALB_AddonPreferences(AddonPreferences):
    bl_idname = __name__

    update_manifest_url: StringProperty(
        name="Update Manifest URL",
        description="JSON URL used to check the latest ScanReady version after publishing",
        default=SCANREADY_UPDATE_MANIFEST_URL,
    )
    release_notes_url: StringProperty(
        name="Release Notes URL",
        description="Page with ScanReady release notes and documentation",
        default=SCANREADY_RELEASE_NOTES_URL,
    )
    latest_version: StringProperty(
        name="Latest Version",
        default="",
    )
    update_available: BoolProperty(
        name="Update Available",
        default=False,
        options={'HIDDEN'},
    )
    update_status: StringProperty(
        name="Update Status",
        default="Ready. Update links are set to the ScanReady docs page.",
    )

    def draw(self, context):
        layout = self.layout
        current_version = get_version_string()

        box = layout.box()
        box.label(text="ScanReady Updates", icon='FILE_REFRESH')
        has_update = is_scanready_update_available(self)
        if has_update:
            draw_scanready_update_notice(box, self, include_actions=False)
        else:
            box.label(text=f"Installed version: {current_version}")
            if self.latest_version:
                box.label(text=f"Latest version: {self.latest_version}")
        status_row = box.row()
        status_row.alert = bool(self.update_available)
        status_row.label(text=self.update_status, icon='ERROR' if self.update_available else 'INFO')

        docs_row = box.row(align=True)
        docs_row.operator("scanready.open_documentation", text="Open Documentation", icon='HELP')
        docs_row.operator("scanready.open_release_notes", text="Release Notes", icon='TEXT')

        row = box.row(align=True)
        row.operator("scanready.check_for_updates", icon='FILE_REFRESH')

# ------------------------------------------------------------
# Register
# ------------------------------------------------------------

classes = (
    ALB_AddonPreferences,
    ALB_OT_check_for_updates,
    ALB_OT_open_documentation,
    ALB_OT_open_release_notes,
    ALB_Properties,
    ALB_OT_analyze_uv_usage,
    ALB_OT_create_preview,
    ALB_OT_generate_uvs,
    ALB_OT_refresh_stats,
    ALB_OT_bake_textures_modal,
    ALB_OT_bake_textures,
    ALB_OT_one_click_bake,
    ALB_OT_auto_cage_extrusion,
    ALB_OT_save_preset,
    ALB_OT_load_preset,
    ALB_OT_delete_preset,
    ALB_OT_recalculate_normals_outside,
    ALB_OT_reset_defaults,
    ALB_PT_panel,
)


def register():
    print(f"ScanReady v{get_version_string()} loaded")
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.alb_props = PointerProperty(type=ALB_Properties)


def unregister():
    del bpy.types.Scene.alb_props
    for c in reversed(classes):
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()





















