import bpy

# Howto
# Get path of current test file:
# import pathlib
# path = pathlib.Path(__file__).parent.resolve()
# Open blend file:
# bpy.ops.wm.open_mainfile(filepath=f"{path}/MESH.blend")


def _create_mesh_ob(name):
    bpy.ops.mesh.primitive_cube_add(size=3.0, location=(5.0, 6.0, 7.0))
    ob = bpy.context.object
    ob.name = name
    ob.bf_namelist_cls = "ON_MESH"
    ob.bf_fyi = "Test info"
    ob.bf_mesh_ijk = 11, 12, 14
    return ob


def test_simple_MESH():
    ob = _create_mesh_ob("test_simple_MESH")
    fds_string = """
Cell Qty: 1848 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_simple_MESH' FYI='Test info' IJK=11,12,14
      XB=3.500,6.500,4.500,7.500,5.500,8.500 /
"""
    assert ob.to_fds_list(bpy.context).to_string() == fds_string[1:-1]


def test_MESH_split_x():
    ob = _create_mesh_ob("test_MESH_split_x")
    ob.bf_mesh_nsplits = 2, 1, 1
    ob.bf_mesh_nsplits_export = True
    fds_string = ob.to_fds_list(bpy.context).to_string()
    expected_fds_string = """
Cell Qty: 1008 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_split_x_s0' IJK=6,12,14
      XB=3.500,5.136,4.500,7.500,5.500,8.500 FYI='Test info' /
Cell Qty: 840 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_split_x_s1' IJK=5,12,14
      XB=5.136,6.500,4.500,7.500,5.500,8.500 FYI='Test info' /
"""
    assert fds_string == expected_fds_string[1:-1]


def test_MESH_split_y():
    ob = _create_mesh_ob("test_MESH_split_y")
    ob.bf_mesh_nsplits = 1, 3, 1
    ob.bf_mesh_nsplits_export = True
    fds_string = ob.to_fds_list(bpy.context).to_string()
    expected_fds_string = """
Cell Qty: 616 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_split_y_s0' IJK=11,4,14
      XB=3.500,6.500,4.500,5.500,5.500,8.500 FYI='Test info' /
Cell Qty: 616 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_split_y_s1' IJK=11,4,14
      XB=3.500,6.500,5.500,6.500,5.500,8.500 FYI='Test info' /
Cell Qty: 616 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_split_y_s2' IJK=11,4,14
      XB=3.500,6.500,6.500,7.500,5.500,8.500 FYI='Test info' /
"""
    assert fds_string == expected_fds_string[1:-1]


def test_MESH_split_z():
    ob = _create_mesh_ob("test_MESH_split_z")
    ob.bf_mesh_nsplits = 1, 1, 4
    ob.bf_mesh_nsplits_export = True
    fds_string = ob.to_fds_list(bpy.context).to_string()
    expected_fds_string = """
Cell Qty: 528 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_split_z_s0' IJK=11,12,4
      XB=3.500,6.500,4.500,7.500,5.500,6.357 FYI='Test info' /
Cell Qty: 528 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_split_z_s1' IJK=11,12,4
      XB=3.500,6.500,4.500,7.500,6.357,7.214 FYI='Test info' /
Cell Qty: 396 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_split_z_s2' IJK=11,12,3
      XB=3.500,6.500,4.500,7.500,7.214,7.857 FYI='Test info' /
Cell Qty: 396 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_split_z_s3' IJK=11,12,3
      XB=3.500,6.500,4.500,7.500,7.857,8.500 FYI='Test info' /
"""
    assert fds_string == expected_fds_string[1:-1]


def test_MESH_split_xyz():
    ob = _create_mesh_ob("test_MESH_split_xyz")
    ob.bf_mesh_nsplits = 2, 3, 2
    ob.bf_mesh_nsplits_export = True
    fds_string = ob.to_fds_list(bpy.context).to_string()
    expected_fds_string = """
Cell Qty: 168 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_split_xyz_s0' IJK=6,4,7
      XB=3.500,5.136,4.500,5.500,5.500,7.000 FYI='Test info' /
Cell Qty: 168 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_split_xyz_s1' IJK=6,4,7
      XB=3.500,5.136,4.500,5.500,7.000,8.500 FYI='Test info' /
Cell Qty: 168 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_split_xyz_s2' IJK=6,4,7
      XB=3.500,5.136,5.500,6.500,5.500,7.000 FYI='Test info' /
Cell Qty: 168 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_split_xyz_s3' IJK=6,4,7
      XB=3.500,5.136,5.500,6.500,7.000,8.500 FYI='Test info' /
Cell Qty: 168 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_split_xyz_s4' IJK=6,4,7
      XB=3.500,5.136,6.500,7.500,5.500,7.000 FYI='Test info' /
Cell Qty: 168 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_split_xyz_s5' IJK=6,4,7
      XB=3.500,5.136,6.500,7.500,7.000,8.500 FYI='Test info' /
Cell Qty: 140 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_split_xyz_s6' IJK=5,4,7
      XB=5.136,6.500,4.500,5.500,5.500,7.000 FYI='Test info' /
Cell Qty: 140 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_split_xyz_s7' IJK=5,4,7
      XB=5.136,6.500,4.500,5.500,7.000,8.500 FYI='Test info' /
Cell Qty: 140 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_split_xyz_s8' IJK=5,4,7
      XB=5.136,6.500,5.500,6.500,5.500,7.000 FYI='Test info' /
Cell Qty: 140 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_split_xyz_s9' IJK=5,4,7
      XB=5.136,6.500,5.500,6.500,7.000,8.500 FYI='Test info' /
Cell Qty: 140 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_split_xyz_s10' IJK=5,4,7
      XB=5.136,6.500,6.500,7.500,5.500,7.000 FYI='Test info' /
Cell Qty: 140 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_split_xyz_s11' IJK=5,4,7
      XB=5.136,6.500,6.500,7.500,7.000,8.500 FYI='Test info' /
"""
    assert fds_string == expected_fds_string[1:-1]


def test_MESH_MULT_dx():
    ob = _create_mesh_ob("test_MESH_MULT_dx")
    ob.bf_mult_export = True
    ob.bf_mult_dx = 3.0
    ob.bf_mult_i_upper = 3
    fds_string = ob.to_fds_list(bpy.context).to_string()
    expected_fds_string = """
Cell Qty: 1848 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_MULT_dx_i0_j0_k0' IJK=11,12,14
      XB=3.500,6.500,4.500,7.500,5.500,8.500 FYI='Test info' /
Cell Qty: 1848 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_MULT_dx_i1_j0_k0' IJK=11,12,14
      XB=6.500,9.500,4.500,7.500,5.500,8.500 FYI='Test info' /
Cell Qty: 1848 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_MULT_dx_i2_j0_k0' IJK=11,12,14
      XB=9.500,12.500,4.500,7.500,5.500,8.500 FYI='Test info' /
Cell Qty: 1848 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_MULT_dx_i3_j0_k0' IJK=11,12,14
      XB=12.500,15.500,4.500,7.500,5.500,8.500 FYI='Test info' /
"""
    assert fds_string == expected_fds_string[1:-1]


def test_MESH_MULT_dx_dx0():
    ob = _create_mesh_ob("test_MESH_MULT_dx_dx0")
    ob.bf_mult_export = True
    ob.bf_mult_dx = 3.0
    ob.bf_mult_dx0 = 1.0
    ob.bf_mult_i_lower = 1
    ob.bf_mult_i_upper = 3
    fds_string = ob.to_fds_list(bpy.context).to_string()
    expected_fds_string = """
Cell Qty: 1848 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_MULT_dx_dx0_i1_j0_k0' IJK=11,12,14
      XB=7.500,10.500,4.500,7.500,5.500,8.500 FYI='Test info' /
Cell Qty: 1848 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_MULT_dx_dx0_i2_j0_k0' IJK=11,12,14
      XB=10.500,13.500,4.500,7.500,5.500,8.500 FYI='Test info' /
Cell Qty: 1848 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_MULT_dx_dx0_i3_j0_k0' IJK=11,12,14
      XB=13.500,16.500,4.500,7.500,5.500,8.500 FYI='Test info' /
"""
    assert fds_string == expected_fds_string[1:-1]


def test_MESH_MULT_dy_dy0():
    ob = _create_mesh_ob("test_MESH_MULT_dy_dy0")
    ob.bf_mult_export = True
    ob.bf_mult_dy = 3.0
    ob.bf_mult_dy0 = 1.0
    ob.bf_mult_j_lower = 1
    ob.bf_mult_j_lower_skip = 3
    ob.bf_mult_j_upper_skip = 5
    ob.bf_mult_j_upper = 7
    fds_string = ob.to_fds_list(bpy.context).to_string()
    expected_fds_string = """
Cell Qty: 1848 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_MULT_dy_dy0_i0_j1_k0' IJK=11,12,14
      XB=3.500,6.500,8.500,11.500,5.500,8.500 FYI='Test info' /
Cell Qty: 1848 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_MULT_dy_dy0_i0_j2_k0' IJK=11,12,14
      XB=3.500,6.500,11.500,14.500,5.500,8.500 FYI='Test info' /
Cell Qty: 1848 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_MULT_dy_dy0_i0_j6_k0' IJK=11,12,14
      XB=3.500,6.500,23.500,26.500,5.500,8.500 FYI='Test info' /
Cell Qty: 1848 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_MULT_dy_dy0_i0_j7_k0' IJK=11,12,14
      XB=3.500,6.500,26.500,29.500,5.500,8.500 FYI='Test info' /
"""
    assert fds_string == expected_fds_string[1:-1]


def test_MESH_MULT_dz_dz0():
    ob = _create_mesh_ob("test_MESH_MULT_dz_dz0")
    ob.bf_mult_export = True
    ob.bf_mult_dz = 3.0
    ob.bf_mult_dz0 = 1.0
    ob.bf_mult_k_lower = 1
    ob.bf_mult_k_lower_skip = 3
    ob.bf_mult_k_upper_skip = 5
    ob.bf_mult_k_upper = 7
    fds_string = ob.to_fds_list(bpy.context).to_string()
    expected_fds_string = """
Cell Qty: 1848 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_MULT_dz_dz0_i0_j0_k1' IJK=11,12,14
      XB=3.500,6.500,4.500,7.500,9.500,12.500 FYI='Test info' /
Cell Qty: 1848 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_MULT_dz_dz0_i0_j0_k2' IJK=11,12,14
      XB=3.500,6.500,4.500,7.500,12.500,15.500 FYI='Test info' /
Cell Qty: 1848 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_MULT_dz_dz0_i0_j0_k6' IJK=11,12,14
      XB=3.500,6.500,4.500,7.500,24.500,27.500 FYI='Test info' /
Cell Qty: 1848 | Size: 0.273·0.250·0.214m | Aspect: 1.3 | Poisson: No
&MESH ID='test_MESH_MULT_dz_dz0_i0_j0_k7' IJK=11,12,14
      XB=3.500,6.500,4.500,7.500,27.500,30.500 FYI='Test info' /
"""
    assert fds_string == expected_fds_string[1:-1]


def test_MESH_import():
    imported_fds_string = """
&MESH ID='test_MESH_import' IJK=24,24,24, XB=-0.12,-0.06,-0.12,-0.06,-0.12,-0.06, MULT_ID='mesh' /
&MULT ID='mesh', DX=0.06, DY=0.06, DZ=0.06, I_UPPER=1, J_UPPER=1, K_UPPER=1 /
"""
    context = bpy.context
    scene = context.scene
    scene.from_fds(context, f90_namelists=imported_fds_string)
    ob = bpy.data.objects["test_MESH_import"]
    fds_string = ob.to_fds_list(bpy.context).to_string()
    expected_fds_string = """
Cell Qty: 13824 | Size: 0.002·0.002·0.002m | Aspect: 1.0 | Poisson: Yes
&MESH ID='test_MESH_import_i0_j0_k0' IJK=24,24,24
      XB=-0.120,-0.060,-0.120,-0.060,-0.120,-0.060 /
Cell Qty: 13824 | Size: 0.002·0.002·0.002m | Aspect: 1.0 | Poisson: Yes
&MESH ID='test_MESH_import_i0_j0_k1' IJK=24,24,24
      XB=-0.120,-0.060,-0.120,-0.060,-0.060,0.000 /
Cell Qty: 13824 | Size: 0.002·0.002·0.002m | Aspect: 1.0 | Poisson: Yes
&MESH ID='test_MESH_import_i0_j1_k0' IJK=24,24,24
      XB=-0.120,-0.060,-0.060,0.000,-0.120,-0.060 /
Cell Qty: 13824 | Size: 0.002·0.002·0.002m | Aspect: 1.0 | Poisson: Yes
&MESH ID='test_MESH_import_i0_j1_k1' IJK=24,24,24
      XB=-0.120,-0.060,-0.060,0.000,-0.060,0.000 /
Cell Qty: 13824 | Size: 0.002·0.002·0.002m | Aspect: 1.0 | Poisson: Yes
&MESH ID='test_MESH_import_i1_j0_k0' IJK=24,24,24
      XB=-0.060,0.000,-0.120,-0.060,-0.120,-0.060 /
Cell Qty: 13824 | Size: 0.002·0.002·0.002m | Aspect: 1.0 | Poisson: Yes
&MESH ID='test_MESH_import_i1_j0_k1' IJK=24,24,24
      XB=-0.060,0.000,-0.120,-0.060,-0.060,0.000 /
Cell Qty: 13824 | Size: 0.002·0.002·0.002m | Aspect: 1.0 | Poisson: Yes
&MESH ID='test_MESH_import_i1_j1_k0' IJK=24,24,24
      XB=-0.060,0.000,-0.060,0.000,-0.120,-0.060 /
Cell Qty: 13824 | Size: 0.002·0.002·0.002m | Aspect: 1.0 | Poisson: Yes
&MESH ID='test_MESH_import_i1_j1_k1' IJK=24,24,24
      XB=-0.060,0.000,-0.060,0.000,-0.060,0.000 /
"""
    assert fds_string == expected_fds_string[1:-1]


def test_MESH_bf_set_suggested_mesh_cell_size():
    ob = _create_mesh_ob("test_MESH_bf_set_suggested_mesh_cell_size")
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
    fds_string = ob.to_fds_list(bpy.context).to_string()
    expected_fds_string = """
Cell Qty: 7600 | Size: 0.158·0.150·0.150m | Aspect: 1.1 | Poisson: Yes
&MESH ID='test_MESH_bf_set_suggested_mesh_cell_size' FYI='Test info'
      IJK=19,20,20 XB=3.500,6.500,4.500,7.500,5.500,8.500 /
"""
    assert fds_string == expected_fds_string[1:-1]


def test_MESH_bf_set_mesh_cell_size():
    ob = _create_mesh_ob("test_MESH_bf_set_mesh_cell_size")
    bpy.ops.object.bf_set_mesh_cell_size(
        bf_cell_sizes=(0.23, 0.23, 0.23),
        bf_poisson_restriction=False,
    )
    fds_string = ob.to_fds_list(bpy.context).to_string()
    expected_fds_string = """
Cell Qty: 2197 | Size: 0.231·0.231·0.231m | Aspect: 1.0 | Poisson: No
&MESH ID='test_MESH_bf_set_mesh_cell_size' FYI='Test info' IJK=13,13,13
      XB=3.500,6.500,4.500,7.500,5.500,8.500 /
"""
    assert fds_string == expected_fds_string[1:-1]


def test_MESH_bf_set_mesh_cell_size_w_Poisson():
    ob = _create_mesh_ob("test_MESH_bf_set_mesh_cell_size_w_Poisson")
    bpy.ops.object.bf_set_mesh_cell_size(
        bf_cell_sizes=(0.23, 0.23, 0.23),
        bf_poisson_restriction=True,
    )
    fds_string = ob.to_fds_list(bpy.context).to_string()
    expected_fds_string = """
Cell Qty: 2925 | Size: 0.231·0.200·0.200m | Aspect: 1.2 | Poisson: Yes
&MESH ID='test_MESH_bf_set_mesh_cell_size_w_Poisson' FYI='Test info'
      IJK=13,15,15 XB=3.500,6.500,4.500,7.500,5.500,8.500 /
"""
    assert fds_string == expected_fds_string[1:-1]


def test_MESH_bf_align_to_mesh():  # test operator
    pass


def test_MESH_align_meshes():
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


def test_MESH_calc_meshes():
    from bl_ext.user_default.bfds.lang.ON_MESH import calc_meshes

    assert tuple(calc_meshes.get_factor(142)) == (1, 2, 71)
    assert calc_meshes.get_n_for_poisson(28) == 30
    assert calc_meshes.get_poisson_ijk((11, 11, 13)) == (11, 12, 15)

    context = bpy.context
    ob = _create_mesh_ob("test_MESH_calc_meshes")
    desired_cs = (0.5, 0.7, 0.9)
    poisson = True
    res = calc_meshes.get_ijk_from_desired_cs(context, ob, desired_cs, poisson)
    assert res == (6, 4, 3)

    res = calc_meshes.get_cell_sizes(context, ob)
    assert res == (0.2727272727272727, 0.25, 0.21428571428571427)

    assert calc_meshes.get_mesh_geometry(context, ob) == (
        ("test_MESH_calc_meshes",),  # hids
        [(11, 12, 14)],  # ijks
        [(3.5, 6.5, 4.5, 7.5, 5.5, 8.5)],  # xbs
        1,  # nmesh
        1,  # nsplit
        1,  # nmult
        1848,  # ncell_tot
        1848,  # ncell
        (0.2727272727272727, 0.25, 0.21428571428571427),  # cs
        1.2727272727272727,  # aspect
        "No",  # has_good_ijk
    )

    cell_sizes = 0.50, 0.75, 1.00
    assert calc_meshes.get_cell_aspect(cell_sizes) == 2.0


def test_MESH_split_mesh():
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
