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

dependencies = Graph()
# EQV, ITE, DEF
def add_aux(lit, inputs, gate_type):
    if(dependencies.add_parent(inputs, lit)):
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