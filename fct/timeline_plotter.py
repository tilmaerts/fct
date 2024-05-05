#! /usr/bin/env python

# Adjusting the plot based on the new requirements
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import yaml
import textwrap
import fire


def plot_timeline(ymlfile=None, outfile=None):
    print(ymlfile)
    if ymlfile == None:
        exit("input timeline file")

    if not ymlfile.endswith(".yml"):
        print("Input file should be a .yml file")
        return
    if not outfile:
        outfile = ymlfile.split(".yml")[0] + ".png"
    # Sample data for two axes
    tls = yaml.load(open(ymlfile), Loader=yaml.FullLoader)

    if "xticks" in tls:
        if tls["xticks"] == "weekdays":
            weekday_labels = True
    else:
        weekday_labels = False
    # Plotting with reduced margin between axes and text closer to bars and points
    np = len(tls["timeline"])
    fig, axes = plt.subplots(
        np, 1, figsize=(12, np * 1.0), sharex=True, gridspec_kw={"hspace": 0}
    )

    if "title" in tls:
        fig.suptitle(tls["title"])
    # Upper Axis: Point Events
    for ax, timeline in zip(axes, tls["timeline"]):
        # print(timeline)
        ax.set_ylabel(timeline["name"])
        ax.grid(True, alpha=0.5)
        marker = "s" if "marker" not in timeline else timeline["marker"]
        for event in timeline["events"]:
            event["name"] = textwrap.fill(event["name"], 15)
            ax.set_yticks([])
            ax.set_ylim(-1.3, 1.3)
            if "time" in event:
                y = 0 if "y" not in event else event["y"]
                ax.axvline(
                    event["time"],
                    color="b" if not "color" in event else event["color"],
                    alpha=0.5,
                )
                ax.text(
                    event["time"],
                    y,
                    event["name"],
                    ha="center",
                    va="center",
                    rotation=30 if "angle" not in timeline else timeline["angle"],
                    clip_on=True,
                    # transform=ax.transAxes,
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
                    rotation=30 if "angle" not in timeline else timeline["angle"],
                )
    # If weekday_labels option is True, format x-axis labels as weekdays
    if weekday_labels:
        axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%A"))
    else:
        # Formatting
        axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=30)
    plt.tight_layout()
    # Show plot
    fig.savefig(outfile, dpi=200)
    print("Saved to ", outfile)


def main():
    fire.Fire(plot_timeline)


if __name__ == "__main__":
    main()
    # fire.Fire(plot_timeline)
