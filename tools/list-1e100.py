#!/usr/bin/env python

import sys

table = (
    'ams', 'arn', 'atl', 'ber', 'bom', 'bru', 'bud', 'cbf',
    'del', 'den', 'dfw', 'dub', 'eze', 'fra', 'gru', 'ham',
    'hkg', 'iad', 'kix', 'kul', 'lax', 'lga', 'lhr', 'lis',
    'maa', 'mad', 'mia', 'mil', 'mrs', 'muc', 'nrt', 'nuq',
    'ord', 'par', 'pek', 'prg', 'qro', 'sea', 'sha', 'sin',
    'sjc', 'sof', 'syd', 'tsa', 'waw', 'yyz', 'zrh'
)

def list_1e100(iata):
    for i in range(1, 40):
        for j in range(1, 90):
            print iata + str(i).zfill(2) + 's' + str(j).zfill(2) + '-in-'\
                  'x' + '01.1e100.net'

def main():
    if len(sys.argv) > 1:
        list_1e100(sys.argv[1])
    else:
        for iata in table:
            list_1e100(iata)

if __name__ == '__main__':
    main()

