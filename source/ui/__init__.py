# SPDX-License-Identifier: GPL-3.0-or-later

"""!
BFDS, simplification of Blender interface.
"""

from . import simple

ms_to_register = (simple,)


def register():
    for m in ms_to_register:
        m.register()


def unregister():
    for m in ms_to_register:
        m.unregister()
