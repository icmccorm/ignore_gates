#!/bin/bash
echo "AUX"
./kissat $1 | python3 ./select_aux.py > vars.aux
echo "SOLVE"    
SECONDS=0
cat vars.aux | ./elim-uip $1 ./proof.out
echo "CadicalTimeElased: " $SECONDS
echo "VERIFY"
rm vars.aux
./drabt $1 ./proof.out
rm proof.out