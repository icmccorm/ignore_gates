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

RESULT_DIRS.add("control")
RESULT_DIRS.add("control.noelim")
RESULT_DIRS.add("control.side-effects")
RESULT_DIRS.add("control.lastuip")

RESULT_DIRS.add("cnftools.br")
RESULT_DIRS.add("cnftools.elim")
RESULT_DIRS.add("cnftools.br.elim")
RESULT_DIRS.add("cnftools.br.uip")
RESULT_DIRS.add("cnftools.br.elim.uip")

RESULT_DIRS.add("kissat.br")
RESULT_DIRS.add("kissat.elim")
RESULT_DIRS.add("kissat.br.elim")
RESULT_DIRS.add("kissat.br.uip")
RESULT_DIRS.add("kissat.br.elim.uip")

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
RESTART = re.compile('restarts:[ ]*([0-9]*)')
REDUCED = re.compile('reduced:[ ]*([0-9]*)[ ]*([0-9]*.[0-9]*)')
PROPAGATIONS = re.compile('propagations:[ ]*([0-9]*)[ ]*([0-9]*.[0-9]*)')
BEGAN_SOLVING = re.compile('([0-9]*.[0-9]*)\/[0-9]*.[0-9]*\s*SOLVE')
BEGAN_AUX = re.compile('([0-9]*.[0-9]*)\/[0-9]*.[0-9]*\s*AUX\n')
CNFSTATS = re.compile("c found 'p cnf ([0-9]*) ([0-9]*)' header")
ELIMSTATS = re.compile("eliminated:[ ]*([0-9]*)[ ]*([0-9]*.[0-9]*)")
SUBSTATS = re.compile("subsumed:[ ]*([0-9]*)[ ]*([0-9]*.[0-9]*)")
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
INFO["num_decisions"] = 0
INFO["decisions_per_sec"] = 0
INFO["num_conflicts"] = 0
INFO["conflicts_per_sec"] = 0
INFO["num_restarts"] = 0
INFO["num_reduced"] = 0
INFO["percent_reduced_per_conflict"] = 0
INFO["num_propagations"] = 0
INFO["propagations_per_sec"] = 0
INFO["unzip_cpu_time"] = 0
INFO["aux_cpu_time"] = 0
INFO["total_num_clauses"] = 0
INFO["total_num_variables"] = 0
INFO['percent_variables_auxiliary'] = 0
INFO['num_eliminated'] = 0
INFO['num_subsumed'] = 0
INFO['percent_eliminated'] = 0
INFO['percent_subsumed'] = 0
#benchmark_name, memory usage, cpu time, wallclock time
def extract_data(FILE):
    solve_time = -1
    aux_time = -1
    currline = FILE.readline()
    datamap = {}
    while(currline):
        match_sub = SUBSTATS.search(currline)
        if(match_sub):
            num_sub = int(match_sub.group(1))
            per_sub = float(match_sub.group(2))
            datamap['num_subsumed'] = num_sub
            datamap['percent_subsumed'] = per_sub
            currline = FILE.readline()
            continue                  
        match_elim = ELIMSTATS.search(currline)
        if(match_elim):
            num_elim = int(match_elim.group(1))
            per_elim = float(match_elim.group(2))
            datamap['num_eliminated'] = num_elim
            datamap['percent_eliminated'] = per_elim
            currline = FILE.readline()
            continue            
        match_cnfstats = CNFSTATS.search(currline)
        if(match_cnfstats):
            num_variables = int(match_cnfstats.group(1))
            num_clauses = int(match_cnfstats.group(2))
            datamap['total_num_clauses'] = num_clauses
            datamap['total_num_variables'] = num_variables
            currline = FILE.readline()
            continue            
        match_aux = BEGAN_AUX.search(currline)
        if(match_aux):
            aux_time = float(match_aux.group(1))
            currline = FILE.readline()
            continue
        match_solve = BEGAN_SOLVING.search(currline)
        if(match_solve):
            solve_time = float(match_solve.group(1))
            currline = FILE.readline()
            continue
        match_aux = AUXLIST.search(currline)
        if(match_aux):
            NUM_AUX = 0
            for i in range(1, 10):
                NUM_AUX += int(match_aux.group(i))
            datamap['NUM_EQV'] = int(match_aux.group(1))
            datamap['NUM_DEF'] = int(match_aux.group(2))
            datamap['NUM_ITE'] = int(match_aux.group(3))
            datamap['NUM_AND'] = int(match_aux.group(4))
            datamap['NUM_XOR'] = int(match_aux.group(5))
            datamap['NUM_FUL'] = int(match_aux.group(6))
            datamap['NUM_OR'] = int(match_aux.group(7))
            datamap['NUM_TRI'] = int(match_aux.group(8))
            datamap['NUM_GEN'] = int(match_aux.group(9))
            datamap['NUM_AUX'] = NUM_AUX
            currline = FILE.readline()
            continue
        match_restart = RESTART.search(currline)
        if(match_restart):
            num_restarts = int(match_restart.group(1))
            datamap['num_restarts'] = num_restarts
            currline = FILE.readline()
            continue
        match_reduced = REDUCED.search(currline)
        if(match_reduced):
            num_reduced = int(match_reduced.group(1))
            percent_reduced_per_conflict = float(match_reduced.group(2))
            datamap['num_reduced'] = num_reduced
            datamap['percent_reduced_per_conflict'] = percent_reduced_per_conflict
            currline = FILE.readline()
            continue
        match_prop = PROPAGATIONS.search(currline)
        if(match_prop):
            num_propagations = int(match_prop.group(1))
            per_sec = float(match_prop.group(2))
            datamap['num_propagations'] = num_propagations
            datamap['propagations_per_sec'] = per_sec
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
            datamap['num_decisions'] = num_dec
            datamap['decisions_per_sec'] = per_sec
            currline = FILE.readline()
            continue
        match_conf = CONFLICTS.search(currline)
        if(match_conf):
            num_conf = int(match_conf.group(1))
            per_sec = float(match_conf.group(2))
            datamap['num_conflicts'] = num_conf
            datamap['conflicts_per_sec'] = per_sec
            currline = FILE.readline()
            continue
        currline = FILE.readline()
    if(solve_time >= 0 and aux_time >= 0):
        datamap["unzip_cpu_time"] = aux_time
        datamap["aux_cpu_time"] = solve_time - aux_time
    elif(solve_time >= 0):
        datamap["unzip_cpu_time"] = solve_time
        datamap["aux_cpu_time"] = 0
    else:
        print("UNABLE TO DETECT TIME. ERROR!")
        exit(1)
    datamap['percent_variables_auxiliary'] = datamap['NUM_AUX']/datamap['total_num_variables']
    return datamap

for dirpath, dirnames, _ in os.walk(START):
    for dirname in dirnames:
        if(dirname in RESULT_DIRS):
            print("Walking " + dirname + ":")
            for solverDirPath, solverDirNames, solverFileNames in os.walk(dirpath + "/" + dirname + "/"):
                if(len(solverDirNames) > 0):
                    result_dirs = [dir for dir in solverDirNames if dir.endswith(".cnf.xz")]
                    for result_dir in result_dirs:
                        BENCHMARK = BENCH_PREFIX + result_dir
                        SOLVER = dirname
                        for _, _, benchmark_results in os.walk(solverDirPath + result_dir):
                            for file in benchmark_results:
                                if(RESULT_FORMAT.match(file)):
                                    FILE = open(solverDirPath + result_dir + "/" + file, 'r')
                                    datamap = extract_data(FILE)
                                    FILE.close()
                                    for key in datamap:
                                        INFO.loc[((INFO.benchmark == BENCHMARK) & (INFO.configuration == SOLVER)), key] = datamap[key]
                        print("     * " + BENCHMARK)

OUTPUT_FILE.write(INFO.to_csv(index=False))
OUTPUT_FILE.close()

