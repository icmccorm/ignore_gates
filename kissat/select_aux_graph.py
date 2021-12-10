import sys
import networkx as nx

aux_list = []
used_clauses = []
DG = nx.DiGraph()

def add_aux(lit, literals, gate_type):
    edges = [(l, lit) for l in literals]
    DG.add_edges_from(edges)

    if len(list(nx.simple_cycles(DG))) > 0:
        DG.remove_edges_from(edges)
        return

    aux_list.append(lit)
    print(str(lit) + " " + gate_type)



# fname =sys.argv[1]
# fp = open(fname, "r")
fp = sys.stdin
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










