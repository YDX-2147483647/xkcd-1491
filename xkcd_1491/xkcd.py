"""xkcd style

Usage:
```python
from matplotlib.pyplot import rc_context
from .xkcd import xkcd

with rc_context(xkcd):
    # plot as you want
```

Modified from `matplotlib.pyplot.xkcd`.

See: [`matplotlib.pyplot.xkcd` doc][xkcd-doc], [its source][xkcd-src],
and [rc explanation][rc-doc].

Remark: Some values are impossible to set from a `matplotlibrc` file.

[xkcd-doc]: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.xkcd.html
[xkcd-src]: https://github.com/matplotlib/matplotlib/blob/v3.6.3/lib/matplotlib/pyplot.py#L597-L661
[rc-doc]: https://matplotlib.org/stable/tutorials/introductory/customizing.html#the-default-matplotlibrc-file
"""  # noqa: E501

from matplotlib.patheffects import withStroke

xkcd = {
    "font.family": [
        "xkcd",  # https://github.com/ipython/xkcd-font/blob/master/xkcd/build/xkcd.otf
        "HYRuiYunXiuWu",  # 汉仪瑞云袖舞 https://www.hanyi.com.cn/productdetail?id=8191&type=0
        "Source Han Sans CN",
        "STKaiti",
        "sans-serif",
    ],
    "path.sketch": (
        1,  # scale
        100,  # length
        2,  # thickness
    ),
    "path.effects": [
        withStroke(linewidth=4, foreground="w"),
    ],
    "figure.facecolor": "white",
    "axes.edgecolor": "black",
    "axes.linewidth": 1.5,
    "lines.linewidth": 2.0,
    "xtick.major.size": 8,
    "xtick.major.width": 3,
    "ytick.major.size": 8,
    "ytick.major.width": 3,
}
