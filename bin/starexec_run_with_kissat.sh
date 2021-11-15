#!/bin/bash
echo "SOLVE"
unxz -c $1 | ./kissat | python ../kissat/select_aux.py | ./cadical $1 ./proof.out
p=$(./drat-trim $1 ./proof.out -D -v | grep "VERIFIED" | wc | awk '{print  $1}')
if [ $p -gt 0 ]
then
echo "VERIFIED"
else
echo "NOT VERIFIED"
fi