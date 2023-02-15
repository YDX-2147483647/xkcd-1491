from pathlib import Path

from adjustText import adjust_text
from matplotlib.pyplot import rc_context, show, subplots

from .data import load_data
from .util import draw, palette
from .xkcd import xkcd

data = load_data(Path("data").iterdir())

with rc_context(xkcd):
    fig, ax = subplots(
        layout="constrained",
        figsize=(8, 12),
    )

    ax.set_xlabel("written in".title())
    ax.set_ylabel("set in - written in".title())

    ax.set_yscale("symlog")

    ax.grid(visible=True)

    texts = []

    for publication in data:
        texts.extend(draw(publication, ax, color=next(palette)))

    adjust_text(
        texts,
        lim=15,
        arrowprops=dict(
            color="gray",
            alpha=0.4,
            arrowstyle="-",
        ),
    )

show()
