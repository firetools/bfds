# SPDX-License-Identifier: GPL-3.0-or-later

"""!
Simple binpacking algorithm.
"""


def _argmin(l):
    """Get the index of min item in an iterable."""
    l = tuple(l)
    return min(range(len(l)), key=l.__getitem__)


def binpack(nbin, item_weigths):
    """First-fit binpacking algorithm with fixed number of bins.

    @param nbin: fixed number of bins
    @param item_weigths: list of items and their weigths: ((w0, item0), (w1, item1), ...)
    @return: list of bins: [[wb0, [item0, item1, ...]], [wb1, [item5, ...]], ...]
    """
    # Reverse sort items by weigth
    item_weigths = list(item_weigths)
    item_weigths.sort(key=lambda k: k[0], reverse=True)

    # Init bins
    bins = list(list((0, list())) for i in range(nbin))

    # Pack
    for i, (weigth, item) in enumerate(item_weigths):
        # Get the index of the lighter bin
        j = _argmin(tuple(bin[0] for bin in bins))
        # Add the weigth and assign the item to the bin
        bins[j][0] += weigth
        bins[j][1].append(item)

    return bins
