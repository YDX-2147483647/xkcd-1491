"""Hard coded minor changes"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from matplotlib.text import Annotation


def amend(texts: list[Annotation]) -> None:
    translations = [
        ("越中览古", (0, -20)),
        ("The Sound of Music (film)", (-100, 0)),
        ("新世紀エヴァンゲリオン／Evangelion", (-200, -40)),
        ("The Cold Equations", (-100, -20)),
        ("風の谷のナウシカ", (0, 20)),
        ("S.A.C. 2045", (0, -40)),
        ("Ready Player Two", (-100, -10)),
        ("Back to the Future Part Ⅱ", (0, -10)),
        ("Voyager", (0, -10)),
        ("Rendezvous with Rama", (0, -30)),
        ("§2 逃逸时代", (40, 0)),
    ]

    for n, t in translations:
        _set_offset(_find(texts, n), t)


def _find(texts: list[Annotation], name) -> Annotation:
    candidates = [t for t in texts if t.get_text() == name]
    assert len(candidates) == 1
    return candidates[0]


def _set_offset(text: Annotation, offset: tuple[float, float]) -> None:
    """
    Parameters:
        - `offset`: offset from the annotated point in display coordinates.
    """

    t = text.axes.transData
    text.xyann = t.inverted().transform(t.transform(text.xyann) + offset)