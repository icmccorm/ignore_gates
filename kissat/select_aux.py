import sys
aux_list = []

class Graph:
    def __init__(self):
        self.children_to_parents = {}
    def add_parent(self, children, parent):
        if parent not in self.children_to_parents:
            self.children_to_parents[parent] = set()
        for child in children:
            if(child not in self.children_to_parents):
                self.children_to_parents[child] = set()
            if(child in self.children_to_parents[parent]):
                return False
            else:
                self.children_to_parents[child].add(parent)
        return True

SWITCH = {
    "EQV": 0,
    "ITE": 0,
    "DEF": 0,
    "AND": 0,
    "XOR": 0
}

SUMMARY = False
if(len(sys.argv) > 1 and sys.argv[1] == '-s'):
    SUMMARY = True

dependencies = Graph()
# EQV, ITE, DEF
def add_aux(lit, inputs, gate_type):
    if(dependencies.add_parent(inputs, lit)):
        if(SUMMARY):
            SWITCH[gate_type] += 1
        else:
            print(str(lit) + " " + gate_type)
line = sys.stdin.readline()
while line:
    # line = lit, gate_type 
    words = line.split()
    lit =  int(words[0])
    gate_type = words[1]
    inputs = set()
    while True:
        line = sys.stdin.readline()
        if "endG" in line:
            break
        for x in line.split():
            if lit != int(x):
                inputs.add(int(x))
    add_aux(lit, inputs, gate_type)
    line = sys.stdin.readline()
if(SUMMARY): print("%d,%d,%d,%d,%d" % (SWITCH["EQV"], SWITCH["ITE"], SWITCH["DEF"], SWITCH["AND"], SWITCH["XOR"]))
