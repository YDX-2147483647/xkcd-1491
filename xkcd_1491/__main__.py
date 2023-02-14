from pathlib import Path

from matplotlib.pyplot import rc_context, show, subplots

from .data import load_data
from .util import palette
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

    for publication in data:
        color = next(palette)

        if len(publication.series) == 1:
            event = publication.series[0]

            try:
                assert not isinstance(event.written_in, tuple)
                assert not isinstance(event.set_in, tuple)
            except AssertionError:
                # todo
                pass

            position = (
                event.written_in_average,
                event.set_in_average - event.written_in_average,
            )
            label = event.name or publication.name

            ax.plot(
                [position[0]],
                [position[1]],
                marker=".",
                alpha=0.8,
                color=color,
            )
            ax.annotate(
                text=label,
                xy=position,
                xytext=(5, -5),
                textcoords="offset points",
                verticalalignment="top",
                color=color,
            )
        else:
            ax.plot(
                [e.written_in_average for e in publication.series],
                [e.set_in_average - e.written_in_average for e in publication.series],
                alpha=0.5,
                color=color,
            )

            for event in publication.series:
                try:
                    assert not isinstance(event.written_in, tuple)
                    assert not isinstance(event.set_in, tuple)
                except AssertionError:
                    # todo
                    pass

                position = (
                    event.written_in_average,
                    event.set_in_average - event.written_in_average,
                )
                label = event.name or publication.name

                ax.annotate(
                    text=label,
                    xy=position,
                    verticalalignment="top",
                    color=color,
                )

show()
