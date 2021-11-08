#!/bin/bash

# run this on kissat directory. 
# example: bash> ./remove_type (cnf file name) (output file name)

build/kissat $1 -q  | sed 's/AND//' | sed 's/EQV//' | sed 's/ITE//' | sed 's/XOR//' | sed 's/DEF//' > $2

