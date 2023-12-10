#! /usr/bin/env python

# Adjusting the plot based on the new requirements
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# from datetime import datetime
import yaml
import textwrap
import fire


def plot_timeline(ymlfile="inp.yml", outfile="gg.png"):
    # Sample data for two axes
    tls = yaml.load(open(ymlfile), Loader=yaml.FullLoader)

    # Plotting with reduced margin between axes and text closer to bars and points
    np = len(tls["timeline"])
    fig, axes = plt.subplots(
        np, 1, figsize=(12, np * 1.5), sharex=True, gridspec_kw={"hspace": 0}
    )

    fig.suptitle(tls["title"])
    # Upper Axis: Point Events
    for ax, timeline in zip(axes, tls["timeline"]):
        print(timeline)
        ax.set_ylabel(timeline["name"])
        ax.grid(True, alpha=0.5)
        marker = "s" if "marker" not in timeline else timeline["marker"]
        for event in timeline["events"]:
            event["name"] = textwrap.fill(event["name"], 15)
            ax.set_yticks([])
            if "time" in event:
                ax.plot(
                    event["time"],
                    0,
                    marker,
                    color="b" if not "color" in event else event["color"],
                    markersize=10,
                    alpha=0.5,
                )
                ax.text(
                    event["time"],
                    0.01,
                    event["name"],
                    ha="center",
                    va="center",
                    rotation=45 if "angle" not in timeline else timeline["angle"],
                )
            elif "start" in event:
                y = 0 if "y" not in event else event["y"]
                ax.hlines(
                    y,
                    event["start"],
                    event["end"],
                    linewidth=30,
                    alpha=0.3,
                    color="r" if not "color" in event else event["color"],
                )
                ax.text(
                    (event["start"] + (event["end"] - event["start"]) * 0.5),
                    y,
                    event["name"],
                    ha="center",
                    va="center",
                    rotation=45 if "angle" not in timeline else timeline["angle"],
                )

    # Formatting
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Show plot
    fig.savefig(outfile, dpi=200)
    print("Saved to ", outfile)


if __name__ == "__main__":
    fire.Fire(plot_timeline)
