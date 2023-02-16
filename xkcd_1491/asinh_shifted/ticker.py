"""
Adapt from matplotlib.
https://github.com/matplotlib/matplotlib/blob/v3.7.0/lib/matplotlib/ticker.py#L2623-L2732
https://matplotlib.org/stable/users/project/license.html
"""

import math

import numpy as np
from matplotlib.ticker import Locator


class AsinhLocator(Locator):
    """
    An axis tick locator specialized for the inverse-sinh scale

    This is very unlikely to have any use beyond
    the `~.scale.AsinhScale` class.

    .. note::

       This API is provisional and may be revised in the future
       based on early user feedback.
    """

    center: float

    def __init__(
        self,
        linear_width,
        center: float,
        numticks=11,
        symthresh=0.2,
        base=10,
        subs=None,
    ):
        """
        Parameters
        ----------
        linear_width : float
            The scale parameter defining the extent
            of the quasi-linear region.
        center : float
            The center of symmetry, can be used to offset.
        numticks : int, default: 11
            The approximate number of major ticks that will fit
            along the entire axis
        symthresh : float, default: 0.2
            The fractional threshold beneath which data which covers
            a range that is approximately symmetric about zero
            will have ticks that are exactly symmetric.
        base : int, default: 10
            The number base used for rounding tick locations
            on a logarithmic scale. If this is less than one,
            then rounding is to the nearest integer multiple
            of powers of ten.
        subs : tuple, default: None
            Multiples of the number base, typically used
            for the minor ticks, e.g. (2, 5) when base=10.
        """
        super().__init__()
        self.center = center
        self.linear_width = linear_width
        self.numticks = numticks
        self.symthresh = symthresh
        self.base = base
        self.subs = subs

    def set_params(self, numticks=None, symthresh=None, base=None, subs=None):
        """Set parameters within this locator."""
        if numticks is not None:
            self.numticks = numticks
        if symthresh is not None:
            self.symthresh = symthresh
        if base is not None:
            self.base = base
        if subs is not None:
            self.subs = subs if len(subs) > 0 else None

    def __call__(self):
        vmin, vmax = self.axis.get_view_interval()
        if ((vmin - self.center) * (vmax - self.center)) < 0 and abs(
            1 + (vmax - self.center) / (vmin - self.center)
        ) < self.symthresh:
            # Data-range appears to be almost symmetric, so round up:
            bound = max(abs(vmin - self.center), abs(vmax - self.center))
            return self.tick_values(self.center - bound, self.center + bound)
        else:
            return self.tick_values(vmin, vmax)

    def tick_values(self, vmin, vmax):
        # Construct a set of "on-screen" locations
        # that are uniformly spaced:
        ymin, ymax = self.linear_width * np.arcsinh(
            (np.array([vmin, vmax]) - self.center) / self.linear_width
        )
        ys = np.linspace(ymin, ymax, self.numticks)
        zero_dev = np.abs(ys / (ymax - ymin))
        if (ymin * ymax) < 0:
            # Ensure that the zero tick-mark is included,
            # if the axis straddles zero
            ys = np.hstack([ys[(zero_dev > 0.5 / self.numticks)], 0.0])

        # Transform the "on-screen" grid to the shifted data space:
        xs = self.linear_width * np.sinh(ys / self.linear_width)
        zero_xs = ys == 0

        # Round the shifted-data-space values to be intuitive base-n numbers,
        # keeping track of positive and negative values separately,
        # but giving careful treatment to the zero value:
        if self.base > 1:
            log_base = math.log(self.base)
            powers = np.where(zero_xs, 0, np.sign(xs)) * np.power(
                self.base,
                np.where(
                    zero_xs,
                    0.0,
                    np.floor(np.log(np.abs(xs) + zero_xs * 1e-6) / log_base),
                ),
            )
            if self.subs:
                qs = np.outer(powers, self.subs).flatten()
            else:
                qs = powers
        else:
            powers = np.where(xs >= 0, 1, -1) * np.power(
                10,
                np.where(zero_xs, 0.0, np.floor(np.log10(np.abs(xs) + zero_xs * 1e-6))),
            )
            qs = powers * np.round(xs / powers)
        ticks = np.array(sorted(set(qs))) + self.center

        if len(ticks) >= 2:
            return ticks
        else:
            return np.linspace(vmin, vmax, self.numticks)
