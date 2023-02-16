from __future__ import annotations

from typing import TYPE_CHECKING

from matplotlib.scale import FuncScale
from numpy import arcsinh, sinh

if TYPE_CHECKING:
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
        center: float,
        linear_widths: tuple[float, float] = (1.0, 1.0),
    ) -> None:
        """
        Parameters:
            - `axis`: Only for back-compatibility and never used
            - `center`: The center of symmetry, can be used to offset
            - `linear_widths`:
                The scale parameters defining the extent of the quasi-linear region.
        """

        def forward(x):
            return asinh_(asinh_(x - center, linear_widths[0]), linear_widths[1])

        def inverse(y):
            return sinh_(sinh_(y, linear_widths[1]), linear_widths[0]) + center

        super().__init__(axis, functions=(forward, inverse))
