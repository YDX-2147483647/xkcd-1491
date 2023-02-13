from pathlib import Path

from matplotlib.pyplot import rc_context, show, subplots

from .data import load_data
from .xkcd import xkcd


data = load_data(Path("data").iterdir())

with rc_context(xkcd):
    fig, ax = subplots(layout="constrained")

    ax.set_xlabel("written in".title())
    ax.set_ylabel("set in".title())

    for publication in data:
        for event in publication.series:
            assert not isinstance(event.written_in, tuple)
            assert not isinstance(event.set_in, tuple)

            ax.annotate(
                text=event.name or publication.name,
                xy=(event.written_in, event.set_in),
                xytext=(10, -10),
                textcoords="offset points",
                verticalalignment="top",
                arrowprops=dict(
                    color="purple",
                    alpha=0.4,
                    arrowstyle="->",
                    connectionstyle="arc3,rad=-0.2",
                ),
            )

    ax.set_xlim(1900, 2023)
    ax.set_ylim(1900, 2200)
    ax.grid(visible=True)

show()
