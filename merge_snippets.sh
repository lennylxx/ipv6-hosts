#!/bin/bash

if [ $# -ne 1 ]; then
    echo -e "Usage:"
    echo -e "    $ ./merge_snippets.sh new_hosts\n"
    exit 1
fi

new_hosts_file=$1

if [ -f $new_hosts_file ]; then
    new_hosts_file=${new_hosts_file}".new"
    printf "" > $new_hosts_file
fi

export LC_ALL="C"

printf "\
##  __                                 __                               \r\n\
## |__| _____  __ __ ┌─────┐          |  |                  __          \r\n\
## |  ||     ||  |  ||   ──|  ______  |  |──┐┌─────┐.─────.|  |_ .─────.\r\n\
## |  ||  ─  ||  |  ||  ─  | |______| |     ||  ─  ||__ ──||   _||__ ──|\r\n\
## |__||  ┌──┘ \___/ |_____|          |__|__||_____||_____||____||_____|\r\n\
##     |__|                                                             \r\n\
##                                                          · lennylxx ·\r\n\
##\r\n\
## +-------------------------  >>d(' _ ')b<<  -------------------------+\r\n\
## |                                                                   |\r\n\
## |         Project: https://github.com/lennylxx/ipv6-hosts           |\r\n\
## |         Update : `date    +"%a, %d %b %Y %T %z"`                  |\r\n\
## |                                                                   |\r\n\
## +-------------------------------------------------------------------+\r\n\
" >> $new_hosts_file

unset LC_ALL

printf "\r\n127.0.0.1 localhost\r\n" >> $new_hosts_file
printf "::1 localhost ip6-localhost ip6-loopback\r\n\r\n" >> $new_hosts_file

cat snippets/??_*.txt >> $new_hosts_file

printf "\
## +-------------------------------------------------------------------+\r\n\
## |                            End of File                            |\r\n\
## +-------------------------------------------------------------------+\r\n\
" >> $new_hosts_file

exit 0
