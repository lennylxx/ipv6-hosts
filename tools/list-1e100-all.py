#!/usr/bin/env python

import sys

def main():
    infile = open(sys.argv[1], 'r')
    hosts = infile.readlines()

    for line in hosts:
        arr = line.split()
        if len(arr) == 0:
            continue
        for k in range(0, 32):
            print arr[1][:8] + '-in-x' + hex(k)[2:].zfill(2) + '.1e100.net' 

if __name__ == '__main__':
    main()

