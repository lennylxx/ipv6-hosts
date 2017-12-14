#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import ipaddress

def main():
    with open(sys.argv[1], 'r') as infile:
        hosts = infile.readlines()
        hosts.sort(key=lambda x: ipaddress.ip_address(x.split()[0]))

        with open(sys.argv[1] + '.out', 'w') as outfile:
            outfile.writelines(hosts)

    sys.exit(0)

if __name__ == '__main__':
    main()
