# this script should generate a csv file with the name of each benchmark in every row, and then the following information from the output of the benchmark:
# the following lines have been added to the output
# AUXLIST: %d,%d,%d,%d,%d,%d,%d,%d,%d 
#   * this contains gate types in this order: EQV, DEF, ITE, AND, XOR, FUL, OR, TRI, GEN
# AUX DECISIONS: %d
#   * the number of times auxiliary variables were decided on
# we also want to record the time that "SOLVE" was printed and the time that "VERIFY" was printed; the difference is the duration of the solver actually running.
# we can combine this csv file with results to get our data.
import os, pandas, re

RESULT_DIRS = set()

NUM_RESULTS = 12
RESULT_DIRS.add("control.sh")
RESULT_DIRS.add("control_noelim.sh")

RESULT_DIRS.add("cnftools_br.sh")
RESULT_DIRS.add("cnftools_elim.sh")
RESULT_DIRS.add("cnftools_br-elim.sh")
RESULT_DIRS.add("cnftools_br-uip.sh")
RESULT_DIRS.add("cnftools_br-elim-uip.sh")

RESULT_DIRS.add("kissat_br.sh")
RESULT_DIRS.add("kissat_elim.sh")
RESULT_DIRS.add("kissat_br-elim.sh")
RESULT_DIRS.add("kissat_br-uip.sh")
RESULT_DIRS.add("kissat_br-elim-uip.sh")

foundNames = set()
START = "./results"

BENCH_PREFIX = "cnf_proj/"
INFO = pandas.DataFrame()
RESULTS_FOUND = 0

RESULT_FORMAT = re.compile('[0-9]*.txt')

for dirpath, dirnames, filenames in os.walk(START):
    for filename in filenames:
        if filename == "info.csv":
            print("FOUND")
            #INFO = pandas.concat(INFO, pandas.read_csv(dirpath + "/" + filename))
            RESULTS_FOUND += 1

INFO["NUM_EQV"] = 0
INFO["NUM_DEF"] = 0
INFO["NUM_ITE"] = 0
INFO["NUM_AND"] = 0
INFO["NUM_XOR"] = 0
INFO["NUM_FUL"] = 0
INFO["NUM_OR"] = 0
INFO["NUM_TRI"] = 0
INFO["NUM_GEN"] = 0


for dirpath, dirnames, filenames in os.walk(START):
    for dirname in dirnames:
        if(dirname in RESULT_DIRS):
            print("Walking " + dirname + ":")
            for dirpath, dirnames, filenames in os.walk(dirpath + "/" + dirname + "/"):
                result_dirs = [dir for dir in dirnames if dir.endswith(".cnf.xz")]
                for result_dir in result_dirs:
                    BENCHMARK = BENCH_PREFIX + result_dir
                    SOLVER = dirname
                    print(SOLVER)
                    for dirpath, dirnames, filenames in os.walk(dirpath + result_dir):
                        for file in filenames:
                            if(RESULT_FORMAT.match(file)):
                                print()
                                FILE = open(dirpath + file, 'r')
                                datamap = extract_data(FILE)
                                FILE.close()
                                row_to_modify = INFO[INFO['benchmark'] == BENCHMARK & INFO['configuration'] == SOLVER]

if(RESULTS_FOUND != NUM_RESULTS):
    print("A benchmark output file (info.csv) is missing! Only " + str(RESULTS_FOUND) + " were found.")
    exit(1)

#benchmark_name, memory usage, cpu time, wallclock time
def extract_data(file):
    currline = FILE.readline()
    datamap = {}
    while(currline):

        currline = FILE.readline()
    return datamap

INFO = INFO[INFO['status'] == 'complete' & INFO['result'].isin(['UNSAT', 'SAT-INCORRECT'])]
INFO = INFO.query('NUM_EQV > 0 | NUM_DEF > 0 | NUM_ITE > 0 | NUM_AND > 0 | NUM_XOR > 0 | NUM_FUL > 0 | NUM_OR > 0 | NUM_TRI > 0 | NUM_GEN > 0')