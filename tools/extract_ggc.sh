d=$(dirname $0)
cat $d/../hosts \
	| grep -oP '(?<=sn\-)([a-z0-9]{1,}\-[a-z0-9]{1,})(?=(\.))' \
	| sort -u \
	| xargs -i sh -c "$d/conv.py -g {}; echo {}" \
	| paste -d' ' - - \
	| sort -V -u - $d/../data/ggc.txt -o $d/../data/ggc.txt
