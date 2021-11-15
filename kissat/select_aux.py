import sys
aux_list = []
USED = set()
# EQV, ITE, DEF
def add_aux(lit, clauses, gate_type):
    newly_used = set()
    for c in clauses:
        if tuple(c) in USED:
            return set()
        newly_used.add(tuple(c))
    aux_list.append(lit)
    print(str(lit) + " " + gate_type)
    return newly_used

line = sys.stdin.readline()
while line:
    # line = lit, gate_type 
    words = line.split()
    lit =  int(words[0])
    gate_type = words[1]
    clauses = []
    while True:
        line = sys.stdin.readline()
        if "endG" in line:
            break
        clause = [int(x) for x in line.split()]
        clauses.append(clause)
    clauses.sort(key=len)
    USED = USED.union(add_aux(lit, clauses, gate_type))
    line = sys.stdin.readline()










