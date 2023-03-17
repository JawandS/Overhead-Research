# iterate through all files in the probesExp folder
import os

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# perform a logarithmic regression on the data
def csReg(serverType, governor):
    allJobs = []
    allProbes = []
    path = os.getcwd() + "\\Results\\csExp"
    for file in os.listdir(path):
        if serverType in file and governor in file:
            lines = open(path + "\\" + file, "r").readlines()
            allProbes = allProbes + [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 10 # add the probes to array
            allJobs = allJobs + eval(lines[19]) # add the jobs to array
    # convert arrays to numpy arrays
    x = np.array(allProbes)
    y = np.array(allJobs)
    # perform regression
    m, b = np.polyfit(x, np.log(y), 1)
    # print the results
    print(f"{serverType} {governor}: {m}x + {b}")
    # print the error
    print(f"Error: {np.sum(np.abs(np.log(y) - (m * x + b)))}")
    

# read in data from all experiments
def visualize(serverType, governor, experiment, timePerJob):
    allJobs = []
    allEvents = []
    colors = [] # number of cores for AWS instance
    path = os.getcwd() + "\\Results\\" + experiment
    for file in os.listdir(path):
        if serverType in file and governor in file and "B" not in file:
            lines = open(path + "\\" + file, "r").readlines()
            if timePerJob:
                allJobs.append([round(20.0 / val, 3) for val in eval(lines[19])])
            else:
                allJobs.append(eval(lines[19]))
            if experiment == "probesExp":
                allEvents.append(eval(lines[21]))
            else:  # context switch experiment
                allEvents.append([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 10)
                # if "C0" in file:
                #     colors.append(("One Core", "red"))
                # elif "0-1" in file:
                #     colors.append(("Two Cores", "green"))
                # elif "0-3" in file:
                #     colors.append(("Four Cores", "purple"))
                # elif "0-7" in file:
                #     colors.append(("Eight Cores", "blue"))
                if "1_" in file or "1B_" in file:
                    colors.append(("One Core", "red"))
                elif "2_" in file:
                    colors.append(("Two Cores", "green"))
                elif "8_" in file:
                    colors.append(("Eight Cores", "blue"))

    # create a scatter plot of the data
    fig, ax1 = plt.subplots(figsize=(10, 10))
    # label the y-axis as the number of jobs completed
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
            plt.scatter(allEvents[idx], allJobs[idx], c=colors[idx][1])
        else:
            plt.scatter(allEvents[idx], allJobs[idx], label=f"Run {idx + 1}")
    if colors:
        red_patch = mpatches.Patch(color='red', label='One Core')
        green_patch = mpatches.Patch(color='green', label='Two Cores')
        purple_patch = mpatches.Patch(color='purple', label='Four Cores')
        blue_patch = mpatches.Patch(color='blue', label='Eight Cores')
        plt.legend(handles=[red_patch, green_patch, purple_patch, blue_patch])
    if experiment == "probesExp":
        ax1.set_title(f"Events to Jobs for {serverType} {governor}")
    else:
        ax1.set_title(f"Probes to Jobs for {serverType} {governor}")
    # set the y min as 0
    ax1.set_ylim(bottom=0)
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


# general plot using x/y vars
def genPlot(computerName, experiment, xVar, yVar):
    x = []
    y = []
    path = os.getcwd() + "\\Results\\" + experiment
    # get data 
    for file in os.listdir(path):
        if computerName in file:
            lines = open(path + "\\" + file, "r").readlines()
            # independent var
            if xVar == "probes":
                x = x + [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 10
            elif xVar == "cores":
                if "aws_" in file:
                    x = x + [1] * 110
                elif "aws2" in file:
                    x = x + [2] * 110
                elif "aws8" in file:
                    x = x + [8] * 110
            elif xVar == "events":
                x = x + eval(lines[21])
            # dependent var
            if yVar == "jobs":
                y = y + eval(lines[19])
            elif yVar == "events":
                y = y + eval(lines[21])
    # plot the data
    fig, ax1 = plt.subplots(figsize=(10, 10))
    # labels
    ax1.set_xlabel(xVar)
    ax1.set_ylabel(yVar)
    ax1.set_title(f"{xVar} to {yVar} for {computerName}")
    # plot the points
    plt.scatter(x, y)
    # save the figure
    plt.savefig(f"{os.getcwd()}\\Figures\\{experiment}\\{computerName}_{xVar}To{yVar}.png")


def runManual():
    servers = [("aws_", ""), ("aws2", ""), ("aws8", ""), ("cloudlab", ""), ("home", "per"), ("home", "ps"), ("school_", "per"), ("school_", "ps"), ("schoolC0", "")]
    # servers = [("aws", "")]  # for testing
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


def runAutomatic():
    import sys
    args = sys.argv
    machine = args[1]
    experimentType = args[2]
    visualize(machine, "", experimentType, False)
    # for machine in ["school0-1", "school0-3", "school0-7"]:
    #     experimentType = "csExp"


if __name__ == "__main__":
    # runManual()
    runAutomatic() # machine, experiment type
    # csReg("schoolC0", "")
    # genPlot("schoolC0", "csExp", "events", "jobs")