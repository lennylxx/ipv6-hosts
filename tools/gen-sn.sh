awk '{print $2}' ../data/iata.txt | xargs -n 1 ./list-sn.py > sn-all.txt
