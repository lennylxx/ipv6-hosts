#!/usr/bin/env python3

import sys
from conv import num2code

def main():
    encoded_iata = sys.argv[1]
    for i in range(0, 100):
        for j in range(0, 100):
            sn = encoded_iata + num2code(str(i).zfill(2)) + 'n' + num2code(str(j).zfill(2))
            dm = 'r2---' + 'sn-' + sn + '.googlevideo.com'
            print(dm)

if __name__ == '__main__':
    main()

