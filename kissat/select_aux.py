import sys

aux_list = []
used_clauses = []

def add_aux(lit, clauses, gate_type):
    for c in clauses:
        for used_c in used_clauses:   # does this work??  int list equivalence?   
            if c == used_c:
                return

    for c in clauses:
        used_clauses.append(c)
    aux_list.append(lit)
    print(str(lit) + " " + gate_type)



fname =sys.argv[1]
fp = open(fname, "r")

line = fp.readline()

while line:
    # line = lit, gate_type 
    words = line.split()
    lit =  int(words[0])
    gate_type = words[1]
    clauses = []
    while True:
        line = fp.readline()
        if "endG" in line:
            break
        clause = [int(x) for x in line.split()]
        clause = sorted(clause)
        clauses.append(clause)

    add_aux(lit, clauses, gate_type)
    line = fp.readline()










