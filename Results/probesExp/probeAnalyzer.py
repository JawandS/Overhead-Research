import pandas as pd
import os


def runAnalysis(code):
    # data collection
    machines = ["aws", "cloudlabA", "cloudlabB", "home", "school"]
    print(f"Analysis of {machines[code]}")
    probeClass = ["X", "rcu", "syscalls", "sched", "sched", "timer", "cpu", "syscalls"]
    probeTypes = ["X", "rcu_utilization", "sys_enter_nanosleep", "sched_switch", "sched_wakeup", "time_start", "cpuhp_enter", "sys_enter_getcpu"]
    typesToJobs = {type: 0 for type in probeTypes}
    typeToEvents = {type: 0 for type in probeTypes}
    # iteratre though files in current directory (probesExp)
    directory = os.getcwd() + "\\Results\\probesExp\\"
    machineType = machines[code]
    for file in os.listdir(directory):
        if file.endswith(".txt") and machineType in file:
            with open(directory + file, "r") as f:
                data = f.readlines()
                # number of jobs
                jobs = eval(data[19])
                for i in range(0, len(probeTypes)):
                    typesToJobs[probeTypes[i]] += jobs[i]
                # number of events
                events = eval(data[21])
                for i in range(0, len(probeTypes)):
                    typeToEvents[probeTypes[i]] += events[i]

    # change to percentages
    totalJobs = sum(typesToJobs.values())
    totalEvents = sum(typeToEvents.values())
    for type in typesToJobs.keys():
        typesToJobs[type] = round(typesToJobs[type] / totalJobs * 100, 2)
        typeToEvents[type] = round(typeToEvents[type] / totalEvents * 100, 2)
    # print results
    df = pd.DataFrame([typesToJobs, typeToEvents], index=["jobs (%)", "events (%)"])
    # {type: round(typeToEvents[type] / typesToJobs[type], 1) for type in typesToJobs.keys()}
    print(df.to_string())
    print("\n")

# go through all machine codes
for i in range(0, 5):
    runAnalysis(i)
