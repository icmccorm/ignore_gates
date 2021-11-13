#!/bin/bash
echo "SOLVE"
./cnftools-binary aux -o 1 $1 | ./cadical $1 $2/proof.out