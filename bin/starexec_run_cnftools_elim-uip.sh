#!/bin/bash
echo "AUX"
./cnftools-binary aux $1 > vars.aux
echo "SOLVE"    
cat vars.aux | ./elim-uip $1 ./proof.out
echo "VERIFY"
rm vars.aux
./drabt $1 ./proof.out
rm proof.out