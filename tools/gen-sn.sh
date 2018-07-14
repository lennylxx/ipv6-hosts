d=$(dirname $0)
awk '{print $2}' $d/../data/iata.txt | xargs -n 1 $d/list-sn.py > sn-all.txt
