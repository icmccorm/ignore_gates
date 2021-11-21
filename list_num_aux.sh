
cd ./cnf
rm -f ../results/auxlist.csv > /dev/null
echo "benchmark,EQV,ITE,DEF,AND,XOR" >> ../results/auxlist.csv
for FILE in *; do
    echo "$FILE"
    GATES=$(../kissat/build/kissat "$FILE" | python ../kissat/select_aux.py -s)
    CSV_LINE="$1/$FILE.xz,$GATES"
    echo "$CSV_LINE" >> ../results/auxlist.csv
done