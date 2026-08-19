# SPDX-License-Identifier: GPL-3.0-or-later

import bpy, pytest


def test_blender_version():
    assert bpy.app.version >= (5, 2, 0)


def test_ops_wm_bf_load_bfds_settings():
    try:
        bpy.ops.wm.bf_load_bfds_settings()
    except:
        pytest.fail("Loding BFDS default setting failed.")


def test_ops_preferences_addon_enable():
    try:
        bpy.ops.preferences.addon_disable(module="bl_ext.user_default.bfds")
        bpy.ops.preferences.addon_enable(module="bl_ext.user_default.bfds")
    except:
        pytest.fail("Disabling/enabling BFDS module failed.")


def test_simplified_ui_replacements():
    from bl_ext.user_default.bfds import config
    from bl_ext.user_default.bfds.ui.simple import toggle_simple_ui
    from bl_ext.user_default.bfds.ui.replace.space_view3d import VIEW3D_HT_header

    prefs = bpy.context.preferences.addons[config.ADDON_PACKAGE].preferences
    prefs.bf_pref_simplify_ui = True
    toggle_simple_ui()

    assert bpy.types.VIEW3D_HT_header.__module__.endswith(
        "bfds.ui.replace.space_view3d"
    )
    assert bpy.types.TOPBAR_MT_editor_menus.__module__.endswith(
        "bfds.ui.replace.space_topbar"
    )
    assert VIEW3D_HT_header._mesh_paint_automasking_icon(
        bpy.context.scene.tool_settings.sculpt
    ) in {"CLIPUV_DEHLT", "CLIPUV_HLT"}
