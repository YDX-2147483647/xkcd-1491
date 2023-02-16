from __future__ import annotations

from functools import reduce
from typing import TYPE_CHECKING

from matplotlib.scale import FuncScale
from numpy import arcsinh, sinh

if TYPE_CHECKING:
    from typing import Reversible

    from matplotlib.axis import Axis


def sinh_(x, linear_width: float):
    return linear_width * sinh(x / linear_width)


def asinh_(x, linear_width: float):
    return linear_width * arcsinh(x / linear_width)


class WarpScale(FuncScale):
    """Warp Scale

    More warp than log.
    """

    def __init__(
        self,
        axis: Axis,
        *,
        center: float = 0.0,
        linear_widths: Reversible[float] = (1.0, 1.0),
    ) -> None:
        """
        Parameters:
            - `axis`: Only for back-compatibility and never used
            - `center`: The center of symmetry, can be used to offset
            - `linear_widths`:
                The scale parameters defining the extent of the quasi-linear region.
        """

        def forward(x):
            return reduce(asinh_, linear_widths, x - center)

        def inverse(y):
            return reduce(sinh_, reversed(linear_widths), y) + center

        super().__init__(axis, functions=(forward, inverse))
