# SPDX-License-Identifier: GPL-3.0-or-later

import bpy

# Howto
# Get path of current test file:
# import pathlib
# path = pathlib.Path(__file__).parent.resolve()
# Open blend file:
# bpy.ops.wm.open_mainfile(filepath=f"{path}/MESH.blend")


def _create_ob():
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(5.0, 6.0, 7.0))
    ob = bpy.context.object
    ob.name = "Test"
    ob.bf_namelist_cls = "ON_MESH"
    ob.bf_fyi = "Fyi"
    ob.bf_mesh_ijk = 11, 12, 14
    return ob


def _remove_ob(ob):
    bpy.data.objects.remove(ob, do_unlink=True)


def test_simple():
    ob = _create_ob()
    res = ob.to_fds_list(bpy.context).to_string()
    fds_string = """
Cell Qty: 1848 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test' FYI='Fyi' IJK=11,12,14 XB=4.500,5.500,5.500,6.500,6.500,7.500 /
"""
    _remove_ob(ob)
    assert res == fds_string[1:-1]


def test_split_x():
    ob = _create_ob()
    ob.bf_mesh_nsplits = 2, 1, 1
    ob.bf_mesh_nsplits_export = True
    res = ob.to_fds_list(bpy.context).to_string()
    fds_string = """
Cell Qty: 1008 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_s0' IJK=6,12,14 XB=4.500,5.045,5.500,6.500,6.500,7.500 FYI='Fyi' /
Cell Qty: 840 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_s1' IJK=5,12,14 XB=5.045,5.500,5.500,6.500,6.500,7.500 FYI='Fyi' /
"""
    _remove_ob(ob)
    assert res == fds_string[1:-1]


def test_split_y():
    ob = _create_ob()
    ob.bf_mesh_nsplits = 1, 3, 1
    ob.bf_mesh_nsplits_export = True
    res = ob.to_fds_list(bpy.context).to_string()
    fds_string = """
Cell Qty: 616 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_s0' IJK=11,4,14 XB=4.500,5.500,5.500,5.833,6.500,7.500 FYI='Fyi' /
Cell Qty: 616 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_s1' IJK=11,4,14 XB=4.500,5.500,5.833,6.167,6.500,7.500 FYI='Fyi' /
Cell Qty: 616 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_s2' IJK=11,4,14 XB=4.500,5.500,6.167,6.500,6.500,7.500 FYI='Fyi' /
"""
    _remove_ob(ob)
    assert res == fds_string[1:-1]


def test_split_z():
    ob = _create_ob()
    ob.bf_mesh_nsplits = 1, 1, 3
    ob.bf_mesh_nsplits_export = True
    res = ob.to_fds_list(bpy.context).to_string()
    fds_string = """
Cell Qty: 660 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_s0' IJK=11,12,5 XB=4.500,5.500,5.500,6.500,6.500,6.857 FYI='Fyi' /
Cell Qty: 660 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_s1' IJK=11,12,5 XB=4.500,5.500,5.500,6.500,6.857,7.214 FYI='Fyi' /
Cell Qty: 528 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_s2' IJK=11,12,4 XB=4.500,5.500,5.500,6.500,7.214,7.500 FYI='Fyi' /
"""
    _remove_ob(ob)
    assert res == fds_string[1:-1]


def test_split_xyz():
    ob = _create_ob()
    ob.bf_mesh_nsplits = 1, 3, 2
    ob.bf_mesh_nsplits_export = True
    res = ob.to_fds_list(bpy.context).to_string()
    fds_string = """
Cell Qty: 308 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_s0' IJK=11,4,7 XB=4.500,5.500,5.500,5.833,6.500,7.000 FYI='Fyi' /
Cell Qty: 308 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_s1' IJK=11,4,7 XB=4.500,5.500,5.500,5.833,7.000,7.500 FYI='Fyi' /
Cell Qty: 308 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_s2' IJK=11,4,7 XB=4.500,5.500,5.833,6.167,6.500,7.000 FYI='Fyi' /
Cell Qty: 308 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_s3' IJK=11,4,7 XB=4.500,5.500,5.833,6.167,7.000,7.500 FYI='Fyi' /
Cell Qty: 308 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_s4' IJK=11,4,7 XB=4.500,5.500,6.167,6.500,6.500,7.000 FYI='Fyi' /
Cell Qty: 308 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_s5' IJK=11,4,7 XB=4.500,5.500,6.167,6.500,7.000,7.500 FYI='Fyi' /
"""
    _remove_ob(ob)
    assert res == fds_string[1:-1]


def test_MULT_dx_dx0():
    ob = _create_ob()
    ob.bf_mult_export = True
    ob.bf_mult_dx = 3.0
    ob.bf_mult_dx0 = 1.0
    ob.bf_mult_i_lower = 1
    ob.bf_mult_i_upper = 3
    res = ob.to_fds_list(bpy.context).to_string()
    fds_string = """
Cell Qty: 1848 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_i1_j0_k0' IJK=11,12,14 XB=8.500,9.500,5.500,6.500,6.500,7.500
      FYI='Fyi' /
Cell Qty: 1848 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_i2_j0_k0' IJK=11,12,14 XB=11.500,12.500,5.500,6.500,6.500,7.500
      FYI='Fyi' /
Cell Qty: 1848 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_i3_j0_k0' IJK=11,12,14 XB=14.500,15.500,5.500,6.500,6.500,7.500
      FYI='Fyi' /
"""
    _remove_ob(ob)
    assert res == fds_string[1:-1]


def test_MULT_dy_dy0():
    ob = _create_ob()
    ob.bf_mult_export = True
    ob.bf_mult_dy = 3.0
    ob.bf_mult_dy0 = 1.0
    ob.bf_mult_j_lower = 1
    ob.bf_mult_j_lower_skip = 3
    ob.bf_mult_j_upper_skip = 5
    ob.bf_mult_j_upper = 7
    res = ob.to_fds_list(bpy.context).to_string()
    fds_string = """
Cell Qty: 1848 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_i0_j1_k0' IJK=11,12,14 XB=4.500,5.500,9.500,10.500,6.500,7.500
      FYI='Fyi' /
Cell Qty: 1848 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_i0_j2_k0' IJK=11,12,14 XB=4.500,5.500,12.500,13.500,6.500,7.500
      FYI='Fyi' /
Cell Qty: 1848 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_i0_j6_k0' IJK=11,12,14 XB=4.500,5.500,24.500,25.500,6.500,7.500
      FYI='Fyi' /
Cell Qty: 1848 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_i0_j7_k0' IJK=11,12,14 XB=4.500,5.500,27.500,28.500,6.500,7.500
      FYI='Fyi' /
"""
    _remove_ob(ob)
    assert res == fds_string[1:-1]


def test_MULT_dz_dz0():
    ob = _create_ob()
    ob.bf_mult_export = True
    ob.bf_mult_dz = 3.0
    ob.bf_mult_dz0 = 1.0
    ob.bf_mult_k_lower = 1
    ob.bf_mult_k_lower_skip = 3
    ob.bf_mult_k_upper_skip = 5
    ob.bf_mult_k_upper = 7
    res = ob.to_fds_list(bpy.context).to_string()
    fds_string = """
Cell Qty: 1848 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_i0_j0_k1' IJK=11,12,14 XB=4.500,5.500,5.500,6.500,10.500,11.500
      FYI='Fyi' /
Cell Qty: 1848 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_i0_j0_k2' IJK=11,12,14 XB=4.500,5.500,5.500,6.500,13.500,14.500
      FYI='Fyi' /
Cell Qty: 1848 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_i0_j0_k6' IJK=11,12,14 XB=4.500,5.500,5.500,6.500,25.500,26.500
      FYI='Fyi' /
Cell Qty: 1848 | Size: 0.091·0.083·0.071m | Aspect: 1.3 | Poisson: No
&MESH ID='Test_i0_j0_k7' IJK=11,12,14 XB=4.500,5.500,5.500,6.500,28.500,29.500
      FYI='Fyi' /
"""
    _remove_ob(ob)
    assert res == fds_string[1:-1]


def test_import():
    import_fds_string = """
&MESH ID='Test' IJK=24,24,24, XB=-0.12,-0.06,-0.12,-0.06,-0.12,-0.06, MULT_ID='mesh' /
&MULT ID='mesh', DX=0.06, DY=0.06, DZ=0.06, I_UPPER=1, J_UPPER=1, K_UPPER=1 /
"""
    context = bpy.context
    scene = context.scene
    scene.from_fds(context, f90_namelists=import_fds_string)
    ob = bpy.data.objects["Test"]
    res = ob.to_fds_list(bpy.context).to_string()
    fds_string = """
Cell Qty: 13824 | Size: 0.002·0.002·0.002m | Aspect: 1.0 | Poisson: Yes
&MESH ID='Test_i0_j0_k0' IJK=24,24,24
      XB=-0.120,-0.060,-0.120,-0.060,-0.120,-0.060 /
Cell Qty: 13824 | Size: 0.002·0.002·0.002m | Aspect: 1.0 | Poisson: Yes
&MESH ID='Test_i0_j0_k1' IJK=24,24,24
      XB=-0.120,-0.060,-0.120,-0.060,-0.060,0.000 /
Cell Qty: 13824 | Size: 0.002·0.002·0.002m | Aspect: 1.0 | Poisson: Yes
&MESH ID='Test_i0_j1_k0' IJK=24,24,24
      XB=-0.120,-0.060,-0.060,0.000,-0.120,-0.060 /
Cell Qty: 13824 | Size: 0.002·0.002·0.002m | Aspect: 1.0 | Poisson: Yes
&MESH ID='Test_i0_j1_k1' IJK=24,24,24 XB=-0.120,-0.060,-0.060,0.000,-0.060,0.000 /
Cell Qty: 13824 | Size: 0.002·0.002·0.002m | Aspect: 1.0 | Poisson: Yes
&MESH ID='Test_i1_j0_k0' IJK=24,24,24
      XB=-0.060,0.000,-0.120,-0.060,-0.120,-0.060 /
Cell Qty: 13824 | Size: 0.002·0.002·0.002m | Aspect: 1.0 | Poisson: Yes
&MESH ID='Test_i1_j0_k1' IJK=24,24,24 XB=-0.060,0.000,-0.120,-0.060,-0.060,0.000 /
Cell Qty: 13824 | Size: 0.002·0.002·0.002m | Aspect: 1.0 | Poisson: Yes
&MESH ID='Test_i1_j1_k0' IJK=24,24,24 XB=-0.060,0.000,-0.060,0.000,-0.120,-0.060 /
Cell Qty: 13824 | Size: 0.002·0.002·0.002m | Aspect: 1.0 | Poisson: Yes
&MESH ID='Test_i1_j1_k1' IJK=24,24,24 XB=-0.060,0.000,-0.060,0.000,-0.060,0.000 /
"""
    _remove_ob(ob)
    assert res == fds_string[1:-1]


def test_bf_set_suggested_mesh_cell_size():
    ob = _create_ob()
    bpy.ops.object.bf_set_suggested_mesh_cell_size(
        bf_max_hrr=2000,
        bf_ncell=8,
        bf_poisson_restriction=True,
        bf_density=1.204,
        bf_cp=1.005,
        bf_t=25.0,
        bf_g=9.81,
    )
    # -- Suggested cell size calculation
    # According to the NUREG 1824, US NRC (2007), given the max HRR: 2000.0 kW,
    # density: 1.204 kg/m³, Cp: 1.005 KJ/(kg·K), temperature: 25.0°C, gravity: 9.81 m/s²,
    # then the characteristic fire diameter D* is calculated as: 1.257 m
    # and the cell size range for D*/dx ratio between 4 and 16 is: 0.079 ÷ 0.314 m
    res = ob.to_fds_list(bpy.context).to_string()
    fds_string = """
Cell Qty: 216 | Size: 0.167·0.167·0.167m | Aspect: 1.0 | Poisson: Yes
&MESH ID='Test' FYI='Fyi' IJK=6,6,6 XB=4.500,5.500,5.500,6.500,6.500,7.500 /
"""
    _remove_ob(ob)
    assert res == fds_string[1:-1]


def test_bf_set_mesh_cell_size():
    ob = _create_ob()
    bpy.ops.object.bf_set_mesh_cell_size(
        bf_cell_sizes=(0.07, 0.07, 0.07),
        bf_poisson_restriction=False,
    )
    res = ob.to_fds_list(bpy.context).to_string()
    fds_string = """
Cell Qty: 2744 | Size: 0.071·0.071·0.071m | Aspect: 1.0 | Poisson: No
&MESH ID='Test' FYI='Fyi' IJK=14,14,14 XB=4.500,5.500,5.500,6.500,6.500,7.500 /
"""
    _remove_ob(ob)
    assert res == fds_string[1:-1]


def test_bf_set_mesh_cell_size_w_Poisson():
    ob = _create_ob()
    bpy.ops.object.bf_set_mesh_cell_size(
        bf_cell_sizes=(0.07, 0.07, 0.07),
        bf_poisson_restriction=True,
    )
    res = ob.to_fds_list(bpy.context).to_string()
    fds_string = """
Cell Qty: 3150 | Size: 0.071·0.067·0.067m | Aspect: 1.1 | Poisson: Yes
&MESH ID='Test' FYI='Fyi' IJK=14,15,15 XB=4.500,5.500,5.500,6.500,6.500,7.500 /
"""
    _remove_ob(ob)
    assert res == fds_string[1:-1]


def test_bf_align_to_mesh():  # test operator  # FIXME
    pass


def test_align_meshes():
    from bl_ext.user_default.bfds.lang.ON_MESH import align_meshes

    # reference mesh: rijk, rxb
    # treated mesh: mijk, mxb
    rijk, rxb, mijk, mxb, msg = align_meshes(
        rijk=[10, 10, 10],
        rxb=[0.0, 5.0, 0.0, 5.0, 0.0, 5.0],
        # meshing difference
        mijk=[9, 11, 10],
        # little gap along z and displacement along x and y
        mxb=[0.1, 5.2, 0.1, 5.2, 5.1, 10.0],
        poisson=True,
        protect_rxb=True,
    )
    assert rijk == [10, 10, 10]
    assert rxb == [0.0, 5.0, 0.0, 5.0, 0.0, 5.0]
    assert mijk == [10, 10, 10]
    assert mxb == [0.0, 5.0, 0.0, 5.0, 5.0, 10.0]
    assert msg == ""

    # reference mesh: rijk, rxb
    # treated mesh: mijk, mxb
    rijk, rxb, mijk, mxb, msg = align_meshes(
        rijk=[15, 37, 51],
        rxb=[0.0, 5.0, 0.0, 5.0, 0.0, 5.0],
        mijk=[9, 38, 20],
        mxb=[0.1, 5.2, 0.1, 5.2, 5.1, 10.0],
        poisson=True,
        protect_rxb=False,
    )
    assert rijk == [16, 40, 51]
    assert rxb == [0.0, 5.333333333333333, 0.0, 5.405405405405405, 0.0, 5.0]
    assert mijk == [8, 40, 20]
    assert mxb == [
        0.0,
        5.333333333333333,
        0.13513513513513514,
        5.54054054054054,
        5.0,
        10.0,
    ]
    assert msg == "increased ref size along x axis, increased ref size along y axis"


def test_calc_meshes():
    from bl_ext.user_default.bfds.lang.ON_MESH import calc_meshes

    assert tuple(calc_meshes.get_factor(142)) == (1, 2, 71)
    assert calc_meshes.get_n_for_poisson(28) == 30
    assert calc_meshes.get_poisson_ijk((11, 11, 13)) == (11, 12, 15)
    assert calc_meshes.get_cell_aspect(cell_sizes=(0.50, 0.75, 1.00)) == 2.0

    ob = _create_ob()
    res = calc_meshes.get_ijk_from_desired_cs(
        context=bpy.context, ob=ob, desired_cs=(0.079, 0.079, 0.079), poisson=True
    )
    _remove_ob(ob)
    assert res == (13, 15, 15)

    ob = _create_ob()
    res = calc_meshes.get_cell_sizes(context=bpy.context, ob=ob)
    _remove_ob(ob)
    assert res == (0.09090909090909091, 0.08333333333333333, 0.07142857142857142)

    ob = _create_ob()
    res = calc_meshes.get_mesh_geometry(context=bpy.context, ob=ob)
    _remove_ob(ob)
    assert res == (
        ("Test",),  # hids
        [(11, 12, 14)],  # ijks
        [(4.5, 5.5, 5.5, 6.5, 6.5, 7.5)],  # xbs
        1,  # nmesh
        1,  # nsplit
        1,  # nmult
        1848,  # ncell_tot
        1848,  # ncell
        (0.09090909090909091, 0.08333333333333333, 0.07142857142857142),  # cs
        1.272727272727273,  # aspect
        "No",  # has_good_ijk
    )


def test_split_mesh():
    from bl_ext.user_default.bfds.lang.ON_MESH import split_mesh

    assert split_mesh.split_cells(ncell=10, nsplit=3) == [4, 3, 3]  # ncells

    assert split_mesh.split_mesh(
        hid="T", ijk=(10, 20, 30), export=True, nsplits=(2, 2, 2), xb=(0, 1, 0, 1, 0, 1)
    ) == (
        ("T_s0", "T_s1", "T_s2", "T_s3", "T_s4", "T_s5", "T_s6", "T_s7"),  # hids
        [  # ijks
            (5, 10, 15),
            (5, 10, 15),
            (5, 10, 15),
            (5, 10, 15),
            (5, 10, 15),
            (5, 10, 15),
            (5, 10, 15),
            (5, 10, 15),
        ],
        [  # xbs
            (0.0, 0.5, 0.0, 0.5, 0.0, 0.5),
            (0.0, 0.5, 0.0, 0.5, 0.5, 1.0),
            (0.0, 0.5, 0.5, 1.0, 0.0, 0.5),
            (0.0, 0.5, 0.5, 1.0, 0.5, 1.0),
            (0.5, 1.0, 0.0, 0.5, 0.0, 0.5),
            (0.5, 1.0, 0.0, 0.5, 0.5, 1.0),
            (0.5, 1.0, 0.5, 1.0, 0.0, 0.5),
            (0.5, 1.0, 0.5, 1.0, 0.5, 1.0),
        ],
        750,  # ncell
        (0.1, 0.05, 0.03333333333333333),  # cs
        8,  # nsplit
    )
