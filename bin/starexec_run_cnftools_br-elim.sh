#!/bin/bash
echo "AUX"
./cnftools-binary aux $1 > vars.aux
echo "SOLVE"    
SECONDS=0
cat vars.aux | ./br-elim $1 ./proof.out
echo "CadicalTimeElased: " $SECONDS
echo "VERIFY"
rm vars.aux
./drabt $1 ./proof.out
rm proof.out