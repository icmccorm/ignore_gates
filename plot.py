import matplotlib.pyplot as plt
import pandas as pd
from numpy import *
import os

if(not os.path.exists('./original.csv') or not os.path.exists('./nogates.csv')):
    print("Requires ./original.csv and ./nogates.csv in root directory.")
    print("Download the corresponding job info files from StarExec:")
    print("     * original.csv : CaDiCaL-sc2021")
    print("     * nogates.csv : modded CaDiCaL, ignoring gate literals")
    exit(1)
original = pd.read_csv("./original.csv")
nogates = pd.read_csv("./nogates.csv")

if(os.path.exists('./incorrect.txt')): os.remove("./incorrect.txt")
incorrect = open("./incorrect.txt", "a")

print()
print("------- Unknown Results -------")
original_unknown_benchmark_ids = original[original['result'] == 'UNKNOWN']
original_crashed = original_unknown_benchmark_ids[original_unknown_benchmark_ids['status'] == 'complete']
print("* Cadical: " + str(len(original_unknown_benchmark_ids)))
original_timed_out = original_unknown_benchmark_ids[original_unknown_benchmark_ids['status'] == 'complete']
print("     - # Timed Out: " + str(len(original_unknown_benchmark_ids) - len(original_crashed)))
print("     - # Crashed: " + str(len(original_crashed)))

nogates_unknown_benchmark_ids = nogates[nogates['result'] == 'UNKNOWN']
nogates_crashed = nogates_unknown_benchmark_ids[nogates_unknown_benchmark_ids['status'] == 'complete']
print("* Cadical w/o Gates: " + str(len(nogates_unknown_benchmark_ids)))
print("     - # Timed Out: " + str(len(nogates_unknown_benchmark_ids) - len(nogates_crashed)))
print("     - # Crashed: " + str(len(nogates_crashed)))

print("")
original = original.loc[~original['benchmark id'].isin(original_unknown_benchmark_ids['benchmark id'])]
original = original.loc[~original['benchmark id'].isin(nogates_unknown_benchmark_ids['benchmark id'])]
nogates = nogates.loc[~nogates['benchmark id'].isin(original_unknown_benchmark_ids['benchmark id'])]
nogates = nogates.loc[~nogates['benchmark id'].isin(nogates_unknown_benchmark_ids['benchmark id'])]

original = original.sort_values("benchmark id")
nogates = nogates.sort_values("benchmark id")

numDiffering = 0
differing = []
numSat = 0
numUnsat = 0
for i in range(0, len(original)):
    if(original['result'].iloc[i] != nogates['result'].iloc[i]):
        if(str(nogates['result'].iloc[i]) == "UNSAT"):
            numUnsat += 1
        else:
            numSat += 1
        differing.append(str(original['benchmark'].iloc[i]))
        benchname = str(original['benchmark'].iloc[i])
        benchname = benchname[benchname.find('/') + 1:-1] + "\n"
        incorrect.write(benchname)
        numDiffering += 1
print("------- Incorrect Results -------")
print("* Total Incorrect: " + str(numDiffering))
print("     - # Incorrectly SAT: " + str(numSat))
print("     - # Incorrectly UNSAT: " + str(numUnsat))
print()

original = original[~original['benchmark'].isin(differing)]
nogates = nogates[~nogates['benchmark'].isin(differing)]
original = original.sort_values("benchmark id")
nogates = nogates.sort_values("benchmark id")

num_unsat = len(original[original['result'] == 'UNSAT'])
num_sat = len(original) - num_unsat


def calculateDiff(key, original, nogates):
    diff = []
    usedMore = []
    usedLess = []
    usedSame = []
    for i in range(0, len(nogates[key])):
        currDiff = (original[key].iloc[i] - nogates[key].iloc[i])
        if(currDiff > 0): 
            usedLess.append(str(nogates['benchmark'].iloc[i]))
        elif(currDiff < 0):
            usedMore.append(str(nogates['benchmark'].iloc[i]))
        else:
            usedSame.append(str(nogates['benchmark'].iloc[i]))
        diff.append(currDiff)

    return (diff, usedLess, usedSame, usedMore)

print("* Total results to compare: " + str(len(original)))
print("     - # SAT: " + str(num_sat))
print("     - # UNSAT: " + str(num_unsat))

cpu_time_diff = calculateDiff("cpu time", original, nogates)
memory_usage_diff = calculateDiff("memory usage", original, nogates)

cdiff = cpu_time_diff[0]
cdiff.sort()

mdiff = memory_usage_diff[0]
mdiff.sort()

fig, axs = plt.subplots(2)
t = linspace(1, len(memory_usage_diff[0]), len(memory_usage_diff[0]))
axs[0].plot(t, cdiff, 'b')
axs[0].axhline(y=0, linestyle='-')
axs[0].title.set_text("Reduction in CPU time (sec) from ignoring gate literals")
axs[0].axes.xaxis.set_visible(False)
axs[1].plot(t, mdiff, 'r')
axs[1].axhline(y=0, linestyle='-')
axs[1].title.set_text("Reduction in memory usage (MB) from ignoring gate literals")
axs[1].axes.xaxis.set_visible(False)
plt.subplots_adjust(hspace = .75)
plt.show()

#plt.plot(t, memory_usage_diff, 'r')
#plt.axhline(y=0, linestyle='-')
#plt.show()

#types to compare (with statistically significant differences FOR AUX and AUX+CONFLICT):
    # timed out with our approach, but didn't with cadical
    # used more CPU than cadical
    # used less CPU than cadical
    # used more memory than cadical
    # used less memory than cadical