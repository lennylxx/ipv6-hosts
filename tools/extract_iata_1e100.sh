d=$(dirname $0)
cat $d/../snippets/1e100.txt \
	| grep -oP '([a-z0-9]{3})(?=([a-z0-9]{5}\-in))' \
	| sort -u \
	| xargs -i sh -c "echo {}; $d/conv.py -i {}" \
	| paste -d' ' - - \
	| sort -k1 -u - $d/../data/iata.txt -o $d/../data/iata.txt
