#!/bin/bash
echo "AUX"
./kissat $1 | python3 ./select_aux.py > vars.aux
echo "SOLVE"    
cat vars.aux | ./br-uip $1 ./proof.out
echo "VERIFY"
rm vars.aux
./drabt $1 ./proof.out
rm proof.out