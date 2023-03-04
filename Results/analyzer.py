# iterate through all files in the probesExp folder
import os

import matplotlib.pyplot as plt


# read in data from all experiments
def visualize(serverType, governor=""):
    allJobs = []
    allEvents = []
    for file in os.listdir("csExp"):
        if serverType in file and governor in file:
            lines = open("csExp/" + file, "r").readlines()
            allJobs.append(eval(lines[19]))
            allEvents.append(eval(lines[21]))

    # create a scatter plot of the data
    fig, ax1 = plt.subplots(figsize=(10, 10))
    for idx in range(len(allEvents)):
        plt.scatter(allEvents[idx], allJobs[idx], label=f"Run {idx + 1}")
    ax1.set_title(f"Events to Jobs for {serverType} {governor}")
    fig.show()
    plt.show()
    # fig.savefig(f"Figures/{idVal}_eventsToJobs.png")


servers = [("aws", ""), ("cloudlab", ""), ("home", "per"), ("home", "ps"), ("school", "per"), ("school", "ps")]
serversNoGov = [("aws", ""), ("cloudlab", ""), ("home", ""), ("school", "")]
for server, governor in serversNoGov:
    visualize(server, governor)

# serverTypes = [("aws", "per", "home", "school", "cloudlab", "cloudlabA", "cloudlabC"]
# print([f"{idx}: {serverType}" for idx, serverType in enumerate(serverTypes)])
# idVal = int(input("Server number: "))
# governor = ""
# if serverTypes[idVal] in ["home", "school", "cloudlabB"]:
#     governor = input("Governor Types (per/ps): ")
