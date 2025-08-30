# SPDX-License-Identifier: GPL-3.0-or-later

"""!
BFDS, operators to load default settings.
"""

import bpy, logging
from bpy.types import Operator

from ... import config

log = logging.getLogger(__name__)


class WM_OT_bf_load_bfds_settings(Operator):
    """!
    Load default BFDS settings, deleting current data.
    """

    bl_label = "Load Default BFDS Settings"
    bl_idname = "wm.bf_load_bfds_settings"
    bl_description = "Load default BFDS settings, deleting current data!"

    def invoke(self, context, event):
        # Ask for confirmation
        wm = context.window_manager
        return wm.invoke_confirm(self, event)

    def execute(self, context):
        # Set default startup.blend
        filepath = config.ADDON_STARTUP_FILEPATH
        bpy.ops.wm.open_mainfile(filepath=filepath, load_ui=True, use_scripts=True)
        bpy.ops.wm.save_homefile()
        # Load default commands
        bpy.ops.wm.bf_restore_default_commands()
        # Set simplified UI
        bf_prefs = context.preferences.addons[config.ADDON_PACKAGE].preferences
        bf_prefs.bf_pref_simplify_ui = True
        # Save user preferences
        bpy.ops.wm.save_userpref()
        # Open new file (unlink startup)
        bpy.ops.wm.read_homefile()
        # Report
        self.report({"INFO"}, "Default settings loaded")
        return {"FINISHED"}


bl_classes = [
    WM_OT_bf_load_bfds_settings,
]


def register():
    from bpy.utils import register_class

    for c in bl_classes:
        register_class(c)


def unregister():
    from bpy.utils import unregister_class

    for c in reversed(bl_classes):
        unregister_class(c)
