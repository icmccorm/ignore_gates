#!/bin/bash
echo "SOLVE"
./cnftools aux -o 1 $1 | ./cadical $1 ./proof.out
p=$(./drat-trim $1 ./proof.out -D -v | grep "VERIFIED" | wc | awk '{print  $1}')
if [ $p -gt 0 ]
then
echo "VERIFIED"
else
echo "NOT VERIFIED"
fi