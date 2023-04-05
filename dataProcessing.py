import os
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import math

# read lines from a file
def read_file(file):
    # add file lines to list
    with open(file, 'r') as f:
        return f.readlines()
    

def exp_func(x, a, b, c):
    return a * np.exp(-b * x) + c

def lin_func(x, a, b):
    return a * x + b

# main method
if __name__ == "__main__":
    includeFirstElem = True
    xVal = []
    yVal = []
    # get files in csExp dir
    files = os.listdir("Results/csExp")
    # process each file
    for file in files:
        # only read data from files with key word
        if "school0-1" not in file:
            continue
        # read file
        lines = read_file("Results/csExp/" + file)
        # process data
        xTemp = [counter for counter in range(0, 11)] * 10
        if not includeFirstElem:
            xTemp = [x for x in xTemp if x != 0]
        xVal += xTemp # add the probes
        yTemp = eval(lines[19])
        # remove every tenth value of yTemp including the first one
        if not includeFirstElem:
            idxs = [0]
            while idxs[-1] < len(yTemp):
                idxs.append(idxs[-1] + 11)
            yTemp = [yTemp[i] for i in range(len(yTemp)) if i not in idxs]
        yVal += yTemp # add the jobs
    # perform regression
    xVar = np.array(xVal)
    yVar = np.array(yVal)
    popt, pcov = curve_fit(exp_func, xVar, yVar, maxfev=10000)
    a_opt, b_opt, c_opt = popt
    a_err, b_err, c_err = np.sqrt(np.diag(pcov))
    plt.plot(xVar, yVar, 'b.', label='data')
    plt.plot(xVar, exp_func(xVar, *popt), 'r-', label='fit')
    plt.legend()
    plt.show()
    # output results
    print(f"y = {a_opt:.2f} * exp({b_opt:.2f} * x) + {c_opt:.2f}")
    print(f"{a_err:.2f}, {b_err:.2f}, {c_err:.2f}")
    # output percent diff in first/second jobs
    if includeFirstElem:
        print(f"Avg percent diff: {(sum(yVal[0::11]) - sum(yVal[1::11])) / sum(yVal[0::11]) * 100:.2f}%")
