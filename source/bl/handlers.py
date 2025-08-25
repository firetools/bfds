# SPDX-License-Identifier: GPL-3.0-or-later

"""!
BFDS, handlers.
"""

import bpy, logging
from bpy.app.handlers import persistent, load_post, save_pre, depsgraph_update_post
from bpy.types import Object
from .. import utils
from .. import config
from ..types import BFNamelistSc

from ..ui.prop_panels import toggle_simple_property_panel
from ..lang.bf_object import OP_other
from ..lang.bf_material import MP_other

log = logging.getLogger(__name__)


@persistent
def _load_post(self):
    """!
    Run automatic setup after loading a Blender file.
    """
    # Beware: self is None

    # Check file format version
    bf_file_version = tuple(bpy.data.scenes[0].bf_file_version)

    if bf_file_version == (0, 0, 0):
        # New file, set current file format version
        for sc in bpy.data.scenes:
            sc.bf_file_version = config.SUPPORTED_FILE_VERSION

    elif bf_file_version < config.SUPPORTED_FILE_VERSION:
        bpy.ops.wm.bf_dialog(
            "INVOKE_DEFAULT",
            msg="Check your data!",
            description="This file was created with an old and unsupported BFDS version.",
            type="ERROR",
        )

    elif bf_file_version > config.SUPPORTED_FILE_VERSION:
        bpy.ops.wm.bf_dialog(
            "INVOKE_DEFAULT",
            msg="Install latest BFDS!",
            description="This file was created with a new BFDS version.",
            type="ERROR",
        )

    # Remove all caches and tmp objects, clean up to remove stale caches
    utils.geometry.rm_geometric_caches()
    utils.geometry.rm_tmp_objects()

    # Init FDS default materials
    for k, v in config.DEFAULT_MAS.items():
        ma = bpy.data.materials.get(k)  # k is ID
        if not ma:
            ma = bpy.data.materials.new(k)
        ma.diffuse_color = v[0]  # RGB
        ma.bf_surf_export = True
        ma.use_fake_user = True

    # Set default appearances of Scene, Object, Material instances
    context = bpy.context
    for sc in bpy.data.scenes:
        # set only once
        BFNamelistSc(sc).set_appearance(context=context)
    for ob in bpy.data.objects:
        bf_namelist = ob.bf_namelist
        if bf_namelist:
            # config.SET_OBJECT_APPEARANCE is checked in bf_namelist
            bf_namelist.set_appearance(context=context)
    for ma in bpy.data.materials:
        bf_namelist = ma.bf_namelist
        if bf_namelist:
            # config.SET_MATERIAL_APPEARANCE is checked in bf_namelist
            bf_namelist.set_appearance(context=context)

    # Set simplified property panel
    toggle_simple_property_panel()


@persistent
def _save_pre(self):
    """!
    Run automatic setup before saving a Blender file.
    """
    # Beware: self is None
    # Remove all caches and tmp objects, clean up to prevent stale caches
    utils.geometry.rm_geometric_caches()
    utils.geometry.rm_tmp_objects()
    # Set file format version
    for sc in bpy.data.scenes:
        sc.bf_file_version = config.SUPPORTED_FILE_VERSION


@persistent
def _depsgraph_update_post(scene):
    """!
    Detect object change and erase cached geometry.
    """
    for update in bpy.context.view_layer.depsgraph.updates:
        ob = update.id.original
        if (
            isinstance(ob, Object)
            and ob.type in {"MESH", "CURVE", "SURFACE", "FONT", "META"}
            and (update.is_updated_geometry or update.is_updated_transform)
        ):
            ob["ob_to_xbs_cache"] = None


# Register


def register():
    log.debug("Register handlers...")
    load_post.append(_load_post)
    save_pre.append(_save_pre)
    depsgraph_update_post.append(_depsgraph_update_post)


def unregister():
    log.debug("Unregister handlers...")
    depsgraph_update_post.remove(_depsgraph_update_post)
    save_pre.remove(_save_pre)
    load_post.remove(_load_post)
