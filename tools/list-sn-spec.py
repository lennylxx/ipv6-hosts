#!/usr/bin/env python

import sys

def main():
    sn = sys.argv[1]
    for k in range(1, 21):
    	print 'r%d' % k + '---' + 'sn-' + sn + '.googlevideo.com'

if __name__ == '__main__':
    main()

