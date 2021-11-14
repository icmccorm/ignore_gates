#!/bin/bash
echo "SOLVE"    
./kissat $1 | ./cadical $1 ./proof.out
./drabt $1 ./proof.out