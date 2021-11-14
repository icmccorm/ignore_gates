echo "SOLVE"
echo -n | ./cadical $1 ./proof.out
./drabt $1 ./proof.out