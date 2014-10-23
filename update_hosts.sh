#!/bin/bash

if [ $# -ne 2 ]; then
    echo -e "Usage:"
    echo -e "    $ ./update_hosts.sh hosts new_hosts\n"
    exit 1
fi

hosts_file=$1
new_hosts_file=$2

if [ ! -f "$hosts_file" ]; then
    echo -e $1" doesn't exists, plz retry!\n"
    exit 1
fi

if [ -f $new_hosts_file ]; then
    new_hosts_file=${new_hosts_file}".new"
    printf "" > $new_hosts_file
fi

touch $new_hosts_file

he_net="2001:470:20::2"
google_a="2001:4860:4860::8888"
google_b="2001:4860:4860::8844"

dns=$he_net

blackhole=(
'10::2222'
'101::1234'
'21:2::2'
'2001::212'
'2001:da8:112::21ae'
'2003:ff:1:2:3:4:5fff:6'
'2003:ff:1:2:3:4:5fff:7'
'2003:ff:1:2:3:4:5fff:8'
'2003:ff:1:2:3:4:5fff:9'
'2003:ff:1:2:3:4:5fff:10'
'2003:ff:1:2:3:4:5fff:11'
'2003:ff:1:2:3:4:5fff:12'
'2123::3e12')

num=1

while read line
do
{
    #delete CR
    line=$(printf "$line"|tr -d '\r')
    #printf "$line"|od -tx1

    if [[ $line == "" ]]; then 
        printf "\r\n" >> $new_hosts_file
        continue
    fi

    if [ "${line:0:2}" == "##" ]; then 
        printf "$line\r\n" >> $new_hosts_file
        continue
    fi
    
    if [ "${line:0:1}" == "#" ]; then 
        line=${line#'#'}
    fi
    
    url=$(printf "$line"|cut -d" " -f2)

    result=$(nslookup -querytype=AAAA "$url" "$dns"|grep 'AAAA address')
    
    name=$(printf "$result"|cut -f1)
    ip=$(printf "$result"|cut -d' ' -f4)
    
    for var in "${blackhole[@]}"; do
    if [[ $ip == "$var" && $ip != "" ]]; then
        ip=$(nslookup -vc -querytype=AAAA "$url" "$dns"|grep 'AAAA address'|cut -d' ' -f4)
        break
    fi
    done
    
    if [[ $ip == "" ]]; then
        printf "#$line\r\n" >> $new_hosts_file
        continue
    fi

    if [[ $name != $url && $name != "" ]]; then
        url=${url}" #"${name}
    fi

    printf "$ip $url\r\n" >> $new_hosts_file

    #print log to stdio
    echo "$num" "$ip" "$url"
    num=$((num+1))
}
done < $hosts_file

exit 0
