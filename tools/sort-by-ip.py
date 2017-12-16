#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import ipaddress

def main():
    with open(sys.argv[1], 'r') as infile:
        hydration = []
        for line in infile.readlines():
            line = line.strip()
            if line == '' or line[0] == '#':
                continue
            hydration.append(line.split())

        hydration.sort(key=lambda x: ipaddress.ip_address(x[0]))

        with open(sys.argv[1] + '.out', 'w') as outfile:
            for host_arr in hydration:
                outfile.write(' '.join(host_arr) + '\r\n')

    sys.exit(0)

if __name__ == '__main__':
    main()
