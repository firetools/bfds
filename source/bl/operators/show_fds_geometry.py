# SPDX-License-Identifier: GPL-3.0-or-later

"""!
BFDS, operators to show generated FDS geometry.
"""


import logging
from bpy.types import Operator
from bpy.props import BoolProperty
from ...types import BFException
from ... import utils, lang

log = logging.getLogger(__name__)


class OBJECT_OT_bf_show_fds_geometry(Operator):
    """!
    Show geometry of Object as exported to FDS.
    """

    bl_label = "Show Geometry"
    bl_idname = "object.bf_show_fds_geometry"
    bl_description = "Show/Hide generated temporary geometry as exported to FDS"

    @classmethod
    def poll(cls, context):
        ob = context.object  # object or active_object? always object
        return ob and not ob.bf_is_tmp and not ob.bf_has_tmp

    def execute(self, context):
        # Init
        w = context.window_manager.windows[0]
        w.cursor_modal_set("WAIT")
        sc = context.scene
        ob = context.object

        # Export and import back as temporary geometry
        try:
            f90_namelists = ob.to_fds_list(context).to_string()
            sc.from_fds(
                context=context,
                f90_namelists=f90_namelists,
                set_tmp=True,
            )
        except BFException as err:
            utils.geometry.rm_tmp_objects()
            self.report({"ERROR"}, str(err))
            return {"CANCELLED"}
        else:
            utils.geometry.set_has_tmp(context=context, ob=ob)
            self.report({"INFO"}, "FDS geometry shown")
            return {"FINISHED"}
        finally:
            w.cursor_modal_restore()


class SCENE_OT_bf_hide_tmp_geometry(Operator):
    """!
    Hide all temporary geometry.
    """

    bl_label = "Hide Geometry"
    bl_idname = "scene.bf_hide_fds_geometry"
    bl_description = "Hide all generated temporary geometry"

    def execute(self, context):
        w = context.window_manager.windows[0]
        w.cursor_modal_set("WAIT")

        ob = context.object
        utils.geometry.rm_tmp_objects()
        try:
            context.view_layer.objects.active = ob
        except ReferenceError:
            try:
                context.view_layer.objects.active = context.selected_objects[0]
            except IndexError:
                pass

        w.cursor_modal_restore()
        self.report({"INFO"}, "Temporary geometry hidden")
        return {"FINISHED"}


bl_classes = [
    OBJECT_OT_bf_show_fds_geometry,
    SCENE_OT_bf_hide_tmp_geometry,
]


def register():
    from bpy.utils import register_class

    for c in bl_classes:
        register_class(c)


def unregister():
    from bpy.utils import unregister_class

    for c in reversed(bl_classes):
        unregister_class(c)
