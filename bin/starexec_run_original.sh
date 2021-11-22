echo "SOLVE"
echo -n | ./cadical $1 ./proof.out
echo "VERIFY"
./drabt $1 ./proof.out