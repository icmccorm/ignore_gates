#!/bin/bash
echo "SOLVE"    
./kissat $1 | ./cadical $1 $2/proof.out