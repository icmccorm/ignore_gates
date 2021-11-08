#!/bin/bash
echo "SOLVE"
./../kissat/build/kissat $1 | ./../cadical/build/cadical $1 ./proof.out
p=$(./../drat-trim/drat-trim $1 ./proof.out -D -v | grep "VERIFIED" | wc | awk '{print  $1}')
if [ $p -gt 0 ]
then
echo "VERIFIED\n" > $2/drat.txt
else
echo "NOT VERIFIED\n" > $2/drat.txt
fi