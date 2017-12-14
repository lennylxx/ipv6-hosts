awk '{print $1}' ../data/iata.txt | xargs -n 1 ./list-1e100.py > 1e100-all.txt
