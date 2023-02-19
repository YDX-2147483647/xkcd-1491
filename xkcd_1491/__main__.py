from datetime import date
from pathlib import Path

from adjustText import adjust_text
from matplotlib.pyplot import rc_context, show, subplots
from matplotlib.ticker import AsinhLocator, EngFormatter, FixedLocator, MultipleLocator

from .data import load_data
from .util import draw, draw_areas, palette
from .warp_scale import WarpScale
from .xkcd import xkcd

data = load_data(Path("data").iterdir())
today = date.today().year
origins = [today, 2020, 2000, 1960, 1900, 1800, 1600, 1300, 600, 0, -2000]

with rc_context(xkcd):
    fig, ax = subplots(
        layout="constrained",
        figsize=(10, 10),
    )

    ax.grid(visible=True)

    # X axis
    ax.set_xlabel("released".title())
    ax.xaxis.set_tick_params(which="both", top=True, labeltop=True)
    ax.set_xscale(WarpScale(ax.xaxis, center=today, linear_widths=(50, 20)))
    ax.xaxis.set_major_locator(FixedLocator(origins))
    ax.xaxis.set_minor_locator(MultipleLocator(base=20))

    # Y axis
    ax.set_ylabel("setting - released".title())
    ax.yaxis.set_tick_params(which="both", right=True, labelright=True)
    ax.set_yscale(WarpScale(ax.yaxis, linear_widths=(100, 20)))
    ax.yaxis.set_major_locator(AsinhLocator(linear_width=20))
    ax.yaxis.set_major_formatter(EngFormatter(places=0))
    ax.yaxis.set_minor_locator(AsinhLocator(linear_width=20, subs=(2, 4, 6, 8)))

    # Draw

    texts = []

    for publication in data:
        texts.extend(draw(publication, ax, color=next(palette)))

    draw_areas(ax, origins=origins)

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
