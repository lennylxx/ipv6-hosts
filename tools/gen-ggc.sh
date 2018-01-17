d=$(dirname $0)
awk '{print $2}' $d/../data/ggc.txt | xargs -n 1 $d/list-sn-spec.py > ggc-all.txt
