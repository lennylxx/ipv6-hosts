d=$(dirname $0)
cat $d/../hosts \
	| grep -oP '(?<=sn\-)([a-z0-9]{3})(?=([a-z0-9]{5}\.))' \
	| sort -u \
	| xargs -i sh -c "$d/conv.py -s {}; echo {}" \
	| paste -d' ' - - \
	| sort -k1 -u - $d/../data/iata.txt -o $d/../data/iata.txt
