#!/usr/bin/env python

import sys

table = (
'arn', 'atl', 'ber', 'bom', 'bud', 'del', 'den', 'dfw',
'fra', 'ham', 'hkg', 'iad', 'kix', 'kul', 'lax', 'lga',
'lhr', 'lis', 'maa', 'mad', 'mia', 'mil', 'mrs', 'muc',
'nrt', 'nuq', 'ord', 'par', 'prg', 'qro', 'sea', 'sin',
'sof', 'syd', 'yyz', 'zrh'
)

def main():
    for iata in table:
        for i in range(1, 40):
            for j in range(1, 90):
                print iata + str(i).zfill(2) + 's' + str(j).zfill(2) + '-in-'\
                      'x' + '01.1e100.net'

if __name__ == '__main__':
    main()

