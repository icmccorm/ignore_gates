echo "SOLVE"
echo -n | ./cadical $1 ./proof.out --no-elim
echo "VERIFY"
./drabt $1 ./proof.out