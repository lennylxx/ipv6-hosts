#!/usr/bin/env python

import sys

table = (
'pe', 'ni', 'sa', 'hg', 'tb', 'tf', 'tg', 'ib',
'ie', 'ig', 'yh', 'gg', 'yn', 'yv', 'yk', 'ob',
'oa', 'of', 'oe', 'og', 've', 'vb', 'vc', 'vh',
'qa', 'qc', 'qe', 'qg', 'qh', 'da', 'ph', 'pd',
'pa', 'pc', 'fa', 'bk', 'dn', 'de', 'wg', 'wj',
'we', 'wi', 'wb', 'la', 'lb', 'ee', 'ea'
)

def main():
    for xx in table:
        for i in range(0x00, 0x100):
            print xx + '-in-' + 'x' + hex(i)[2:].zfill(2) + '.1e100.net'

if __name__ == '__main__':
    main()

