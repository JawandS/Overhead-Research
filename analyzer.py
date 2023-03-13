# iterate through all files in the probesExp folder
import os

import matplotlib.pyplot as plt


# read in data from all experiments
def visualize(serverType, governor, experiment, timePerJob):
    allJobs = []
    allEvents = []
    colors = [] # number of cores for AWS instance
    path = os.getcwd() + "\\Results\\" + experiment
    for file in os.listdir(path):
        if serverType in file and governor in file:
            lines = open(path + "\\" + file, "r").readlines()
            if timePerJob:
                allJobs.append([round(20.0 / val, 3) for val in eval(lines[19])])
            else:
                allJobs.append(eval(lines[19]))
            if experiment == "probesExp":
                allEvents.append(eval(lines[21]))
            else:  # context switch experiment
                allEvents.append([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 10)
                # if "aws_" in file:
                #     colors.append(("One Core", "red"))
                # elif "aws2" in file:
                #     colors.append(("Two Cores", "green"))
                # elif "aws8" in file:
                #     colors.append(("Eight Cores", "blue"))

    # create a scatter plot of the data
    fig, ax1 = plt.subplots(figsize=(10, 10))
    # labe the y-axis as the number of jobs completed
    if not timePerJob:
        ax1.set_ylabel("Jobs Completed")
    else:
        ax1.set_ylabel("Time per Job (s)")
    # label the x-axis as the number of events or probes
    if experiment == "probesExp":
        ax1.set_xlabel("Events")
    else:
        ax1.set_xlabel("Number of Context Switch Probes")
    for idx in range(len(allEvents)):
        if colors:
            plt.scatter(allEvents[idx], allJobs[idx], label=colors[idx][0])
        else:
            plt.scatter(allEvents[idx], allJobs[idx], label=f"Run {idx + 1}")
    if colors:
        plt.legend()
    if experiment == "probesExp":
        ax1.set_title(f"Events to Jobs for {serverType} {governor}")
    else:
        ax1.set_title(f"Probes to Jobs for {serverType} {governor}")
    # fig.show()
    if governor:
        if timePerJob:
            plt.savefig(f"{os.getcwd()}\\Figures\\{experiment}TPJ\\{serverType}_{governor}.png")
        else:
            plt.savefig(f"{os.getcwd()}\\Figures\\{experiment}\\{serverType}_{governor}.png")
    else:
        if timePerJob:
            plt.savefig(f"{os.getcwd()}\\Figures\\{experiment}TPJ\\{serverType}.png")
        else:
            plt.savefig(f"{os.getcwd()}\\Figures\\{experiment}\\{serverType}.png")
    plt.close()


servers = [("aws_", ""), ("aws2", ""), ("aws8", ""), ("cloudlab", ""), ("home", "per"), ("home", "ps"), ("school", "per"), ("school", "ps")]
serversNoGov = [("aws", ""), ("cloudlab", ""), ("home", ""), ("school", "")]
allServers = [("aws", ""), ("cloudlabA", ""), ("cloudlabB", "per"), ("cloudlabB", "ps"), ("home", "per"), ("home", "ps"), ("school", "per"), ("school", "ps")]
newServers = [("schoolC0", "")]
experimentType = ["probesExp", "csExp", "csExpTPJ"][int(input("probesExp (0) or csExp(1) or csExpTPJ (2): "))]
if experimentType == "csExp":
    for server, governor in servers:
        visualize(server, governor, experimentType, False)
elif experimentType == "probesExp":
    for server, governor in allServers:
        visualize(server, governor, experimentType, False)
else:  # context switch experiment with time per job
    for server, governor in servers:
        visualize(server, governor, "csExp", True)
