#!/bin/bash
echo "SOLVE"    
./cnftools-binary aux $1 | ./cadical $1 ./proof.out --no-elim
./drabt $1 ./proof.out