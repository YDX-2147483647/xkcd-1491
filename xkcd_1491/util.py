from __future__ import annotations

from itertools import chain, cycle
from typing import TYPE_CHECKING
from warnings import warn

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.colors import Color
    from matplotlib.text import Annotation

    from .data import Event, Publication

palette = cycle(
    [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
    ]
)


def draw(publication: Publication, ax: Axes, *, color: Color) -> list[Annotation]:
    """Plot and annotate a publication"""

    if len(publication.series) == 1:
        event = publication.series[0]

        if event.name is not None:
            warn(
                "Duplicate names of a single event: "
                f"“{publication.name}” (publication) and “{event.name}” (event). "
                "Please consider remove the event name."
            )

        return _draw_event(
            event,
            ax,
            color=color,
            name_fallback=publication.name,
            text_props=dict(fontweight="bold"),
        )

    else:
        return _draw_series(publication, ax, color=color)


def event_to_xy(event: Event) -> tuple[float | int, float | int]:
    return (
        event.written_in_average,
        event.set_in_average - event.written_in_average,
    )


def _draw_event(
    event: Event,
    ax: Axes,
    *,
    color: Color,
    name_fallback: str | None = None,
    text_props={},
) -> list[Annotation]:
    """Plot and annotate an event

    Parameter:
        - name_fallback: If not given, an event without a name won't be annotated.
        - text_props: Properties of annotations
    """

    try:
        assert not isinstance(event.written_in, tuple)
        assert not isinstance(event.set_in, tuple)
    except AssertionError:
        # todo: Change dot size by time ranges.
        pass

    xy = event_to_xy(event)
    ax.plot([xy[0]], [xy[1]], marker=".", alpha=0.8, color=color)

    if name := event.name or name_fallback:
        return [ax.annotate(text=name, xy=xy, color=color, **text_props)]
    else:
        return []


def _draw_series(
    publication: Publication, ax: Axes, *, color: Color
) -> list[Annotation]:
    """Plot and annotate a series of events"""

    assert publication.series, f"Cannot draw an empty series: “{publication.name}”"

    texts = []

    # draw the line
    ax.plot(
        *zip(*map(event_to_xy, publication.series)),
        alpha=0.5,
        color=color,
    )

    texts.append(
        ax.annotate(
            text=publication.name,
            xy=event_to_xy(publication.series[0]),
            color=color,
            fontweight="bold",
        )
    )

    # draw events
    texts.extend(
        chain.from_iterable(
            _draw_event(
                event,
                ax,
                color=color,
                text_props=dict(fontsize="x-small"),
            )
            for event in publication.series
        )
    )

    return texts
