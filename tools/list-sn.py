#!/usr/bin/env python

import sys
from conv import num2code

def main():
    prefix = sys.argv[1]
    for i in range(0, 100):
        for j in range(0, 100):
            sn = prefix + num2code(str(i).zfill(2)) + 'n' + num2code(str(j).zfill(2))
            dm = 'r2---' + 'sn-' + sn + '.googlevideo.com'
            print dm

if __name__ == '__main__':
    main()

