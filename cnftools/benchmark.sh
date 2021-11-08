echo "filename,process time (sec),real time (sec),max memory (MB)" >> results.csv
for file in ./bench
do
    echo -n "$file," && cadical "$file" | grep "initialization:\|process:" out | grep -oe '\([0-9]*\.[0-9]*\)' | paste -s -d ',' - >> results.csv
done