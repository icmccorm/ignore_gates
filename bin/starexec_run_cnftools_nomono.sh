#!/bin/bash
echo "SOLVE"
./cnftools-binary aux $1 | ./cadical $1 $2/proof.out
