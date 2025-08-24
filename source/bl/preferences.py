# SPDX-License-Identifier: GPL-3.0-or-later

"""!
BFDS, preferences panel.
"""

import bpy
import logging
from bpy.types import AddonPreferences
from bpy.props import BoolProperty, StringProperty
from ..ui.simple import toggle_simple_ui
from .. import config

log = logging.getLogger(__name__)

# Get preference value like this:
# config.ADDON_PREFS.bf_pref_simplify_ui


def update_bf_pref_simplify_ui(_, context):
    toggle_simple_ui(context)


class BFPreferences(AddonPreferences):
    """!
    BFDS, preferences panel
    """

    bl_idname = config.ADDON_PACKAGE

    bf_pref_simplify_ui: BoolProperty(
        name="Simplify Blender UI",
        description="Simplify Blender user interface",
        default=True,
        update=update_bf_pref_simplify_ui,
    )

    bf_pref_fds_command: StringProperty(
        name="Run FDS",
        description="\n".join(
            (
                "Run FDS command:",
                " <{n}> is replaced by the number of MPI processes,",
                " <{t}> by the number of threads,",
                " <{f}> by the fds case filepath (eg. /example/case.fds),",
                " <{p}> by the fds case path (eg. /example/).",
            )
        ),
        default="",
    )

    bf_pref_smv_command: StringProperty(
        name="Open Smokeview",
        description="\n".join(
            (
                "Open Smokeview command:",
                " <{f}> is replaced by the smv filepath (eg. /example/case.smv),",
                " <{p}> by the fds case path (eg. /example/).",
            )
        ),
        default="",
    )

    def draw(self, context):
        """!
        Draw UI elements into the panel UI layout.
        @param context: the Blender context.
        @return Blender layout.
        """
        paths = context.preferences.filepaths
        layout = self.layout

        row = layout.row()
        row.operator("wm.bf_load_bfds_settings")
        if context.window_manager.get("bf_restart_required"):
            alert_row = row.row()
            alert_row.alert = True
            alert_row.operator("wm.quit_blender", text="Restart Blender", icon="ERROR")

        col = layout.column()
        col.prop(self, "bf_pref_simplify_ui")
        col.prop(paths, "use_load_ui", text="Load UI setup when loading .blend files")
        col.prop(
            paths,
            "use_relative_paths",
            text="Default to relative paths in the file selector",
        )

        box = layout.box()
        box.label(text="External Commands")

        row = box.row(align=True)
        row.prop(self, "bf_pref_fds_command", text="FDS")
        row.operator(
            "wm.bf_restore_default_commands", text="", icon="LOOP_BACK"
        ).bf_command = "FDS"

        row = box.row(align=True)
        row.prop(self, "bf_pref_smv_command", text="Smokeview")
        row.operator(
            "wm.bf_restore_default_commands", text="", icon="LOOP_BACK"
        ).bf_command = "Smokeview"

        return layout


def register():
    log.debug("Register preferences...")
    bpy.utils.register_class(BFPreferences)


def unregister():
    log.debug("Unregister preferences...")
    bpy.utils.unregister_class(BFPreferences)
