from __future__ import annotations

from dataclasses import dataclass
from itertools import chain
from typing import TYPE_CHECKING

import polars as pl
from ruamel.yaml import YAML

from .util import average, tuple_or_int

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Iterable


@dataclass
class Event:
    name: str | None
    written_in: int | tuple[int, int]
    set_in: int | tuple[int, int]

    @property
    def written_in_average(self) -> float | int:
        return average(self.written_in)

    @property
    def set_in_average(self) -> float | int:
        return average(self.set_in)


@dataclass
class Publication:
    name: str
    author: str | None
    series: list[Event]


def _load_events(file: Path) -> list[Publication]:
    events = pl.scan_csv(
        file,
        dtypes={
            "publication": pl.Utf8,
            "author": pl.Utf8,
            "written_in": pl.Int64,
            "set_in": pl.Int64,
        },
    ).select(["publication", "author", "written_in", "set_in"])

    return [
        Publication(
            name=e[0],
            author=e[1],
            series=[Event(name=None, written_in=e[2], set_in=e[3])],
        )
        for e in events.collect().rows()
    ]


def _load_series(file: Path) -> list[Publication]:
    publications = YAML(typ="safe").load(file.read_text(encoding="utf-8"))

    return [
        Publication(
            author=p.get("author"),
            name=p["publication"],
            series=[
                Event(
                    name=e.get("name"),
                    written_in=tuple_or_int(e["written_in"]),
                    set_in=tuple_or_int(e["set_in"]),
                )
                for e in p["series"]
            ],
        )
        for p in publications
    ]


def _load_data(file: Path) -> list[Publication]:
    """Load a set of data"""

    match file.suffix:  # noqa E501 for https://github.com/charliermarsh/ruff/issues/282
        case ".yaml" | ".yml":
            return _load_series(file)
        case ".csv":
            return _load_events(file)
        case _:
            raise ValueError(f"Unknown data format: “{file}”")


def load_data(files: Iterable[Path]) -> Iterable[Publication]:
    """Load data from files

    Data format:
        - csv: events.
        - yaml: series.
    """

    return chain.from_iterable(map(_load_data, files))
