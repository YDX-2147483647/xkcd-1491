import logging
from datetime import date
from pathlib import Path

from matplotlib.pyplot import rc_context, subplots
from matplotlib.ticker import AsinhLocator, EngFormatter, FixedLocator, MultipleLocator

from .adjust_text import adjust_text
from .amend import amend
from .data import load_data
from .util import draw, draw_areas, palette
from .warp_scale import WarpScale
from .xkcd import xkcd

data = load_data(Path("data").iterdir())
today = date.today().year
past_years = [today, 2020, 2000, 1960, 1900, 1800, 1600, 1300, 600, 0, -2000]
futures = [2020 - today, 0, 10, 20, 50, 100, 1e3, 1e4, 1e5]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logging.info("📐 Initializing…")

with rc_context(xkcd):
    fig, ax = subplots(
        layout="constrained",
        figsize=(10, 14),
    )

    ax.text(
        s="过去和未来的故事",
        x=0.014,
        y=0.987,
        va="top",
        transform=ax.transAxes,
        fontweight="black",
        fontsize=40,
    )
    ax.text(
        s="github.com/YDX-2147483647/xkcd-1491",
        y=0.984,
        x=0.522,
        va="top",
        transform=ax.transAxes,
        fontfamily="Source Han Sans CN",
        fontstyle="oblique",
        fontsize="small",
    )
    ax.grid(visible=True)

    # X axis
    ax.set_xlabel("创作时间（公元纪年）")
    ax.xaxis.set_label_position("top")
    ax.xaxis.set_tick_params(which="both", top=True, labeltop=True)
    ax.set_xscale(WarpScale(ax.xaxis, center=today, linear_widths=(50, 20)))
    ax.xaxis.set_major_locator(FixedLocator(past_years))
    ax.xaxis.set_minor_locator(MultipleLocator(base=20))

    # Y axis
    ax.set_ylabel("(设定时间 − 创作时间) / 年")
    ax.set_ylim(-10e6, 31e6)  # Auto mode has too much margins
    ax.yaxis.set_tick_params(which="both", right=True, labelright=True)
    ax.set_yscale(WarpScale(ax.yaxis, linear_widths=(100, 20)))
    ax.yaxis.set_major_locator(AsinhLocator(linear_width=20, numticks=20))
    ax.yaxis.set_major_formatter(EngFormatter(places=0))
    ax.yaxis.set_minor_locator(
        AsinhLocator(linear_width=20, numticks=20, subs=(2, 4, 6, 8))
    )

    # Draw
    logging.info("📈 Drawing…")

    texts = []

    for publication in data:
        texts.extend(draw(publication, ax, color=next(palette)))

    draw_areas(ax, past_years=past_years, futures=futures)

    logging.info("👻 Amending texts…")
    amend(texts)

    logging.info(
        "💾 Saving original version…"
        " (for https://github.com/Phlya/adjustText/issues/138)"
    )
    fig.savefig("output-original.png")

    logging.info("🔧 Adjusting texts…")
    n_iter = adjust_text(
        texts,
        lim=15,
        expand_text=(1.15, 1.3),
        arrowprops=dict(
            color="gray",
            alpha=0.4,
            arrowstyle="-",
        ),
    )
    logging.info(f"🔧 Texts adjustment iterated {n_iter} time(s).")

logging.info("💾 Saving…")
fig.savefig("output.png")

logging.info("🎉 Finished.")
