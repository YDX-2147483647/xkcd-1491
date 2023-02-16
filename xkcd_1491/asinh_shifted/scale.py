"""
Adapt from matplotlib.
https://github.com/matplotlib/matplotlib/blob/v3.7.0/lib/matplotlib/scale.py#L465-L579
https://matplotlib.org/stable/users/project/license.html
"""

from typing import Literal, Sequence

import numpy as np
from matplotlib.scale import ScaleBase
from matplotlib.ticker import LogFormatterSciNotation, NullFormatter
from matplotlib.transforms import Transform

from .ticker import AsinhLocator


class AsinhTransform(Transform):
    """Inverse hyperbolic-sine transformation used by `.AsinhScale`"""

    center: float

    input_dims = output_dims = 1

    def __init__(self, linear_width, center: float):
        super().__init__()
        if linear_width <= 0.0:
            raise ValueError(
                "Scale parameter 'linear_width' " + "must be strictly positive"
            )
        self.linear_width = linear_width

        self.center = center

    def transform_non_affine(self, a):
        return self.linear_width * np.arcsinh((a - self.center) / self.linear_width)

    def inverted(self):
        return InvertedAsinhTransform(self.linear_width, self.center)


class InvertedAsinhTransform(Transform):
    """Hyperbolic sine transformation used by `.AsinhScale`"""

    center: float

    input_dims = output_dims = 1

    def __init__(self, linear_width, center: float):
        super().__init__()
        self.linear_width = linear_width
        self.center = center

    def transform_non_affine(self, a):
        return self.linear_width * np.sinh(a / self.linear_width) + self.center

    def inverted(self):
        return AsinhTransform(self.linear_width, self.center)


class AsinhScale(ScaleBase):
    """
    A quasi-logarithmic scale based on the inverse hyperbolic sine (asinh)
    For values close to zero, this is essentially a linear scale,
    but for large magnitude values (either positive or negative)
    it is asymptotically logarithmic. The transition between these
    linear and logarithmic regimes is smooth, and has no discontinuities
    in the function gradient in contrast to
    the `.SymmetricalLogScale` ("symlog") scale.
    Specifically, the transformation of an axis coordinate :math:`a` is
    :math:`a \\rightarrow a_0 \\sinh^{-1} (a / a_0)` where :math:`a_0`
    is the effective width of the linear region of the transformation.
    In that region, the transformation is
    :math:`a \\rightarrow a + \\mathcal{O}(a^3)`.
    For large values of :math:`a` the transformation behaves as
    :math:`a \\rightarrow a_0 \\, \\mathrm{sgn}(a) \\ln |a| + \\mathcal{O}(1)`.
    .. note::
       This API is provisional and may be revised in the future
       based on early user feedback.
    """

    name = "asinh"

    auto_tick_multipliers = {
        3: (2,),
        4: (2,),
        5: (2,),
        8: (2, 4),
        10: (2, 5),
        16: (2, 4, 8),
        64: (4, 16),
        1024: (256, 512),
    }

    def __init__(
        self,
        axis,
        *,
        linear_width=1.0,
        base=10,
        center: float = 0.0,
        subs: Sequence[int] | Literal["auto"] = "auto",
        **kwargs,
    ):
        """
        Parameters
        ----------
        linear_width : float, default: 1
            The scale parameter (elsewhere referred to as :math:`a_0`)
            defining the extent of the quasi-linear region,
            and the coordinate values beyond which the transformation
            becomes asymptotically logarithmic.
        base : int, default: 10
            The number base used for rounding tick locations
            on a logarithmic scale. If this is less than one,
            then rounding is to the nearest integer multiple
            of powers of ten.
        center : float, default: 0
            The center of symmetry, can be used to offset.
        subs : sequence of int
            Multiples of the number base used for minor ticks.
            If set to 'auto', this will use built-in defaults,
            e.g. (2, 5) for base=10.

        Caveats
        ----------
        `~.ticker.LogFormatterSciNotation` is not supported for non-zero center.

        The axis is only for back-compatibility and never used.
        """
        super().__init__(axis)
        self._transform = AsinhTransform(linear_width, center)
        self._base = int(base)
        if subs == "auto":
            self._subs = self.auto_tick_multipliers.get(self._base)
        else:
            self._subs = subs

    linear_width = property(lambda self: self._transform.linear_width)
    center = property(lambda self: self._transform.center)

    def get_transform(self):
        return self._transform

    def set_default_locators_and_formatters(self, axis):
        axis.set(
            major_locator=AsinhLocator(self.linear_width, self.center, base=self._base),
            minor_locator=AsinhLocator(
                self.linear_width, self.center, base=self._base, subs=self._subs
            ),
            minor_formatter=NullFormatter(),
        )

        if self.center == 0 and self._base > 1:
            axis.set_major_formatter(LogFormatterSciNotation(self._base))
        else:
            axis.set_major_formatter("{x:.3g}")
