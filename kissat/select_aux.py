import sys

aux_list = []
used_literals = []

def add_aux(lit, literals, gate_type):
    for l in literals:
        if l in used_literals:
            return

    aux_list.append(lit)
    print(str(lit) + " " + gate_type)
    for l in literals:
        used_literals.append(l)
    
    used_literals.append(lit)



fname =sys.argv[1]
fp = open(fname, "r")

line = fp.readline()
while line:
    # line = lit, gate_type 
    words = line.split()
    lit =  int(words[0])
    gate_type = words[1]
    literals = []
    while True:
        line = fp.readline()
        if "endG" in line:
            break
        clause = [int(x) for x in line.split()]
        for l in clause:
            if l < 0:
                l = -l
            if l != lit and l not in literals:
                literals.append(l)
        
    literals = sorted(literals)
    add_aux(lit, literals, gate_type)
    line = fp.readline()










