#!/bin/bash
echo "UNZIP"
cp $1 ./bench.xz
xz --decompress ./bench.xz
mv bench bench.cnf

echo "AUX"
./kissat bench.cnf | python3 ./select_aux.py > vars.aux

echo "SOLVE"    
cat vars.aux | ./elim bench.cnf ./proof.out | tee solver.out

echo "VERIFY"
rm vars.aux
p=$(grep " SATISFIABLE" solver.out | wc | awk '{print  $1}')
  if [ $p -gt 0 ]
  then
    rm bench.cnf
    rm proof.out
    echo "v VERIFIED C\n"
  else
    ./drat-trim bench.cnf ./proof.out
    rm proof.out
  fi
rm solver.out
