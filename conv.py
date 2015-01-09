#!/usr/bin/env python

# Read the wiki for more infomation
# https://github.com/lennylxx/ipv6-hosts/wiki/sn-domains

import sys
table = '1023456789abcdefghijklmnopqrstuvwxyz'

def iata2sn(iata):
    global table
    sn = ''
    for v in iata[0:3]:
        i = ((ord(v) - ord('a')) * 7 + 5) % 36
        sn += table[i]
    return sn

def sn2iata(sn):
    global table
    iata = ''
    for v in sn:
        i = table.index(v)
        i = (5 - i % 7) * 5 + i / 7 + 10
        iata += table[i]
    return iata

def num2code(num):
    global table
    code = ''
    for v in num:
        i = ((ord(v) - ord('0') + 1) * 7) % 36
        code += table[i]
    return code
    
def code2num(code):
    global table
    num = ''
    for v in code:
        i = table.index(v)
        i = i / 7 + i % 7 - 1
        num += str(i)
    return num

def main():
    if len(sys.argv) != 3:
        print 'usage:\n\t./%s -i iata\n\t./%s -s sn'\
            % (sys.argv[0], sys.argv[0])
        sys.exit(1)

    input = sys.argv[2]
    ret = ''
    if sys.argv[1] == '-i':
        ret += iata2sn(input[0:3])
        ret += num2code(input[3:5])
        ret += 'n'
        ret += num2code(input[6:8])
        print ret
    elif sys.argv[1] == '-s':
        ret += sn2iata(input[0:3])
        ret += code2num(input[3:5])
        ret += 's'
        ret += code2num(input[6:8])
        print ret
    else:
        print 'Unknown option.'
        sys.exit(1)

if __name__ == '__main__':
    main()
