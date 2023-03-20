# iterate through all files in the probesExp folder
import os

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def visualize():
    # data
    xVar = [] # number of threads
    yVar = [] # number of jobs
    colors = [] # colors for the legend
    # go through the files
    path = os.getcwd() + "\\Logs\\csExp"
    for file in os.listdir(path):
        if "ZTC" in file and "tsLog" not in file:
            # read the data
            fileData = [int(elem) for elem in open(path + "\\" + file, "r").readlines()[0::2]]
            # add the data to the arrays
            xVar.append([200, 100, 10, 1] * 5)
            yVar.append(fileData)
            # add the color to the legend
            if "ZTC_" in file: 
                # one core
                colors.append(("One Core", "red"))
            elif "ZTC0-1_" in file:
                # two cores
                colors.append(("Two Cores", "green"))
            elif "ZTC0-4_" in file:
                # four cores
                colors.append(("Four Cores", "purple"))
    # plot the data
    fig, ax = plt.subplots()
    for i in range(len(xVar)):
        ax.scatter(xVar[i], yVar[i], color=colors[i][1])
    # add the legend
    colors = [("One Core", "red"), ("Two Cores", "green"), ("Four Cores", "purple")]
    legend = []
    for i in range(len(colors)):
        legend.append(mpatches.Patch(color=colors[i][1], label=colors[i][0]))
    ax.legend(handles=legend)
    # label the axes
    ax.set_xlabel("Number of Threads")
    ax.set_ylabel("Number of Jobs Completed")
    # show the plot
    plt.show()
    # save the plot
    plt.savefig(f"{os.getcwd()}\\Figures\\csExp\\variableCoreTest.png")

if __name__ == "__main__":
    visualize()
