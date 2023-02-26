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
    RUNS = 8  # number of runs in each experiment
    numArr = RUNS * 2
    # process into data points
    jobs = [lines[i] for i in range(0, len(lines), 2)]
    events = [lines[i + 1] for i in range(0, len(lines), 2)]
    # split into tracing and not tracing runs
    data = [[] for _ in range(numArr)]  # runs and log size
    for counter in range(0, len(lines)):
        data[counter % numArr].append(lines[counter])
    # get totals
    allJobs = [sum(data[i]) for i in range(0, numArr, 2)]
    totalJobs = sum(allJobs)
    allEvents = [sum(data[i]) for i in range(1, numArr, 2)]
    totalEvents = sum(allEvents)
    # process relative amounts
    relJobs = [round(100 * (float(allJobs[i]) / totalJobs), 5) for i in range(0, len(allJobs))]
    relEvents = [round(100 * (float(allEvents[i]) / totalEvents), 5) for i in range(0, len(allEvents))]
    # return relative values
    return relJobs, relEvents, allJobs, allEvents, jobs, events


def linReg(allEvents, allJobs, var):
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
    return f"jobs = {reg.coef_[0][0]} * {var} + {reg.intercept_[0]}", f"r^2 = {reg.score(x, y)}"


def main(args):
    run = args[1]
    # read file
    lines = read_file("Logs/log_" + run + ".txt")
    # process data
    relJobs, relEvents, allJobs, allEvents, jobs, events = get_data(lines)
    # get the regression
    regA, errA = linReg(np.array(events), np.array(jobs), "events")
    # regB, errB = linReg(np.array([0, 1, 2, 1, 1, 3, 6, 10] * 10), np.array(jobs), "probes")
    regB, errB = linReg(np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 10), np.array(jobs), "probes")
    # write results to file
    with open("Results/result_" + run + ".txt", 'w') as f:
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
        # runs = ["2", "3", "4", "5", "C1", "C2"]
        # runs = ["aws_1_X", "cloudlab_1_X", "cloudlab_2_X", "home_1_ps", "home_2_per", "home_3_ps"]
        runs = ["csExp_home_1_ps", "csExp_cloudlab_1", "csExp_aws_1"]
        for run in runs:
            args = ["", run, 10, "20", 500, 1500, "powersave"]
            # args = []
            main(args)
