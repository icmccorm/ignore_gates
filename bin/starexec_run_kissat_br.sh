#!/bin/bash
echo "AUX"
./kissat $1 | python3 ./select_aux.py > vars.aux

echo "SOLVE"    
cat vars.aux | ./br $1 ./proof.out > solver.out

echo "PRINT"
rm vars.aux
cat solver.out

echo "VERIFY"
p=$(grep " SATISFIABLE" solver.out | wc | awk '{print  $1}')
  if [ $p -gt 0 ]
  then
    rm proof.out
    echo "v VERIFIED C\n"
  else
    ./drabt $1 ./proof.out
    rm proof.out
  fi
rm solver.out