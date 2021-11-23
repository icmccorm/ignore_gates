echo "SOLVE"
echo -n | ./control $1 ./proof.out --no-elim
echo "VERIFY"
./drabt $1 ./proof.out