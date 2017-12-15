d=$(dirname $0)
awk '{print $1}' $d/../data/iata.txt | xargs -n 1 $d/list-1e100.py > 1e100-all.txt
