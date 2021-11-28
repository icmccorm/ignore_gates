import sys
# EQV, ITE, DEF

USED = set()

def add_aux(lit, clauses, gate_type, globalSet):
    overlapping = False
    for clause in clauses:
        if clause in globalSet:
            overlapping = True
        else:
            globalSet.add(clause)
    if(not overlapping): print(str(lit) + " " + gate_type)

line = sys.stdin.readline()
while line:
    # line = lit, gate_type 
    words = line.split()
    lit =  int(words[0])
    gate_type = words[1]
    clauses = set()
    while True:
        line = sys.stdin.readline()
        if "endG" in line:
            break
        list = [int(x) for x in line.split()]
        list.sort()
        clause = tuple(list)
        clauses.add(clause)
    add_aux(lit, clauses, gate_type, USED)
    line = sys.stdin.readline()
