# SPDX-License-Identifier: GPL-3.0-or-later

"""!
BFDS, simplify Blender ui.
"""

import logging, bpy
from bpy.utils import register_class, unregister_class
from bpy.types import Menu
from bpy.app.translations import contexts as i18n_contexts
from .. import config
from . import replace

log = logging.getLogger(__name__)


# Names of original Blender classes to be removed
# from: 4.5/scripts/startup/bl_ui/*_workspace.py
_remove_class_names = (
    # Scene panel
    "SCENE_UL_keying_set_paths",
    "SCENE_PT_scene",
    # "SCENE_PT_unit",  # for BlenderBIM addon compat
    "SCENE_PT_physics",
    "SCENE_PT_simulation",
    "SCENE_PT_keying_sets",
    "SCENE_PT_keying_set_paths",
    "SCENE_PT_keyframing_settings",
    "SCENE_PT_audio",
    "SCENE_PT_rigid_body_world",
    "SCENE_PT_rigid_body_world_settings",
    "SCENE_PT_rigid_body_cache",
    "SCENE_PT_rigid_body_field_weights",
    "SCENE_PT_eevee_next_light_probes",
    "SCENE_PT_animation",
    "SCENE_PT_custom_props",
    # Collection panel
    "COLLECTION_MT_context_menu_instance_offset",
    "COLLECTION_PT_collection_flags",
    "COLLECTION_PT_viewlayer_flags",
    "COLLECTION_PT_instancing",
    "COLLECTION_PT_lineart_collection",
    "COLLECTION_PT_collection_custom_props",
    "COLLECTION_PT_exporters",
    # Object panel
    # "OBJECT_PT_context_object",
    # "OBJECT_PT_transform",  # for BlenderBIM addon compat
    # "OBJECT_PT_delta_transform",
    # "OBJECT_PT_relations",
    # "COLLECTION_MT_context_menu",
    # "OBJECT_PT_collections",
    "OBJECT_PT_instancing",
    "OBJECT_PT_instancing_size",
    "OBJECT_PT_motion_paths",
    "OBJECT_PT_motion_paths_display",
    # "OBJECT_PT_display",
    "OBJECT_PT_shading",
    "OBJECT_MT_light_linking_context_menu",
    "OBJECT_PT_light_linking",
    "OBJECT_MT_shadow_linking_context_menu",
    "OBJECT_PT_shadow_linking",
    "OBJECT_PT_shadow_terminator",
    # "OBJECT_PT_visibility",
    "OBJECT_PT_lineart",
    "OBJECT_PT_animation",
    "OBJECT_PT_custom_props",
    # Material panel
    # "MATERIAL_MT_context_menu",
    # "MATERIAL_UL_matslots",
    # "MATERIAL_PT_preview",
    # "EEVEE_MATERIAL_PT_context_material",
    "EEVEE_MATERIAL_PT_surface",
    "EEVEE_MATERIAL_PT_volume",
    "EEVEE_MATERIAL_PT_displacement",
    "EEVEE_MATERIAL_PT_thickness",
    "EEVEE_MATERIAL_PT_settings",
    "EEVEE_NEXT_MATERIAL_PT_settings_surface",
    "EEVEE_NEXT_MATERIAL_PT_settings_volume",
    "MATERIAL_PT_lineart",
    "MATERIAL_PT_viewport",
    "EEVEE_MATERIAL_PT_viewport_settings",
    "MATERIAL_PT_animation",
    "MATERIAL_PT_custom_props",
)

# Names of original Blender classes to be replaced,
# see their definition in the replace folder
_replace_class_names = (
    "TOPBAR_MT_editor_menus",
    "VIEW3D_HT_header",
    "VIEW3D_MT_editor_menus",
    "VIEW3D_MT_add",
    "VIEW3D_MT_object",
)


# List of refs to removed original Blender classes.
# After unregistering, this list keeps the original refs
# to allow restoration of normal UI.
_remove_classes = list()


def _init_remove_classes():
    log.debug(f"Init refs to original Blender ui classes...")
    for n in _remove_class_names + _replace_class_names:
        module_name = f"bpy.types.{n}"
        try:
            _remove_classes.append(eval(module_name))
        except:
            log.debug(f"Impossible to init original ui class <{module_name}>")


# Set simple UI, restore normal UI


def _set_simple_ui():
    log.debug("Set simple UI...")

    # Check if UI is already simple, by the first removed class
    if not hasattr(bpy.types, _remove_class_names[0]):
        log.debug("UI is already simple.")
        return

    # Unregister original classes,
    # included those that will be replaced
    for c in _remove_classes:
        try:
            unregister_class(c)
        except:
            log.debug(f"Impossible to unregister original class <{c}>")

    # Register replacement classes
    for n in _replace_class_names:
        try:
            register_class(getattr(replace, n))
        except:
            log.debug(f"Impossible to register replacement class <{n}>")


def _set_normal_ui():
    log.debug("Set normal UI...")

    # Check if UI is already normal, by the first removed class
    if hasattr(bpy.types, _remove_class_names[0]):
        log.debug("UI is already simple.")
        return

    # Unregister replacement classes
    for n in _replace_class_names:
        try:
            unregister_class(getattr(replace, n))
        except:
            log.debug(f"Impossible to unregister replacement class <{n}>")

    # Register original classes,
    # included those that were replaced
    for c in _remove_classes:
        try:
            register_class(c)
        except:
            log.debug(f"Impossible to register original class <{c}>")


def toggle_simple_ui(context=None, force_normal=False):
    log.debug("Toggle simple ui...")

    # First start, load original references
    if not _remove_classes:
        _init_remove_classes()

    if force_normal:
        _set_normal_ui()
        return

    if context is None:
        context = bpy.context

    bf_prefs = context.preferences.addons[config.ADDON_PACKAGE].preferences
    if bf_prefs.bf_pref_simplify_ui:
        _set_simple_ui()
    else:
        _set_normal_ui()


# Register/Unregister


def register():
    toggle_simple_ui()  # at start, check and set


def unregister():
    toggle_simple_ui(force_normal=True)  # at end, restore
