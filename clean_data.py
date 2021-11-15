import matplotlib.pyplot as plt
import pandas as pd
from numpy import *
import math
import os
import subprocess

if(not os.path.exists('./original.csv') or not os.path.exists('./nogates.csv')):
    print("Requires ./original.csv and ./nogates.csv in root directory.")
    print("Download the corresponding job info files from StarExec:")
    print("     * original.csv : CaDiCaL-sc2021")
    print("     * nogates.csv : modded CaDiCaL, ignoring gate literals")
    exit(1)
original = pd.read_csv("./original.csv")
nogates = pd.read_csv("./ignore_select.csv")

print()
print("------- Unknown Results -------")

original_unknown_benchmark_ids = original[original['result'] == 'UNKNOWN']
original_crashed = original_unknown_benchmark_ids[original_unknown_benchmark_ids['status'] == 'complete']
original_timed_out = original_unknown_benchmark_ids[original_unknown_benchmark_ids['status'] != 'complete']

print("* Cadical: " + str(len(original_unknown_benchmark_ids)))
print("     - # Timed Out: " + str(len(original_unknown_benchmark_ids) - len(original_crashed)))
print("     - # Crashed: " + str(len(original_crashed)))

nogates_unknown_benchmark_ids = nogates[nogates['result'] == 'UNKNOWN']
nogates_crashed = nogates_unknown_benchmark_ids[nogates_unknown_benchmark_ids['status'] == 'complete']
nogates_timed_out = nogates_unknown_benchmark_ids[nogates_unknown_benchmark_ids['status'] != 'complete']

print("* Cadical w/o Gates: " + str(len(nogates_unknown_benchmark_ids)))
print("     - # Timed Out: " + str(len(nogates_unknown_benchmark_ids) - len(nogates_crashed)))
print("     - # Crashed: " + str(len(nogates_crashed)))

both_timed_out = nogates_timed_out[nogates_timed_out['benchmark'].isin(original_timed_out['benchmark'])]
both_crashed = nogates_crashed[nogates_crashed['benchmark'].isin(original_crashed['benchmark'])]

print("* Timed out for both: " + str(len(both_timed_out)))
if(len(nogates_timed_out) > len(both_timed_out)):
    print("     - " + str(len(nogates_timed_out) - len(both_timed_out)) + " additional for Cadical w/o Gates")
else:
    print("     - " + str(len(original_timed_out) - len(both_timed_out)) + " additional for Cadical")

print("* Crashed for both: " + str(len(both_crashed)))
if(len(nogates_crashed) > len(both_crashed)):
    print("     - " + str(len(nogates_crashed) - len(both_crashed)) + " additional for Cadical w/o Gates")
else:
    print("     - " + str(len(original_crashed) - len(both_crashed)) + " additional for Cadical")


original_solved = original[original['result'].isin(["UNSAT", "SAT-INCORRECT"])]
nogates_solved = nogates[nogates['result'].isin(["UNSAT", "SAT-INCORRECT"])]

print("")

nogates_solved_matching = nogates_solved[nogates_solved['benchmark'].isin(original_solved['benchmark'])]

num_unsat = 0
num_sat = 0
original_solved = original_solved[original_solved['benchmark'].isin(nogates_solved['benchmark'])]
filtered_frame = []
for row in original_solved.itertuples():
    row_benchmark = row[2]
    row_result = row[12]
    nogates_row = nogates_solved[nogates_solved['benchmark'] == row_benchmark]
    if(len(nogates_row) > 0):
        nogates_row_result = nogates_row.iloc[0]['result']
        if(nogates_row_result != row_result):
            if(nogates_row_result == 'UNSAT'):
                num_unsat += 1
            else:
                num_sat += 1
            benchname = row_benchmark[row_benchmark.find('/') + 1:]
        else:
            filtered_frame.append(nogates_row.iloc[0])
print("")

print("------- Different SAT/UNSAT Results -------")
print("* Total Different: " + str(num_unsat + num_sat))
print("     - # Different SAT: " + str(num_sat))
print("     - # Different UNSAT: " + str(num_unsat))
print()

num_matching = len(filtered_frame) + len(both_timed_out) + len(both_crashed)
print("------- Matching Results -------")
print("* A total of " + str(num_matching) + " benchmarks (~" + str(math.floor(num_matching/len(original)*100)) + "%) had the same results between each solver")
if(len(both_crashed) > 0): print("     - Crashed: " + str(len(both_crashed)))
print("     - Timed out: " + str(len(both_timed_out)))
print("     - Solved: " + str(len(filtered_frame)))
print()

nogates_correct = pd.DataFrame(filtered_frame, columns=nogates.columns)

