#!/bin/bash
echo "SOLVE"    
./kissat $1 | python3 ./select_aux.py | ./cadical $1 ./proof.out --no-elim
./drabt $1 ./proof.out