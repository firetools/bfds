# SPDX-FileCopyrightText: 2009-2023 Blender Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

from bpy.types import Menu


class TOPBAR_MT_editor_menus(Menu):
    bl_idname = "TOPBAR_MT_editor_menus"
    bl_label = ""

    def draw(self, context):
        layout = self.layout

        # Allow calling this menu directly (this might not be a header area).
        if getattr(context.area, "show_menus", False):
            layout.menu("TOPBAR_MT_blender", text="", icon="BLENDER")
        else:
            layout.menu("TOPBAR_MT_blender", text="Blender")

        layout.menu("TOPBAR_MT_file")
        layout.menu("TOPBAR_MT_edit")

        # layout.menu("TOPBAR_MT_render")

        layout.menu("TOPBAR_MT_window")
        layout.menu("TOPBAR_MT_help")
