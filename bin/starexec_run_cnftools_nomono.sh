#!/bin/bash
echo "SOLVE"
./cnftools aux $1 | ./cadical $1 $2/proof.out
