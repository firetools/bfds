# SPDX-License-Identifier: GPL-3.0-or-later

# BFDS, an open tool for the NIST Fire Dynamics Simulator
# Copyright (C) 2013  Emanuele Gissi
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import logging

# Reading class definitions,
# bl should be imported before lang,
# because it imports ui_lists
from . import bl, lang, ui

logging.basicConfig(level=logging.INFO)  # INFO or DEBUG
log = logging.getLogger(__name__)


# Automatic registering/deregistering
# of Blender entities
def register():
    log.info("Register BFDS...")
    bl.register()
    lang.register()
    ui.register()


def unregister():
    log.info("Unregister BFDS...")
    ui.unregister()
    lang.unregister()
    bl.unregister()
