#!/bin/bash
echo "AUX"
./cnftools-bin2 aux $1 > vars.aux
echo "SOLVE"    
cat vars.aux | ./br $1 ./proof.out
echo "VERIFY"
rm vars.aux
./drabt $1 ./proof.out
rm proof.out