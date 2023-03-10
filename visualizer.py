import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def linePlot(run_num):
    # line plot of the events compared to jobs and probes
    with open(f"Results/result_{run_num}.txt") as file:
        #  get data
        lines = [line.rstrip() for line in file]
        totalJobs = eval(lines[16])
        totalEvents = eval(lines[18])
        numProbes = [0, 1, 2, 1, 1, 3, 6, 10] * 10
        # numProbes = [0, 1, 2, 3, 4] * 10
        probeType = ["X", "A", "B", "C", "D", "E", "F", "G"] * 10
        # probeType = ["X", 1, 2, 3, 4] * 10
        df = pd.DataFrame({
            'Probe Type': probeType,  # 10 runs
            'Number of Tracepoints': numProbes,
            'Number of Events': totalEvents,
            'Jobs Completed': totalJobs,
        })
        # plot a scatter plot with regression
        fig, ax1 = plt.subplots(figsize=(10, 10))
        sns.scatterplot(x='Number of Events', y='Jobs Completed', data=df, ax=ax1, hue='Probe Type')
        sns.despine(fig)
        fig.savefig(f"Figures/{run_num}_events.png")
        # close the plot
        plt.close()
        # plot probes to jobs
        fig, ax1 = plt.subplots(figsize=(10, 10))
        sns.scatterplot(x='Number of Tracepoints', y='Jobs Completed', data=df, ax=ax1, hue='Probe Type')
        sns.despine(fig)
        fig.savefig(f"Figures/{run_num}_probes.png")


if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        run_num = args[1]
        linePlot(run_num)
    else:
        # runs = ["aws_1_X", "cloudlab_1_X", "cloudlab_2_X", "home_1_ps", "home_2_per", "home_3_ps"]
        runs = ["home_csVariant_2_per"]
        for run_num in runs:
            linePlot(run_num)
