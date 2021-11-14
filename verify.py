# make sure that an output directory is present containing the job output from StarExec.
# visit every folder in ./output containing a benchmark result that is UNSAT
# for each benchmark result, look at the file "drat.txt". Make sure all contain 'VERIFIED'.

import os, re

OUTPUT_DIR = './output'
OUTPUT_TEXT_REGEX = re.compile('[0-9]*.txt')
if(not os.path.exists(OUTPUT_DIR)):
    print("The 'output' folder containing benchmark results must be present in the root directory.")
    exit(1)

UNSAT_INCORRECT_BENCHMARKS = ""

dirs = next(os.walk(OUTPUT_DIR))[1]

UNSAT_INCORRECT_COUNT = 0
SAT_INCORRECT_COUNT = 0
for currRoot in dirs:
    currFiles = next(os.walk(OUTPUT_DIR + "/" + currRoot))[2]
    BENCH_OUTPUT = None
    for file in currFiles:
        if OUTPUT_TEXT_REGEX.match(file):
            BENCH_OUTPUT = OUTPUT_DIR + '/' + currRoot + "/" + file
    if(BENCH_OUTPUT != None):
        file = open(BENCH_OUTPUT, mode='r')
        contents = file.read()
        if ' SATISFIABLE' in contents:
 
            print("", end="")
        elif ' UNSATISFIABLE' in contents:
            if 'NOT VERIFIED' in contents:
                print("Error: UNSAT result for " + currRoot + " is incorrect.")
                UNSAT_INCORRECT_COUNT += 1
        file.close()
    else:
        print("Unable to locate benchmark output for " + currRoot + '.')
        exit(1)

print('____________\n')
print('# incorrect UNSAT: ' + str(UNSAT_INCORRECT_COUNT))
print('# incorrect SAT: ' + str(SAT_INCORRECT_COUNT))
print('____________\n')
