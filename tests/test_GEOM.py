# SPDX-License-Identifier: GPL-3.0-or-later

import bpy

from bl_ext.user_default.bfds.lang.ON_GEOM import bingeom


def _create_ob(name="pyramid", path=".", location=(5.0, 6.0, 7.0)):
    # Create Object data
    verts = [
        (-1, -1, 0),  # 0 base front-left
        (1, -1, 0),  # 1 base front-right
        (1, 1, 0),  # 2 base back-right
        (-1, 1, 0),  # 3 base back-left
        (0, 0, 2),  # 4 apex
    ]
    faces = [
        (3, 2, 1, 0),  # base (quad)
        (0, 1, 4),  # front side
        (1, 2, 4),  # right side
        (2, 3, 4),  # back side
        (3, 0, 4),  # left side
    ]
    me = bpy.data.meshes.new(f"{name}_data")
    me.from_pydata(verts, [], faces)
    me.update()
    # Create Object
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    ob.location = location
    ob.bf_namelist_cls = "ON_GEOM"
    # Create Materials
    ma = bpy.data.materials.new(name="yellow")
    ma.diffuse_color = (0.7, 0.7, 0.0, 1)
    mar = bpy.data.materials.new(name="red")
    mar.diffuse_color = (1, 0, 0, 1)  # RGBA
    mag = bpy.data.materials.new(name="green")
    mag.diffuse_color = (0, 1, 0, 1)  # RGBA
    mab = bpy.data.materials.new(name="blue")
    mab.diffuse_color = (0, 0, 1, 1)  # RGBA
    # Add materials to the object slots
    ob.data.materials.append(ma)  # slot 0
    ob.data.materials.append(mar)  # slot 1
    ob.data.materials.append(mag)  # slot 2
    ob.data.materials.append(mab)  # slot 3
    # Set faces materials
    ob.data.polygons[2].material_index = 1  # red
    ob.data.polygons[1].material_index = 2  # green
    ob.data.polygons[0].material_index = 3  # blue
    # Save blend file
    bpy.ops.wm.save_mainfile(filepath=str(path / "test.blend"))
    return ob


def _remove_ob(ob):
    for ma in ob.data.materials:
        bpy.data.materials.remove(ma, do_unlink=True)
    bpy.data.meshes.remove(ob.data, do_unlink=True)
    # bpy.data.objects.remove(ob, do_unlink=True)


def test_simple(tmp_path):
    name = "test_simple"
    ob = _create_ob(name=name, path=tmp_path)
    res = ob.to_fds_list(bpy.context).to_string()
    fds_string = """
Vertices: 15 | Faces: 18
&GEOM ID='test_simple' SURF_ID='yellow','red','green','blue'
      BINARY_FILE='test_simple_data.bingeom' /
"""
    _remove_ob(ob)
    assert res == fds_string[1:-1]

    n_surf_id, fds_verts, fds_faces, fds_surfs, fds_volus, geom_type = (
        bingeom.read_bingeom_file(str(tmp_path / f"{name}_data.bingeom"))
    )
    assert n_surf_id == 4
    assert tuple(fds_verts) == (
        4.0,
        5.0,
        7.0,
        6.0,
        5.0,
        7.0,
        6.0,
        7.0,
        7.0,
        4.0,
        7.0,
        7.0,
        5.0,
        6.0,
        9.0,
    )
    assert tuple(fds_faces) == (3, 1, 4, 1, 2, 5, 2, 3, 5, 3, 4, 5, 4, 1, 5, 3, 2, 1)
    assert tuple(fds_surfs) == (4, 3, 2, 1, 1, 4)
    assert tuple(fds_volus) == ()
    assert geom_type == 1


def test_bingeom(tmp_path):
    # from bl_ext.user_default.bfds.lang.ON_GEOM import bingeom

    # round trip test of writing/reading a bingeom
    geom_type = 2
    n_surf_id = 4
    fds_verts = (5.0, 6.0, 7.0, -8.0, -9.0, -10.0)
    fds_faces = (9, 10, 11, 12, 13, 14)
    fds_surfs = (13, 14)
    fds_volus = ()
    filepath = str(tmp_path / "test.bingeom")

    bingeom.write_bingeom_file(
        geom_type=geom_type,
        n_surf_id=n_surf_id,
        fds_verts=fds_verts,
        fds_faces=fds_faces,
        fds_surfs=fds_surfs,
        fds_volus=fds_volus,
        filepath=filepath,
        force_dir=False,
    )

    n_surf_id2, fds_verts2, fds_faces2, fds_surfs2, fds_volus2, geom_type2 = (
        bingeom.read_bingeom_file(filepath)
    )
    assert geom_type2 == geom_type
    assert n_surf_id2 == n_surf_id
    assert tuple(fds_verts2) == fds_verts
    assert tuple(fds_faces2) == fds_faces
    assert tuple(fds_surfs2) == fds_surfs
    assert tuple(fds_volus2) == fds_volus


def test_geom_to_ob():  # FIXME
    from bl_ext.user_default.bfds.lang.ON_GEOM import geom_to_ob

    pass


def test_ob_to_geom():  # FIXME
    from bl_ext.user_default.bfds.lang.ON_GEOM import ob_to_geom

    pass


# FIXME test instances
