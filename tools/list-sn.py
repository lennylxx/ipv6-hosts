#!/usr/bin/env python3

import sys
from conv import num2code

def main():
    encoded_iata = sys.argv[1]
    for i in range(0, 100):
        for j in range(0, 100):
            a = num2code(str(i).zfill(2))
            b = num2code(str(j).zfill(2))
            print('r2---' + 'sn-' + encoded_iata + a + 'n' + b + '.googlevideo.com')
            print('r2---' + 'sn-' + encoded_iata + a + 'u' + b + '.googlevideo.com')

if __name__ == '__main__':
    main()

