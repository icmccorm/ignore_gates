#!/bin/bash
echo "SOLVE"
./cnftools aux -o 1 $1 | ./cadical $1 $2/proof.out