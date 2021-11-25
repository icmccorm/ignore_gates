import sys
aux_list = []
USED = set()
# EQV, ITE, DEF
def add_aux(lit, clauses, gate_type):
    if(clauses not in USED):
        aux_list.append(lit)
        print(str(lit) + " " + gate_type)

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
        clause = tuple(int(x) for x in line.split())
        clauses.add(clause)
    add_aux(lit, clauses, gate_type)
    line = sys.stdin.readline()

