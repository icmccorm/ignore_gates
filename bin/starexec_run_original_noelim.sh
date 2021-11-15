echo "SOLVE"
echo -n | ./cadical $1 ./proof.out --no-elim
./drabt $1 ./proof.out