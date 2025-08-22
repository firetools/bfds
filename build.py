#! /usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later

BLENDER = "../blender-4.5.0-linux-x64/blender"
SOURCE_DIR = "./source"
OUTPUT_DIR = "."
CWD_PATH = "."

import subprocess

# blender --command extension build --source-dir SOURCE_DIR
#                                   [--output-dir OUTPUT_DIR]
#                                   [--output-filepath OUTPUT_FILEPATH]
#                                   [--valid-tags VALID_TAGS_JSON]
#                                   [--split-platforms] [--verbose]


command = [
    BLENDER,
    "--command",
    "extension",
    "build",
    "--source-dir",
    SOURCE_DIR,
    "--output-dir",
    OUTPUT_DIR,
    "--verbose",
]

print("Build...")
res = subprocess.run(command, cwd=CWD_PATH, capture_output=True, text=True)
output = res.stdout + res.stderr
print(output)
