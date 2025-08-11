# SPDX-License-Identifier: GPL-3.0-or-later

"""!
BFDS, Blender related extensions.
"""

from . import handlers, menus, operators, panels, preferences, ui_lists

ms_to_register = (
    handlers,
    menus,
    operators,
    panels,
    preferences,
    ui_lists,
)


def register():
    for m in ms_to_register:
        m.register()


def unregister():
    for m in ms_to_register:
        m.unregister()
