echo "SOLVE"
SECONDS=0
echo -n | ./control $1 ./proof.out --no-elim
echo "CadicalTimeElased: " $SECONDS
echo "VERIFY"
./drabt $1 ./proof.out