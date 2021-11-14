unxz -c $1 | ./kissat/build/kissat | python ./kissat/select_aux.py | ./cadical/build/cadical $1 ./proof.out

