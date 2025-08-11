"""!
BFDS, set visibility of Blender property panels.
"""

import logging, bpy
from .. import config

log = logging.getLogger(__name__)


def _set_property_panels_visibility(space):
    space.show_properties_tool = False
    space.show_properties_render = False
    space.show_properties_output = False
    space.show_properties_view_layer = False
    space.show_properties_scene = True
    space.show_properties_world = False
    space.show_properties_collection = True
    space.show_properties_object = True
    space.show_properties_modifiers = True
    space.show_properties_effects = False
    space.show_properties_particles = False
    space.show_properties_physics = False
    space.show_properties_constraints = False
    space.show_properties_data = False
    space.show_properties_bone = False
    space.show_properties_bone_constraints
    space.show_properties_material = True
    space.show_properties_texture = False


# Called by _load_post handler


def toggle_simple_property_panel():
    if not config.ADDON_PREFS.preferences.bf_pref_simplify_ui:
        return
    log.debug(f"Set visibility of Blender property panels...")
    # Get all spaces of areas of type "PROPERTIES" and set panel visibility
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == "PROPERTIES":
                for space in area.spaces:
                    _set_property_panels_visibility(space)
