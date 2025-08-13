# SPDX-License-Identifier: GPL-3.0-or-later

import bpy


def test_binpacking():
    from bl_ext.user_default.bfds.utils import binpacking

    item_weigths = ((10, "A"), (12, "B"), (11, "C"), (4, "D"), (3, "E"), (2, "F"))

    bins = binpacking.binpack(nbin=1, item_weigths=item_weigths)
    assert bins == [[42, ["B", "C", "A", "D", "E", "F"]]]

    bins = binpacking.binpack(nbin=2, item_weigths=item_weigths)
    assert bins == [[21, ["B", "D", "E", "F"]], [21, ["C", "A"]]]

    bins = binpacking.binpack(nbin=3, item_weigths=item_weigths)
    assert bins == [[14, ["B", "F"]], [14, ["C", "E"]], [14, ["A", "D"]]]

    bins = binpacking.binpack(nbin=4, item_weigths=item_weigths)
    assert bins == [[12, ["B"]], [11, ["C"]], [10, ["A"]], [9, ["D", "E", "F"]]]

    bins = binpacking.binpack(nbin=5, item_weigths=item_weigths)
    assert bins == [[12, ["B"]], [11, ["C"]], [10, ["A"]], [4, ["D"]], [5, ["E", "F"]]]

    bins = binpacking.binpack(nbin=6, item_weigths=item_weigths)
    assert bins == [
        [12, ["B"]],
        [11, ["C"]],
        [10, ["A"]],
        [4, ["D"]],
        [3, ["E"]],
        [2, ["F"]],
    ]

    bins = binpacking.binpack(nbin=7, item_weigths=item_weigths)
    assert bins == [
        [12, ["B"]],
        [11, ["C"]],
        [10, ["A"]],
        [4, ["D"]],
        [3, ["E"]],
        [2, ["F"]],
        [0, []],
    ]


def test_gis():
    from bl_ext.user_default.bfds.utils import gis

    assert gis.lonlat_to_zn(lat=40.8518, lon=14.2681) == 33  # Naples, Italy
    assert gis.lat_to_ne(lat=40.8518) == True
    assert gis.zn_to_central_lon(zn=33) == 15
    assert gis.lonlat_to_utm(
        lat=40.8518, lon=14.2681, force_zn=None, force_ne=None
    ) == (33, True, 438308.1773737638, 4522563.411221754)
    assert gis.zn_ne_to_epsg(zn=33, ne=True) == "EPSG:32633"
    assert gis.epsg_to_code(epsg="EPSG:32633") == "32633"
    assert gis.epsg_to_zn_ne(epsg="EPSG:32633") == (33, True)
    assert gis.lonlat_to_epsg(lat=40.8518, lon=14.2681) == "EPSG:32633"
    assert gis.webMercToLonLat(x=1588317.6265875068, y=4990506.711860527) == (
        14.2681,  # lon
        40.8518,  # lat
    )
    assert gis.lonLatToWebMerc(lat=40.8518, lon=14.2681) == (
        1588317.6265875068,
        4990506.711860527,
    )
