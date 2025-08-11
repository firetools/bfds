# SPDX-License-Identifier: GPL-3.0-or-later

"""
Align MESHes correctly according to cells.
"""

import logging
from ... import config
from ...types import BFException
from .calc_meshes import get_n_for_poisson

log = logging.getLogger(__name__)

# Mesh alignment:
#
# Before:
#   |   |rcs|   |   | ri  ref mesh
#   ·---·---·---·---·
#  rx0   <-rl->    rx1
# mx0      <-ml->      mx1
#  ·------·------·------·
#  |      | mcs  |      | mi  other mesh
# ---> axis

# Either protect rl or rcs.
# Instead ml and mcs are changed for alignment.

# After:
#  |   |   |   |   |
#  ·---·---·---·---·-------·
#  |       |       |       |

# Not allowed:
#  |    |     |    |
#  ·----·--·--·----·
#  |       |       |

#  |   |   |   |
#  ·---·---·---·---·
#  |       |       |


def _align_along_axis(ri, rx0, rx1, mi, mx0, mx1, poisson, protect_rxb, protect_rcs):
    """Align coarse MESH to fixed ref MESH along an axis."""
    # Init
    if rx0 >= rx1 or mx0 >= mx1:
        raise Exception("Coordinate order error")
    rl, ml = rx1 - rx0, mx1 - mx0  # lengths
    rcs, mcs = rl / ri, ml / mi  # cell sizes

    # Coarsening ratio
    if mcs / rcs < 0.501:  # same or coarser allowed, protect from float err
        raise BFException(
            None, f"Aligned MESH should be coarser than reference: {mcs} > {rcs}"
        )
    n = round(mcs / rcs)

    # Set ref cell count multiple of n
    # to allow full cover of coarse cells by ref cells
    rim = round(ri / n) * n
    if poisson:
        rim = get_n_for_poisson(rim)
    msg = None
    if abs(ri - rim) > 0.00001:  # not multiple!
        if protect_rcs:
            if protect_rxb:
                raise BFException(
                    None, "Alignment impossible, allow resizing reference."
                )
            else:
                rl = rcs * rim  # extend ref length due to updated ri
                rx1 = rx0 + rl
                msg = "increased ref size"
        else:
            rcs = rl / rim  # reduce ref cell size
            msg = "decreased ref cell size"

    # Calc new coarse cell size from ref cell size
    mcs = rcs * n

    # Calc new coarse cell count,
    # trying to keep ml as close as possible to the original
    mi = round(ml / mcs)
    if poisson:
        mi = get_n_for_poisson(mi)

    # Align coarse mesh positions to the ref mesh
    mx0 = rx0 + round((mx0 - rx0) / mcs) * mcs
    ml = mcs * mi  # extend other mesh due to updated mi
    mx1 = mx0 + ml

    return rim, rx0, rx1, mi, mx0, mx1, msg


def _align_along_x(rijk, rxb, mijk, mxb, poisson, protect_rxb, protect_rcs):
    """Align coarse MESH to fixed ref MESH along axis x."""
    rijk[0], rxb[0], rxb[1], mijk[0], mxb[0], mxb[1], msg = _align_along_axis(
        ri=rijk[0],
        rx0=rxb[0],
        rx1=rxb[1],
        mi=mijk[0],
        mx0=mxb[0],
        mx1=mxb[1],
        poisson=False,  # not needed along x
        protect_rxb=protect_rxb,
        protect_rcs=protect_rcs,
    )
    return msg and f"{msg} along x axis"


def _align_along_y(rijk, rxb, mijk, mxb, poisson, protect_rxb, protect_rcs):
    """Align coarse MESH to fixed ref MESH along axis y."""
    rijk[1], rxb[2], rxb[3], mijk[1], mxb[2], mxb[3], msg = _align_along_axis(
        ri=rijk[1],
        rx0=rxb[2],
        rx1=rxb[3],
        mi=mijk[1],
        mx0=mxb[2],
        mx1=mxb[3],
        poisson=poisson,  # needed along y
        protect_rxb=protect_rxb,
        protect_rcs=protect_rcs,
    )
    return msg and f"{msg} along y axis"


def _align_along_z(rijk, rxb, mijk, mxb, poisson, protect_rxb, protect_rcs):
    """Align coarse MESH to fixed ref MESH along axis z."""
    rijk[2], rxb[4], rxb[5], mijk[2], mxb[4], mxb[5], msg = _align_along_axis(
        ri=rijk[2],
        rx0=rxb[4],
        rx1=rxb[5],
        mi=mijk[2],
        mx0=mxb[4],
        mx1=mxb[5],
        poisson=poisson,  # needed along z
        protect_rxb=protect_rxb,
        protect_rcs=protect_rcs,
    )
    return msg and f"{msg} along z axis"


# rx0 rx1
#  .---.
#       delta .----.
#            mx0  mx1


def _is_far(rxb, mxb, deltas):
    return (
        rxb[0] - mxb[1] > deltas[0]
        or mxb[0] - rxb[1] > deltas[0]  # x
        or rxb[2] - mxb[3] > deltas[1]
        or mxb[2] - rxb[3] > deltas[1]  # y
        or rxb[4] - mxb[5] > deltas[2]
        or mxb[4] - rxb[5] > deltas[2]  # z
    )


def align_meshes(
    rijk, rxb, mijk, mxb, poisson=False, protect_rxb=True, protect_rcs=True
):
    """
    Function to align meshes.
    @param rijk:  ijk of the ref mesh.
    @param rxb: xbs of the ref mesh.
    @param mijk: ijk of the other mesh.
    @param mxb: xbs of the other mesh.
    @param poisson: True for respecting the Poisson constraint.
    @param protect_rxb: True to protect ref xb.
    @param protect_rcs: True to protect ref cell size.
    @return return new rijk, rxb, mijk, mxb, and msg.
    """
    # Init
    deltas = (  # rcs
        abs(rxb[0] - rxb[1]) / rijk[0] * config.MAGNET_NCELL,
        abs(rxb[2] - rxb[3]) / rijk[1] * config.MAGNET_NCELL,
        abs(rxb[4] - rxb[5]) / rijk[2] * config.MAGNET_NCELL,
    )
    msgs = list()

    # Are meshes far apart?
    if _is_far(rxb=rxb, mxb=mxb, deltas=deltas):
        msgs.append("far apart, no alignment.")
        return rijk, rxb, mijk, mxb, msgs

    # Transform to list()
    rijk, rxb, mijk, mxb = list(rijk), list(rxb), list(mijk), list(mxb)

    # If mesh sides are close, then snap them
    # otherwise align their meshes
    if abs(rxb[0] - mxb[1]) <= deltas[0]:  # -x close?
        log.debug("ref x0 snapped")
        mxb[1] = rxb[0]
    elif abs(mxb[0] - rxb[1]) <= deltas[0]:  # +x close?
        log.debug("ref x1 snapped")
        mxb[0] = rxb[1]
    else:
        msg = _align_along_x(rijk, rxb, mijk, mxb, poisson, protect_rxb, protect_rcs)
        msgs.append(msg)
        log.debug("x axis aligned")
    if abs(rxb[2] - mxb[3]) <= deltas[1]:  # -y close?
        log.debug("ref y0 snapped")
        mxb[3] = rxb[2]
    elif abs(mxb[2] - rxb[3]) <= deltas[1]:  # +y close?
        log.debug("ref y1 snapped")
        mxb[2] = rxb[3]
    else:
        msg = _align_along_y(rijk, rxb, mijk, mxb, poisson, protect_rxb, protect_rcs)
        msgs.append(msg)
        log.debug("y axis aligned")
    if abs(rxb[4] - mxb[5]) <= deltas[2]:  # -z close?
        log.debug("ref z0 aligned")
        mxb[5] = rxb[4]
    elif abs(mxb[4] - rxb[5]) <= deltas[2]:  # +z close?
        log.debug("ref z1 snapped")
        mxb[4] = rxb[5]
    else:
        msg = _align_along_z(rijk, rxb, mijk, mxb, poisson, protect_rxb, protect_rcs)
        msgs.append(msg)
        log.debug("z axis aligned")

    # Set msg
    msg = ", ".join(m for m in msgs if m)
    return rijk, rxb, mijk, mxb, msg
