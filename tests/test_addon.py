# SPDX-License-Identifier: GPL-3.0-or-later

import bpy, pytest


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
