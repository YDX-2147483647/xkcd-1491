from __future__ import annotations

from itertools import chain, cycle, pairwise
from typing import TYPE_CHECKING
from warnings import warn

from numpy import linspace

if TYPE_CHECKING:
    from typing import Iterable

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
    assert len(publication.series) > 1

    texts = []

    # Plot the line
    ax.plot(
        *zip(*map(event_to_xy, publication.series)),
        alpha=0.5,
        color=color,
    )

    # Annotate the line between the first two events
    # (agnostic about axis' scales)
    first, second = map(event_to_xy, publication.series[:2])
    texts.append(
        ax.annotate(
            text=publication.name,
            xy=((first[0] + second[0]) / 2, (first[1] + second[1]) / 2),
            color=color,
            fontweight="bold",
        )
    )

    # Draw events
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


def draw_areas(ax: Axes, past_years: Iterable[float], futures: Iterable[float]) -> None:
    past_years = sorted(past_years, reverse=True)
    origin = past_years[0]
    futures = sorted(futures)

    x_start, x_end = ax.xaxis.get_view_interval()
    y_interval = ax.yaxis.get_view_interval()

    t = ax.xaxis.get_transform()
    # `xs` are uniform spaced after scaling.
    xs = t.inverted().transform(
        linspace(*t.transform([x_start, origin]), num=100, endpoint=True)
    )

    # Draw past areas
    for right, left in pairwise(past_years):
        ax.fill_between(xs, left - xs, right - xs, alpha=0.2)
    # Draw obsolete past line
    ax.plot(xs, xs - origin, alpha=0.2, linestyle="--")
    # Draw future areas
    for left, right in pairwise(futures):
        ax.fill_between(xs, origin + left - xs, origin + right - xs, alpha=0.2)

    # Drawing areas may expand the view. We should revert it.
    ax.set_xlim(x_start, x_end)
    ax.set_ylim(*y_interval)
