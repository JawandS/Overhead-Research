import sys

import numpy as np
from sklearn.linear_model import LinearRegression


def read_file(file):
    # add file lines to list
    lines = []
    with open(file, 'r') as f:
        for line in f:
            if line != '\n' and line != "":
                if ".txt" in line:
                    lines.append(float(line.split(" ")[0]))
                else:
                    lines.append(float(line))
    return lines


def get_data(lines):
    numVars = 11  # number of different independent variables
    runs = 10  # number of runs in each experiment
    jobs = [lines[i] for i in range(0, len(lines), 2)]
    events = [lines[i + 1] for i in range(0, len(lines), 2)]
    # get totals
    allJobs = [sum(jobs[i: numVars * runs: numVars]) for i in range(numVars)]
    totalJobs = sum(allJobs)
    allEvents = [sum(events[i: numVars * runs: numVars]) for i in range(numVars)]
    totalEvents = sum(allEvents)
    # process relative amounts
    relJobs = [round(100 * (float(allJobs[i]) / totalJobs), 5) for i in range(0, len(allJobs))]
    relEvents = [round(100 * (float(allEvents[i]) / totalEvents), 5) for i in range(0, len(allEvents))]
    # return relative values
    return relJobs, relEvents, allJobs, allEvents, jobs, events


def linReg(allEvents, allJobs, xVar, yVar):
    # get the data
    x = allEvents  # number of events
    y = allJobs  # number of jobs
    # reshape the arrays to make them 2-dimensional
    x = x.reshape(-1, 1)
    y = y.reshape(-1, 1)
    # get the regression
    reg = LinearRegression()
    reg.fit(x, y)
    # return the results
    return f"{yVar} = {reg.coef_[0][0]} * {xVar} + {reg.intercept_[0]}", f"r^2 = {reg.score(x, y)}"


def main(args):
    run = args[1]
    # read file
    lines = read_file("Logs/probesExp/log_" + run + ".txt")
    # process data
    relJobs, relEvents, allJobs, allEvents, jobs, events = get_data(lines)
    # get the regressions
    regA, errA = linReg(np.array(events), np.array(jobs), "events", "jobs")
    regB, errB = linReg(np.array([0, 1, 1, 1, 1, 1, 1, 1] * 10), np.array(jobs), "probes", "jobs")
    regC, errC = linReg(np.array([0, 1, 1, 1, 1, 1, 1, 1] * 10), np.array(events), "probes", "events")
    # write results to file
    with open("Results/probesExp/result_" + run + ".txt", 'w') as f:
        f.write(f"iterations {args[2]} | time {args[3]} | threads {args[4]} | depth {args[5]} | governor {args[6]}\n")
        f.write("Relative amounts of jobs\n")
        f.write(f"{relJobs}\n")
        f.write("Relative amounts of events\n")
        f.write(f"{relEvents}\n")
        f.write("Total amounts of jobs\n")
        f.write(f"{allJobs}\n")
        f.write("Total amounts of events\n")
        f.write(f"{allEvents}\n")
        f.write("Events to Jobs\n")
        f.write(f"{regA}\n")
        f.write(f"{errA}\n")
        f.write("Probes to Jobs\n")
        f.write(f"{regB}\n")
        f.write(f"{errB}\n")
        f.write("Probes to Events\n")
        f.write(f"{regC}\n")
        f.write(f"{errC}\n")
        f.write("All jobs\n")
        f.write(f"{jobs}\n")
        f.write("All events\n")
        f.write(f"{events}\n")


if __name__ == "__main__":
    # get the run number
    args = sys.argv
    if len(args) > 1:
        run = args[1]
        main(args)
    else:
        runs = ["csExp_aws_1", "csExp_cloudlab_1", "csExp_home_1_ps", "csExp_aws_2", "csExp_cloudlab_2",
                "csExp_home_2_per", "csExp_aws_3", "csExp_cloudlab_3", "csExp_home_3_ps", "csExp_aws_4",
                "csExp_cloudlab_4", "csExp_home_4_per"]
        for run in runs:
            args = ["", run, 10, "20", 500, 1500, "powersave"]
            # args = []
            main(args)
