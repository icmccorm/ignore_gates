#!/bin/bash
echo "SOLVE"    
./cnftools aux $1 | ./cadical $1 ./proof.out
./drabt $1 ./proof.out