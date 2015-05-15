#!/usr/bin/env python

import sys

table = (
    'ams', 'arn', 'atl', 'ber', 'bom', 'bru', 'bud', 'cbf',
    'del', 'den', 'dfw', 'dub', 'eze', 'fra', 'gru', 'ham',
    'hkg', 'iad', 'kix', 'kul', 'lax', 'lga', 'lhr', 'lis',
    'maa', 'mad', 'mia', 'mil', 'mrs', 'muc', 'nrt', 'nuq',
    'ord', 'par', 'pek', 'prg', 'qro', 'sea', 'sha', 'sin',
    'sjc', 'sof', 'syd', 'waw', 'yyz', 'zrh'
)

def main():
    for iata in table:
        for i in range(1, 40):
            for j in range(1, 90):
                print iata + str(i).zfill(2) + 's' + str(j).zfill(2) + '-in-'\
                      'x' + '01.1e100.net'

if __name__ == '__main__':
    main()

