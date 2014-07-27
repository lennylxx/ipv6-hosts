#!/bin/bash

hosts_file=$1
new_hosts_file=$2

he_net="2001:470:20::2"
google_a="2001:4860:4860::8888"
google_b="2001:4860:4860::8844"

dns=$he_net

blackhole=(
'10::2222'
'101::1234'
'21:2::2'
'2123::3e12'
'2001::212'
'2003:ff:1:2:3:4:5fff:6'
'2003:ff:1:2:3:4:5fff:7'
'2003:ff:1:2:3:4:5fff:8'
'2003:ff:1:2:3:4:5fff:9'
'2003:ff:1:2:3:4:5fff:10'
'2003:ff:1:2:3:4:5fff:11'
'2003:ff:1:2:3:4:5fff:12'
'2001:da8:112::21ae')

num=1

cat $hosts_file | while read line
do
{
	if [[ $line == "" ]]; then 
		echo "" >> $new_hosts_file
		continue
	fi

	if [ "${line:0:2}" == "##" ]; then 
		echo "$line" >> $new_hosts_file
		continue
	fi
	
	if [ "${line:0:1}" == "#" ]; then 
		line=${line#'#'}
	fi
	
	url=$(echo "$line" | cut -d' ' -f2)
	
	result=$(nslookup -querytype=AAAA "$url" "$dns"|grep 'AAAA address')
	
	name=$(echo "$result"|cut -f1)
	ip=$(echo "$result"|cut -d' ' -f4)

	for var in "${blackhole[@]}"; do
	if [[ $ip == "$var" && $ip != "" ]]; then
		ip=$(nslookup -vc -querytype=AAAA "$url" "$dns"|grep 'AAAA address'|cut -d' ' -f4)
		break
	fi
	done
	
	if [[ $ip == "" ]]; then
		echo '#'"$line" >> $new_hosts_file
		continue
	fi
	
	if [[ $name != $url && $name != "" ]]; then
		url=${url}" #"${name}
	fi

	echo "$ip" "$url" >> $new_hosts_file

	#print log
	echo "$num" "$ip" "$url"
	num=$((num+1))
}
done
wait

exit 0
