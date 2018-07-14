#!/usr/bin/env python3

import sys

def main():
    iata = sys.argv[1]
    for i in range(1, 40):
        for j in range(1, 90):
            print(iata + str(i).zfill(2) + 's' + str(j).zfill(2) + '-in-'\
                  'x' + '01.1e100.net')

if __name__ == '__main__':
    main()

