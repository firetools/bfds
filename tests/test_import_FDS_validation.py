# SPDX-License-Identifier: GPL-3.0-or-later

import bpy, pytest
import subprocess, os, pathlib, fnmatch

FDS_COMMAND = "fds"
FDS_CASES_PATHS = (
    "../firemodels/fds-master/Validation",
    "../firemodels/fds-master/firemodels/fds-master/Verification",
)
EXCLUDE_PATTERNS = (
    "*/Validation/BGC_GRI_LNG_Fires*",
    "*/Validation/NIST_Pool_Fires*",
    "*/Validation/FAA_Cargo_Compartments*",
    "*/Validation/Bluff_Body_Flows*",
    "*/Validation/Crown_Fires*",
    "*/Validation/MPI_Scaling_Tests*",
    "*/Validation/McCaffrey_Plume*",
    "*/Validation/Memorial_Tunnel*",
    "*/Validation/Montoir_LNG_Fires*",
    "*/Validation/NIST_Backdraft/FDS_Input_Files/fine_mesh.fds",
    "*/Validation/NIST_Backdraft/FDS_Input_Files/veryfine_mesh.fds",
    "*/Validation/NIST_NRC_Parallel_Panels*",
    "*/Validation/NRCC_Smoke_Tower*",
)


def _has_pattern(filename):
    for pattern in EXCLUDE_PATTERNS:
        if fnmatch.fnmatch(filename, pattern):
            return True
    return False


def get_fds_filepath():
    for fds_cases_path in FDS_CASES_PATHS:
        fds_cases_path = os.path.abspath(fds_cases_path)
        for dirpath, dirnames, filenames in os.walk(fds_cases_path):
            print("dirpath:", dirpath)
            if _has_pattern(dirpath):
                continue
            for filename in filenames:
                print("filename:", filename)
                if _has_pattern(filename):
                    continue
                if filename.endswith(".fds"):
                    yield os.path.join(dirpath, filename)


# def get_fds_filepath():
#     yield "/var/home/egissi/.local/opt/FDS/FDS6/Examples/Pressure_Solver/stairwell.fds"


@pytest.mark.parametrize("fds_filepath", get_fds_filepath())
def test_run_fds_case(tmp_path, fds_filepath):
    # Open the empty blend file and save it in tmp
    empty_blend_filepath = (
        f"{bpy.utils.user_resource('EXTENSIONS')}/user_default/bfds/empty.blend"
    )
    bpy.ops.wm.open_mainfile(filepath=empty_blend_filepath)
    # Import the fds case
    bpy.ops.import_to_scene.fds(filepath=fds_filepath)
    # Set TIME T_END to T_BEGIN, only setup is performed
    sc = bpy.context.scene
    sc.bf_time_t_end = sc.bf_time_t_begin
    # Save tmp blend file
    blend_filepath = f"{tmp_path}/test.blend"
    bpy.ops.wm.save_as_mainfile(filepath=blend_filepath)
    # Export the fds case
    new_fds_filepath = f"{tmp_path}/test.fds"
    bpy.ops.export_scene.fds(filepath=new_fds_filepath)
    # Run FDS case
    res = subprocess.run(
        [FDS_COMMAND, new_fds_filepath], cwd=tmp_path, capture_output=True, text=True
    )
    output = res.stdout + res.stderr
    assert "STOP: Set-up only" in output
