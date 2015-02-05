#!/usr/bin/env python

import sys

def main():
    infile = open(sys.argv[1], 'r')
    hosts = infile.readlines()

    for line in hosts:
        if line[0] == '#':
            continue
        arr = line.split()
        for k in range(1, 21):
            print 'r%d' % k + arr[1][2:]

if __name__ == '__main__':
    main()

