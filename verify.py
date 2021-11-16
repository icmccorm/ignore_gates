# make sure that an output directory is present containing the job output from StarExec.
# visit every folder in ./output containing a benchmark result that is UNSAT
# for each benchmark result, look at the file "drat.txt". Make sure all contain 'VERIFIED'.

import os, re, sys, os
from shutil import which
from subprocess import Popen, PIPE, STDOUT, Popen
from threading import Thread
NUMBER = re.compile('p cnf ([0-9]*) ([0-9]*)')

class Command(object):
    def __init__(self, benchmark, filename, comparison):
        self.cmd = CADICAL_COMMAND
        self.benchmark = benchmark
        self.filename = filename
        self.process = None
        self.thread = None
        self.incorrect = False
        self.comparison = comparison
    def run(self):
        def target():
            self.process = Popen(CADICAL_COMMAND, stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
            cadical_stdout = self.process.communicate(input=self.benchmark.encode('ascii'))[0]
            cadical_result = cadical_stdout.decode()
            if ' SATISFIABLE' not in cadical_result:
                out = open('./output.txt', 'w')
                out.write(self.benchmark)
                out.close()
                print("Error: SAT result for " + self.filename + " is incorrect.")
                self.incorrect = True
        self.thread = Thread(target=target)
        self.thread.start()

    def join(self, timeout):
        self.thread.join(timeout)
        if self.thread.is_alive():
            self.process.terminate()
            self.thread.join()
            if(not self.incorrect):
                self.incorrect = True
                print("Error: SAT result for " + self.filename + " timed out.")

if(len(sys.argv) < 2 or not os.path.exists(sys.argv[1])):
    print("Usage: python3 ./verify.py [output directory]")
    exit(1)
OUTPUT_DIR = sys.argv[1]
BENCHMARK_DIR = './cnf'
OUTPUT_TEXT_REGEX = re.compile('[0-9]*.txt')
CADICAL_COMMAND = ['cadical']

def getAssigned(contents):
    assigned_list = []
    contents = contents.split('\n')
    assigned = ""
    for line in contents:
        index = line.find('v ')
        if (index >= 0):
            variables = line[index + 1:]
            variables = variables.strip()
            varlist = variables.split(" ")
            for var in varlist:
                int_var = int(var)
                if int_var > 0:
                    assigned_list.append(int_var)
                    assigned += str(int_var) + " 0\n"
    return assigned_list

if(not os.path.exists(OUTPUT_DIR)):
    print("The 'output' folder containing benchmark results must be present in the root directory.")
    exit(1)
if(which('cadical') is None):
    print("CaDiCaL must be added to PATH to verify SAT results.")
    exit(1)
if(not os.path.exists(BENCHMARK_DIR)):
    print("Unable to find benchmark directory to verify SAT results.")
    exit(1)
if(os.path.exists('./incorrect_unsat.txt')): os.remove("./incorrect_unsat.txt")
incorrect_unsat = open("./incorrect_unsat.txt", "a")
if(os.path.exists('./incorrect_sat.txt')): os.remove("./incorrect_sat.txt")
incorrect_sat = open("./incorrect_sat.txt", "a")

UNSAT_INCORRECT_BENCHMARKS = ""
SAT_INCORRECT_BENCHMARKS = ""
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
            assigned_list = []
            contents = contents.split('\n')
            assigned = ""
            num_clauses = 0
            for line in contents:
                index = line.find('v ')
                if (index > 0):
                    variables = line[index + 1:]
                    variables = variables.strip()
                    varlist = variables.split()
                    for var in varlist:
                        int_var = int(var)
                        if(int_var > 0):
                            num_clauses += 1
                            assigned_list.append(int_var)
                            assigned += str(int_var) + " " + "0\n"
            benchname = currRoot[:-3]
            benchmark_location = BENCHMARK_DIR + "/" + benchname
            if(not os.path.exists(benchmark_location)):
                print("ERROR: unable to locate " + benchname + " in " + BENCHMARK_DIR)
                exit(1)
            else:
                benchcontents = open(benchmark_location, 'r')
                header = benchcontents.readline().strip()
                while(header.startswith("c")):
                    header = benchcontents.readline().strip()
                matches = NUMBER.search(header)
                new_header = "p cnf " + matches.group(1) + " " + str(int(matches.group(2)) + num_clauses) + '\n'

                rest = benchcontents.read()
                benchcontents.close()
                new_benchmark = new_header + assigned + rest + '\n'
                process = Popen(CADICAL_COMMAND, stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
                cadical_stdout = process.communicate(input=new_benchmark.encode('ascii'))[0]
                cadical_result = cadical_stdout.decode()
                if ' SATISFIABLE' not in cadical_result:
                    print("Error: SAT result for " + benchname + " is incorrect.")
                    SAT_INCORRECT_COUNT += 1
                    incorrect_sat.write(benchname + "\n") 
        elif ' UNSATISFIABLE' in contents:
            if 'NOT VERIFIED' in contents:
                print("Error: UNSAT result for " + currRoot + " is incorrect.")
                UNSAT_INCORRECT_COUNT += 1
                incorrect_unsat.write(currRoot[:-3] + "\n")
        file.close()
    else:
        print("Unable to locate benchmark output for " + currRoot + '.')
        exit(1)

print('____________\n')
print('# incorrect UNSAT: ' + str(UNSAT_INCORRECT_COUNT))
print('# incorrect SAT: ' + str(SAT_INCORRECT_COUNT))
print('____________\n')
incorrect_sat.close()
incorrect_unsat.close()