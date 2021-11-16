#!/bin/bash
echo "SOLVE"    
./kissat $1 | python3 ./select_aux.py | ./cadical $1 ./proof.out
./drabt $1 ./proof.out