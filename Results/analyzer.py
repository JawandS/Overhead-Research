# iterate through all files in the probesExp folder
import os

import matplotlib.pyplot as plt


# read in data from all experiments
def visualize(serverType, governor="", experiment="probesExp"):
    allJobs = []
    allEvents = []
    path = os.getcwd() + "\\Results\\" + experiment
    for file in os.listdir(path):
        if serverType in file and governor in file:
            lines = open(path + "\\" + file, "r").readlines()
            allJobs.append(eval(lines[19]))
            if experiment == "probesExp":
                allEvents.append(eval(lines[21]))
            else:  # context switch experiment
                allEvents.append([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 10)

    # create a scatter plot of the data
    fig, ax1 = plt.subplots(figsize=(10, 10))
    for idx in range(len(allEvents)):
        plt.scatter(allEvents[idx], allJobs[idx], label=f"Run {idx + 1}")
    if experiment == "probesExp":
        ax1.set_title(f"Events to Jobs for {serverType} {governor}")
    else:
        ax1.set_title(f"Probes to Jobs for {serverType} {governor}")
    fig.show()
    plt.show()
    # fig.savefig(f"Figures/{idVal}_eventsToJobs.png")


servers = [("aws", ""), ("cloudlab", ""), ("home", "per"),
           ("home", "ps"), ("school", "per"), ("school", "ps")]
serversNoGov = [("aws", ""), ("cloudlab", ""), ("home", ""), ("school", "")]
allServers = [("aws", ""), ("cloudlabA", ""), ("cloudlabB", "per"), ("cloudlabB",
                                                                     "ps"), ("home", "per"), ("home", "ps"), ("school", "per"), ("school", "ps")]
experimentType = ["probesExp", "csExp"][int(input("probesExp (0) or csExp(1): "))]
if experimentType == "csExp":
    for server, governor in servers:
        visualize(server, governor, experimentType)
else:
    for server, governor in allServers:
        visualize(server, governor, experimentType)