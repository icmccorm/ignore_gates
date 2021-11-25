#!/bin/bash
echo "AUX"
./cnftools-bin2 aux $1 > vars.aux

echo "SOLVE"    
cat vars.aux | ./elim $1 ./proof.out > solver.out

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