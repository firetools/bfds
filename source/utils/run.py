# SPDX-License-Identifier: GPL-3.0-or-later

"""!
BFDS, run external commands utilities.
"""

import os, sys, shutil, logging
from .. import config

log = logging.getLogger(__name__)


def run_in_terminal(cmd, title="Run"):
    """Run"""
    platform = sys.platform
    term_cmd = None
    if platform == "linux":
        # find an available terminal emulator command
        for t in config.LINUX_TERM_COMMAND:
            if shutil.which(t.split()[0]):
                term_cmd = t
                # Append the available shell command
                shell = os.environ.get("SHELL", "sh")
                term_cmd = term_cmd.replace("{cmd}", f"""{shell} -c "{{cmd}}" """)
                break
    elif platform == "darwin":
        # always available
        term_cmd = """osascript -e 'tell app "Terminal" to do script "{cmd}" ' """
    elif platform == "win32":
        # always available
        term_cmd = """START "{title}" cmd /c "{cmd}" """
    else:
        raise Exception(f"Unsupported platform: {platform}")
    if not term_cmd:
        raise Exception("Terminal emulator not found, open a BFDS issue")
    # Set title and command
    term_cmd = term_cmd.format(cmd=cmd, title=title)
    # Run command in terminal
    log.info(f"Run in terminal:\n<{term_cmd}>")
    res = os.system(term_cmd)
    if not res == 0:
        raise Exception(f"Error while running:\n<{term_cmd}>")
