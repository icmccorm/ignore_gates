# this script should generate a csv file with the name of each benchmark in every row, and then the following information from the output of the benchmark:
# the following lines have been added to the output
# AUXLIST: %d,%d,%d,%d,%d,%d,%d,%d,%d 
#   * this contains gate types in this order: EQV, DEF, ITE, AND, XOR, FUL, OR, TRI, GEN
# AUX DECISIONS: %d
#   * the number of times auxiliary variables were decided on
# we also want to record the time that "SOLVE" was printed and the time that "VERIFY" was printed; the difference is the duration of the solver actually running.
# we can combine this csv file with results to get our data.
import os, pandas, re

#benchmark_name, memory usage, cpu time, wallclock time
def extract_data(FILE):
    currline = FILE.readline()
    datamap = {}
    gate_types = []
    while(currline):
        match_aux = AUXLIST.search(currline)
        if(match_aux):
            datamap['NUM_EQV'] = int(match_aux.group(1))
            datamap['NUM_DEF'] = int(match_aux.group(2))
            datamap['NUM_ITE'] = int(match_aux.group(3))
            datamap['NUM_AND'] = int(match_aux.group(4))
            datamap['NUM_XOR'] = int(match_aux.group(5))
            datamap['NUM_FUL'] = int(match_aux.group(6))
            datamap['NUM_OR'] = int(match_aux.group(7))
            datamap['NUM_TRI'] = int(match_aux.group(8))
            datamap['NUM_GEN'] = int(match_aux.group(9))
            currline = FILE.readline()
            continue
        match_cpu = CPUTIME.search(currline)
        if(match_cpu):
            time = float(match_cpu.group(1))
            datamap['cpu time'] = time
            currline = FILE.readline()
            continue
        match_wallclock = WALLCLOCK.search(currline)
        if(match_wallclock):
            time = float(match_wallclock.group(1))
            datamap['wallclock time'] = time
            currline = FILE.readline()
            continue
        match_mem = MEM.search(currline)
        if(match_mem):
            mem = float(match_mem.group(1))
            datamap['memory usage'] = mem
            currline = FILE.readline()
            continue
        match_dec = DECISIONS.search(currline)
        if(match_dec):
            num_dec = int(match_dec.group(1))
            per_sec = float(match_dec.group(2))
            datamap['num dec'] = num_dec
            datamap['dec per sec'] = per_sec
            currline = FILE.readline()
            continue
        match_conf = CONFLICTS.search(currline)
        if(match_conf):
            num_conf = int(match_conf.group(1))
            per_sec = float(match_conf.group(2))
            datamap['num conf'] = num_conf
            datamap['conf per sec'] = per_sec
            currline = FILE.readline()
            continue
        currline = FILE.readline()
    return datamap


RESULT_DIRS = set()

RESULT_DIRS.add("control")
RESULT_DIRS.add("control_noelim")

RESULT_DIRS.add("cnftools_br")
RESULT_DIRS.add("cnftools_elim")
RESULT_DIRS.add("cnftools_br-elim")
RESULT_DIRS.add("cnftools_br-uip")
RESULT_DIRS.add("cnftools_br-elim-uip")

RESULT_DIRS.add("kissat_br")
RESULT_DIRS.add("kissat_elim")
RESULT_DIRS.add("kissat_br-elim")
RESULT_DIRS.add("kissat_br-uip")
RESULT_DIRS.add("kissat_br-elim-uip")

foundNames = set()
START = "./results"

OUTPUT_FILE = "./results/results.csv"
if(os.path.exists(OUTPUT_FILE)):
    os.remove(OUTPUT_FILE)
OUTPUT_FILE = open(OUTPUT_FILE, 'w')


BENCH_PREFIX = "cnf_proj/"
INFO = pandas.DataFrame()
RESULT_FORMAT = re.compile('[0-9]*.txt')

AUXLIST = re.compile('AUXLIST: ([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*)')
CPUTIME = re.compile('CPUTIME:[ ]*([0-9]*.[0-9]*)')
WALLCLOCK = re.compile('WALLCLOCK:[ ]*([0-9]*.[0-9]*)')
MEM = re.compile('MEM:[ ]*([0-9]*.[0-9]*)')
CONFLICTS = re.compile('conflicts:[ ]*([0-9]*)[ ]*([0-9]*.[0-9]*)')
DECISIONS = re.compile('decisions:[ ]*([0-9]*)[ ]*([0-9]*.[0-9]*)')

for dirpath, dirnames, filenames in os.walk(START):
    for filename in filenames:
        if filename.endswith("info.csv"):
            INFO = pandas.concat([INFO, pandas.read_csv(dirpath + "/" + filename)])

INFO["NUM_EQV"] = 0
INFO["NUM_DEF"] = 0
INFO["NUM_ITE"] = 0
INFO["NUM_AND"] = 0
INFO["NUM_XOR"] = 0
INFO["NUM_FUL"] = 0
INFO["NUM_OR"] = 0
INFO["NUM_TRI"] = 0
INFO["NUM_GEN"] = 0
INFO["NUM_AUX"] = 0
INFO["num dec"] = 0
INFO["dec per sec"] = 0
INFO["num conf"] = 0
INFO["conf per sec"] = 0

for dirpath, dirnames, _ in os.walk(START):
    for dirname in dirnames:
        if(dirname in RESULT_DIRS):
            print("Walking " + dirname + ":")
            for solverDirPath, solverDirNames, solverFileNames in os.walk(dirpath + "/" + dirname + "/"):
                if(len(solverDirNames) > 0):
                    result_dirs = [dir for dir in solverDirNames if dir.endswith(".cnf.xz")]
                    for result_dir in result_dirs:
                        BENCHMARK = BENCH_PREFIX + result_dir
                        SOLVER = dirname + ".sh"
                        for _, _, benchmark_results in os.walk(solverDirPath + result_dir):
                            for file in benchmark_results:
                                if(RESULT_FORMAT.match(file)):
                                    FILE = open(solverDirPath + result_dir + "/" + file, 'r')
                                    datamap = extract_data(FILE)
                                    FILE.close()
                                    for key in datamap:
                                        INFO.loc[((INFO.benchmark == BENCHMARK) & (INFO.configuration == SOLVER)), key] = datamap[key]


OUTPUT_FILE.write(INFO.to_csv(index=False))
OUTPUT_FILE.close()