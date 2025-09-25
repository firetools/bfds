# SPDX-License-Identifier: GPL-3.0-or-later

"""!
BFDS, operators to check GEOM sanity and intersections.
"""

import logging
from bpy.types import Operator
from ...types import BFException
from ... import lang

log = logging.getLogger(__name__)


class OBJECT_OT_bf_check_intersections(Operator):
    """!
    Check self-intersections or intersections of the active object with other selected objects.
    """

    bl_label = "Check Intersections"
    bl_idname = "object.bf_geom_check_intersections"
    bl_description = (
        "Check self-intersections or intersections with other selected objects"
    )

    @classmethod
    def poll(cls, context):
        return context.object

    def execute(self, context):
        w = context.window_manager.windows[0]
        w.cursor_modal_set("WAIT")
        ob = context.object
        obs = context.selected_objects
        if obs:
            obs.remove(ob)
        try:
            lang.ON_GEOM.check_intersections(
                context, ob, obs, protect=ob.data.bf_geom_protect
            )
        except BFException as err:
            self.report({"ERROR"}, f"Check intersections: {err}")
            return {"CANCELLED"}
        else:
            self.report({"INFO"}, "No intersection detected")
            return {"FINISHED"}
        finally:
            w.cursor_modal_restore()


class OBJECT_OT_bf_check_sanity(Operator):
    """!
    Check if the active object is a closed orientable 2-manifold, with no degenerate geometry.
    """

    bl_label = "Check Sanity"
    bl_idname = "object.bf_geom_check_sanity"
    bl_description = "Check if the active object is a closed orientable 2-manifold, with no degenerate geometry"

    @classmethod
    def poll(cls, context):
        return context.object

    def execute(self, context):
        w = context.window_manager.windows[0]
        w.cursor_modal_set("WAIT")
        ob = context.object
        try:
            lang.ON_GEOM.check_geom_sanity(
                context,
                ob,
                protect=ob.data.bf_geom_protect,
                is_open=ob.data.bf_geom_is_terrain,
            )
        except BFException as err:
            self.report({"ERROR"}, f"Check sanity: {err}")
            return {"CANCELLED"}
        else:
            self.report({"INFO"}, "Geometry sanity ok")
            return {"FINISHED"}
        finally:
            w.cursor_modal_restore()


bl_classes = [OBJECT_OT_bf_check_intersections, OBJECT_OT_bf_check_sanity]


def register():
    from bpy.utils import register_class

    for c in bl_classes:
        register_class(c)


def unregister():
    from bpy.utils import unregister_class

    for c in reversed(bl_classes):
        unregister_class(c)
