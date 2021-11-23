echo "SOLVE"
echo -n | ./control $1 ./proof.out
echo "VERIFY"
./drabt $1 ./proof.out