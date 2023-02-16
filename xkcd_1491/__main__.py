from pathlib import Path

from adjustText import adjust_text
from matplotlib.pyplot import rc_context, show, subplots
from matplotlib.ticker import MultipleLocator

from .asinh_shifted import AsinhScale
from .data import load_data
from .util import draw, palette
from .xkcd import xkcd

data = load_data(Path("data").iterdir())

with rc_context(xkcd):
    fig, ax = subplots(
        layout="constrained",
        figsize=(8, 12),
    )

    ax.set_xlabel("released".title())
    ax.set_ylabel("setting - released".title())

    ax.xaxis.set_tick_params(which="both", top=True, labeltop=True)
    ax.xaxis.set_minor_locator(MultipleLocator(base=20))
    ax.yaxis.set_tick_params(which="both", right=True, labelright=True)

    ax.set_yscale(AsinhScale(ax.yaxis, linear_width=20, subs=(2, 4, 6, 8)))
    # The axis is only for back-compatibility and never used

    ax.grid(visible=True)

    texts = []

    for publication in data:
        texts.extend(draw(publication, ax, color=next(palette)))

    adjust_text(
        texts,
        lim=15,
        expand_text=(1.15, 1.3),
        arrowprops=dict(
            color="gray",
            alpha=0.4,
            arrowstyle="-",
        ),
    )

show()
